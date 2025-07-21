
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


REGION_PRICES = {
    ("Antalya Havaliman", "Kemer(Beldibi)"): 50,
    ("Antalya Havaliman", "Kemer(Göynük)"): 50,
    ("Antalya Havaliman", "Kemer"): 50,
    ("Antalya Havaliman", "Kemer(Çamyuva)"): 60,
    ("Antalya Havaliman", "Kemer(Tekirova)"): 60,
    ("Antalya Havaliman", "Antalya(merkez)"): 30,
    ("Antalya Havaliman", "Konyaaltı"): 35,
    ("Antalya Havaliman", "Belek"): 35,
    ("Antalya Havaliman", "Side"): 60,
    ("Antalya Havaliman", "Alanya"): 80
}


@app.get("/")
def root():
    return {"message": "Transfer API is running"}

class PriceLookup(BaseModel):
    from_address: str
    to_address: str

@app.post("/get-price")
def get_price(data: PriceLookup):
    key = (data.from_address, data.to_address)
    price = REGION_PRICES.get(key)
    if price is None:
        raise HTTPException(status_code=404, detail="Маршрут не найден")
    return {"price": price}

class BookingRequest(BaseModel):
    from_address: str
    to_address: str
    travel_date: str
    adults: int
    children: int
    comment: str = ""
    need_wifi: bool = False
    russian_driver: bool = False
    promo_code: str = ""

@app.post("/book-transfer")
def book_transfer(data: BookingRequest):
    key = (data.from_address, data.to_address)
    price = REGION_PRICES.get(key)
    if price is None:
        raise HTTPException(status_code=404, detail="Маршрут не найден")

    message = (
    "📥 Новое бронирование:\n\n"
    f"🚗 Маршрут: {data.from_address} → {data.to_address}\n"
    f"📅 Дата: {data.travel_date}\n"
    f"👨‍👩‍👧 Взрослые: {data.adults}, Дети: {data.children}\n"
    f"💶 Цена: {data.price} $\n"
    f"📡 Wi-Fi: {'Да' if data.need_wifi else 'Нет'}\n"
    f"🇷🇺 Рус. водитель: {'Да' if data.russian_driver else 'Нет'}\n"
    f"📝 Комментарий: {data.comment or '—'}"
)
    send_telegram_message(message)

    return {"status": "success", "message": "Бронирование принято", "price": price}

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
