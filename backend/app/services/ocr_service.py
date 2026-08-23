from __future__ import annotations

from io import BytesIO

import fitz
import pytesseract
from PIL import Image


class OCRProcessingError(Exception):
    """Raised when OCR processing fails."""


def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extract text from JPG, JPEG, or PNG images using Tesseract OCR.
    """

    if not image_bytes:
        raise OCRProcessingError(
            "The uploaded image is empty."
        )

    try:
        image = Image.open(
            BytesIO(image_bytes)
        ).convert("RGB")

        extracted_text = pytesseract.image_to_string(
            image,
            lang="eng",
        )

        return extracted_text.strip()

    except OCRProcessingError:
        raise

    except Exception as exc:
        raise OCRProcessingError(
            "Unable to process the uploaded image using OCR."
        ) from exc


def extract_text_from_scanned_pdf(
    file_bytes: bytes,
    dpi: int = 150,
) -> tuple[str, int]:
    """
    Render each page of a scanned PDF and run
    Tesseract OCR on each page.

    Returns:
        Tuple containing extracted text and page count.
    """

    document = None

    try:
        document = fitz.open(
            stream=file_bytes,
            filetype="pdf",
        )

        if document.page_count == 0:
            raise OCRProcessingError(
                "The uploaded PDF contains no pages."
            )

        extracted_pages = []

        zoom = dpi / 72
        matrix = fitz.Matrix(
            zoom,
            zoom,
        )

        for page in document:
            pixmap = page.get_pixmap(
                matrix=matrix,
                alpha=False,
            )

            image = Image.frombytes(
                "RGB",
                (
                    pixmap.width,
                    pixmap.height,
                ),
                pixmap.samples,
            )

            page_text = pytesseract.image_to_string(
                image,
                lang="eng",
            ).strip()

            if page_text:
                extracted_pages.append(
                    page_text
                )

        extracted_text = "\n\n".join(
            extracted_pages
        ).strip()

        return (
            extracted_text,
            document.page_count,
        )

    except OCRProcessingError:
        raise

    except Exception as exc:
        raise OCRProcessingError(
            "Unable to process the scanned PDF using OCR."
        ) from exc

    finally:
        if document is not None:
            document.close()