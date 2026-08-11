from pathlib import Path
import random

from aqt import gui_hooks, mw
from aqt.qt import QDialog, QLabel, QMovie, QVBoxLayout, QTimer, QSize

from .starters import choose_starter
from .wilds import handle_wild


SAVE_NAME = "pokeanki_game18"

eevee_evols = ["Flareon", "Vaporeon", "Jolteon", "Espeon",
               "Umbreon", "Leafeon", "Glaceon", "Sylveon"]
evolutions = {
    "Bulbasaur": "Ivysaur",
    "Ivysaur": "Venusaur",
    "Charmander": "Charmeleon",
    "Charmeleon": "Charizard",
    "Squirtle": "Wartortle",
    "Wartortle": "Blastoise",
    "Pikachu": "Raichu",
    "Eevee": random.choice(eevee_evols),
    "Jigglypuff": "Wigglytuff",
    "Vulpix": "Ninetales",
    "Wooloo": "Dubwool",
    "Munchlax": "Snorlax",
    "Mudkip": "Marshtomp",
    "Marshtomp": "Swampert",
    "Oshawott": "Dewott",
    "Dewott": "Samurott"
}


# load previous progress
game = mw.col.get_config(SAVE_NAME, {})

# if no saved progress:
if not game:
    starter = choose_starter()

    if starter:
        #active = pokemon leveling up (default to starter), collection = all pokemons
        game = {
            "cards": 0,
            "active": 0,
            "collection": [
                {
                    "name": starter,
                    "level": 1,
                    "cards": 0,
                },
            ],
        }
        mw.col.set_config(SAVE_NAME, game)



#level up and evolution message
def show_pokemon_message(time, message, pokemon):
    dialog = QDialog(mw)
    layout = QVBoxLayout(dialog)

    message_label = QLabel(message)
    gif_label = QLabel()

    gif_path = Path(__file__).parent / "gifs" / f"{pokemon}.gif"
    movie = QMovie(str(gif_path))
    movie.setScaledSize(QSize(100, 100))

    gif_label.setMovie(movie)

    layout.addWidget(message_label)
    layout.addWidget(gif_label)

    movie.start()

    if time == 1500: #if leveling up, move to corner
        dialog.show()
        screen = dialog.screen().availableGeometry()
        popup = dialog.frameGeometry()

        x = screen.right() - popup.width() - 20
        y = screen.bottom() - popup.height() - 20
        dialog.move(x, y)

        QTimer.singleShot(time, dialog.accept)
        dialog.exec()
        return
    
    else:
        QTimer.singleShot(time, dialog.accept)
        dialog.exec()
        return


#leveling up and evolving
#edit later to be selected pokemon

def on_card_answered(reviewer, card, ease):
    if not game:
        return

    #count cards for ANY pokemon
    game["cards"] += 1
    handle_wild(game)

    #find active pokemon
    active = game["collection"][game["active"]]
    active["cards"] += 1

    # level up after every 5 cards for ACTIVE pokemon
    if active["cards"] % 5 == 0:
        active["level"] += 1

        # evolve at levels 10 and 15
        if active["level"] in (10, 15) and active["name"] in evolutions:
            old_pokemon = active["name"] #identify pre-evolution pokemon
            active["name"] = evolutions[old_pokemon] #evolve and update pokemon name
            message = f'{old_pokemon} evolved into {active["name"]}!'
            show_pokemon_message(2000, message, active["name"])

            # #find old pokemon in collection
            # index = game["collection"].index(old_pokemon) 
            # #replace old pokemon with evolved pokemon in collection
            # game["collection"][index] = active["name"]

        else:
            message = f'{active["name"]} reached level {active["level"]}!'
            show_pokemon_message(1500, message, active["name"])

    mw.col.set_config(SAVE_NAME, game)


gui_hooks.reviewer_did_answer_card.append(on_card_answered)
