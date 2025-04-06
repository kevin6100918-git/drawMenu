import json

from response import response
import drawMenuHandler



def lambda_handler(event: dict, context: dict):
    
    payload = json.loads(event.get("body"))
    print(payload)

    if payload["events"]: # 驗證用

        if replyToken := payload["events"][0]["replyToken"]:
            if payload["events"][0]["type"] == "message":
                drawResult = drawMenuHandler.draw_menu(payload["events"][0])
                menuCategory = drawResult["category"]
                menuFile = drawResult["menuFile"]
                restaurantName = drawResult["restaurantName"]

                messagePayload = {
                    "replyToken": replyToken,
                    "messages": [
                        {
                            "type": "image",
                            "originalContentUrl": menuFile,
                            "previewImageUrl": menuFile
                        },
                        {
                            "type": "text",
                            "text": f"吃 {restaurantName}"
                        }
                    ]
                }
                drawMenuHandler.sendMessage(payload=messagePayload)
                # print(messagePayload)
    
    return response("application/json", 200, json.dumps({"message": "OK"}))