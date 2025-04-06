import json
import base64

from response import response
import githubImageHandler


def lambda_handler(event: dict, context: dict):
    
    bodyData:dict = json.loads(event.get("body"))
    if not bodyData:
        return response("application/json", 400, json.dumps({"message": "missing image data."}))
    
    fileName: str = bodyData.get("fileName")
    extension = fileName.split('.')[-1]
    menuName = f"{bodyData.get('name')}.{extension}"
    imgData: str = bodyData.get("fileData")
    category: str = bodyData.get('category')
    imgByte = base64.b64decode(imgData.split(',')[1])

    statusCode = githubImageHandler.upload_menu(meal=category, menuName=menuName, imageData=imgByte)

    if statusCode == 200:
        return response("application/json", 200, json.dumps({"message": "上傳成功"}))
    
    elif statusCode == 422:
        return response("application/json", 400, json.dumps({"message": f"檔案已存在"}))
    
    else:
        return response("application/json", statusCode, json.dumps({"message": f"上傳失敗"}))
