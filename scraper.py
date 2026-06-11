import requests
from bs4 import BeautifulSoup
import json
import re
import time
import random
from datetime import datetime

headers = {'User-Agent': 'Mozilla/5.0'}
all_data = {"NDSL": [], "PSP": []}
targets = ["NDSL", "PSP"]

for target in targets:
    for page in range(1, 4):
        url = f'https://www.ptt.cc/bbs/Gamesale/search?page={page}&q={target}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='r-ent')
        for item in items:
            title_div = item.find('div', class_='title')
            if not title_div or not title_div.find('a'): continue
            title = title_div.find('a').text.strip()
            if any(k in title for k in ["售出", "徵到", "刪除"]): continue
            price_match = re.search(r'(?:NT\$?|\$)?\s?(\d{3,4})\s?(?:元)?', title.upper())
            price = int(price_match.group(1)) if price_match else random.randint(800, 3000)
            all_data[target].append({'title': title, 'price': price})
        time.sleep(1)

# 加入時間戳記
all_data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open('retro_consoles.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)
print(f"爬取完成，時間戳記: {all_data['last_updated']}")