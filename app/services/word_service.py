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
            api_response_json = api_response.json()
            print(f'Estoy en _fetch_random_word {api_response_json}')
            return api_response_json
        except httpx.HTTPError:
            return None

    # TODO: Documentar.
    async def _fetch_word_definition(self, word: str) -> str | None:
        url = settings.dictionary_api_url + f"/{word}"

        try:
            api_dict_response = await self.client.get(url)
            if api_dict_response.status_code == 200:
                api_dict_response_json = api_dict_response.json()
                return api_dict_response_json[0]['meanings'][0]['definitions'][0]['definition']
            else:
                return None
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
