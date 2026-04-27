from pydantic import BaseModel, Field


class GuessRequest(BaseModel):
    """Defines the information sent by the front-end.
    """
    letter: str = Field(min_length=1, max_length=1, pattern=r"^[a-zA-Z]$")


class NewGameResponse(BaseModel):
    """Defines the back-end response to a new game.
    """
    game_id: str
    masked_word: str
    hint: str
    attempts_remaining: int


class GuessResponse(BaseModel):
    """Defines the back-end response to a new letter essay.
    """
    status: str
    masked_word: str
    guessed_letters: list[str]
    attempts_remaining: int
    word: str | None = None
    correct: bool


class GameStatusResponse(BaseModel):
    """Defines the state endpoint response.
    """
    status: str
    masked_word: str
    hint: str
    guessed_letters: list[str]
    attempts_remaining: int
    word: str | None = None
