from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.get("/")
def root():
    return {"message": "Transfer API is running"}

class PriceRequest(BaseModel):
    distance_km: float

@app.post("/get-price")
def get_price(data: PriceRequest):
    rate_per_km = 1.5
    price = data.distance_km * rate_per_km
    return {"price": round(price, 2)}

class BookingRequest(BaseModel):
    from_address: str
    to_address: str
    distance_km: float
    price: float
    travel_date: str
    adults: int
    children: int
    comment: str = ""
    need_wifi: bool = False
    russian_driver: bool = False
    promo_code: str = ""

@app.post("/book-transfer")
def book_transfer(data: BookingRequest):
    message = (
        "📥 Новое бронирование:\n\n"
        f"🚗 Маршрут: {data.from_address} → {data.to_address}\n"
        f"📅 Дата: {data.travel_date}\n"
        f"👨‍👩‍👧 Взрослые: {data.adults}, Дети: {data.children}\n"
        f"💶 Цена: {data.price} €\n"
        f"📡 Wi-Fi: {'Да' if data.need_wifi else 'Нет'}\n"
        f"🇷🇺 Рус. водитель: {'Да' if data.russian_driver else 'Нет'}\n"
        f"📝 Комментарий: {data.comment or '—'}"
    )
    send_telegram_message(message)
    return {"status": "success", "message": "Бронирование принято", "price": data.price}

def send_telegram_message(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    try:
        httpx.post(url, json=payload, timeout=10)
    except Exception as e:
        print("Ошибка при отправке в Telegram:", e)
