import json
import time
from confluent_kafka import Producer
from stock_fetcher import fetch_stock_prices
from datetime import datetime

# Load config
with open("data_ingestion/config/kafka_config.json") as f:
    conf = json.load(f)

producer = Producer({
    "bootstrap.servers": conf["bootstrap.servers"],
    "security.protocol": conf["security.protocol"],
    "sasl.mechanisms": conf["sasl.mechanisms"],
    "sasl.username": conf["sasl.username"],
    "sasl.password": conf["sasl.password"],
    "compression.type": "lz4",  # or "snappy"
    "queue.buffering.max.messages": 100000  # Increase buffer
})

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
        # Log to Prometheus/grafana
    else:
        print(f"Delivered to {msg.topic()} [Partition: {msg.partition()}]")
        # Monitor latency
        latency = time.time() - msg.timestamp()[1] / 1000
        print(f"Latency: {latency:.2f} sec")

def stream_stock_data():
    stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", 
              "TSLA", "NVDA", "JPM", "V", "WMT"]
    
    while True:
        try:
            print(f"\nFetching data at {datetime.now()}")
            data = fetch_stock_prices(stocks)
            
            if data.empty:
                print("Warning: Empty DataFrame received")
                continue
                
            for stock in stocks:
                # Access MultiIndex correctly
                if stock in data.columns.levels[0]:
                    latest = data[stock].iloc[-1].to_dict()
                    latest['symbol'] = stock
                    latest['timestamp'] = str(datetime.now())
                    
                    producer.produce(
                        topic="stock_prices",
                        key=stock,
                        value=json.dumps(latest),
                        callback=delivery_report
                    )
            producer.flush()
            time.sleep(60)
            
        except Exception as e:
            print(f"Error: {str(e)}")
            time.sleep(10)  # Wait before retry

if __name__ == "__main__":
    stream_stock_data()