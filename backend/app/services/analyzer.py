import re
from typing import Any


CTA_PATTERNS = [
    r"\bclick\b",
    r"\blearn more\b",
    r"\bcheck out\b",
    r"\bvisit\b",
    r"\bexplore\b",
    r"\bdiscover\b",
    r"\btry\b",
    r"\bget started\b",
    r"\bsign up\b",
    r"\bsubscribe\b",
    r"\bdownload\b",
    r"\bcontact\b",
    r"\bshop\b",
    r"\bbuy\b",
    r"\bbook\b",
    r"\bfollow\b",
    r"\bshare\b",
    r"\bcomment\b",
    r"\blet us know\b",
    r"\btell us\b",
]


def _count_sentences(text: str) -> int:
    sentences = re.split(r"[.!?]+", text)

    return len(
        [
            sentence
            for sentence in sentences
            if sentence.strip()
        ]
    )


def _extract_hashtags(text: str) -> list[str]:
    return re.findall(
        r"#[A-Za-z0-9_]+",
        text,
    )


def _extract_mentions(text: str) -> list[str]:
    return re.findall(
        r"@[A-Za-z0-9_.]+",
        text,
    )


def _count_emojis(text: str) -> int:
    emoji_pattern = re.compile(
        "["
        "\U0001F300-\U0001F5FF"
        "\U0001F600-\U0001F64F"
        "\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FAFF"
        "\U00002700-\U000027BF"
        "\U00002600-\U000026FF"
        "]"
    )

    return len(
        emoji_pattern.findall(text)
    )


def _has_cta(text: str) -> bool:
    lowered_text = text.lower()

    return any(
        re.search(
            pattern,
            lowered_text,
        )
        for pattern in CTA_PATTERNS
    )


def _calculate_readability_score(
    word_count: int,
    sentence_count: int,
) -> int:
    if word_count == 0:
        return 0

    if sentence_count == 0:
        return 5

    average_sentence_length = (
        word_count / sentence_count
    )

    if average_sentence_length <= 12:
        return 10

    if average_sentence_length <= 20:
        return 9

    if average_sentence_length <= 28:
        return 7

    if average_sentence_length <= 40:
        return 5

    return 3


def _calculate_hook_score(
    text: str,
) -> int:
    if not text.strip():
        return 0

    first_sentence = re.split(
        r"[.!?]+",
        text.strip(),
    )[0].strip()

    score = 5

    if len(first_sentence.split()) <= 15:
        score += 3

    if (
        "?" in first_sentence
        or "!" in first_sentence
    ):
        score += 2

    return min(score, 10)


def _calculate_cta_score(
    text: str,
) -> int:
    if _has_cta(text):
        return 10

    if "?" in text:
        return 7

    return 3


def _calculate_hashtag_score(
    hashtags: list[str],
) -> int:
    count = len(hashtags)

    if 2 <= count <= 5:
        return 10

    if count == 1:
        return 7

    if count == 0:
        return 3

    if 6 <= count <= 10:
        return 7

    return 4


def _calculate_engagement_score(
    hook_score: int,
    clarity_score: int,
    cta_score: int,
    hashtag_score: int,
    readability_score: int,
    question_present: bool,
    emoji_count: int,
) -> int:
    base_score = (
        hook_score
        + clarity_score
        + cta_score
        + hashtag_score
        + readability_score
    )

    engagement_bonus = 0

    if question_present:
        engagement_bonus += 3

    if 1 <= emoji_count <= 5:
        engagement_bonus += 2

    score = base_score + engagement_bonus

    return max(
        0,
        min(score, 100),
    )


def _get_clarity_score(
    word_count: int,
    sentence_count: int,
) -> int:
    if word_count == 0:
        return 0

    if sentence_count == 0:
        return 5

    average_sentence_length = (
        word_count / sentence_count
    )

    if average_sentence_length <= 15:
        return 10

    if average_sentence_length <= 25:
        return 9

    if average_sentence_length <= 35:
        return 7

    if average_sentence_length <= 45:
        return 5

    return 3


def _build_strengths(
    hook_score: int,
    clarity_score: int,
    cta_score: int,
    hashtag_score: int,
    readability_score: int,
    question_present: bool,
    emoji_count: int,
) -> list[str]:
    strengths = []

    if hook_score >= 8:
        strengths.append(
            "The opening has a reasonably strong hook."
        )

    if clarity_score >= 8:
        strengths.append(
            "The content is clear and easy to understand."
        )

    if cta_score >= 8:
        strengths.append(
            "A clear call-to-action is present."
        )

    if hashtag_score >= 8:
        strengths.append(
            "The hashtag usage is well balanced."
        )

    if readability_score >= 8:
        strengths.append(
            "The content is easy to read."
        )

    if question_present:
        strengths.append(
            "A question can encourage audience interaction."
        )

    if 1 <= emoji_count <= 5:
        strengths.append(
            "Relevant emoji usage adds visual appeal."
        )

    if not strengths:
        strengths.append(
            "The content provides a base message that can be improved."
        )

    return strengths


def _build_weaknesses(
    hook_score: int,
    clarity_score: int,
    cta_score: int,
    hashtag_score: int,
    readability_score: int,
    question_present: bool,
) -> list[str]:
    weaknesses = []

    if hook_score < 7:
        weaknesses.append(
            "The opening could use a stronger attention-grabbing hook."
        )

    if clarity_score < 7:
        weaknesses.append(
            "Some sentences may be too long or dense."
        )

    if cta_score < 7:
        weaknesses.append(
            "There is no strong call-to-action."
        )

    if hashtag_score < 7:
        weaknesses.append(
            "Hashtag usage could be improved."
        )

    if readability_score < 7:
        weaknesses.append(
            "The content could be made more concise and readable."
        )

    if not question_present:
        weaknesses.append(
            "Adding a relevant question could encourage comments."
        )

    return weaknesses


