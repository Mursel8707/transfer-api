from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

route_prices = {
    ("Antalya Havaliman", "Kemer(Beldibi)"): 50,
    ("Antalya Havaliman", "Kemer(Göynük)"): 50,
    ("Antalya Havaliman", "Antalya(AVM)"): 50,
    ("Kemer(Beldibi)", "Antalya(AVM)"): 100,
    ("Kemer(Göynük)", "Antalya(AVM)"): 100,
    ("Alanya(Mahmutlar)", "Antalya(AVM)"): 200
    # ... добавь остальные маршруты здесь вручную или импортом
}

@app.get("/")
def root():
    return {"message": "Transfer API is running"}

class PriceByRegionRequest(BaseModel):
    from_address: str
    to_address: str

@app.post("/get-price")
def get_price(data: PriceByRegionRequest):
    key = (data.from_address, data.to_address)
    price = route_prices.get(key)
    if price is None:
        return {"error": "Маршрут не найден"}
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
    price = route_prices.get(key)
    if price is None:
        return {"error": "Маршрут не найден"}

    message = (
        "📥 Новое бронирование:

"
        f"🚗 Маршрут: {data.from_address} → {data.to_address}
"
        f"📅 Дата: {data.travel_date}
"
        f"👨‍👩‍👧 Взрослые: {data.adults}, Дети: {data.children}
"
        f"💶 Цена: {price} $
"
        f"📡 Wi-Fi: {'Да' if data.need_wifi else 'Нет'}
"
        f"🇷🇺 Рус. водитель: {'Да' if data.russian_driver else 'Нет'}
"
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
