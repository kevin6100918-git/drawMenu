from linebot import LineBotApi, WebhookHandler
import requests
import os
import json
import random
import base64


from htmlResponseModel import response_html
class randomImage:
    def __init__(self, path):
        # path = fr'{os.getcwd()}/{path}'
        self.imagelist = os.listdir(path=path)
        self.randomShuffle()
        print(f"imgList: {self.imagelist}")
    
    def randomShuffle(self):
        random.shuffle(self.imagelist)

    def get(self):
        return list(self.imagelist)[0]

line_bot_api = LineBotApi(os.environ['channel_access_token'])
handler = WebhookHandler(os.environ['channel_secret'])
my_line_id = os.environ['channel_id']
end_point = os.environ['end_point']
HEADER = {
    'Content-type': 'application/json',
    'Authorization': F'Bearer {os.environ["channel_access_token"]}'
}

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

def lambda_handler(event, context):

    print(f"event: {event}")
    print(f"listdir: {os.listdir('./')}")
    print(f"listdir: {os.listdir('./menus')}")

    httpMethod = event.get("httpMethod")
    resource = event.get("resource")

    # Line chatbot event
    if httpMethod == "POST":
        body = json.loads(event.get("body"))
        print(body)
        events = body.get("events")
        print(events)
        if events[0].get("replyToken"):
            payload = {}
            replyToken = events[0]["replyToken"]
            payload["replyToken"] = replyToken
            if events[0]["type"] == "message":
                if events[0]["message"]["type"] == "text":
                    text = events[0]["message"]["text"]
                    if "吃甚麼" in text or "吃什麼" in text:
                        payload["messages"] = [getTextMessage(),]
                        # payload["messages"] = [getTextMessage(), getImageMessage()]
                    # elif text == "新增菜單":
                    #     payload["messages"] = [uploadMenu()]
                    elif text == "菜單":
                        payload["messages"] = [getMenuUrl()]
                    sendMessage(payload=payload)

        return response("application/json", 200, json.dumps({"message": "hello world"}))
    
    elif httpMethod == "GET" and resource == "/draw":
        print(fr"imgList: {os.listdir('./menus')}")
        query = event.get("queryStringParameters")
        if not query:
            return response("application/json", 400, json.dumps({"message": "missing query parameters"}))
        
        imgFileName = query.get("img")
        if not imgFileName:
            return response("application/json", 400, json.dumps({"message": "missing imgFile"}))
        
        print(f"filename: {imgFileName}")
        with open(fr'./menus/{imgFileName}', 'rb') as imageFile:
            encoded_image = base64.b64encode(imageFile.read()).decode('utf-8')
            print(f"base64 content: {encoded_image}")
        responseHtml = response_html.return_singal_image(imgFileName, encoded_image)
        return response("text/html", 200, responseHtml)

    elif httpMethod == "GET" and (resource == "/draw/menu" or resource == "/draw/menu/delete"):
        print(f"resource: {event.get('resource')}")
        imgContentList = []
        for imgFileName in os.listdir(fr"./menus"):
            with open(fr'./menus/{imgFileName}', 'rb') as imageFile:
                encoded_image = base64.b64encode(imageFile.read()).decode('utf-8')
            imgContentList.append((imgFileName, encoded_image))
        responseHtml = response_html.return_menu_list(resource, imgContentList)
        return response("text/html", 200, responseHtml)
    
    # elif httpMethod == "DELETE":
    #     bodyData = json.loads(event.get("body"))
    #     if not bodyData:
    #         return response("application/json", 400, json.dumps({"message": "missing query parameters"}))
        
    #     imgFileName = bodyData.get("img")
    #     if not imgFileName:
    #         return response("application/json", 400, json.dumps({"message": "missing imgFile"}))
        
    #     print(f"delete filename: {imgFileName}")
    #     try:
    #         os.remove(fr"./menus/{imgFileName}")
    #     except OSError as er:
    #         return response("application/json", 400, json.dumps({"message": f"DELETE faild: {er}"}))
    #     return response("application/json", 200, json.dumps({"message": "DELETE success"}))


def getImage():
    path = fr'menus'
    result = randomImage(path=fr'./{path}').get()
    return fr'{end_point}?img={result}'

def getImageMessage():
    originalContentUrl = getImage()
    message = {
        "type": "image",
        "originalContentUrl": originalContentUrl,
        "previewImageUrl": originalContentUrl
    }
    return message

def getTextMessage():
    message = {
        "type": "text",
        "text": f"吃這間\n{getImage()}"
    }
    return message

def getMenuUrl():
    message = {
        "type": "text",
        "text": f"菜單一覽\n{end_point}/menu"
    }
    return message

def sendMessage(payload):
    dic = {"replyToken":f"{payload['replyToken']}",
           "messages":payload['messages']}
    response = requests.post(url='https://api.line.me/v2/bot/message/reply', headers=HEADER, json=dic)
    print(response.status_code)
    print(response.content)
    print(dic)
    return 'OK'

