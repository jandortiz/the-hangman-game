"""
In this module, the Settings class is created to allow access to environment
variables from anywhere in the code.

Environment variables are initially loaded using the load_dotenv() function,
and then stored in the variables defined in the constructor.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        """Allows to use the wordGameDb API.
        """
        self.word_api_url = os.getenv("WORD_API_URL", "https://www.wordgamedb.com/api/v1/words/random")
        self.dictionary_api_url = os.getenv("DICTIONARY_API_URL", "https://www.wordgamedb.com/api/v1/words/random")
        self.environment = os.getenv("ENVIRONMENT", "development")


settings = Settings()