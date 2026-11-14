import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .celery_app import celery_app
from ..config import Config
from ..models.schema import CreatorProfile, MediaObject, TriggerKeyword, DestinationURL
from ..services.ai_orchestrator import GeminiIntentClassifier, ClaudeGenerativeDMEngine
from ..services.instagram_adapter import InstagramAdapterFactory

logger = logging.getLogger("Antigravity.AutomationTask")

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

gemini_classifier = GeminiIntentClassifier()
claude_engine = ClaudeGenerativeDMEngine()

@celery_app.task(bind=True, max_retries=3, default_retry_delay=10)
def process_incoming_comment_event(self, event_payload: dict):
    """
    Asynchronously orchestrates:
    1. Parsing comment and metadata
    2. Looking up Creator Profile and active Trigger Keywords
    3. Gemini NLP intent validation
    4. Claude personalized DM generation with referral link
    5. Adapter dispatch (Graph API or instagrapi fallback)
    """
    logger.info(f"Processing event payload: {event_payload}")
    db = SessionLocal()
    try:
        media_id = event_payload.get("media_id")
        comment_id = event_payload.get("comment_id")
        comment_text = event_payload.get("text", "")
        sender_id = event_payload.get("from_id")
        sender_username = event_payload.get("from_username", "there")
        creator_ig_id = event_payload.get("recipient_id")

        creator = db.query(CreatorProfile).filter(CreatorProfile.instagram_user_id == creator_ig_id).first()
        if not creator or not creator.is_active:
            logger.warning(f"No active CreatorProfile for ID {creator_ig_id}")
            return {"status": "skipped", "reason": "creator_not_found"}

        # Fetch active triggers for this media or account
        triggers = (
            db.query(TriggerKeyword)
            .join(DestinationURL)
            .filter(DestinationURL.creator_id == creator.id, TriggerKeyword.is_active.is_(True))
            .all()
        )
        if not triggers:
            logger.info("No active triggers registered for creator.")
            return {"status": "skipped", "reason": "no_triggers"}

        keyword_map = {t.keyword.lower(): t for t in triggers}
        active_keywords = list(keyword_map.keys())

        # Step 1: Gemini Intent Classification
        classification = gemini_classifier.classify_comment(
            comment_text=comment_text,
            active_triggers=active_keywords
        )

        if classification.get("status") != "trigger_matched":
            logger.info(f"Comment '{comment_text}' did not match intent criteria.")
            return {"status": "ignored", "classification": classification}

        matched_keyword = classification.get("keyword", "").lower()
        trigger_record = keyword_map.get(matched_keyword) or triggers[0]
        destination = trigger_record.destination

        wrapped_url = f"{Config.BASE_TRACKING_URL}{destination.short_code}?uid={sender_id}"

        # Step 2: Claude Personalized DM Synthesis
        personalized_dm = claude_engine.generate_personalized_dm(
            creator_name=creator.username,
            user_name=sender_username,
            comment_text=comment_text,
            destination_title=destination.title,
            wrapped_referral_url=wrapped_url
        )

        # Step 3: Outbound Dispatch via Adapter
        adapter = InstagramAdapterFactory.get_adapter(creator)
        dispatch_result = adapter.send_direct_message(
            recipient_id=sender_id,
            message_text=personalized_dm
        )

        # Optional: Public Reply to comment
        adapter.reply_to_comment(
            comment_id=comment_id,
            reply_text=f"Sent the link to your DMs @{sender_username}! Check your inbox."
        )

        return {
            "status": "dispatched",
            "dispatch_result": dispatch_result,
            "classification": classification
        }

    except Exception as exc:
        logger.error(f"Error in automation pipeline: {exc}", exc_info=True)
        raise self.retry(exc=exc)
    finally:
        db.close()
