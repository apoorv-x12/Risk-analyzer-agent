# moved from project root
import fitz  # PyMuPDF

def load_document(pdf_path):
    """Loads a PDF and returns its full text as a string."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

if __name__ == "__main__":
    pdf_path = "sample.pdf"
    text = load_document(pdf_path)
    print(text[:1000])  # Print the first 1000 characters for preview 