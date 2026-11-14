import os
import hmac
import hashlib
import logging
from flask import Blueprint, request, jsonify, redirect, abort, current_app
from ..config import Config
from ..tasks.automation_tasks import process_incoming_comment_event
from ..services.link_tracker import LinkTrackerService
from ..models.schema import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger("Antigravity.Webhooks")
webhook_bp = Blueprint("webhooks", __name__)

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def verify_meta_signature(req) -> bool:
    """Verifies X-Hub-Signature-256 header sent by Meta Webhook."""
    signature_header = req.headers.get("X-Hub-Signature-256")
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    expected_hash = signature_header.split("sha256=")[1]
    computed_hash = hmac.new(
        Config.INSTAGRAM_APP_SECRET.encode("utf-8"),
        req.get_data(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_hash, computed_hash)


@webhook_bp.route("/webhook/instagram", methods=["GET"])
def meta_hub_challenge():
    """
    Handles Meta App webhook endpoint registration challenge.
    """
    mode = request.args.get("hub.mode")
    verify_token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and verify_token == Config.INSTAGRAM_VERIFY_TOKEN:
        logger.info("[Meta Webhook] Verification challenge accepted.")
        return challenge, 200
    
    logger.warning("[Meta Webhook] Verification token mismatch or invalid mode.")
    return "Forbidden", 403


@webhook_bp.route("/webhook/instagram", methods=["POST"])
def ingest_instagram_event():
    """
    High-throughput webhook ingestion route.
    Validates signature, dispatches payloads to Celery queue, and immediately returns 200 OK.
    """
    # In production, enforce Meta signature verification:
    if os.getenv("ENFORCE_META_SIGNATURE", "false").lower() == "true":
        if not verify_meta_signature(request):
            logger.warning("[Meta Webhook] Signature verification failed.")
            return jsonify({"status": "unauthorized"}), 401

    payload = request.get_json(silent=True) or {}
    object_type = payload.get("object")

    if object_type == "instagram":
        for entry in payload.get("entry", []):
            recipient_id = entry.get("id")  # Instagram Business Account ID
            for change in entry.get("changes", []):
                field = change.get("field")
                value = change.get("value", {})

                if field == "comments":
                    event_data = {
                        "recipient_id": recipient_id,
                        "media_id": value.get("media", {}).get("id"),
                        "comment_id": value.get("id"),
                        "text": value.get("text", ""),
                        "from_id": value.get("from", {}).get("id"),
                        "from_username": value.get("from", {}).get("username")
                    }
                    # Asynchronously offload to Celery
                    process_incoming_comment_event.delay(event_data)
                    logger.info(f"[Meta Webhook] Enqueued comment event from {event_data.get('from_username')}")

                elif field == "messages":
                    # Direct message fallback routing
                    messaging = value.get("messaging", [{}])[0]
                    # Enqueue DM event logic if needed
                    logger.info(f"[Meta Webhook] Received DM event from {messaging.get('sender', {}).get('id')}")

    # Immediately acknowledge webhook within < 50ms to prevent Meta retry spikes
    return jsonify({"status": "received"}), 200


@webhook_bp.route("/r/<short_code>", methods=["GET"])
def referral_redirect(short_code):
    """
    Outbound referral link wrapper. Logs click telemetry and 302-redirects to original creator destination.
    """
    db = SessionLocal()
    try:
        user_id = request.args.get("uid")
        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        user_agent = request.headers.get("User-Agent")
        referrer = request.headers.get("Referer")

        destination_url = LinkTrackerService.record_click(
            db=db,
            short_code=short_code,
            instagram_user_id=user_id,
            referrer=referrer,
            user_agent=user_agent,
            client_ip=client_ip
        )

        if not destination_url:
            abort(404)

        return redirect(destination_url, code=302)
    finally:
        db.close()
