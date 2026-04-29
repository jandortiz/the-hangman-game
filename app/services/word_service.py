"""
Word service module.

This module provides the WordService class, which is responsible for
retrieving random words and their hints from an external API. If the API
is unavailable, it falls back to a local JSON file.
"""

import json
import httpx
import random
from pathlib import Path
from app.config import settings



class WordService:
    """Service for retrieving random words and hints.

    This service attempts to fetch words from an external API. If the API
    request fails or returns an invalid response, it falls back to a local
    dataset stored in a JSON file.

    Attributes:
        client (httpx.AsyncClient): Asynchronous HTTP client used to make requests.
    """

    def __init__(self, client: httpx.AsyncClient):
        """Initializes the WordService.

        Args:
            client (httpx.AsyncClient): An asynchronous HTTP client instance
                used to perform API requests.
        """

        self.client = client

    
    async def _fetch_random_word(self) -> str | None:
        """Obtiene una palabra aleatoria desde una API externa.

        Realiza una petición HTTP asíncrona para recuperar una palabra con la
        longitud especificada.

        Args:
            length: longitud de la palabra a buscar.

        Returns:
            str: Palabra aleatoria entregada por el API y con la longitud dada.
            None: Si ocurre un error HTTP o la respuesta no es válida.
        """
        try:
            api_response = await self.client.get(url=settings.word_api_url)

            if api_response.status_code != 200:
                return None
            
            api_response_json = api_response.json()
            return api_response_json
        except httpx.HTTPError:
            return None


    # TODO: Documentar.
    def _get_fallback_word(self):
        json_path = Path(__file__).parent.parent / "data" / "fallback_words.json"

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            record = random.choice(data)
        return record
    
    
    #TODO: Documentar.
    async def get_word_with_hint(self):
        word_requested = await self._fetch_random_word()
        if(word_requested):
            return {"word": word_requested["word"], "hint": word_requested["hint"]}
        else:
            return self._get_fallback_word()
