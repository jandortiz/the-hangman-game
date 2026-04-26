from fastapi import APIRouter, Request
from app.schemas.game import NewGameResponse, GuessResponse, GameStatusResponse, GuessRequest
from app.services.game_service import game_service


router = APIRouter(prefix="/api/game")

@router.post("/new", response_model=NewGameResponse)
async def create_new_game(request: Request):
    # request.app.state.word_service

    word_data = await request.app.state.word_service.get_word_with_hint()
    print(word_data)

    new_game_id = game_service.create_game(word=word_data['word'], hint=word_data['hint'])
    current_game_status = game_service.get_game_status(game_id=new_game_id)

    current_game_status["game_id"] = new_game_id
    return current_game_status


@router.post("/{game_id}/guess", response_model=GuessResponse)
def create_game_guess(game_id: str, guess: GuessRequest):
    word = game_service.games[game_id]['word']
    game_service.guess_letter(game_id=game_id, letter=guess.letter)
    current_game_status = game_service.get_game_status(game_id=game_id)

    correct = True if guess.letter.lower() in word else False

    current_game_status['correct'] = correct

    return current_game_status


@router.get("/{game_id}/status", response_model=GameStatusResponse)
def get_game_guess(game_id: str):
    return game_service.get_game_status(game_id=game_id)



