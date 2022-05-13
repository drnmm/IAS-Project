import json, pymongo
import azure.functions as func

from hashlib import sha256

client = pymongo.MongoClient("YOUR_MONGODB_CONNECTION_URI_HERE")
db = client.iasproject
useracc = db.useracc

userData = None

def doLogin(uname, upass):
    global userData
    for user in useracc.find({"username":uname,"password":sha256(str(upass).encode()).hexdigest()}):
        if user.get("username"):
            userData = user
            return True
    return False


def twoFA():
    if userData.get("uoid"):
        return True
    return False

def main(req: func.HttpRequest) -> func.HttpResponse:
    header = {
        "Content-Type":"application/json, charset=utf-8"
    }
    if req.method == "POST":
        try:
            req_body = req.get_json()
            # return func.HttpResponse(json.dumps(req_body), status_code=200, headers=header)
            if doLogin(req_body["username"], req_body["password"]):
                if twoFA():
                    return func.HttpResponse(json.dumps({
                        "login": True,
                        "twoAuth": True,
                        "UOID": userData["uoid"]
                    }), status_code=200, headers=header)
                else:
                    return func.HttpResponse(json.dumps({
                        "login": True,
                        "twoAuth": False,
                        "UOID": userData["uoid"]
                    }), status_code=200, headers=header)
            return func.HttpResponse(json.dumps({
                "login": False
            }), status_code=403, headers=header)
        except Exception as e:
            return func.HttpResponse(json.dumps({"status":str(e)}), status_code=200)
    elif req.method == "GET":
        return func.HttpResponse(req.url, status_code=200)
    else:
        header = {
            "Content-Type":"application/json, charset=utf-8",
        }
        return func.HttpResponse(json.dumps({"status":"Request method not supported.","version":1.0}, indent=4), status_code=200, headers=header)