def _build_suggestions(
    hook_score: int,
    clarity_score: int,
    cta_score: int,
    hashtag_count: int,
    readability_score: int,
    question_present: bool,
) -> list[str]:
    suggestions = []

    if hook_score < 7:
        suggestions.append(
            "Start with a stronger hook that immediately communicates value."
        )

    if clarity_score < 7:
        suggestions.append(
            "Break long sentences into shorter, easier-to-scan lines."
        )

    if cta_score < 7:
        suggestions.append(
            "Add a direct call-to-action such as asking users to comment, visit, or learn more."
        )

    if hashtag_count == 0:
        suggestions.append(
            "Add 2–5 relevant hashtags to improve content discoverability."
        )

    elif hashtag_count == 1:
        suggestions.append(
            "Consider adding a few more relevant hashtags."
        )

    elif hashtag_count > 10:
        suggestions.append(
            "Reduce the number of hashtags and keep only the most relevant ones."
        )

    if not question_present:
        suggestions.append(
            "End with a relevant question to encourage audience interaction."
        )

    if readability_score < 7:
        suggestions.append(
            "Use shorter sentences and clearer formatting for better readability."
        )

    if not suggestions:
        suggestions.append(
            "The content is already well structured. Test different hooks and CTAs to improve performance."
        )

    return suggestions


def _build_improved_version(
    text: str,
    hashtags: list[str],
    question_present: bool,
    cta_present: bool,
) -> str:
    cleaned_text = " ".join(
        text.split()
    )

    if not cleaned_text:
        return ""

    sentences = re.split(
        r"(?<=[.!?])\s+",
        cleaned_text,
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    if not sentences:
        return cleaned_text

    first_sentence = sentences[0]

    if len(first_sentence.split()) > 15:
        words = first_sentence.split()

        hook = (
            " ".join(words[:15])
            .rstrip(",;:")
            + "..."
        )

    else:
        hook = first_sentence

    remaining_sentences = sentences[1:4]

    result_parts = [
        f"✨ {hook}"
    ]

    result_parts.extend(
        remaining_sentences
    )

    if not question_present:
        result_parts.append(
            "What do you think? Let us know in the comments!"
        )

    elif not cta_present:
        result_parts.append(
            "Let us know what you think!"
        )

    if hashtags:
        result_parts.append(
            " ".join(hashtags[:5])
        )

    return "\n\n".join(
        result_parts
    )


def analyze_content(
    text: str,
) -> dict[str, Any]:
    """
    Perform transparent rule-based social media analysis.
    """

    cleaned_text = text.strip()

    if not cleaned_text:
        raise ValueError(
            "No text was provided for content analysis."
        )

    words = re.findall(
        r"\b[\w'-]+\b",
        cleaned_text,
    )

    word_count = len(words)

    sentence_count = _count_sentences(
        cleaned_text
    )

    hashtags = _extract_hashtags(
        cleaned_text
    )

    mentions = _extract_mentions(
        cleaned_text
    )

    emoji_count = _count_emojis(
        cleaned_text
    )

    question_present = (
        "?" in cleaned_text
    )

    cta_present = _has_cta(
        cleaned_text
    )

    hashtag_count = len(
        hashtags
    )

    hook_score = _calculate_hook_score(
        cleaned_text
    )

    clarity_score = _get_clarity_score(
        word_count,
        sentence_count,
    )

    cta_score = _calculate_cta_score(
        cleaned_text
    )

    hashtag_score = _calculate_hashtag_score(
        hashtags
    )

    readability_score = (
        _calculate_readability_score(
            word_count,
            sentence_count,
        )
    )

    engagement_score = (
        _calculate_engagement_score(
            hook_score=hook_score,
            clarity_score=clarity_score,
            cta_score=cta_score,
            hashtag_score=hashtag_score,
            readability_score=readability_score,
            question_present=question_present,
            emoji_count=emoji_count,
        )
    )

    strengths = _build_strengths(
        hook_score=hook_score,
        clarity_score=clarity_score,
        cta_score=cta_score,
        hashtag_score=hashtag_score,
        readability_score=readability_score,
        question_present=question_present,
        emoji_count=emoji_count,
    )

    weaknesses = _build_weaknesses(
        hook_score=hook_score,
        clarity_score=clarity_score,
        cta_score=cta_score,
        hashtag_score=hashtag_score,
        readability_score=readability_score,
        question_present=question_present,
    )

    suggestions = _build_suggestions(
        hook_score=hook_score,
        clarity_score=clarity_score,
        cta_score=cta_score,
        hashtag_count=hashtag_count,
        readability_score=readability_score,
        question_present=question_present,
    )

    improved_version = (
        _build_improved_version(
            text=cleaned_text,
            hashtags=hashtags,
            question_present=question_present,
            cta_present=cta_present,
        )
    )

    return {
        "engagement_score": engagement_score,
        "metrics": {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "hashtag_count": hashtag_count,
            "mention_count": len(mentions),
            "emoji_count": emoji_count,
            "question_present": question_present,
            "cta_present": cta_present,
        },
        "scores": {
            "hook": hook_score,
            "clarity": clarity_score,
            "call_to_action": cta_score,
            "hashtags": hashtag_score,
            "readability": readability_score,
        },
        "hashtags": hashtags,
        "mentions": mentions,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
        "improved_version": improved_version,
        "ai_analysis": None,
    }