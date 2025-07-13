# Telegram Analytics Pipeline

An end-to-end data pipeline for analyzing medical business data from Telegram channels, leveraging modern data engineering practices.

## Project Overview

This project implements a robust data pipeline that:
- Scrapes raw data from Telegram channels
- Stores data in a structured data lake
- Transforms data using dbt into a dimensional star schema
- Provides an analytical API for data access

## Project Structure

```
.
├── README.md
├── .env
├── .gitignore
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── data/
│   └── raw/
├── dbt/
│   ├── models/
│   ├── tests/
│   └── sources.yml
├── src/
│   ├── scraper/
│   ├── transformer/
│   └── api/
├── requirements.txt
└── scripts/
    └── run_pipeline.sh
```

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- PostgreSQL
- Git

## Setup Instructions

1. Clone the repository
2. Create a `.env` file with required credentials:
   ```
   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=telegram_analytics
   ```
3. Build and run containers:
   ```bash
   docker-compose up --build
   ```

## Data Pipeline Architecture

1. **Data Collection**
   - Telegram scraping using Telethon
   - Raw data stored in partitioned JSON files
   - Image collection for YOLO processing

2. **Data Lake**
   - Structured storage in `data/raw/YYYY-MM-DD/channel_name.json`
   - Partitioned by date and channel
   - Raw data preservation

3. **Data Transformation**
   - dbt models for staging and marts
   - Star schema implementation
   - Automated testing

4. **Analytical API**
   - FastAPI endpoints
   - Data validation
   - Real-time analytics

## Usage

### Running the Pipeline

1. Start the Docker containers
2. Run the pipeline:
   ```bash
   ./scripts/run_pipeline.sh
   ```

### Accessing the API

API endpoints available at: `http://localhost:8000`

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.