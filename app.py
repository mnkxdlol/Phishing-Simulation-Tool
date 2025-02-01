from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage
from config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/tracking.db'
db = SQLAlchemy(app)

class ClickTracking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(255), nullable=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    recipient = request.form['email']
    phishing_link = f"http://127.0.0.1:5000/tracking?user={recipient}"

    msg = EmailMessage()
    msg['Subject'] = "security update"
    msg['From'] = SMTP_USER
    msg['To'] = recipient
    msg.set_content(f"Click on this link to update your information : {phishing_link}")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

    return f"email sent to {recipient}"

@app.route('/tracking')
def tracking():
    user = request.args.get('user')
    new_click = ClickTracking(user=user, reason="He's curious! :p")
    db.session.add(new_click)
    db.session.commit()
    return "You've been trapped !"

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)