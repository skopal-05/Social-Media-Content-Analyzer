import fitz


class PDFExtractionError(Exception):
    """Raised when PDF text extraction fails."""


def extract_text_from_pdf(file_bytes: bytes) -> tuple[str, int]:
    """
    Extract text from a PDF using PyMuPDF.

    Args:
        file_bytes: PDF file contents as bytes.

    Returns:
        A tuple containing:
        - extracted text
        - number of pages

    Raises:
        PDFExtractionError: If the PDF cannot be opened or processed.
    """
    document = None

    try:
        document = fitz.open(
            stream=file_bytes,
            filetype="pdf",
        )

        if document.page_count == 0:
            raise PDFExtractionError(
                "The uploaded PDF contains no pages."
            )

        extracted_pages = []

        for page in document:
            page_text = page.get_text(
                "text",
                sort=True,
            ).strip()

            if page_text:
                extracted_pages.append(page_text)

        extracted_text = "\n\n".join(
            extracted_pages
        ).strip()

        return extracted_text, document.page_count

    except PDFExtractionError:
        raise

    except Exception as exc:
        raise PDFExtractionError(
            "The uploaded file could not be processed as a valid PDF."
        ) from exc

    finally:
        if document is not None:
            document.close()