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

    
    async def _fetch_random_word(self, length: int = 7) -> str | None:
        """Obtiene una palabra aleatoria desde una API externa.

        Realiza una petición HTTP asíncrona para recuperar una palabra con la
        longitud especificada.

        Args:
            length: longitud de la palabra a buscar.

        Returns:
            str: Palabra aleatoria entregada por el API y con la longitud dada.
            None: Si ocurre un error HTTP o la respuesta no es válida.
        """
        # url = settings.word_api_url + "/word" + f"?length={length}"
        url = settings.word_api_url
        
        try:
            api_response = await self.client.get(url=url)
            api_response_json = api_response.json()
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
        intentos = 0
        word_randon_length = random.randint(4, 16)

        while (intentos < 5):
            word_requested = await self._fetch_random_word(word_randon_length)
            # word_definition = await self._fetch_word_definition(word_requested)
            if(word_requested):
                return {"word": word_requested["word"], "hint": word_requested["hint"]}
            else:
                return self._get_fallback_word()
            
            intentos+=1




# async def main():
#     async with httpx.AsyncClient() as client:
#         service = WordService(client)
#         # word_result = await service._fetch_random_word(4)
#         # word_result_2 = service._get_fallback_word()
#         # print(f"Palabra obtenida: {word_result_2}")
#         # dict_result = await service._fetch_word_definition(word_result)
#         # print(dict_result[0]["meanings"])
#         dict_result_2 =  await service.get_word_with_hint()
#         print(dict_result_2)
        


# if __name__=="__main__":
#     asyncio.run(main())