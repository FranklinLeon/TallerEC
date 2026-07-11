import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class WhatsAppService:
    def __init__(self):
        self.token = os.getenv('WHATSAPP_TOKEN')
        self.phone_id = os.getenv('WHATSAPP_PHONE_ID')
        self.nombre_taller = os.getenv('NOMBRE_TALLER', 'Grip Motos')
        
        # Leemos la URL del frontend desde el .env. Si no existe, usamos localhost por defecto.
        self.frontend_url = os.getenv('VITE_URL_FRONTEND', 'http://localhost:5173')
        
        self.url = f"https://graph.facebook.com/v18.0/{self.phone_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def _enviar_plantilla(self, numero_cliente, nombre_plantilla, nombre_cliente, placa_moto, hash_seguimiento, idioma="es"):
        """Función interna reutilizable para cualquier plantilla de 4 variables"""
        
        # Limpiamos posibles barras diagonales al final de la URL base para evitar enlaces rotos (ej: //seguimiento/)
        base_url = self.frontend_url.rstrip('/')
        url_seguimiento = f"{base_url}/seguimiento/{hash_seguimiento}"

        payload = {
            "messaging_product": "whatsapp",
            "to": numero_cliente,
            "type": "template",
            "template": {
                "name": nombre_plantilla, 
                "language": { "code": idioma },
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": nombre_cliente},      # {{1}}
                            {"type": "text", "text": placa_moto},          # {{2}}
                            {"type": "text", "text": self.nombre_taller},  # {{3}} Taller Dinámico (Desde el .env)
                            {"type": "text", "text": url_seguimiento}      # {{4}} URL de Ngrok/Producción cliqueable
                        ]
                    }
                ]
            }
        }
        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    # --- DISPARADORES OFICIALES ---

    def enviar_mensaje_bienvenida(self, numero_cliente, nombre_cliente, placa_moto, hash_seguimiento):
        # Envía la plantilla 'ingreso_moto1' en inglés ('en') como está guardada en tu Meta
        return self._enviar_plantilla(numero_cliente, "ingreso_moto1", nombre_cliente, placa_moto, hash_seguimiento, idioma="en")

    def enviar_mensaje_moto_lista(self, numero_cliente, nombre_cliente, placa_moto, hash_seguimiento):
        # Envía la plantilla 'moto_lista' en español ('es')
        return self._enviar_plantilla(numero_cliente, "moto_lista", nombre_cliente, placa_moto, hash_seguimiento, idioma="es")

    def enviar_cotizacion(self, numero_cliente, nombre_cliente, placa_moto, total, contexto, cotizacion_id):
        payload = {
            "messaging_product": "whatsapp",
            "to": numero_cliente,
            "type": "template",
            "template": {
                "name": "cotizacion_moto",
                "language": {"code": "es"},
                "components": [
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": nombre_cliente},
                            {"type": "text", "text": placa_moto},
                            {"type": "text", "text": contexto},
                            {"type": "text", "text": f"${total:.2f}"},
                        ]
                    },
                    {
                        "type": "button",
                        "sub_type": "quick_reply",
                        "index": "0",
                        "parameters": [{"type": "payload", "payload": f"aprobar_{cotizacion_id}"}]
                    },
                    {
                        "type": "button",
                        "sub_type": "quick_reply",
                        "index": "1",
                        "parameters": [{"type": "payload", "payload": f"rechazar_{cotizacion_id}"}]
                    }
                ]
            }
        }
        try:
            response = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
            return response.json()
        except Exception as e:
            return {"error": str(e)}