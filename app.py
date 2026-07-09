from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

@app.route("/")
def home():
    return "SMTP Backend is running!"

@app.route("/send-email", methods=["POST"])
def send_email():
    try:
        data = request.get_json()

        receiver_email = data.get("receiverEmail")
        subject = data.get("subject")
        message = data.get("message")

        if not receiver_email or not subject or not message:
            return jsonify({
                "success": False,
                "message": "Receiver email, subject and message are required"
            }), 400

        if not EMAIL_USER or not EMAIL_PASS:
            return jsonify({
                "success": False,
                "message": "EMAIL_USER or EMAIL_PASS not found in environment"
            }), 500

        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, receiver_email, msg.as_string())
        server.quit()

        return jsonify({
            "success": True,
            "message": "Email sent successfully!"
        })

    except smtplib.SMTPAuthenticationError:
        return jsonify({
            "success": False,
            "message": "Authentication failed. Check your Gmail and App Password."
        }), 401

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
