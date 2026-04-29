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

    
    async def _fetch_random_word(self) -> dict | None:
        """Fetches a random word from an external API.

        Performs an asynchronous HTTP GET request to retrieve a word and its hint.

        Returns:
            dict | None: A dictionary containing the word and its hint if the
            request is successful. Returns None if:
                - The HTTP response status is not 200.
                - An HTTP error occurs during the request.
                - The response body is invalid.
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
        """Retrieves a random word from a local fallback dataset.

        Loads a JSON file containing predefined words and hints, then selects
        one record at random.

        Returns:
            dict: A dictionary containing:
                - word (str): The word to guess.
                - hint (str): A hint associated with the word.

        Notes:
            - The fallback file is located at `app/data/fallback_words.json`.
            - This method is used when the external API is unavailable.
        """

        json_path = Path(__file__).parent.parent / "data" / "fallback_words.json"

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            record = random.choice(data)
        return record
    

    async def get_word_with_hint(self):
        """Retrieves a word and its hint.

        Attempts to fetch a word from the external API. If the request fails,
        it falls back to a local dataset.

        Returns:
            dict: A dictionary containing:
                - word (str): The word to guess.
                - hint (str): A hint associated with the word.

        Behavior:
            - Uses the external API as the primary source.
            - Falls back to local data if the API request fails or returns None.
        """
        word_requested = await self._fetch_random_word()
        if(word_requested):
            return {"word": word_requested["word"], "hint": word_requested["hint"]}
        else:
            return self._get_fallback_word()
