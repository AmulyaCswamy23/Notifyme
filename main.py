# app.py
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Send email function
def send_reminder_email(to_email, subject, message_body):
    from_email = "your_email@gmail.com"
    app_password = "uwyf fplp anvl qfkn"  # <-- Your 16-char app password

    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(message_body, 'plain'))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_email, app_password)
            server.sendmail(from_email, to_email, message.as_string())
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

# Streamlit UI
st.title("📧 Email Reminder App")

to_email = st.text_input("Recipient Email")
reminder_subject = st.text_input("Subject", "💧 Water Reminder")
reminder_msg = st.text_area("Message", "Hey! Time to drink water 💦")

if st.button("Send Reminder"):
    if to_email and reminder_msg:
        success = send_reminder_email(to_email, reminder_subject, reminder_msg)
        if success:
            st.success(f"Email sent to {to_email} ✅")
    else:
        st.warning("Please fill in all fields.")
