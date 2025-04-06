from datetime import datetime, timezone
import os
from urllib.parse import quote
import requests
from linebot import LineBotApi, WebhookHandler
from os import getenv
import random

import githubImageHandler


# Linebot Setting
line_bot_api = LineBotApi(getenv('LINE_BOT_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(getenv('LINE_BOT_CHANNEL_SECRET'))
my_line_id = getenv('LINE_BOT_CHANNEL_ID')
HEADER = {
    'Content-type': 'application/json',
    'Authorization': f'Bearer {getenv("LINE_BOT_CHANNEL_ACCESS_TOKEN")}'
}

class randomImage:
    def __init__(self, imgList: list[tuple[str, str]]):
        self.imageList = imgList
        self.randomShuffle()
    
    def randomShuffle(self):
        random.shuffle(self.imageList)

    def get(self):
        return list(self.imageList)[0]

def random_get_menu_file(category: str=""):
    # get time now
    timenow = int(datetime.now(tz=timezone.utc).hour)+8
    # select meal
    if not category:
        if timenow < 11 or timenow >= 22:
            category = "breakfast"
        else:
            category = "dinner"
    # menuRandomPool = os.listdir(os.path.join("drawMenu", "menus", category))
    menuRandomPool = githubImageHandler.get_menu_list(category)

    return category, randomImage(menuRandomPool).get()

def draw_menu(event:dict):
    if event["message"]["type"] == "text":
        text = event["message"]["text"]
        if "吃甚麼" in text or "吃什麼" in text:
            if "早" in text:
                category, menuFile =  random_get_menu_file(category="breakfast")
            
            elif "晚" in text:
                category, menuFile =  random_get_menu_file(category="dinner")
            
            else:
                category, menuFile =  random_get_menu_file()
            
            # restaurantName = os.path.basename(menuFile).split(".")[0]
            restaurantName = menuFile[0].split(".")[0]

            return {
                "category": category,
                "menuFile": menuFile[1],
                "restaurantName": restaurantName
            }

def sendMessage(payload):
    response = requests.post(url="https://api.line.me/v2/bot/message/reply", headers=HEADER, json=payload)
    # print(response.status_code)
    # print(response.content)
    return ""