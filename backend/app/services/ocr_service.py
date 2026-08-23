from __future__ import annotations

from io import BytesIO

import easyocr
import fitz
import numpy as np
from PIL import Image


class OCRProcessingError(Exception):
    """Raised when OCR processing fails."""


# English OCR reader.
# The reader is created once and reused for subsequent requests.
_reader: easyocr.Reader | None = None


def get_ocr_reader() -> easyocr.Reader:
    """
    Create and return a reusable EasyOCR reader.

    The model is loaded only once instead of being loaded
    for every uploaded file.
    """
    global _reader

    if _reader is None:
        _reader = easyocr.Reader(
            ["en"],
            gpu=False,
            verbose=False,
        )

    return _reader


def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extract text from a JPG, JPEG, or PNG image using EasyOCR.
    """
    if not image_bytes:
        raise OCRProcessingError("The uploaded image is empty.")

    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        image_array = np.array(image)

        reader = get_ocr_reader()

        results = reader.readtext(
            image_array,
            detail=1,
            paragraph=False,
        )

        extracted_lines = []

        for result in results:
            if len(result) >= 2:
                detected_text = result[1].strip()

                if detected_text:
                    extracted_lines.append(detected_text)

        return "\n".join(extracted_lines).strip()

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
    Render each page of an image-only PDF and run OCR on it.

    Returns:
        extracted text and page count.
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

        reader = get_ocr_reader()
        extracted_pages = []

        zoom = dpi / 72
        matrix = fitz.Matrix(zoom, zoom)

        for page in document:
            pixmap = page.get_pixmap(
                matrix=matrix,
                alpha=False,
            )

            image_array = np.frombuffer(
                pixmap.samples,
                dtype=np.uint8,
            )

            image_array = image_array.reshape(
                pixmap.height,
                pixmap.width,
                pixmap.n,
            )

            if pixmap.n == 4:
                image_array = image_array[:, :, :3]

            results = reader.readtext(
                image_array,
                detail=1,
                paragraph=False,
            )

            page_lines = []

            for result in results:
                if len(result) >= 2:
                    detected_text = result[1].strip()

                    if detected_text:
                        page_lines.append(detected_text)

            page_text = "\n".join(page_lines).strip()

            if page_text:
                extracted_pages.append(page_text)

        extracted_text = "\n\n".join(
            extracted_pages
        ).strip()

        return extracted_text, document.page_count

    except OCRProcessingError:
        raise

    except Exception as exc:
        raise OCRProcessingError(
            "Unable to process the scanned PDF using OCR."
        ) from exc

    finally:
        if document is not None:
            document.close()