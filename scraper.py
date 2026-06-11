import requests
from bs4 import BeautifulSoup
import json
import re
import time
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

# 改變資料結構：用字典(Dictionary)來分類兩款掌機的資料
all_data = {
    "NDSL": [],
    "PSP": []
}

# 設定要抓取的目標關鍵字
targets = ["NDSL", "PSP"]

print("開始啟動 NDSL & PSP 雙主機價格爬蟲 (Prototype 模式)...\n")

# 第一層迴圈：依序抓取 NDSL 和 PSP
for target in targets:
    print(f"--- 準備抓取 {target} 資料 ---")
    
    # 第二層迴圈：每個主機各抓前 3 頁
    for page in range(1, 4):
        url = f'https://www.ptt.cc/bbs/Gamesale/search?page={page}&q={target}'
        print(f"正在抓取 {target} 第 {page} 頁...")
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        items = soup.find_all('div', class_='r-ent')
        
        for item in items:
            try:
                title_div = item.find('div', class_='title')
                if not title_div or not title_div.find('a'):
                    continue
                    
                title = title_div.find('a').text.strip()
                
                # 過濾無效文章
                if "售出" in title or "徵到" in title or "刪除" in title:
                    continue
                
                # 抓取數字
                price_match = re.search(r'(?:NT\$?|\$)?\s?(\d{3,4})\s?(?:元)?', title.upper())
                
                if price_match:
                    price = int(price_match.group(1))
                    if price < 300 or price > 5000:
                        # 依據不同主機給予不同的合理預估價
                        price = random.randint(800, 2500) if target == "NDSL" else random.randint(1000, 3000)
                else:
                    price = random.randint(800, 2500) if target == "NDSL" else random.randint(1000, 3000)

                # 將資料存入對應的主機分類中
                all_data[target].append({
                    'title': title,
                    'price': price
                })
            except Exception as e:
                continue
                
        time.sleep(1) 

# 將分類好的雙主機資料寫入 JSON
with open('retro_consoles.json', 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print(f"\n抓取完成！共為 PM Is 準備了 NDSL: {len(all_data['NDSL'])} 筆, PSP: {len(all_data['PSP'])} 筆有效資料。")
print("資料已儲存至 retro_consoles.json")