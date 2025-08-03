from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import aio_pika
import os
import json
import asyncio
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
ORDER_QUEUE = os.getenv("RABBITMQ_ORDER_QUEUE", "trade.orders")

app = FastAPI()

class Order(BaseModel):
    symbol: str
    quantity: int
    side: str  # BUY or SELL

rabbitmq_channel = None

async def init_rabbitmq():
    global rabbitmq_channel
    retries = 5
    for i in range(retries):
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            rabbitmq_channel = await connection.channel()
            await rabbitmq_channel.declare_queue(ORDER_QUEUE, durable=True)
            print("✅ Connected to RabbitMQ")
            return
        except Exception as e:
            print(f"🔁 RabbitMQ connection retry {i+1} failed: {e}")
            await asyncio.sleep(3)
    raise RuntimeError("Failed to connect to RabbitMQ after retries")

@app.on_event("startup")
async def startup_event():
    await init_rabbitmq()

@app.post("/order")
async def submit_order(order: Order):
    if order.side.upper() not in {"BUY", "SELL"}:
        raise HTTPException(status_code=400, detail="Invalid order side")

    message = json.dumps(order.dict()).encode()
    await rabbitmq_channel.default_exchange.publish(
        aio_pika.Message(body=message),
        routing_key=ORDER_QUEUE
    )
    return {"status": "submitted", "order": order}
