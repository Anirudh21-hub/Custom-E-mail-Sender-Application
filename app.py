from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
import threading
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = Flask(__name__)
CORS(app)

# Configure SQLite Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///emails.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# Define Email model
class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default="Pending")  # Pending, Sent, Failed
    scheduled_time = db.Column(db.String(50), nullable=True)


# Initialize DB
with app.app_context():
    db.create_all()


# Email Sender Function
def send_email(recipient, subject, body):
    try:
        # Configure your SMTP server and credentials
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "your-email@gmail.com"
        sender_password = "your-password"

        # Create email
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, msg.as_string())

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


# API Endpoints
@app.route("/upload", methods=["POST"])
def upload_csv():
    file = request.files["file"]
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    try:
        data = pd.read_csv(file)
        for index, row in data.iterrows():
            new_email = Email(
                recipient=row["Email"], subject=row["Subject"], body=row["Body"]
            )
            db.session.add(new_email)
        db.session.commit()
        return jsonify({"message": "Emails added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/send", methods=["POST"])
def send_emails():
    emails = Email.query.filter_by(status="Pending").all()
    for email in emails:
        success = send_email(email.recipient, email.subject, email.body)
        if success:
            email.status = "Sent"
        else:
            email.status = "Failed"
        db.session.commit()
    return jsonify({"message": "Emails processed"}), 200


@app.route("/schedule", methods=["POST"])
def schedule_emails():
    data = request.json
    time = data.get("time")

    def scheduled_job():
        emails = Email.query.filter_by(status="Pending").all()
        for email in emails:
            success = send_email(email.recipient, email.subject, email.body)
            if success:
                email.status = "Sent"
            else:
                email.status = "Failed"
            db.session.commit()

    schedule.every().day.at(time).do(scheduled_job)

    # Run scheduler in a separate thread
    threading.Thread(target=run_scheduler).start()
    return jsonify({"message": f"Emails scheduled at {time}"}), 200


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
