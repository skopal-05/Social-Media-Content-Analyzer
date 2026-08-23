from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.schemas import PDFAnalysisResponse
from app.services.ai_analyzer import (
    AIAnalysisError,
    generate_ai_analysis,
)
from app.services.analyzer import analyze_content
from app.services.ocr_service import (
    OCRProcessingError,
    extract_text_from_scanned_pdf,
)
from app.services.pdf_extractor import (
    PDFExtractionError,
    extract_text_from_pdf,
)


router = APIRouter(
    prefix="/analyze",
    tags=["PDF Analysis"],
)


MAX_FILE_SIZE = 10 * 1024 * 1024

ALLOWED_EXTENSION = ".pdf"

ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/x-pdf",
}


@router.post(
    "/pdf",
    response_model=PDFAnalysisResponse,
    summary="Upload and analyze a PDF",
    description=(
        "Extracts text from normal or scanned PDFs "
        "and provides rule-based and optional "
        "AI-powered analysis."
    ),
)
async def analyze_pdf(
    file: UploadFile = File(...),
):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename was provided.",
        )

    filename = file.filename.strip()

    if not filename.lower().endswith(
        ALLOWED_EXTENSION
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported.",
        )

    if (
        file.content_type
        and file.content_type
        not in ALLOWED_CONTENT_TYPES
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is not a valid PDF.",
        )

    try:
        file_bytes = await file.read()

        if not file_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded PDF is empty.",
            )

        if len(file_bytes) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds the 10 MB limit.",
            )

        # ---------------------------------------------------------
        # Step 1: Try normal PDF text extraction using PyMuPDF
        # ---------------------------------------------------------
        try:
            extracted_text, page_count = (
                extract_text_from_pdf(
                    file_bytes
                )
            )

        except PDFExtractionError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc

        # ---------------------------------------------------------
        # Step 2: If no selectable text is found,
        #         use Tesseract OCR on the scanned PDF.
        # ---------------------------------------------------------
        if not extracted_text.strip():

            try:
                extracted_text, page_count = (
                    extract_text_from_scanned_pdf(
                        file_bytes
                    )
                )

            except OCRProcessingError as exc:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=str(exc),
                ) from exc

            if not extracted_text.strip():
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=(
                        "No readable text was found in this PDF, "
                        "even after OCR processing. "
                        "Please upload a clearer document."
                    ),
                )

            file_type = "PDF (OCR)"

        else:
            file_type = "PDF"

        # ---------------------------------------------------------
        # Step 3: Rule-based content analysis
        # ---------------------------------------------------------
        try:
            analysis = analyze_content(
                extracted_text
            )

        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc),
            ) from exc

        # ---------------------------------------------------------
        # Step 4: Optional Gemini AI analysis
        # ---------------------------------------------------------
        try:
            ai_result = generate_ai_analysis(
                extracted_text
            )

            if ai_result is not None:
                analysis["ai_analysis"] = (
                    ai_result
                )

        except AIAnalysisError:
            # AI failure should not prevent the
            # rule-based analysis from being returned.
            analysis["ai_analysis"] = None

        # ---------------------------------------------------------
        # Step 5: Calculate basic text statistics
        # ---------------------------------------------------------
        word_count = len(
            extracted_text.split()
        )

        character_count = len(
            extracted_text
        )

        # ---------------------------------------------------------
        # Step 6: Return structured response
        # ---------------------------------------------------------
        return PDFAnalysisResponse(
            filename=filename,
            file_type=file_type,
            page_count=page_count,
            character_count=character_count,
            word_count=word_count,
            extracted_text=extracted_text,
            analysis=analysis,
        )

    finally:
        await file.close()