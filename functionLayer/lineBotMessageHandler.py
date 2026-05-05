from os import getenv
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, URIAction, TemplateSendMessage, CarouselTemplate, CarouselColumn

from drawMenuHandler import draw_menu


# Linebot Setting
line_bot_api = LineBotApi(getenv("LINE_BOT_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(getenv("LINE_BOT_CHANNEL_SECRET"))
my_line_id = getenv("LINE_BOT_CHANNEL_ID")

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
                text=f"請點選以下連結可管理菜單：\n{url}",
                # quick_reply=QuickReply(
                #     items=[
                #         QuickReplyButton(
                #             action=URIAction(
                #                 label="上傳菜單按這裡",
                #                 uri=url
                #             )
                #         )
                #     ]
                # )
            )

            

def reply_message(replyToken, message):
    line_bot_api.reply_message(replyToken, message)