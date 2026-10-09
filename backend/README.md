
# Kisaan Setu Backend

Python FastAPI backend for crop market intelligence.

## Install

```bash
python -m venv .venv
```

Activate the environment, then run:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## API documentation

Open http://127.0.0.1:8000/docs

## Endpoints

- GET /api/health
- GET /api/crops
- GET /api/markets
- GET /api/compare?crop=Potato
- GET /api/listings
- POST /api/listings

Prices are synthetic demo data, not verified market rates.
