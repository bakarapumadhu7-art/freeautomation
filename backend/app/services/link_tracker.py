import hashlib
import secrets
from typing import Optional
from sqlalchemy.orm import Session
from ..models.schema import DestinationURL, ReferralClick

class LinkTrackerService:
    """
    Handles generation of unique referral short-codes and records granular telemetry
    for conversion and CTR reporting.
    """

    @staticmethod
    def generate_short_code(length: int = 7) -> str:
        return secrets.token_urlsafe(length)[:length]

    @staticmethod
    def record_click(
        db: Session,
        short_code: str,
        instagram_user_id: Optional[str] = None,
        referrer: Optional[str] = None,
        user_agent: Optional[str] = None,
        client_ip: Optional[str] = None
    ) -> Optional[str]:
        """
        Records the click event, updates aggregate metrics, and returns the original destination URL.
        """
        dest = db.query(DestinationURL).filter(DestinationURL.short_code == short_code).first()
        if not dest:
            return None

        # Anonymize IP via SHA256 hash
        ip_hash = hashlib.sha256(client_ip.encode("utf-8")).hexdigest() if client_ip else None

        click = ReferralClick(
            destination_url_id=dest.id,
            instagram_user_id=instagram_user_id,
            referrer=referrer,
            user_agent=user_agent,
            ip_hash=ip_hash
        )
        dest.click_count += 1
        db.add(click)
        db.commit()

        return dest.original_url
