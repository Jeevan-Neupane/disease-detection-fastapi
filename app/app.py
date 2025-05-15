import torch
import torch.nn as nn
from efficientnet_pytorch import EfficientNet
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import requests
import os
from torchvision import transforms
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import io

# ----- Load .env -----
load_dotenv()

# ----- Configure Cloudinary -----
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# ----- Load EfficientNet-B4 Model -----
model = EfficientNet.from_pretrained('efficientnet-b4')
model._fc = nn.Linear(model._fc.in_features, 1)
model_path = os.path.join("data", "external", "best_zoomed_pad.pth")

model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()

# ----- Transformations for EfficientNet-B4 (380x380) -----
transform = transforms.Compose([
    transforms.Resize((380, 380)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

# ----- FastAPI App Setup -----
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageURL(BaseModel):
    url: str

def predict_image(image: Image.Image):
    image = image.convert('RGB')
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)
        probability = torch.sigmoid(output).item()

    predicted_class = int(probability > 0.5)
    return probability, predicted_class

# ----- Predict from Image URL -----
@app.post("/predict/")
async def predict_from_url(image_data: ImageURL):
    try:
        response = requests.get(image_data.url)
        if response.status_code != 200:
            return {"error": "Failed to fetch image from URL."}

        image = Image.open(io.BytesIO(response.content))
        probability, prediction = predict_image(image)

        return {
            "probability": probability,
            "prediction": prediction
        }
    except Exception as e:
        return {"error": str(e)}

# ----- Upload to Cloudinary -----
@app.post("/upload/")
async def upload_image_to_cloudinary(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        result = cloudinary.uploader.upload(contents, resource_type="image")

        return {
            "url": result.get("secure_url"),
            "public_id": result.get("public_id"),
            "format": result.get("format")
        }
    except Exception as e:
        return {"error": str(e)}

# ----- Entry point for local testing -----
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
