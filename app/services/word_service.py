import json
import httpx
import random
import asyncio
from pathlib import Path
from app.config import settings



class WordService:
    """Representa el servicio que permite consultar palabras aleatorias.

    Attributes:
        client: cliente HTTP asíncrono.
    """
    # TODO: Documentar.
    def __init__(self, client: httpx.AsyncClient):
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
            print(f"estoy en _fetch_random_word() {api_response.status_code}")
            print(f"JSON recibido: {api_response.text}")
            if api_response.status_code != 200:
                return None
            
            api_response_json = api_response.json()
            print(f'Estoy en _fetch_random_word {api_response_json}')
            
            return api_response_json
        except httpx.HTTPError:
            return None


    # TODO: Documentar.
    def _get_fallback_word(self):
        json_path = Path(__file__).parent.parent / "data" / "fallback_words.json"
        print(f'Estoy en _get_fallback_word() {json_path}')

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
