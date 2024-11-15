import requests
from flask import current_app

class ChatService:
    @staticmethod
    def send_message_to_magicloops(data):
        MAGICLOOPS_API_URL = "https://magicloops.dev/api/loop/dcc1548f-2aff-4bba-8573-a0511b550359/run"
        MAGICLOOPS_API_KEY = ""

        message = data.get('message')
        if not message:
            return {"message": "Message is required"}, 400

        payload = {
            "message": message,
            "context": data.get('context', {}) 
        }
        headers = {
            "Authorization": f"Bearer {MAGICLOOPS_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(MAGICLOOPS_API_URL, json=payload, headers=headers)
            response_data = response.json()

            if response.status_code == 200:
                return {"magicloops_response": response_data}, 200
            else:
                return {"message": "Error from MagicLoops", "details": response_data}, response.status_code

        except requests.exceptions.RequestException as e:
            return {"message": "Failed to connect to MagicLoops", "error": str(e)}, 500
