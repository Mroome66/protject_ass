from langchain_community.chat_models import GigaChat
from langchain.schema import BaseMessage, LLMResult
from typing import Any, Optional, Dict, Sequence
import logging


class LogGigaChat(GigaChat):
    class Config:
        extra = "allow"

    def __init__(self, log_file: str, **kwargs):
        super().__init__(**kwargs)
        self.request_tokens = 0
        self.response_tokens = 0
        self.total_tokens = 0

        self.logger = logging.getLogger("CustomGigaChat")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file, encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def add_tokens(self, add_input_tokens: int, add_output_tokens: int, add_total_tokens: int):
        self.request_tokens = add_input_tokens
        self.response_tokens = add_output_tokens
        self.total_tokens += add_total_tokens

    def log_tokens(self):
        try:
            self.logger.info(f"request tokens: {self.request_tokens}, response tokens: {self.response_tokens}, total tokens: {self.total_tokens}")
        except Exception as e:
            self.logger.error(f"Error calculating tokens: {str(e)}")

    def invoke(self, input: Any, **kwargs: Any) -> Any:
        self.logger.info(f"Starting invoke  with: {input}")
        
        try:
            response = super().invoke(input=input, **kwargs )
            token_data = response.response_metadata['token_usage'] # Словарь содержащий метаданные запроса по ключу token_usage можно получить всё о токенах
            token_data = dict(token_data)
            self.add_tokens(token_data['prompt_tokens'],token_data['completion_tokens'], token_data['total_tokens'])
            self.log_tokens()
            return response
        except Exception as e:
            self.logger.error(f"Error during invoke: {str(e)}")
            raise
    def get_token_stats(self) -> Dict[str, int]:
        return {
            "total_request_tokens": self.request_tokens,
            "total_response_tokens": self.response_tokens,
            "total_tokens": self.total_tokens
        }

