import datetime
import time
from pprint import pprint
from hashlib import sha512
import uuid
import os

os.system('cls')

class NotSufficientDataError(Exception):
    pass

#User Data
NAME = "Subhadeep Banerjee"
EMAIL = "subhadeep762@gmail.com"
LICENSE_PLATE_No = "7TYP290"
START_DATE = datetime.date.today()
START_TIME = 1
END_DATE = None
END_TIME = None



payload = {
    "name": NAME,
    "email-id": EMAIL,
    "license-plate": LICENSE_PLATE_No,
    "start-date": START_DATE,
    "start-time": START_TIME,
    "end-date": END_DATE,
    "end-time": END_TIME
}


def user_details():
    for i in payload.items():
        pprint(i, depth=2)


def private_key():
    if(len(payload["name"]) and len(payload["email-id"]) and len(payload["license-plate"]) > 0):
        user_private_key = sha512(str(payload.get("name") + payload.get("email-id") + payload.get("license-plate")).encode()).hexdigest()
    else:
        print("Missing Some Data")
    return user_private_key

def public_key():
    return uuid.uuid1()

def secret_key():
    secret = private_key() + str(public_key())
    print(secret)


