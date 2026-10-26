import json, os, re, html as h
import requests

URL = "https://www.nevsehir.edu.tr/tr/tumduyurular/tip/1"
TOKEN = os.environ["TG_TOKEN"]
CHAT = os.environ["TG_CHAT"]
DOSYA = "gorulen.json"

sayfa = requests.get(URL, timeout=30, headers={"User-Agent": "Mozilla/5.0"}).text

# <a href="https://www.nevsehir.edu.tr/tr/59117" ...> Başlık </a> yapısını yakala
duyurular = {}
for href, icerik in re.findall(r'<a[^>]+href="(?:https://www\.nevsehir\.edu\.tr)?(/tr/\d+)"[^>]*>(.*?)</a>', sayfa, re.S):
    baslik = h.unescape(re.sub(r"<[^>]+>", "", icerik)).strip()
    if baslik:
        duyurular["https://www.nevsehir.edu.tr" + href] = baslik

try:
    eski = json.load(open(DOSYA, encoding="utf-8"))
except FileNotFoundError:
    eski = None  # ilk çalıştırma

if eski is not None:
    for url, baslik in duyurular.items():
        if url not in eski:
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                         params={"chat_id": CHAT, "text": f"📢 NEVÜ Duyuru\n{baslik}\n{url}"}, timeout=30)

json.dump(duyurular, open(DOSYA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"{len(duyurular)} duyuru okundu.")
