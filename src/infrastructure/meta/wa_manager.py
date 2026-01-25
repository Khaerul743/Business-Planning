import os

import requests
from dotenv import load_dotenv
from fastapi import Request

from src.core.exceptions import TokenIsNotVerified, WhatsappBadRequest
from src.core.utils import get_logger

load_dotenv()


class WhatsappManager:
    def __init__(self):
        self.waba_verify_token = os.environ.get("WABA_VERIFY_TOKEN")
        self.waba_access_token = os.environ.get("WABA_ACCESS_TOKEN")
        self.waba_phone_number_id = os.environ.get("PHONE_NUMBER_ID")
        self._logger = get_logger(__name__)

        # URL
        self.url_messages = (
            f"https://graph.facebook.com/v19.0/{self.waba_phone_number_id}/messages"
        )

    def verify_webhook(self, request: Request):
        mode = request.query_params.get("hub.mode")
        token = request.query_params.get("hub.verify_token")
        challenge = request.query_params.get("hub.challenge")
        if mode and token:
            if mode == "subscribe" and token == self.waba_verify_token:
                self._logger.info("Webhook verified")
                # Jika token cocok, kirim kembali challenge
                return int(challenge)
            else:
                raise TokenIsNotVerified()
        raise WhatsappBadRequest()

    def send_text_message(self, to_number: str, text_message: str):
        return {"to_number": to_number, "text_message": text_message}

    # def send_text_message(self, to_number: str, text_message: str):
    #     """
    #     Fungsi untuk mengirim pesan keluar menggunakan Token Akses Permanen (Token BE).
    #     """
    #     headers = {
    #         "Authorization": f"Bearer {self.waba_access_token}",
    #         "Content-Type": "application/json",
    #     }

    #     data = {
    #         "messaging_product": "whatsapp",
    #         "to": to_number,
    #         "type": "text",
    #         "text": {"body": text_message},
    #     }

    #     try:
    #         response = requests.post(self.url_messages, headers=headers, json=data)
    #         response.raise_for_status()  # Akan melempar HTTPError jika status code 4xx/5xx
    #         self._logger.info(
    #             f"Send text message is successfully to number {to_number}"
    #         )
    #         return response.json()
    #     except requests.exceptions.HTTPError as err:
    #         self._logger.warning(f"Failed to send text message: {err}")
