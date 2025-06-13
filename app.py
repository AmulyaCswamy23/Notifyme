import streamlit as st
from twilio.rest import Client
import threading
import time

# Twilio credentials (replace with your own)
account_sid = 'ACa7bd845be5ec2545b7ad725e578658fe'
auth_token = '82c34b34ab228f2c7ef6ffda761d2f23'  # Replace with real auth token
messaging_service_sid = 'MG4d34ed5bd40f8d3ce7f43c570c034374'  # Optional

client = Client(account_sid, auth_token)

# Function to send SMS using Twilio
def send_sms(to_number: str, message_text: str):
    try:
        message = client.messages.create(
            messaging_service_sid=messaging_service_sid,
            body=message_text,
            to=to_number
        )
        print(f"✅ Message sent to {to_number}. SID: {message.sid}")
    except Exception as e:
        print(f"❌ Failed to send message to {to_number}: {e}")

# Function that repeatedly sends message every 'interval' seconds
def start_reminder(name, number, message, interval_hours):
    def send_repeatedly():
        while True:
            send_sms(number, f"{name}, reminder: {message}")
            time.sleep(interval_hours * 3600)
    
    thread = threading.Thread(target=send_repeatedly, daemon=True)
    thread.start()

# Streamlit UI
st.title("📱 Personal Notification Reminder App")
st.write("Set up a reminder to get SMS notifications at your chosen interval.")

with st.form("reminder_form"):
    name = st.text_input("Your Name", max_chars=50)
    phone_number = st.text_input("Phone Number (with country code)", placeholder="+91xxxxxxxxxx")
    message = st.text_input("Reminder Message", placeholder="Drink Water 💧")
    frequency = st.selectbox("How often do you want to be reminded?", ("Every 1 hour", "Every 3 hours", "Every 6 hours", "Every 12 hours", "Every 24 hours"))
    
    submit = st.form_submit_button("Start Reminder")

if submit:
    if not all([name, phone_number, message]):
        st.error("⚠️ Please fill out all fields.")
    else:
        interval_map = {
            "Every 1 hour": 1,
            "Every 3 hours": 3,
            "Every 6 hours": 6,
            "Every 12 hours": 12,
            "Every 24 hours": 24,
        }
        interval_hours = interval_map[frequency]

        send_sms(phone_number, f"{name}, this is your first reminder: {message}")
        start_reminder(name, phone_number, message, interval_hours)
        st.success(f"✅ Reminders started! You'll get an SMS every {interval_hours} hour(s).")
