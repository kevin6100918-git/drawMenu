from datetime import datetime, timezone
import os
from urllib.parse import quote
import requests
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, URIAction, TemplateSendMessage, CarouselTemplate, CarouselColumn
from os import getenv
import random

import githubImageHandler


# Linebot Setting
line_bot_api = LineBotApi(getenv("LINE_BOT_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(getenv("LINE_BOT_CHANNEL_SECRET"))
my_line_id = getenv("LINE_BOT_CHANNEL_ID")
HEADER = {
    "Content-type": "application/json",
    "Authorization": f'Bearer {getenv("LINE_BOT_CHANNEL_ACCESS_TOKEN")}'
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

    return randomImage(menuRandomPool).get()

def draw_menu(category: str=""):
    if category == "早":
        menuFile =  random_get_menu_file(category="breakfast")
    
    elif category == "晚":
        menuFile =  random_get_menu_file(category="dinner")
    
    else:
        menuFile =  random_get_menu_file()
    
    # restaurantName = os.path.basename(menuFile).split(".")[0]
    restaurantName = menuFile[0].split(".")[0]

    return {
        "menuFile": menuFile[1],
        "restaurantName": restaurantName
    }

def handle_message(payload: dict, requestContext: dict):
    if payload["message"]["type"] == "text":
        text = payload["message"]["text"]
        if "吃甚麼" in text or "吃什麼" in text:
            if "早" in text:
                drawResult = draw_menu(category="早")
            elif "晚" in text:
                drawResult = draw_menu(category="晚")
            else:
                drawResult = draw_menu()
            menuFile = drawResult["menuFile"]
            restaurantName = drawResult["restaurantName"]

            return TemplateSendMessage(
                alt_text=f"吃 {restaurantName}",
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            thumbnail_image_url=menuFile,
                            title="結果...",
                            text=f"吃 {restaurantName}",
                            actions=[
                                URIAction(
                                    label="看菜單",
                                    uri=menuFile
                                )
                            ]
                        )
                    ]
                )
            )

        elif "菜單" in text:
            domainName = requestContext.get("domainName")
            stage = requestContext.get("stage")
            url = f"https://{domainName}/{stage}"

            return TextSendMessage(
                text="請點選以下按鈕來開啟連結：",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=URIAction(
                                label="上傳菜單按這裡",
                                uri=url
                            )
                        )
                    ]
                )
            )

            

def reply_message(replyToken, message):
    line_bot_api.reply_message(replyToken, message)