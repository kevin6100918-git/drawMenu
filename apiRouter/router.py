from fastapi import APIRouter, Request
from fastapi.responses import Response, HTMLResponse, JSONResponse


from src import getImageHandler, drawMenuHandler


httpRouter = APIRouter()

@httpRouter.get("/menu", response_class=HTMLResponse)
async def menu():
    
    return HTMLResponse(content=open("src/base.html", "r", encoding="utf-8").read(), status_code=200)

@httpRouter.get("/menu/{category}/{menu}", responses={200: {"content": {"image/jpeg": {}}}})
async def get_menu(category, menu):
    # img: bytes = getImageHandler.get_image(meal, menu)
    # return Response(content=img, media_type="image/jpeg")
    return None



apiRouter = APIRouter()

# line webhook
@apiRouter.post("/draw", response_class=JSONResponse)
async def draw(request: Request):
    netloc = request.url.netloc
    imagePrefixUrl = f"https://{netloc}"
    payload = await request.json()
    print(payload)

    if payload["events"]: # 驗證用

        if replyToken := payload["events"][0]["replyToken"] and payload["events"][0]["type"] == "message":
            drawResult = drawMenuHandler.draw_menu(payload["events"][0])
            menuCategory = drawResult["category"]
            menuFile = drawResult["menuFile"]
            restaurantName = drawResult["restaurantName"]
            menuImageUrl = httpRouter.url_path_for("get_menu", category=menuCategory, menu=menuFile)

            messagePayload = {
                "replyToken": replyToken,
                "messages": [
                    {
                        "type": "text",
                        "text": f"吃 {restaurantName}"
                    },
                    {
                        "type": "image",
                        "originalContentUrl": menuImageUrl,
                        "previewImageUrl": menuImageUrl
                    }
                ]
            }
            drawMenuHandler.sendMessage(payload=messagePayload)

    return JSONResponse(content="OK", status_code=200)


# test
from fastapi import FastAPI
app = FastAPI()
app.include_router(apiRouter)