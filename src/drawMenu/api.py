import json

from response import response
import lineBotMessageHandler



def lambda_handler(event: dict, context: dict):
    
    payload = json.loads(event.get("body"))
    print(payload)

    if payload["events"]: # 驗證用

        if replyToken := payload["events"][0]["replyToken"]:
            if payload["events"][0]["type"] == "message":
                messagePayload = lineBotMessageHandler.handle_message(payload["events"][0], event.get("requestContext"))
                lineBotMessageHandler.reply_message(replyToken, messagePayload)
                # print(messagePayload)
    
    return response("application/json", 200, json.dumps({"message": "OK"}))