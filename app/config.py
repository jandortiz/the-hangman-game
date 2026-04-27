"""
En este módulo se crea la clase Settings que permite acceder a las variables
de entorno en cualquier parte del código. 

Las variables de entorno se cargan inicialmente mediante la función
load_dotenv(), luego se guardan en las variables definidas en el constructor.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.word_api_url = os.getenv("WORD_API_URL", "https://www.wordgamedb.com/api/v1/words/random")
        self.dictionary_api_url = os.getenv("DICTIONARY_API_URL", "https://www.wordgamedb.com/api/v1/words/random")
        self.environment = os.getenv("ENVIRONMENT", "development")


settings = Settings()