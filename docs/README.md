# twelve_factor_app

This project is a template for a production-ready, reproducible, and maintainable Python application following the [Twelve-Factor App](https://12factor.net/) methodology.

## Features

- FastAPI backend for serving ML models
- EfficientNet-based PyTorch model for image tasks
- Docker-ready and environment-variable driven
- Pre-commit hooks and code linting with Ruff
- Automated testing with pytest

## Project Structure

```
├── LICENSE
├── Makefile
├── README.md
├── .env
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── app/
│   └── app.py
├── data/
│   ├── external/
│   ├── images/
│   ├── interim/
│   ├── processed/
│   └── raw/
├── docs/
│   ├── mkdocs.yml
│   └── docs/
├── models/
├── notebooks/
├── references/
├── reports/
│   └── figures/
├── tests/
│   ├── test_app.py
│   └── test_data.py
└── twelve_factor_app/
    └── __init__.py
```

## Setup

1. **Clone the repository**
2. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```
3. **Set environment variables**  
   Copy `.env` and fill in your secrets.

4. **Run pre-commit hooks (optional)**
    ```sh
    pre-commit install
    ```

5. **Run the application**
    ```sh
    uvicorn app.app:app --reload
    ```

## Testing

Run all tests with:

```sh
pytest
```

## Linting and Formatting

Check code style with:

```sh
make lint
```

Format code with:

```sh
make format
```

## Documentation

Build and serve docs locally:

```sh
mkdocs serve
```

---

MIT License. See [LICENSE](LICENSE) for details.