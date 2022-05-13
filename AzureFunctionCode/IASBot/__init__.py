import os
import sys
import azure.functions as func
import json
from hashlib import sha256
import pymongo, uuid

from random import randint as rndm

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path)

from pymessenger.bot import Bot

MYAPP_TOKEN = "YOUR_FACEBOOK_PAGE_ACCESS_TOKEN_HERE"
VERIFY_TOKEN = "WEBHOOK_VERIFY_TOKEN"

client = pymongo.MongoClient("YOUR_MONGODB_CONNECTION_URI_HERE")
db = client.iasproject
fbuser = db.fbmessenger
useracc = db.useracc

def userExists(recipientID):
    for user in fbuser.find({"rid":recipientID}):
        if user.get("rid"):
            return True
    return False

def hashRecipientID(recipientID):
    return sha256(str(recipientID).encode()).hexdigest()

def generateOTP():
    _OTP = ""
    for i in range(7):
        _OTP += str(rndm(0,9))
    return _OTP

def getUOID(hashID):
    for user in fbuser.find({"rid":hashID}):
        if user.get('rid'):
            return user['uoid']
    return None

def isUOIDUsed(uoid):
    for user in useracc.find({"uoid":uoid}):
        if user.get("uoid"):
            return True
    return False


def sendOTP(recipientID):
    uoid = getUOID(hashRecipientID(recipientID))
    if isUOIDUsed(uoid):
        otp = generateOTP()
        useracc.update_one({
            "uoid": uoid
        },
        {
            "$set": {
                "OTP": otp
            }
        })
        send_message(recipientID, "🔑 Your One Time Pin:")
        send_message(recipientID, otp)
    else:
        send_message(recipientID, "ℹ️ Plase add your UOID to your student portal to generate your One Time Pin (OTP).")
        send_message(recipientID, uoid)

def main(req: func.HttpRequest) -> func.HttpResponse:
    psmenu = {
        "persistent_menu":[
        {
        "locale":"default",
        "composer_input_disabled": True,
        "call_to_actions":[
            {
                "title":"🔑 Get OTP",
                "type":"postback",
                "payload":"get_otp"
            }
        ]
    }
    ]
    }
    gs_data = {
    "get_started":{
        "payload": "get_started"
    }
    }
    global bot
    fb = req.params.get('hub.verify_token')
    if req.method=="GET":
        if fb:
            if fb == VERIFY_TOKEN:
                return func.HttpResponse(req.params.get('hub.challenge'), status_code=200)
            return func.HttpResponse("error", status_code=403)
        elif fb:
            return func.HttpResponse(VERIFY_TOKEN, status_code=200)
        else:
            return func.HttpResponse(
                json.dumps({"stat":"online", "test":Bot.testfunction(),"version":1.2}),
                status_code=200
            )
    else:
        try:
            data = req.get_json()
            if data["object"] == "page":
                for entry in data["entry"]:
                    for messaging_event in entry["messaging"]:
                        bot = Bot(MYAPP_TOKEN)
                        recipient_id = messaging_event["sender"]["id"]
                        # payload = (messaging_event.get("message", {}).get("quick_reply", {}).get("payload"))
                        bot.set_persistent_menu(psmenu)
                        bot.set_get_started(gs_data)
                        if messaging_event.get("postback"):
                            payload = messaging_event["postback"]["payload"]
                            if payload == "get_started":
                                if userExists(hashRecipientID(recipient_id)):
                                    send_message(recipient_id, "🔑 Your UOID is:")
                                    for user in fbuser.find({"rid":hashRecipientID(recipient_id)}):
                                        send_message(recipient_id, user["uoid"])
                                    sendOTP(recipient_id)
                                else:
                                    uoid = str(recipient_id) + str(uuid.uuid4().hex)
                                    uoid = sha256(uoid.encode()).hexdigest()
                                    fbuser.insert_one({
                                        "rid": hashRecipientID(recipient_id),
                                        "uoid": uoid
                                    })
                                    send_message(recipient_id, f"ℹ️ Add this unique ID to your student portal account to get started:")
                                    send_message(recipient_id, uoid)
                                    send_message(recipient_id, "ℹ️ Press Get OTP to get your One Time Password when logging in.")
                            elif payload == "get_otp":
                                sendOTP(recipient_id)
                                # send_message(recipient_id, "this is your OTP")
                            else:
                                send_message(recipient_id, "Unknownd payload.")
                        elif messaging_event.get("message"):
                            send_message(recipient_id, "Hello world from 🏡 using my 💻.")
                        else:
                            send_message(recipient_id, "Bot unable to respond.")                  
            return func.HttpResponse("success", status_code=200)
        except Exception as e:
            return func.HttpResponse(str(req.method), status_code=500)
            
def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"
