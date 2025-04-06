def response(contentType, statusCode, body, event=None):
    res = {
        "headers": {
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Content-Type": contentType,
        } ,
        "body": body,
        "statusCode": statusCode
    }
    if contentType == "image/jpeg":
        res["isBase64Encoded"] = True
    
    return res