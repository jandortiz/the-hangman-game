from pydantic import BaseModel, Field


class GuessRequest(BaseModel):
    """Esquema que define lo que el front-end envía cuando el jugador intenta
    una letra.
    """
    letter: str = Field(min_length=1, max_length=1, pattern=r"^[a-zA-Z]$")


# Esquemas de repuesta.

class NewGameResponse(BaseModel):
    """Define lo que el back-end responde cuando se crea una partida nueva.
    """
    game_id: str
    masked_word: str
    hint: str
    attempts_remaining: int


class GuessResponse(BaseModel):
    """Define lo que el back-end devuelve después de un intento de letra.
    """
    status: str
    masked_word: str
    guessed_letters: list[str]
    attempts_remaining: int
    word: str | None = None
    correct: bool
    
    
    
    
    


class GameStatusResponse(BaseModel):
    """Define la respuesta del endpoint de estado.
    """
    status: str
    masked_word: str
    hint: str
    guessed_letters: list[str]
    attempts_remaining: int
    word: str | None = None
