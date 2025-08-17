from fastapi import FastAPI, HTTPException, Depends, APIRouter
from pydantic import BaseModel
import aio_pika
import os
import json
import asyncio
from dotenv import load_dotenv
from .models import Trade
from .db import SessionLocal, engine, Base
from sqlalchemy.future import select
import asyncio
from typing import List
from datetime import datetime
import re


load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")
ORDER_QUEUE = os.getenv("RABBITMQ_ORDER_QUEUE", "trade.orders")

app = FastAPI()
router = APIRouter()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React app origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Order(BaseModel):
    symbol: str
    quantity: int
    side: str  # BUY or SELL

rabbitmq_channel = None

class TradeOut(BaseModel):
    id: int
    symbol: str
    quantity: int
    side: str
    timestamp: datetime

    class Config:
        orm_mode = True

@app.get("/trades", response_model=List[TradeOut])
async def get_trades():
    async with SessionLocal() as session:
        result = await session.execute(select(Trade).order_by(Trade.timestamp.desc()))
        trades = result.scalars().all()
        return trades

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
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@router.post("/order")
async def submit_order(order: Order):
    # Validate order side
    if order.side.upper() not in {"BUY", "SELL"}:
        raise HTTPException(status_code=400, detail="Invalid order side. Must be 'BUY' or 'SELL'.")

    # Validate quantity
    if order.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be a positive integer.")

    # Validate symbol
    if not re.fullmatch(r"[A-Z]{1,5}", order.symbol.upper()):
        raise HTTPException(status_code=400, detail="Invalid symbol. Must be 1–5 uppercase letters.")

    # Save to DB
    async with SessionLocal() as session:
        db_order = Trade(
            symbol=order.symbol.upper(),
            quantity=order.quantity,
            side=order.side.upper()
        )
        session.add(db_order)
        await session.commit()

    # Publish to RabbitMQ
    message = json.dumps(order.dict()).encode()
    await rabbitmq_channel.default_exchange.publish(
        aio_pika.Message(body=message),
        routing_key=ORDER_QUEUE
    )

    return {"status": "submitted", "order": order}

app.include_router(router)
