"""
Game API router module.

This module defines the HTTP endpoints for managing Hangman-style games.
It includes routes for creating a new game, making guesses, and retrieving
the current game status.

The router interacts with the GameService for game logic and WordService
(via application state) for retrieving words and hints.
"""

from fastapi import APIRouter, Request
from app.services.game_service import game_service
from app.schemas.game import (
    NewGameResponse,
    GuessResponse,
    GameStatusResponse,
    GuessRequest,
)


router = APIRouter(prefix="/api/game")


@router.post("/new", response_model=NewGameResponse)
async def create_new_game(request: Request):
    """Creates a new game.

    This endpoint retrieves a word and hint from the WordService,
    initializes a new game using the GameService, and returns the
    initial game state.

    Args:
        request (Request): FastAPI request object used to access
            application state, including the WordService instance.

    Returns:
        NewGameResponse: The initial game state including:
            - game_id (str): Unique identifier of the game.
            - status (str): Current game status ("playing").
            - guessed_letters (list): Empty list at game start.
            - attempts_remaining (int): Initial number of attempts.
            - hint (str): Hint for the word.
            - masked_word (str): Masked representation of the word.

    Behavior:
        - Fetches a word and hint asynchronously.
        - Creates a new game instance.
        - Returns the initialized game state with the game ID.
    """
    word_data = await request.app.state.word_service.get_word_with_hint()

    new_game_id = game_service.create_game(word=word_data['word'], hint=word_data['hint'])
    current_game_status = game_service.get_game_status(game_id=new_game_id)

    current_game_status["game_id"] = new_game_id
    return current_game_status


@router.post("/{game_id}/guess", response_model=GuessResponse)
def create_game_guess(game_id: str, guess: GuessRequest):
    """Submits a letter guess for a specific game.

    This endpoint processes a player's guessed letter, updates the game state,
    and returns the updated status including whether the guess was correct.

    Args:
        game_id (str): The unique identifier of the game.
        guess (GuessRequest): Request body containing:
            - letter (str): The letter guessed by the player.

    Returns:
        GuessResponse: The updated game state including:
            - status (str): Current game status ("playing", "won", "lost").
            - guessed_letters (list): Letters guessed so far.
            - attempts_remaining (int): Remaining attempts.
            - hint (str): The hint for the word.
            - masked_word (str): Updated masked word.
            - word (str, optional): Full word if game is finished.
            - correct (bool): Indicates whether the guessed letter is in the word.

    Raises:
        KeyError: If the provided game_id does not exist.

    Behavior:
        - Checks if the guessed letter is in the word.
        - Updates the game state via GameService.
        - Returns the updated game status along with correctness of the guess.
    """
    word = game_service.games[game_id]['word']
    game_service.guess_letter(game_id=game_id, letter=guess.letter)
    current_game_status = game_service.get_game_status(game_id=game_id)

    correct = True if guess.letter.lower() in word else False
    current_game_status['correct'] = correct
    return current_game_status


@router.get("/{game_id}/status", response_model=GameStatusResponse)
def get_game_guess(game_id: str):
    return game_service.get_game_status(game_id=game_id)



