import os
import requests
from dotenv import load_dotenv
from src.core.utils.logger import get_logger
from src.app.validators.whatsapp_schema import SendMessagePayload
from src.app.validators.wa_service_schema import (
    WaSessionResponse, WaSessionListResponse, WaSessionDestroyResponse, WaSendMessageResponse
)
from src.core.exceptions.whatsapp_exceptions import WaBridgeException

load_dotenv()


class WhatsappSessionManager:
    def __init__(self):
        self.service_url = f"{os.environ.get('WA_WEB_SERVICE')}"
        self._logger = get_logger(__name__)
        
    def _handle_response(self, response: requests.Response, schema_class):
        try:
            response.raise_for_status()
            data = response.json()
            return schema_class(**data)
        except requests.exceptions.HTTPError as e:
            error_data = {}
            try:
                error_data = response.json()
            except Exception:
                pass
            message = error_data.get("error", {}).get("message", str(e))
            self._logger.error(f"HTTP error from WA bridge: {message}")
            raise WaBridgeException(message=message, status_code=response.status_code)
        except Exception as e:
            self._logger.error(f"Unexpected error parsing WA bridge response: {str(e)}")
            raise WaBridgeException(message=f"Internal Service Error: {str(e)}")

    def create_session(self, business_id: str) -> WaSessionResponse:
        try:
            payload = {"business_id": business_id}
            result = requests.post(f"{self.service_url}/api/sessions", json=payload, timeout=15)
            return self._handle_response(result, WaSessionResponse)
        except Exception as e:
            if isinstance(e, WaBridgeException):
                raise e
            self._logger.error(f"Unexpected error while create session: {e}")
            raise WaBridgeException(message=str(e))

    def get_session_status(self, business_id: str) -> WaSessionResponse:
        try:
            result = requests.get(f"{self.service_url}/api/sessions/{business_id}", timeout=10)
            return self._handle_response(result, WaSessionResponse)
        except Exception as e:
            if isinstance(e, WaBridgeException):
                raise e
            self._logger.error(f"Unexpected error while get session status: {e}")
            raise WaBridgeException(message=str(e))  

    def get_all_session(self) -> WaSessionListResponse:
        try:
            result = requests.get(f"{self.service_url}/api/sessions", timeout=10)
            return self._handle_response(result, WaSessionListResponse)
        except Exception as e:
            if isinstance(e, WaBridgeException):
                raise e
            self._logger.error(f"Unexpected error while get all session: {e}")
            raise WaBridgeException(message=str(e))  
    
    def delete_session(self, business_id: str) -> WaSessionDestroyResponse:
        try:
            result = requests.delete(f"{self.service_url}/api/sessions/{business_id}", timeout=10)
            return self._handle_response(result, WaSessionDestroyResponse)
        except Exception as e:
            if isinstance(e, WaBridgeException):
                raise e
            self._logger.error(f"Unexpected error while delete session: {e}")
            raise WaBridgeException(message=str(e))  
        
    def reconnect_session(self, business_id: str) -> WaSessionResponse:
        try:
            result = requests.post(f"{self.service_url}/api/sessions/{business_id}/reconnect", timeout=15)
            return self._handle_response(result, WaSessionResponse)
        except Exception as e:
            if isinstance(e, WaBridgeException):
                raise e
            self._logger.error(f"Unexpected error while reconnect session: {e}")
            raise WaBridgeException(message=str(e))  
    
    def send_message(self, payload: SendMessagePayload) -> WaSendMessageResponse:
        try:
            payload_dict = payload.model_dump()
            result = requests.post(f"{self.service_url}/api/messages/send", json=payload_dict, timeout=10)
            return self._handle_response(result, WaSendMessageResponse)
        except Exception as e:
            if isinstance(e, WaBridgeException):
                raise e
            self._logger.error(f"Unexpected error while send message: {e}")
            raise WaBridgeException(message=str(e))  
    
whatsapp_session_manager = WhatsappSessionManager()