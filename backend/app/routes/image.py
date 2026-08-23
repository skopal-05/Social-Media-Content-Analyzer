from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.schemas import ImageAnalysisResponse
from app.services.ai_analyzer import (
    AIAnalysisError,
    generate_ai_analysis,
)
from app.services.analyzer import analyze_content
from app.services.ocr_service import (
    OCRProcessingError,
    extract_text_from_image,
)


router = APIRouter(
    prefix="/analyze",
    tags=["Image Analysis"],
)


MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
}

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
}


@router.post(
    "/image",
    response_model=ImageAnalysisResponse,
    summary="Upload and analyze an image",
    description=(
        "Extracts text from JPG, JPEG, or PNG images "
        "using OCR and provides rule-based and optional "
        "AI-powered analysis."
    ),
)
async def analyze_image(
    file: UploadFile = File(...),
):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename was provided.",
        )

    filename = file.filename.strip()

    if "." not in filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Only JPG, JPEG, and PNG image files "
                "are supported."
            ),
        )

    extension = "." + filename.rsplit(
        ".",
        1,
    )[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Only JPG, JPEG, and PNG image files "
                "are supported."
            ),
        )

    if (
        file.content_type
        and file.content_type
        not in ALLOWED_CONTENT_TYPES
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is not a valid image.",
        )

    try:
        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded image is empty.",
            )

        if len(file_bytes) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds the 10 MB limit.",
            )

        try:
            extracted_text = (
                extract_text_from_image(
                    file_bytes
                )
            )

        except OCRProcessingError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc),
            ) from exc

        if not extracted_text:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "No readable text was found in this image. "
                    "Please upload a clearer image."
                ),
            )

        try:
            analysis = analyze_content(
                extracted_text
            )

        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc),
            ) from exc

        # AI is optional. If it fails, the rule-based
        # analysis is still returned.
        try:
            ai_result = generate_ai_analysis(
                extracted_text
            )

            if ai_result is not None:
                analysis["ai_analysis"] = (
                    ai_result
                )

        except AIAnalysisError:
            analysis["ai_analysis"] = None

        word_count = len(
            extracted_text.split()
        )

        character_count = len(
            extracted_text
        )

        return ImageAnalysisResponse(
            filename=filename,
            file_type="IMAGE (OCR)",
            character_count=character_count,
            word_count=word_count,
            extracted_text=extracted_text,
            analysis=analysis,
        )

    finally:
        await file.close()