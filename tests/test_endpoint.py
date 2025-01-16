import requests
import os


# Add a pdf in tests/files/cambodia-visa.pdf
def test_extract_pdf_live():
    # Get the path relative to the project root
    file_path = os.path.join("files", "cambodia-visa.pdf")
    with open(file_path, "rb") as file:
        response = requests.post("http://localhost:8000/extract", files={"file": file})

    assert response.status_code == 200
    assert "result" in response.json()


if __name__ == "__main__":
    test_extract_pdf_live()
