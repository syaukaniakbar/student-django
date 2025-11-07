# utils/firebase_utils.py
import os
import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings

def initialize_firebase():
    if not firebase_admin._apps:
        cred_path = os.path.join(settings.BASE_DIR, 'mahasiswa/firebase_config.json')
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

def send_notification_to_topic(title, body, topic, data=None):
    try:
        initialize_firebase()
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            topic=topic,
            data=data or {}
        )
        response = messaging.send(message)
        print(f"[Firebase] Notification sent to '{topic}': {response}")
        return response
    except Exception as e:
        print(f"[Firebase] Error sending to '{topic}': {e}")
        return None
