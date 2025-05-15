# twelve_factor_app

[![CCDS Project Template](https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter)](https://cookiecutter-data-science.drivendata.org/)

A production-ready, reproducible, and maintainable Python application for automated eye disease detection from images, following the [Twelve-Factor App](https://12factor.net/) methodology.

---

## Overview

This project provides a FastAPI-based backend for:

- **Uploading eye images to Cloudinary** and retrieving a secure URL.
- **Predicting eye disease** from an image URL using a PyTorch EfficientNet-B4 model.

It is designed for easy deployment (Docker-ready), robust testing, and modern Python best practices.

---

## Features

- **REST API** for image upload and disease prediction
- **Cloudinary integration** for secure image storage
- **EfficientNet-B4** PyTorch model for inference
- **Environment variable configuration** via `.env`
- **Automated testing** with pytest
- **Code linting and formatting** with Ruff
- **Docker support** for containerized deployment

---

## Project Structure

```
├── app/
│   └── app.py                # FastAPI application
├── data/
│   └── external/             # Place model weights here (e.g., best_zoomed_pad.pth)
├── tests/
│   └── test_app.py           # API and integration tests
├── twelve_factor_app/
│   └── __init__.py
├── requirements.txt
├── Dockerfile
├── .env
├── Makefile
├── README.md
└── ...
```

---

## Setup

### 1. Clone the repository

```sh
git clone <repo-url>
cd twelve_factor_app
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env` and fill in your Cloudinary credentials:

```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### 4. Download model weights

Place your trained model file (e.g., `best_zoomed_pad.pth`) in `data/external/`.

---

## Usage

### Run the API locally

```sh
python .\app\app.py     
```

### API Endpoints

#### 1. Upload Image to Cloudinary

- **POST** `/upload/`
- **Body:** multipart/form-data (`file`)
- **Response:** `{ "url": "<cloudinary_url>", "public_id": "...", "format": "..." }`

#### 2. Predict Eye Disease from Image URL

- **POST** `/predict/`
- **Body:** JSON `{ "url": "<image_url>" }`
- **Response:** `{ "probability": <float>, "prediction": <0 or 1> }`

---

## Example Workflow

1. **Upload an image** to `/upload/` and get the Cloudinary URL.
2. **Send the URL** to `/predict/` to receive a disease probability and prediction.

---

## Testing

Run all tests:

```sh
pytest
```

---

## Linting & Formatting

Check code style:

```sh
make lint
```

Auto-format code:

```sh
make format
```

---

## Docker

Build and run the app in Docker:

```sh
docker build -t twelve_factor_app .
docker run --env-file .env -p 8000:8000 twelve_factor_app
```

---

## Documentation

Build and serve docs locally:

```sh
mkdocs serve
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.