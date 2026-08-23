from pydantic import BaseModel, Field


class ContentMetrics(BaseModel):
    word_count: int = Field(
        description="Number of words in the extracted content"
    )
    sentence_count: int = Field(
        description="Number of sentences in the extracted content"
    )
    hashtag_count: int = Field(
        description="Number of hashtags found"
    )
    mention_count: int = Field(
        description="Number of mentions found"
    )
    emoji_count: int = Field(
        description="Number of emojis found"
    )
    question_present: bool = Field(
        description="Whether the content contains a question"
    )
    cta_present: bool = Field(
        description="Whether a call-to-action was detected"
    )


class ContentScores(BaseModel):
    hook: int = Field(
        ge=0,
        le=10,
        description="Hook score out of 10"
    )
    clarity: int = Field(
        ge=0,
        le=10,
        description="Clarity score out of 10"
    )
    call_to_action: int = Field(
        ge=0,
        le=10,
        description="Call-to-action score out of 10"
    )
    hashtags: int = Field(
        ge=0,
        le=10,
        description="Hashtag score out of 10"
    )
    readability: int = Field(
        ge=0,
        le=10,
        description="Readability score out of 10"
    )


class AIAnalysis(BaseModel):
    engagement_potential: int = Field(
        ge=0,
        le=100,
        description="AI-estimated engagement potential"
    )
    strengths: list[str]
    weaknesses: list[str]
    suggestions: list[str]
    improved_version: str
    recommended_tone: str
    recommended_content_type: str


class ContentAnalysis(BaseModel):
    engagement_score: int = Field(
        ge=0,
        le=100,
        description="Overall rule-based engagement score"
    )
    metrics: ContentMetrics
    scores: ContentScores
    hashtags: list[str]
    mentions: list[str]
    strengths: list[str]
    weaknesses: list[str]
    suggestions: list[str]
    improved_version: str
    ai_analysis: AIAnalysis | None = Field(
        default=None,
        description=(
            "Optional AI-powered analysis. "
            "Null when AI is not configured or unavailable."
        ),
    )


class PDFAnalysisResponse(BaseModel):
    filename: str = Field(
        description="Name of the uploaded PDF file"
    )
    file_type: str = Field(
        description="Detected file type"
    )
    page_count: int = Field(
        description="Number of pages in the PDF"
    )
    character_count: int = Field(
        description="Number of extracted characters"
    )
    word_count: int = Field(
        description="Number of extracted words"
    )
    extracted_text: str = Field(
        description="Text extracted from the PDF"
    )
    analysis: ContentAnalysis = Field(
        description="Social media content analysis"
    )


class ImageAnalysisResponse(BaseModel):
    filename: str = Field(
        description="Name of the uploaded image file"
    )
    file_type: str = Field(
        description="Detected file type"
    )
    character_count: int = Field(
        description="Number of extracted characters"
    )
    word_count: int = Field(
        description="Number of extracted words"
    )
    extracted_text: str = Field(
        description="Text extracted using OCR"
    )
    analysis: ContentAnalysis = Field(
        description="Social media content analysis"
    )