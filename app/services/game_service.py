"""
Game service module.

This module provides the GameService class, which manages the lifecycle
of Hangman-style word guessing games. 
It allows creating games, making guesses and retrieving the current game status.
"""
import uuid

class GameService:
    """Service class to manage Hangman-style games.

    This class handles game creation, letter guessing, and tracking the current
    state of each game instance.
    """

    def __init__(self):
        """Initializes the GameService.

        Creates an internal dictionary to store active games and each game is
        identified by a unique game ID.
        """
        self.games = {}

    

    def create_game(self, word: str, hint: str) -> str:
        """Creates a new game instance.

        Args:
            word (str): The word that the player must guess.
            hint (str): A hint to help the player guess the word.

        Returns:
            str: A unique identifier (UUID) for the created game.

        Notes:
            - The word is stored in lowercase.
            - The game starts with 6 maximum attempts.
            - Initial game status is set to "playing".
        """
        game_id = str(uuid.uuid4())
        
        self.games[game_id] = {
            "word": word.lower(),
            "hint": hint,
            "guessed_letters":set(),
            "max_attempts": 6,
            "status": "playing"
            }
        return game_id
    

    def guess_letter(self, game_id: str, letter: str) -> dict:
        """Processes a letter guess for a given game.

        Args:
            game_id (str): The unique identifier of the game.
            letter (str): The letter guessed by the player.

        Returns:
            dict: The updated game state, including word, guessed letters,
            remaining attempts, and status.

        Raises:
            KeyError: If the provided game_id does not exist.

        Behavior:
            - Converts the letter to lowercase.
            - Adds the letter to guessed letters if not already used.
            - Decreases remaining attempts if the guess is incorrect.
            - Updates game status to:
                * "won" if all letters are guessed.
                * "lost" if attempts reach zero.
                * "playing" otherwise.
            - If the game is already finished, no changes are applied.
        """
        try:
            current_game = self.games[game_id]

            if current_game['status'] == "playing":
                letter = letter.lower()

                if letter not in current_game['guessed_letters']:
                    current_game['guessed_letters'].add(letter)

                    if letter not in current_game['word']:
                        current_game['max_attempts'] -= 1
                    else:
                        print(f"La letra {letter} ESTÁ en la palabra")
                
                if (set(current_game['word']).issubset(current_game['guessed_letters'])):
                    current_game['status'] = 'won'
                elif (current_game['max_attempts'] == 0):
                    current_game['status'] = 'lost'
            else:
                print("JUEGO TERMINADO")
            return current_game
        except KeyError as e:
            print(f"Ha habido un error: Clave {e} no encontrada.")

    
    #TODO: Documentar.
    def get_game_status(self, game_id: str) -> dict:
        """Retrieves the current status of a game.

        Args:
            game_id (str): The unique identifier of the game.

        Returns:
            dict: A dictionary containing:
                - status (str): Current game status ("playing", "won", "lost").
                - guessed_letters (list): Letters guessed so far.
                - attempts_remaining (int): Remaining attempts.
                - hint (str): The hint for the word.
                - masked_word (str): The word with unguessed letters hidden.
                - word (str, optional): The full word (only if game is finished).

        Raises:
            KeyError: If the provided game_id does not exist.

        Notes:
            - The masked word displays guessed letters and underscores for
              remaining letters.
            - The full word is only revealed if the game is won or lost.
        """

        try:
            current_game = self.games[game_id]

            masked_status = [
                caracter if caracter in current_game['guessed_letters'] else "_" for caracter in current_game['word']                
                ]
            
            masked_word = "".join(masked_status)

            current_game_status = {
                "status": current_game["status"],
                "guessed_letters": list(current_game["guessed_letters"]),
                "attempts_remaining": current_game["max_attempts"],
                "hint": current_game["hint"]
                }

            if current_game["status"] == "playing":
                current_game_status["masked_word"] = masked_word
            else:
                current_game_status["masked_word"] = masked_word
                current_game_status["word"] = current_game["word"] 

            return current_game_status
        except KeyError as e:
            print(f"Juego con clave {e} no encontrado.")


game_service = GameService()
