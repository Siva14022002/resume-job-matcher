
import pdfplumber


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF resume."""

    extracted_text = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                extracted_text.append(page_text)

    return "\n".join(extracted_text).strip()
