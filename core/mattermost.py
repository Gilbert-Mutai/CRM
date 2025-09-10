import requests
from django.conf import settings

def send_to_mattermost(message: str):
    payload = {
        "channel": settings.MATTERMOST_CHANNEL,
        "username": settings.MATTERMOST_USERNAME,
        "text": message,
    }
    try:
        response = requests.post(settings.MATTERMOST_WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[Mattermost] Failed: {e}")

def send_email_alert_to_mattermost(subject: str, recipient_count: int, user_display: str):
    """
    Separate sender for email notifications (does not interfere with CRUD).
    """
    message = (
        f"CRM Updates: A notification with the subject **\"{subject}\"** "
        f"was successfully sent to **{recipient_count} client(s)** by **{user_display}**."
    )
    payload = {
        "channel": settings.MATTERMOST_CHANNEL,
        "username": settings.MATTERMOST_USERNAME,
        "text": message,
    }
    try:
        response = requests.post(settings.MATTERMOST_WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[Mattermost] Email Alert Failed: {e}")