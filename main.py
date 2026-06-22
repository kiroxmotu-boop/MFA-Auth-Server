from flask import Flask, request, jsonify
import random
import time

from email_service import send_otp


app = Flask(__name__)

sessions = {}


def generate_otp():
    return str(random.randint(100000, 999999))


@app.route("/request", methods=["POST"])
def request_login():

    data = request.json

    email = data.get("email")

    if not email:
        return {
            "status": False,
            "message": "Email missing"
        }


    email_otp = generate_otp()
    discord_otp = generate_otp()


    sessions[email] = {

        "email_otp": email_otp,

        "discord_otp": discord_otp,

        "master": "123456",

        "time": time.time()
    }


    # SEND EMAIL OTP
    try:

        send_otp(
            email,
            email_otp
        )

        print("Email OTP sent")

    except Exception as e:

        print("EMAIL ERROR:")
        print(e)

        return {
            "status": False,
            "message": "Email failed"
        }


    # testing ke liye
    print("===================")
    print("EMAIL:", email)
    print("DISCORD OTP:", discord_otp)
    print("MASTER OTP:", "123456")
    print("===================")


    return {
        "status": True,
        "message": "OTP Sent"
    }



@app.route("/verify", methods=["POST"])
def verify():


    data = request.json


    email = data.get("email")


    if email not in sessions:

        return {
            "status": False
        }



    user = sessions[email]


    if time.time() - user["time"] > 300:

        return {
            "status": False,
            "message": "OTP expired"
        }



    if (

        data.get("otp1") == user["email_otp"]

        and

        data.get("otp2") == user["discord_otp"]

        and

        data.get("otp3") == user["master"]

    ):

        return {
            "status": True,
            "message": "Authenticated"
        }



    return {
        "status": False,
        "message": "Wrong OTP"
    }



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )