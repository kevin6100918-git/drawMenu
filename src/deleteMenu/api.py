import json
import base64

from response import response
import githubImageHandler


def lambda_handler(event: dict, context: dict):
    
    bodyData: dict = json.loads(event.get("body", {}))
    if not bodyData:
        return response("application/json", 400, json.dumps({"message": "missing query parameters"}))
    
    imgFileName = bodyData.get("name")
    if not imgFileName:
        return response("application/json", 400, json.dumps({"message": "missing imgFile"}))

    statusCode = githubImageHandler.delete_menu(meal=bodyData.get("category"), menuName=imgFileName)

    if statusCode == 200:
        return response("application/json", 200, json.dumps({"message": "刪除成功"}))
    
    else:
        return response("application/json", statusCode, json.dumps({"message": f"刪除失敗"}))
