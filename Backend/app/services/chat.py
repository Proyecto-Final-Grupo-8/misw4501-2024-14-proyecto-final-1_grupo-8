import requests
from flask import current_app

class ChatService:
    @staticmethod
    def send_message_to_magicloops(data):
        MAGICLOOPS_API_URL = "https://magicloops.dev/api/loop/32f98c71-b8c1-4aa7-bd03-f7731f052c4c/run"
        MAGICLOOPS_API_KEY = ""

        message = data.get('details')
        if not message:
            return {"message": "Details is required"}, 400

        payload = {
            "details": message,
            "context": data.get('context', []) 
        }
        headers = {
            "Authorization": f"Bearer {MAGICLOOPS_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(MAGICLOOPS_API_URL, json=payload, headers=headers)
            response_data = response.json()

            if response.status_code == 200:
                return  response_data, 200
            else:
                return {"message": "Error from MagicLoops", "details": response_data}, response.status_code

        except requests.exceptions.RequestException as e:
            return {"message": "Failed to connect to MagicLoops", "error": str(e)}, 500
