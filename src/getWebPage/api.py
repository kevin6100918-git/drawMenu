from response import response
import githubImageHandler
import json
import os


def lambda_handler(event: dict, context: dict):
    path = event.get('path', '')

    # 判斷是否為獲取清單的 API 請求
    if '/list/' in path:
        category = path.split('/')[-1] # 取得 breakfast 或 dinner
        data = githubImageHandler.get_menu_list(category)
        # 將資料轉為前端易讀的格式: { name, image }
        formatted_data = [{"name": item[0], "image": item[1]} for item in data]
        return response("application/json", 200, json.dumps(formatted_data))

    # 直接讀取 base.html 檔案內容
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, 'base.html')
    
    with open(html_path, 'r', encoding='utf-8') as f:
        htmlContent = f.read()

    return response("text/html", 200, htmlContent)
