import schedule
import time
import requests

def send_phishing_emails():
    requests.post("http://127.0.0.1:5000/send_email", data={"email": "victim@example.com"})

schedule.every().day.at("09:00").do(send_phishing_emails)

while True:
    schedule.run_pending()
    time.sleep(60)