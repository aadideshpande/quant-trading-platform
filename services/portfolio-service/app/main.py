from fastapi import FastAPI
from dotenv import load_dotenv
import aio_pika
import os
import asyncio
import json

load_dotenv()

app = FastAPI()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE", "price.updates")

# in-memory cache of latest prices
price_cache = {}

async def consume_price_updates():
    retries = 5
    delay = 3

    for attempt in range(retries):
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            channel = await connection.channel()
            queue = await channel.declare_queue(QUEUE_NAME, durable=True)

            print(f"✅ Connected to RabbitMQ and listening to queue '{QUEUE_NAME}'")
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        data = json.loads(message.body)
                        symbol = data["symbol"]
                        price = data["price"]
                        price_cache[symbol] = price
                        print(f"📥 Updated {symbol} to {price}")
            return

        except Exception as e:
            print(f"⚠️ [Retry {attempt+1}/{retries}] Failed to connect to RabbitMQ: {e}")
            await asyncio.sleep(delay)

    raise RuntimeError("❌ Could not connect to RabbitMQ after several retries.")


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_price_updates())

@app.get("/price/{symbol}")
def get_price(symbol: str):
    price = price_cache.get(symbol.upper())
    if price is None:
        return {"error": "Symbol not found"}
    return {"symbol": symbol.upper(), "price": price}
