from fastapi import FastAPI
from dotenv import load_dotenv
import os
import asyncio
import random
from typing import Dict

load_dotenv()
app = FastAPI()

prices: Dict[str, float] = {
    "AAPL": 150.0,
    "GOOG": 2800.0,
    "TSLA": 700.0,
    "MSFT": 300.0,
}

@app.get("/price/{symbol}")
def get_price(symbol: str):
    price = prices.get(symbol.upper())
    if price is None:
        return {"error": "Symbol not found"}
    return {"symbol": symbol.upper(), "price": round(price, 2)}

async def simulate_price_updates():
    while True:
        for symbol in prices:
            drift = random.uniform(-1, 1)
            prices[symbol] += drift
        await asyncio.sleep(2)

@app.on_event("startup")
async def start_simulation():
    asyncio.create_task(simulate_price_updates())
