import requests
import logging

logging.basicConfig(level=logging.INFO)

def trigger_webhook(request_id: str, webhook_url: str):
    """Send a webhook notification when processing is complete."""
    payload = {"request_id": request_id, "status": "completed"}

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        response.raise_for_status()
        logging.info(f"Webhook triggered successfully for {request_id}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Webhook trigger failed: {e}")
