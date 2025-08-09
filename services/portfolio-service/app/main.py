from fastapi import FastAPI
from dotenv import load_dotenv
import aio_pika
import os
import asyncio
import json

load_dotenv()

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React app origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


RABBITMQ_URL = os.getenv("RABBITMQ_URL")
QUEUE_NAME = os.getenv("RABBITMQ_QUEUE", "price.updates")

# in-memory cache of latest prices
price_cache = {}
holdings = {}

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

async def consume_trade_orders():
    retries = 5
    delay = 3

    for attempt in range(retries):
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            channel = await connection.channel()
            queue = await channel.declare_queue("trade.orders", durable=True)

            print("✅ Connected to RabbitMQ for trade.orders")

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        data = json.loads(message.body)
                        symbol = data["symbol"].upper()
                        qty = int(data["quantity"])
                        side = data["side"].upper()

                        current_qty = holdings.get(symbol, 0)
                        if side == "BUY":
                            holdings[symbol] = current_qty + qty
                        elif side == "SELL":
                            holdings[symbol] = current_qty - qty

                        print(f"🔄 Updated holdings: {symbol} = {holdings[symbol]}")
            return

        except Exception as e:
            print(f"⚠️ [Retry {attempt+1}/{retries}] Failed to connect to RabbitMQ for trades: {e}")
            await asyncio.sleep(delay)

    raise RuntimeError("❌ Could not connect to RabbitMQ (trade.orders) after retries.")


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_price_updates())
    asyncio.create_task(consume_trade_orders())

@app.get("/price/{symbol}")
def get_price(symbol: str):
    price = price_cache.get(symbol.upper())
    if price is None:
        return {"error": "Symbol not found"}
    return {"symbol": symbol.upper(), "price": price}

@app.get("/portfolio")
def get_portfolio():
    result = []
    total_value = 0.0

    for symbol, qty in holdings.items():
        price = price_cache.get(symbol.upper(), 0.0)
        value = round(qty * price, 2)
        total_value += value

        result.append({
            "symbol": symbol,
            "quantity": qty,
            "price": price,
            "value": value
        })

    return {
        "portfolio": result,
        "total_value": round(total_value, 2)
    }


