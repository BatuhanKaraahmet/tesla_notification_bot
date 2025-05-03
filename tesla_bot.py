import requests
import time
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TESLA_API_URL = 'https://www.tesla.com/inventory/api/v1/inventory-results'
params = {
    "query": {
        "model": "my",
        "condition": "new",
        "arrangeby": "plh",
        "zip": "06690",
        "range": 0
    },
    "offset": 0,
    "count": 50,
    "outsideOffset": 0,
    "outsideSearch": False
}
headers = {'User-Agent': 'Mozilla/5.0'}

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    requests.post(url, data=data)

def get_vehicle_ids():
    try:
        response = requests.get(TESLA_API_URL, headers=headers, params={'query': str(params)})
        if response.status_code == 200:
            data = response.json()
            vehicles = data.get('results', [])
            return set(v.get("VIN") for v in vehicles if v.get("VIN"))
    except Exception as e:
        print(f"Hata: {e}")
    return set()

def main():
    print("TELEGRAM_TOKEN:", TELEGRAM_TOKEN)
    print("TELEGRAM_CHAT_ID:", TELEGRAM_CHAT_ID)
    print("Bot başlatıldı...")
    known = get_vehicle_ids()
    print(f"İlk bilinen araçlar: {known}")
    send_telegram_message(f"Başladı. {len(known)} araç var.")
    while True:
        print("1 dakika bekleniyor...")
        time.sleep(60)
        current = get_vehicle_ids()
        print(f"Güncel araçlar: {current}")
        new = current - known
        if new:
            print(f"Yeni araçlar bulundu: {new}")
            send_telegram_message(f"{len(new)} yeni araç eklendi! 🚗")
            known = current
        else:
            print("Yeni araç yok.")


if __name__ == "__main__":
    main()
