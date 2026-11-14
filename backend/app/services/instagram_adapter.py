import abc
import os
import json
import logging
import requests
from typing import Optional, Dict, Any

logger = logging.getLogger("Antigravity.InstagramAdapter")

class InstagramMessageAdapter(abc.ABC):
    """
    Abstract Adapter defining the contract for dispatching outbound Instagram messages
    and public comment replies.
    """

    @abc.abstractmethod
    def send_direct_message(self, recipient_id: str, message_text: str) -> Dict[str, Any]:
        """Dispatch a private direct message to the user."""
        pass

    @abc.abstractmethod
    def reply_to_comment(self, comment_id: str, reply_text: str) -> Dict[str, Any]:
        """Post a public reply to a specific comment thread."""
        pass


class GraphAPIMessageAdapter(InstagramMessageAdapter):
    """
    Official Meta Instagram Graph API implementation.
    Used for production with approved App Review permissions (instagram_manage_messages, instagram_manage_comments).
    """

    def __init__(self, page_access_token: str, api_version: str = "v19.0"):
        self.page_access_token = page_access_token
        self.api_version = api_version
        self.base_url = f"https://graph.facebook.com/{self.api_version}"

    def send_direct_message(self, recipient_id: str, message_text: str) -> Dict[str, Any]:
        url = f"{self.base_url}/me/messages"
        headers = {
            "Authorization": f"Bearer {self.page_access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": message_text}
        }
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=8)
            response.raise_for_status()
            logger.info(f"[GraphAPI] Dispatched DM to {recipient_id}")
            return {"status": "success", "provider": "graph_api", "response": response.json()}
        except requests.RequestException as e:
            error_data = e.response.json() if e.response else str(e)
            logger.error(f"[GraphAPI] Failed to dispatch DM to {recipient_id}: {error_data}")
            return {"status": "error", "provider": "graph_api", "error": error_data}

    def reply_to_comment(self, comment_id: str, reply_text: str) -> Dict[str, Any]:
        url = f"{self.base_url}/{comment_id}/replies"
        headers = {
            "Authorization": f"Bearer {self.page_access_token}",
            "Content-Type": "application/json"
        }
        payload = {"message": reply_text}
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=8)
            response.raise_for_status()
            logger.info(f"[GraphAPI] Replied to comment {comment_id}")
            return {"status": "success", "provider": "graph_api", "response": response.json()}
        except requests.RequestException as e:
            error_data = e.response.json() if e.response else str(e)
            logger.error(f"[GraphAPI] Failed comment reply {comment_id}: {error_data}")
            return {"status": "error", "provider": "graph_api", "error": error_data}


class InstagrapiMessageAdapter(InstagramMessageAdapter):
    """
    Instagrapi Fallback Adapter.
    Enables local development, staging tests, and accounts pending Meta App Review.
    """

    def __init__(self, username: str, session_data: Optional[str] = None):
        self.username = username
        self.session_data = session_data
        self._client = None
        self._initialize_client()

    def _initialize_client(self):
        try:
            from instagrapi import Client
            cl = Client()
            cl.delay_range = [1, 3]  # Humanized request jitter
            if self.session_data:
                try:
                    cl.set_settings(json.loads(self.session_data))
                    logger.info(f"[Instagrapi] Loaded session for @{self.username}")
                except Exception as e:
                    logger.warning(f"[Instagrapi] Failed to load session JSON: {e}")
            self._client = cl
        except ImportError:
            logger.error("[Instagrapi] instagrapi library not installed in environment.")
            self._client = None

    def send_direct_message(self, recipient_id: str, message_text: str) -> Dict[str, Any]:
        if not self._client:
            return {"status": "error", "provider": "instagrapi", "error": "Client uninitialized"}
        try:
            # direct_send accepts user_ids: list[int/str]
            res = self._client.direct_send(text=message_text, user_ids=[int(recipient_id)])
            logger.info(f"[Instagrapi] Sent DM to user_id {recipient_id}")
            return {"status": "success", "provider": "instagrapi", "thread_id": getattr(res, "id", None)}
        except Exception as e:
            logger.error(f"[Instagrapi] DM dispatch failed: {e}")
            return {"status": "error", "provider": "instagrapi", "error": str(e)}

    def reply_to_comment(self, comment_id: str, reply_text: str) -> Dict[str, Any]:
        if not self._client:
            return {"status": "error", "provider": "instagrapi", "error": "Client uninitialized"}
        try:
            # comment_reply requires media_id and comment_id
            # In instagrapi, comment_like or comment_reply
            res = self._client.comment_reply(media_id="", comment_id=int(comment_id), text=reply_text)
            logger.info(f"[Instagrapi] Replied to comment {comment_id}")
            return {"status": "success", "provider": "instagrapi", "reply_id": getattr(res, "pk", None)}
        except Exception as e:
            logger.error(f"[Instagrapi] Comment reply failed: {e}")
            return {"status": "error", "provider": "instagrapi", "error": str(e)}


class InstagramAdapterFactory:
    """
    Factory creating the designated adapter instance based on configuration or creator profile state.
    """

    @staticmethod
    def get_adapter(creator, force_mode: Optional[str] = None) -> InstagramMessageAdapter:
        mode = force_mode or os.getenv("IG_DISPATCH_ADAPTER", "graph_api")

        if mode == "graph_api" and creator.page_access_token:
            return GraphAPIMessageAdapter(page_access_token=creator.page_access_token)
        
        # Fallback to instagrapi
        logger.info(f"Selecting InstagrapiMessageAdapter fallback for @{creator.username}")
        return InstagrapiMessageAdapter(
            username=creator.username,
            session_data=creator.instagrapi_session_data
        )
