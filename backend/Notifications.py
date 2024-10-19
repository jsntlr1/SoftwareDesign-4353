from flask import Flask
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_email@address.com'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

def send_email_notification(to_email, subject, message):
    with app.app_context():
        msg = Message(subject=subject, sender=app.config["MAIL_USERNAME"], recipients=[to_email])
        msg.body = message
        try:
            mail.send(msg)
            print(f"Email notification sent to {to_email}")
        except Exception as e:
            print(f"ERROR sending email notification to {to_email}")

#pip install APScheduler
#send email at a specific time

#send email 24 hours before event start
def schedule_email_notification(to_email, subject, message, event_start_time):
    scheduler = BackgroundScheduler()
    reminder_time = event_start_time - timedelta(hours = 24)
    if reminder_time <= datetime.now():
        print(f"Reminder time {reminder_time} is in the past, rescheduling")
        reminder_time = datetime.now() + timedelta(minutes=1)

    scheduler.add_job(func=send_email_notification, trigger = "date", run_date = reminder_time, args=[to_email, subject, message])
    scheduler.start()
    print(f"Email scheduled for {reminder_time}")

if __name__ == "__main__":
    #email test
    #to_email = "cpotabirkhoff@gmail.com"
    #subject = "Test: Email in 1 minute"
    #message = "This is a test email to be sent in 1 minute"
    #schedule_email_notification(to_email, subject, message, datetime.now() + timedelta(minutes = 1))
    app.run(debug=True)