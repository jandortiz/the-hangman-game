import uuid

class GameService:
    def __init__(self):
        self.games = {}

    
    #TODO: Documentar.
    def create_game(self, word: str, hint: str) -> str:
        game_id = str(uuid.uuid4())
        
        self.games[game_id] = {
            "word": word.lower(),
            "hint": hint,
            "guessed_letters":set(),
            "max_attempts": 6,
            "status": "playing"
            }
        return game_id
    

    #TODO: Documentar.
    def guess_letter(self, game_id: str, letter: str) -> dict:
        try:
            current_game = self.games[game_id]

            # Comporobación de estado de juego.
            if current_game['status'] == "playing":
                letter = letter.lower()

                # Comprobación de que la letra no se haya usado para agregarla al diccionario de letras usadas.
                if letter not in current_game['guessed_letters']:
                    print(f"La letra {letter} NO está en agregada")
                    current_game['guessed_letters'].add(letter)

                    # Comprobación que la letra NO esté en la palabra para disminuir contador.
                    if letter not in current_game['word']:
                        print(f"La letra {letter} NO está en la palabra")
                        current_game['max_attempts'] -= 1
                    else:
                        print(f"La letra {letter} ESTÁ en la palabra")
                
                # Comprobación de que la palabra buscada esté contenida en el diccionario de palabras usadas.
                if (set(current_game['word']).issubset(current_game['guessed_letters'])):
                    current_game['status'] = 'won'
                    print('Juego ganado')

                # Qué pasa en caso de quedarse sin intentos permitidos? cambio el estado a juego perdido.
                elif (current_game['max_attempts'] == 0):
                    current_game['status'] = 'lost'
                    print('Juego perdido')
            else:
                print("JUEGO TERMINADO")
            return current_game
        except KeyError as e:
            print(f"Ha habido un error: Clave {e} no encontrada.")

    
    #TODO: Documentar.
    def get_game_status(self, game_id: str) -> dict:
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

# # Prueba 1: se crea el id y comprueba en el método guess_letters()
# new_game = GameService()

# # Caso letra nueva y está en la palabra.
# new_game_id_1 = new_game.create_game("Alexa", "Nombre novia")
# new_game.guess_letter(new_game_id_1, "a")
# print(new_game.games)

# # Caso letra nueva y está en la palabra.
# new_game.guess_letter(new_game_id_1, "l")
# # print(new_game.games)

# # Caso letra nueva y está en la palabra.
# new_game.guess_letter(new_game_id_1, "x")
# # print(new_game.games)

# # Caso letra nueva y NO está en la palabra.
# new_game.guess_letter(new_game_id_1, "b")
# # print(new_game.games)

# # Caso letra nueva y NO está en la palabra.
# new_game.guess_letter(new_game_id_1, "m")
# # print(new_game.games)

# # Caso letra ya agregada.
# new_game.guess_letter(new_game_id_1, "m")
# # print(new_game.games)

# # Caso letra ya agregada.
# new_game.guess_letter(new_game_id_1, "b")
# # print(new_game.games)

# # Caso letra ya agregada.
# new_game.guess_letter(new_game_id_1, "x")
# # print(new_game.games)

# # Caso letra nueva y NO está en la palabra.
# new_game.guess_letter(new_game_id_1, "m")
# # print(new_game.games)
# print('ÚLTIMA LETRA PUESTA PARA PERDER')
# # Caso letra nueva y NO está en la palabra.
# new_game.guess_letter(new_game_id_1, "e")
# # print(new_game.games)

# print(new_game.guess_letter(new_game_id_1, "e"))


# # Prueba 2: probando el método get_game_status()

# print(new_game.get_game_status(new_game_id_1))