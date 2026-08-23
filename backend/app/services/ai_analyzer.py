from __future__ import annotations

import json
import os
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


class AIAnalysisError(Exception):
    """Raised when AI-powered analysis fails."""


AI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash-lite",
)


def _get_client() -> genai.Client | None:
    """
    Create a Gemini client if an API key is configured.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    return genai.Client(
        api_key=api_key,
    )


def _build_prompt(text: str) -> str:
    """
    Build a focused prompt for social-media content analysis.
    """

    return f"""
You are a professional social media content strategist.

Analyze the following extracted content.

The content may come from:
- a social media post,
- a marketing document,
- a promotional document,
- or text extracted from a scanned image.

Your task is to provide practical engagement improvements.

Return ONLY valid JSON matching the requested schema.

Focus on:
1. Overall engagement potential.
2. Strong aspects of the content.
3. Weak aspects of the content.
4. Specific actionable improvements.
5. A polished improved version of the content.
6. Suggested tone.
7. Suggested content type.

Do not invent facts that are not present in the original content.

Extracted content:

---BEGIN CONTENT---
{text}
---END CONTENT---
""".strip()


def generate_ai_analysis(
    text: str,
) -> dict[str, Any] | None:
    """
    Generate AI-powered social-media recommendations.

    Returns None when the API key is not configured.

    Raises:
        AIAnalysisError:
            When the API is configured but the request fails.
    """

    client = _get_client()

    if client is None:
        return None

    cleaned_text = text.strip()

    if not cleaned_text:
        return None

    # Prevent unnecessarily large prompts.
    # The rule-based analyzer remains responsible for
    # the complete extracted document.
    max_chars = 12000

    if len(cleaned_text) > max_chars:
        cleaned_text = cleaned_text[:max_chars]

    prompt = _build_prompt(cleaned_text)

    response_schema = {
        "type": "object",
        "properties": {
            "engagement_potential": {
                "type": "integer",
                "description": (
                    "Overall engagement potential from 0 to 100."
                ),
            },
            "strengths": {
                "type": "array",
                "items": {
                    "type": "string",
                },
                "description": "Key strengths of the content.",
            },
            "weaknesses": {
                "type": "array",
                "items": {
                    "type": "string",
                },
                "description": "Key weaknesses of the content.",
            },
            "suggestions": {
                "type": "array",
                "items": {
                    "type": "string",
                },
                "description": (
                    "Specific actionable engagement improvements."
                ),
            },
            "improved_version": {
                "type": "string",
                "description": (
                    "A polished version of the original content."
                ),
            },
            "recommended_tone": {
                "type": "string",
                "description": (
                    "Recommended tone such as professional, "
                    "friendly, conversational, or persuasive."
                ),
            },
            "recommended_content_type": {
                "type": "string",
                "description": (
                    "Suggested content type such as announcement, "
                    "promotional, educational, or engagement post."
                ),
            },
        },
        "required": [
            "engagement_potential",
            "strengths",
            "weaknesses",
            "suggestions",
            "improved_version",
            "recommended_tone",
            "recommended_content_type",
        ],
    }

    try:
        response = client.models.generate_content(
            model=AI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4,
                response_mime_type="application/json",
                response_schema=response_schema,
            ),
        )

        response_text = response.text

        if not response_text:
            raise AIAnalysisError(
                "The AI service returned an empty response."
            )

        try:
            result = json.loads(response_text)

        except json.JSONDecodeError as exc:
            raise AIAnalysisError(
                "The AI service returned an invalid JSON response."
            ) from exc

        return result

    except AIAnalysisError:
        raise

    except Exception as exc:
        raise AIAnalysisError(
            "The AI analysis service is currently unavailable."
        ) from exc