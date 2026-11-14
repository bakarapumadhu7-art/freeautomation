import os
import json
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("Antigravity.AIOrchestrator")

class IntentClassificationSchema(BaseModel):
    status: str = Field(description="'trigger_matched' if an actionable trigger is detected, else 'no_match'")
    confidence_score: float = Field(description="Confidence from 0.00 to 1.00")
    keyword: Optional[str] = Field(default=None, description="The matched trigger keyword or semantic token")
    detected_intent: str = Field(description="E.g., request_link, request_course, price_inquiry, general_praise")
    user_sentiment: str = Field(description="positive, neutral, negative")


class GeminiIntentClassifier:
    """
    Sub-second comment classification using Gemini 2.0 / 1.5 Flash with structured outputs.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
            except ImportError:
                logger.warning("[Gemini] google-genai library not installed. Will use fallback heuristics.")

    def classify_comment(
        self,
        comment_text: str,
        active_triggers: List[str],
        media_caption: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Classifies incoming comment against active creator triggers with strict JSON output schema.
        """
        if not self.client:
            return self._heuristic_fallback(comment_text, active_triggers)

        system_instruction = (
            "You are an enterprise NLP classifier for creator comment automation. "
            "Determine if the user's comment is seeking a link, resource, product, or info related to the active triggers. "
            f"Active trigger keywords: {json.dumps(active_triggers)}. "
            "Return valid JSON matching the schema precisely."
        )

        prompt = (
            f"Media Context Caption: {media_caption or 'None'}\n"
            f"User Comment: \"{comment_text}\"\n"
            "Analyze intent and classify."
        )

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "system_instruction": system_instruction,
                    "response_mime_type": "application/json",
                    "response_schema": IntentClassificationSchema,
                    "temperature": 0.1
                }
            )
            result = json.loads(response.text)
            logger.info(f"[Gemini] Classification result: {result}")
            return result
        except Exception as e:
            logger.error(f"[Gemini] Error during classification: {e}. Reverting to heuristics.")
            return self._heuristic_fallback(comment_text, active_triggers)

    def _heuristic_fallback(self, comment_text: str, active_triggers: List[str]) -> Dict[str, Any]:
        cleaned = comment_text.lower().strip()
        for trig in active_triggers:
            if trig.lower() in cleaned:
                return {
                    "status": "trigger_matched",
                    "confidence_score": 0.95,
                    "keyword": trig,
                    "detected_intent": "request_link",
                    "user_sentiment": "positive"
                }
        return {
            "status": "no_match",
            "confidence_score": 0.20,
            "keyword": None,
            "detected_intent": "general_comment",
            "user_sentiment": "neutral"
        }


class ClaudeGenerativeDMEngine:
    """
    Claude Generative DM Engine for human-sounding, anti-spam conversational copy.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY", "")
        self.client = None
        if self.api_key:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                logger.warning("[Claude] anthropic library not installed. Will use template fallback.")

    def generate_personalized_dm(
        self,
        creator_name: str,
        user_name: str,
        comment_text: str,
        destination_title: str,
        wrapped_referral_url: str
    ) -> str:
        """
        Synthesizes bespoke, spam-filter-resilient DM copy embedding the referral link.
        """
        if not self.client:
            return self._template_fallback(user_name, destination_title, wrapped_referral_url)

        system_prompt = (
            "You are a sophisticated direct messaging assistant for a top digital creator. "
            "Write a natural, warm, 2-to-3 sentence Instagram DM sent to a follower who commented on a post. "
            "CRITICAL CONSTRAINTS:\n"
            "- Do not sound like a generic bot or marketing blast.\n"
            "- Vary the structure to prevent Meta spam detection heuristics.\n"
            "- Naturally embed the referral link provided.\n"
            "- End with an engaging, low-pressure sign-off."
        )

        user_prompt = (
            f"Creator: @{creator_name}\n"
            f"Recipient Username: @{user_name}\n"
            f"User's Comment: \"{comment_text}\"\n"
            f"Requested Resource Title: {destination_title}\n"
            f"Destination Link: {wrapped_referral_url}\n\n"
            "Generate the direct message text."
        )

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=250,
                temperature=0.7,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            generated_text = message.content[0].text.strip()
            logger.info(f"[Claude] Generated personalized DM for @{user_name}")
            return generated_text
        except Exception as e:
            logger.error(f"[Claude] Error generating DM: {e}. Using template fallback.")
            return self._template_fallback(user_name, destination_title, wrapped_referral_url)

    def _template_fallback(self, user_name: str, destination_title: str, wrapped_url: str) -> str:
        return (
            f"Hey @{user_name}! Thanks for checking out the post. "
            f"Here is the direct link to the {destination_title} you requested: {wrapped_url} \n\n"
            f"Let me know if you run into any questions while diving in!"
        )
