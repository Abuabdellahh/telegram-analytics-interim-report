#!/bin/bash

# Exit on error
set -e

# Load environment variables
export $(grep -v '^#' .env | xargs)

# 1. Run the Telegram scraper
python -m src.scraper.telegram_scraper

# 2. Load raw data into PostgreSQL
python -m src.transformer.load_raw_data

# 3. Run dbt transformations
dbt run --profiles-dir dbt

# 4. Run dbt tests
dbt test --profiles-dir dbt

# 5. Run YOLO image processing
python -m src.transformer.process_images

# 6. Start the API server
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
