import requests
import time
import os
import re
import json
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TESLA_URL = "https://www.tesla.com/tr_TR/inventory/new/my?arrangeby=plh&zip=06690&range=0"
headers = {'User-Agent': 'Mozilla/5.0'}

def send_telegram_message(message):
    print(f"Telegram'a mesaj gönderiliyor: {message}")
    try:
        url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
        data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
        response = requests.post(url, data=data)
        print(f"Telegram yanıt kodu: {response.status_code}")
    except Exception as e:
        print(f"Telegram gönderim hatası: {e}")

def get_vehicle_vins():
    try:
        response = requests.get(TESLA_URL, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            script_tag = soup.find("script", text=re.compile("INVENTORY_PAGE"))
            if script_tag:
                match = re.search(r'INVENTORY_PAGE\s*=\s*({.*});', script_tag.string)
                if match:
                    data = json.loads(match.group(1))
                    vehicles = data.get("props", {}).get("results", [])
                    return set(v.get("VIN") for v in vehicles if v.get("VIN"))
        else:
            print("Sayfa alınamadı:", response.status_code)
    except Exception as e:
        print(f"Hata: {e}")
    return set()

def main():
    print("Bot başlatıldı...")
    known = get_vehicle_vins()
    print(f"İlk bilinen araçlar: {known}")
    send_telegram_message(f"Başladı. {len(known)} araç var.")
    send_telegram_message("SelamınAleyküm")
    while True:
        print("1 dakika bekleniyor...")
        time.sleep(60)
        current = get_vehicle_vins()
        print(f"Güncel araçlar: {current}")
        new = current - known
        if new:
            print(f"Yeni araçlar bulundu: {new}")
            send_telegram_message(f"{len(new)} yeni Model Y eklendi! 🚗")
            known = current
        else:
            print("Yeni araç yok.")

if __name__ == "__main__":
    main()
