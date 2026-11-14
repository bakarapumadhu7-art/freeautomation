import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Boolean, Integer, Float, ForeignKey, DateTime, Index
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class CreatorProfile(Base):
    """
    Primary creator profile representing the Instagram account and automation config.
    """
    __tablename__ = "creator_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    instagram_user_id = Column(String(64), unique=True, nullable=False, index=True)
    username = Column(String(128), nullable=False)
    page_access_token = Column(Text, nullable=True)  # Official Graph API Page Token
    instagrapi_session_data = Column(Text, nullable=True)  # Fallback session JSON
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    media_objects = relationship("MediaObject", back_populates="creator", cascade="all, delete-orphan")
    destinations = relationship("DestinationURL", back_populates="creator", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CreatorProfile @{self.username} [{self.instagram_user_id}]>"


class MediaObject(Base):
    """
    Reels, carousels, or feed posts monitored for comment triggers.
    """
    __tablename__ = "media_objects"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    creator_id = Column(String(36), ForeignKey("creator_profiles.id"), nullable=False, index=True)
    instagram_media_id = Column(String(64), unique=True, nullable=False, index=True)
    media_type = Column(String(32), default="REEL")  # REEL, POST, CAROUSEL
    permalink = Column(String(256), nullable=True)
    caption = Column(Text, nullable=True)
    auto_reply_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    creator = relationship("CreatorProfile", back_populates="media_objects")
    triggers = relationship("TriggerKeyword", back_populates="media_object", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MediaObject {self.instagram_media_id} ({self.media_type})>"


class DestinationURL(Base):
    """
    Creator conversion goals: Courses, digital products, affiliate links, lead magnets.
    """
    __tablename__ = "destination_urls"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    creator_id = Column(String(36), ForeignKey("creator_profiles.id"), nullable=False, index=True)
    title = Column(String(128), nullable=False)
    original_url = Column(Text, nullable=False)
    short_code = Column(String(32), unique=True, nullable=False, index=True)
    click_count = Column(Integer, default=0)
    conversion_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    creator = relationship("CreatorProfile", back_populates="destinations")
    triggers = relationship("TriggerKeyword", back_populates="destination")
    clicks = relationship("ReferralClick", back_populates="destination", cascade="all, delete-orphan")

    @property
    def ctr(self) -> float:
        if self.click_count == 0:
            return 0.0
        return round((self.conversion_count / self.click_count) * 100, 2)

    def __repr__(self):
        return f"<DestinationURL {self.title} -> {self.short_code}>"


class TriggerKeyword(Base):
    """
    Specific keywords or semantic intent patterns linked to an automated dispatch.
    """
    __tablename__ = "trigger_keywords"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    media_object_id = Column(String(36), ForeignKey("media_objects.id"), nullable=True, index=True)
    destination_url_id = Column(String(36), ForeignKey("destination_urls.id"), nullable=False, index=True)
    keyword = Column(String(64), nullable=False, index=True)  # e.g., "link", "course", "agent"
    match_strategy = Column(String(32), default="SEMANTIC_AI")  # EXACT, CONTAINS, SEMANTIC_AI
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    media_object = relationship("MediaObject", back_populates="triggers")
    destination = relationship("DestinationURL", back_populates="triggers")

    __table_args__ = (
        Index("idx_keyword_media", "keyword", "media_object_id"),
    )

    def __repr__(self):
        return f"<TriggerKeyword '{self.keyword}' [{self.match_strategy}]>"


class ReferralClick(Base):
    """
    Granular analytics tracking for wrapped outbound referral clicks.
    """
    __tablename__ = "referral_clicks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    destination_url_id = Column(String(36), ForeignKey("destination_urls.id"), nullable=False, index=True)
    instagram_user_id = Column(String(64), nullable=True, index=True)
    referrer = Column(String(256), nullable=True)
    user_agent = Column(Text, nullable=True)
    ip_hash = Column(String(64), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    destination = relationship("DestinationURL", back_populates="clicks")
