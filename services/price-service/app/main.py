from fastapi import FastAPI
from dotenv import load_dotenv
import os, asyncio, random, json
from typing import Dict
import aio_pika

load_dotenv()
app = FastAPI()

prices: Dict[str, float] = {
    "AAPL": 150.0,
    "GOOG": 2800.0,
    "TSLA": 700.0,
    "MSFT": 300.0,
}

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE", "price.updates")
rabbitmq_channel = None

@app.get("/price/{symbol}")
def get_price(symbol: str):
    price = prices.get(symbol.upper())
    if price is None:
        return {"error": "Symbol not found"}
    return {"symbol": symbol.upper(), "price": round(price, 2)}

async def publish_price_updates():
    global rabbitmq_channel
    retries = 5
    for attempt in range(retries):
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            channel = await connection.channel()
            await channel.declare_queue(QUEUE_NAME, durable=True)
            rabbitmq_channel = channel
            print(f"Connected to RabbitMQ and declared queue '{QUEUE_NAME}'")
            return
        except Exception as e:
            print(f"[Retry {attempt+1}/{retries}] RabbitMQ not ready. Retrying in 3s...")
            await asyncio.sleep(3)

    raise RuntimeError("RabbitMQ not available after multiple attempts.")

async def simulate_price_updates():
    while True:
        for symbol in prices:
            drift = random.uniform(-1, 1)
            prices[symbol] += drift

            # publish update
            message = json.dumps({
                "symbol": symbol,
                "price": round(prices[symbol], 2)
            })
            if rabbitmq_channel:
                await rabbitmq_channel.default_exchange.publish(
                    aio_pika.Message(body=message.encode()),
                    routing_key=QUEUE_NAME,
                )
        await asyncio.sleep(2)

@app.on_event("startup")
async def startup_event():
    await publish_price_updates()
    asyncio.create_task(simulate_price_updates())
