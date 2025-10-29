import requests
from bs4 import BeautifulSoup
import json
books_list = []
try:
    response = requests.get("https://books.toscrape.com/catalogue/category/books/travel_2/index.html")
    response.raise_for_status()  # 確保請求成功
    soup=BeautifulSoup(response.text, "lxml")
    print("--- 使用 lxml 解析成功 ---")
    book_data = soup.find_all('article', class_='product_pod')
    for tag in book_data:
        try:
            #取得書名
            tag_title=tag.h3.a['title'] if tag.h3 and tag.h3.a and tag.h3.a['title'] else "No title"#判斷標籤元素是否存在先判斷h3再判斷a標籤再判斷title屬性
            #取得價格
            tag_price=tag.find('p', class_='price_color').text if tag.find('p', class_='price_color') else "No price"#判斷標籤元素是否存在
            #取得評分
            tag_rating=tag.find('p', class_='star-rating')
            if tag_rating:
                tag_rating_class = tag_rating.get('class', [])#輸出是['star-rating', 'Two']
                #取得tag_rating_class的第二個元素
                tag_rating_class2 = tag_rating_class[1] if len(tag_rating_class) > 1 else "No rating"#判斷tag_rating_class的第二個元素是否存在，長度大於1代表存在否則輸出"No rating"
            else:
                tag_rating_class2 = "No rating"
            #建立字典存放書籍資料
            book_dict = {
                "title": tag_title,
                "price": tag_price,
                "rating": tag_rating_class2
            }
        except Exception as e:
            print(f"解析書籍資料時發生錯誤: {e}")         
            continue
        #將書籍資料加入列表
        books_list.append(book_dict)
    
    print(books_list)
    #將書籍資料寫入 JSON 檔案
    book_json = json.dumps(books_list, indent=4, ensure_ascii=False)
    with open("books.json", "w", encoding="utf-8") as f:
        f.write(book_json)
except requests.RequestException as e:
    print(f"網路請求失敗: {e}")
