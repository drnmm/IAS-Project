import json
import azure.functions as func
import pymongo

client = pymongo.MongoClient("YOUR_MONGODB_CONNECTION_URI_HERE")
db = client.iasproject
useracc = db.useracc

def userOTP(username):
    for user in useracc.find({"username":username}):
        if user.get("OTP"):
            return user["OTP"]
    return None


def main(req: func.HttpRequest) -> func.HttpResponse:
    header = {
        "Content-Type":"application/json, charset=utf-8"
    }
    if req.method == "POST":
        try:
            req_body = req.get_json()
            method = req.params.get("method")
            if str(method):
                if method == "2FA":
                    otp = userOTP(req_body["username"])
                    if otp:
                        if otp == str(req_body["otp"]):
                            useracc.update_one({
                                "username":req_body["username"]
                            },
                            {
                                "$set":{
                                    "OTP":""
                                }
                            })
                            return func.HttpResponse(json.dumps({
                                "auth": True
                            }), status_code=200, headers=header)
                        else:
                            return func.HttpResponse(json.dumps({
                                "auth": False
                            }), status_code=200, headers=header)
                    return func.HttpResponse(json.dumps({
                        "auth": False
                    }), status_code=200, headers=header)
                elif method == "updateUOID":
                    useracc.update_one({
                        "username":req_body["username"]
                    },
                    {
                        "$set": {
                            "uoid": req_body["uoid"]
                        }
                    })
                    return func.HttpResponse(json.dumps({
                        "status":"Update done."
                    }), status_code=200, headers=header)
                else:
                    return func.HttpResponse(json.dumps({
                        "status":"Method not available"
                    }), status_code=200, headers=header)
            else:
                return func.HttpResponse(json.dumps({
                    "status":"Invalid transaction."
                }), status_code=200, headers=header)

        except Exception as e:
            return func.HttpResponse(json.dumps({"status":str(e)}), status_code=200, headers=header)
    elif req.method == "GET":
        return func.HttpResponse(json.dumps({"hello":"world"}), status_code=200)
    else:
        header = {
            "Content-Type":"application/json, charset=utf-8",
        }
        return func.HttpResponse(json.dumps({"status":"Request method not supported.","version":1.0}, indent=4), status_code=200, headers=header)