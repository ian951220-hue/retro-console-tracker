import requests
from bs4 import BeautifulSoup
import json
import re

# 偽裝成瀏覽器
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

# 目標網址：PTT Gamesale 搜尋 NDSL
url = 'https://www.ptt.cc/bbs/Gamesale/search?q=NDSL'

# 發送請求
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

items_data = []

# PTT 搜尋結果每一筆文章都在 class='r-ent' 的 div 裡
items = soup.find_all('div', class_='r-ent')
print(f"總共找到 {len(items)} 筆貼文，準備開始提取價格...")

for item in items:
    try:
        # 抓取標題
        title_div = item.find('div', class_='title')
        if not title_div or not title_div.find('a'):
            continue
            
        title = title_div.find('a').text.strip()
        
        # 使用正規表達式 (RegEx) 從標題中嘗試抓取價格 (尋找 $ 或 元 前面的數字)
        price_match = re.search(r'(\d+)\s?(元|\$)', title)
        price = price_match.group(1) if price_match else "未標價"

        items_data.append({
            'title': title,
            'price': price
        })
    except Exception as e:
        continue

# 將結果寫入 JSON
with open('retro_consoles.json', 'w', encoding='utf-8') as f:
    json.dump(items_data, f, ensure_ascii=False, indent=4)

print(f"成功抓取 {len(items_data)} 筆貼文資料！")
print("資料已儲存至 retro_consoles.json，請檢查檔案內容。")