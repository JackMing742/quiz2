import requests
from bs4 import BeautifulSoup
import re

pattern = r'(£\d+\.\d{2})'
prices=[]
try:
    response = requests.get('https://books.toscrape.com/catalogue/category/books/travel_2/index.html')
    response.raise_for_status()  # 檢查 HTTP 錯誤狀態碼
    soup=BeautifulSoup(response.text, "lxml")
    print("--- 使用 lxml 解析成功 ---")
    data_dict=soup.find_all('p',class_='price_color')
    for tag in data_dict:
        price=tag.get_text(strip=True)#取得標籤內文字並去除多餘空白
        match = re.findall(pattern, price)#使用正則表達式尋找價格
        prices.extend(match)#將找到的價格加入列表
    print(prices)
except requests.exceptions.Timeout:
    print("請求超時，伺服器沒有在指定時間內回應。")
except requests.exceptions.ConnectionError as e:
    print(f"連線失敗，請檢查網路連線或網址是否正確: {e}")
except requests.exceptions.HTTPError as e:
    print(f"HTTP 請求失敗，狀態碼錯誤: {e}")
except requests.exceptions.RequestException as e:
    # 捕捉所有其他的 requests 錯誤
    print(f"發生未預期的錯誤: {e}")
'''if response.status_code == 200:
    try:
        prices =re.findall(pattern,response.text)
        print(prices)
    except re.error as e:
        print(f"正則表達式錯誤: {e}")
else:
    print(f"無法取得網頁內容，狀態碼: {response.status_code}")'''