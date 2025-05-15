import pytest
from fastapi.testclient import TestClient
from PIL import Image
from io import BytesIO
import respx
import httpx

from fastapi.testclient import TestClient
from app.app import app  # ✅ Imports the FastAPI instance

client = TestClient(app)

# --- Test /predict/ endpoint with mocked image URL ---
@respx.mock
def test_predict_from_url_png():
    test_url = "https://res.cloudinary.com/doeqiijd7/image/upload/v1747272510/zvz5ufj23kzxuf3sxkpe.png"

    # Create in-memory PNG
    img = Image.new('RGB', (380, 380), color='white')
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    respx.get(test_url).mock(return_value=httpx.Response(200, content=buf.read()))

    response = client.post("/predict/", json={"url": test_url})
    assert response.status_code == 200
    data = response.json()
    assert "probability" in data
    assert "prediction" in data

# --- Test /upload/ endpoint with mocked Cloudinary upload ---
def test_upload_png_to_cloudinary(mocker):
    mocker.patch("cloudinary.uploader.upload", return_value={
        "secure_url": "https://res.cloudinary.com/doeqiijd7/image/upload/v1747272510/zvz5ufj23kzxuf3sxkpe.png",
        "public_id": "sample",
        "format": "png"
    })

    img = Image.new('RGB', (100, 100), color='blue')
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    response = client.post(
        "/upload/",
        files={"file": ("test.png", buf, "image/png")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["format"] == "png"
    assert "url" in data
    assert "public_id" in data
