from google import genai
from core.config import settings

from pageindex import PageIndexClient
import pageindex.utils as utils


class GeminiClient:
    def __init__(self):
        self.gemini = genai.Client(api_key=settings.gemini_api_key)
        self.model_name = settings.gemini_model

    async def generate_text(self, prompt: str) -> str:
        response = self.gemini.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        return response.text

gemini_client = GeminiClient()
pi_client = PageIndexClient(api_key=settings.page_index_api_key)

