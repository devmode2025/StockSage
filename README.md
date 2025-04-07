# StockSage
Real-time stock market pipeline with MLOps.

## Features
- Data ingestion from Yahoo Finance → Kafka
- Spark streaming for real-time processing
- LSTM price predictions (FastAPI)
- React dashboard

## Setup
1. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   cd frontend && npm install
   ```
2. Configure Kafka in `data_ingestion/config/kafka_config.json`.
