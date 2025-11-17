import requests
from shared.config import ACCESS_TOKEN, WHATSAPP_API_URL

class WhatsAppService:
    """Servicio para enviar mensajes por WhatsApp"""
    
    @staticmethod
    def send_text_message(phone_number: str, text: str):
        """Envía un mensaje de texto simple"""
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": text
            }
        }
        
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        return response.json()
    
    @staticmethod
    def send_button_message(phone_number: str, body_text: str, buttons: list):
        """
        Envía un mensaje con botones.
        
        buttons debe ser una lista de diccionarios:
        [
            {"id": "btn_1", "title": "Opción 1"},
            {"id": "btn_2", "title": "Opción 2"}
        ]
        """
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        button_objects = [
            {
                "type": "reply",
                "reply": {
                    "id": btn["id"],
                    "title": btn["title"]
                }
            }
            for btn in buttons
        ]
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body_text},
                "action": {"buttons": button_objects}
            }
        }
        
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        return response.json()
    
    @staticmethod
    def send_list_message(phone_number: str, body_text: str, button_text: str, sections: list):
        """
        Envía un mensaje con lista.
        
        sections debe ser una lista de diccionarios:
        [
            {
                "title": "Categoría 1",
                "rows": [
                    {"id": "item_1", "title": "Item 1", "description": "Desc 1"},
                    {"id": "item_2", "title": "Item 2", "description": "Desc 2"}
                ]
            }
        ]
        """
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {"text": body_text},
                "action": {
                    "button": button_text,
                    "sections": sections
                }
            }
        }
        
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        return response.json()