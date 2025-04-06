from linebot import LineBotApi, WebhookHandler
import requests
from os import getenv
import json
import random
import base64
from github import GithubException
from github import Github
from datetime import datetime
from urllib.parse import quote

import htmlResponseModel


class randomImage:
    def __init__(self, imgList):
        self.imagelist = imgList
        self.randomShuffle()
    
    def randomShuffle(self):
        random.shuffle(self.imagelist)

    def get(self):
        return list(self.imagelist)[0]

# Github username
username = getenv("GITHUB_USER")
# Github acess token
github_access_token = getenv("GITHUB_ACCESS_TOKEN")
# pygithub object
g = Github(github_access_token)
# get that user by username
user = g.get_user(username)
# get repo "drawMenu"
repo_name = getenv("GITHUB_REPO_NAME")
repo = user.get_repo(name=repo_name)

# Linebot Setting
line_bot_api = LineBotApi(getenv('LINE_BOT_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(getenv('LINE_BOT_CHANNEL_SECRET'))
my_line_id = getenv('LINE_BOT_CHANNEL_ID')
# end_point = getenv('API')
HEADER = {
    'Content-type': 'application/json',
    'Authorization': f'Bearer {getenv("LINE_BOT_CHANNEL_ACCESS_TOKEN")}'
}


stage = getenv("STAGE")
def selectMenuPath(pathPara = None):
    if stage == "home":
        if pathPara == "dinner":
            path = "drawMenu/menus/homemeal"
        elif pathPara == "breakfast":
            path = "drawMenu/menus/homemorning"

    # elif stage == "prod":
    #     path = "drawMenu/menus/yude"
    # elif stage == "maio":
    #     path = "drawMenu/menus/maio"
    # else:
    #     path = "drawMenu/menus/yude"
    return path


def response(contentType, statusCode, body, event=None):
    res = {
        'headers': {
            'Access-Control-Allow-Credentials': True,
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Content-Type': contentType,
        } ,
        'body': body,
        'statusCode': statusCode
    }
    if contentType == "image/jpeg":
        res["isBase64Encoded"] = True
    return res

def lambda_handler(event:dict, context:dict):

    print(f"event: {event}")

    httpMethod:str = event.get("httpMethod")
    path:str = event.get("path")

    # Line chatbot event
    if httpMethod == "POST" and path == "/draw":
        body = json.loads(event.get("body"))
        events = body.get("events")
        if events[0].get("replyToken"):
            payload = {}
            replyToken = events[0]["replyToken"]
            payload["replyToken"] = replyToken
            if events[0]["type"] == "message":
                if events[0]["message"]["type"] == "text":
                    text = events[0]["message"]["text"]
                    if "吃甚麼" in text or "吃什麼" in text:
                        if "早" in text:
                            payload["messages"] = genMessage(category="breakfast")
                        elif "晚" in text:
                            payload["messages"] = genMessage(category="dinner")
                        else:
                            payload["messages"] = genMessage()
                        sendMessage(payload=payload)
                    # elif text == "菜單":
                    #     payload["messages"] = [managedMenu()]
                    #     sendMessage(payload=payload)

        return response("application/json", 200, json.dumps({"message": "hello world"}))

    elif httpMethod == "GET" and path == "/menu":
        menu_path_list = {
            category: [(menu.name, fr"https://raw.githubusercontent.com/{username}/{repo_name}/main/{menu.path}") for menu in repo.get_contents(path=selectMenuPath(pathPara=category))]
            for category in ["breakfast", "dinner"]
        }
        responseHtml = htmlResponseModel.return_render_html(menu_path_list)
        return response("text/html", 200, responseHtml)

    elif httpMethod == "POST" and path == "/upload":
        bodyData:dict = json.loads(event.get("body"))
        if not bodyData:
            return response("application/json", 400, json.dumps({"message": "missing image data."}))
        fileName = bodyData.get("fileName")
        extension = fileName.split('.')[-1]
        menuName = f"{bodyData.get('name')}.{extension}"
        imgData = bodyData.get("fileData")
        category = bodyData.get('category')
        imgByte = base64.b64decode(imgData.split(',')[1])
        create_menu_path = f"{selectMenuPath(pathPara=category)}/{menuName}"
        try:
            repo.create_file(create_menu_path, "Upload menu ", imgByte)
            return response("application/json", 200, json.dumps({"message": "上傳成功"}))
        except GithubException as giterr:
            print(giterr)
            if giterr.status == 422:
                return response("application/json", 400, json.dumps({"message": f"檔案已存在"}))
            return response("application/json", 500, json.dumps({"message": f"{giterr}"}))

    elif httpMethod == "DELETE" and path == "/delete":
        bodyData = json.loads(event.get("body"))
        if not bodyData:
            return response("application/json", 400, json.dumps({"message": "missing query parameters"}))
        
        imgFileName = bodyData.get("name")
        if not imgFileName:
            return response("application/json", 400, json.dumps({"message": "missing imgFile"}))
        
        delete_menu_path = f"{selectMenuPath(pathPara=bodyData.get('category'))}/{imgFileName}"
        try:
            menu = repo.get_contents(path=delete_menu_path)
            repo.delete_file(path=delete_menu_path, message="remove menu", sha=menu.sha)
        except Exception as er:
            return response("application/json", 400, json.dumps({"message": f"DELETE faild: {er}"}))
        return response("application/json", 200, json.dumps({"message": "刪除成功"}))
    g.close()

def getImage(category=None):
    # get time now
    timenow = int(datetime.now().hour)+8
    # select meal
    if not category:
        if timenow < 11 or timenow >= 22:
            category = "breakfast"
        else:
            category = "dinner"
    menuPath = selectMenuPath(category)
    menus = repo.get_contents(path=menuPath)
    menuPathList = [menu.path for menu in menus]
    result = randomImage(menuPathList).get()
    return fr"https://raw.githubusercontent.com/{username}/{repo_name}/main/{result}"

def getImageMessage(originalContentUrl):
    message = {
        "type": "image",
        "originalContentUrl": originalContentUrl,
        "previewImageUrl": originalContentUrl
    }
    return message

def getTextMessage(restaurantName):
    message = {
        "type": "text",
        "text": f"吃 {restaurantName}"
    }
    return message

def genMessage(category=None):
    imageUrl = getImage(category)
    restaurantName = imageUrl.split("/")[-1].split(".")[0]
    originalContentUrl = imageUrl.replace(restaurantName, quote(restaurantName, encoding="utf-8"))
    messages = [getTextMessage(restaurantName), getImageMessage(originalContentUrl)]
    return messages

# def managedMenu():
#     message = {
#         "type": "text",
#         "text": "菜單管理",
#         "quickReply": {
#             "items": [
#                 {
#                     "type": "action",
#                     "action": {
#                         "type": "uri",
#                         "label": "菜單管理",
#                         "uri": f"{end_point}/menu"
#                     }
#                 }
#             ]
#         }
#     }
#     return message

def sendMessage(payload):
    dic = {"replyToken":f"{payload['replyToken']}",
           "messages":payload['messages']}
    response = requests.post(url='https://api.line.me/v2/bot/message/reply', headers=HEADER, json=dic)
    print(response.status_code)
    print(response.content)
    print(dic)
    return 'OK'

