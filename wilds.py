import random
from pathlib import Path

from aqt import mw
from aqt.utils import tooltip
from aqt.qt import QDialog, QLabel, QVBoxLayout, QMovie, QSize, QPushButton, QKeySequence

#wild pokemon appearing
# 1 flashcard = 1 pokeball thrown at it

#make random
# future, add random shiny types?
wild_types = ["Pikachu", "Eevee", "Jigglypuff", "Vulpix, Bulbasaur, Charmander, Squirtle, Rowlet, Wooloo, Munchlax"]

#bellcurve function to randomize: pokeballs needed, flashcards until wild type appears
def bell_curve(middle, spread):
    number = round(random.gauss(middle, spread))
    #non zero/negative results
    return max(1, number)


#panel for wild pokemon appearing
def show_wild_pokemon(game, size, message):
    dialog = QDialog(mw)
    layout = QVBoxLayout(dialog)
    label = QLabel()
    label.setText(message)
    layout.addWidget(label)
    
    gif_label = QLabel()

    gif_path = Path(__file__).parent / "gifs" / f"{game['wild_pokemon']}.gif"
    movie = QMovie(str(gif_path))
    movie.setScaledSize(QSize(size, size))

    layout.addWidget(gif_label)
    gif_label.setMovie(movie)

    movie.start()

    if size == 150: #if wild pokemon appears:
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button)
        ok_button.setShortcut(QKeySequence("Space"))


    if size == 151: #if pokemon caught
        QTimer.singleShot(2000, dialog.accept)
    
    dialog.exec()


def handle_wild(game):
    # no wild pokemon state
    if "wild_pokemon" not in game:
        game["wild_pokemon"] = None
        game["cards_until_wild"] = bell_curve(15, 4)
        game["pokeballs"] = 0
        game["pokeballs_needed"] = 0

    # cards needed until next wild pokemon
    if game["wild_pokemon"] is None:
        game["cards_until_wild"] -= 1

        #wild pokemon just appeared
        if game["cards_until_wild"] == 0:
            #random wild_type becomes catchable wild_pokemon
            game["wild_pokemon"] = random.choice(wild_types)
            game["pokeballs"] = 0
            game["pokeballs_needed"] = bell_curve(5, 2)
            message = (f"A wild {game['wild_pokemon']} appeared!\nAnswer flashcards to throw Pokeballs at {game['wild_pokemon']}!")
            size = 150
            show_wild_pokemon(game, size, message)


        return # don't run rest of function if no wild pokemon

    # pokeball thrown = flashcards done
    game["pokeballs"] += 1
    wild_pokemon = game["wild_pokemon"]
    
    # catching pokemon
    if game["pokeballs"] >= game["pokeballs_needed"]:
        #caught, add to collection
        game["collection"].append(
            {
                "name": wild_pokemon,
                "level": 1,
                "cards": 0,
            }
        )

        message = (f"You caught {game['wild_pokemon']}!")
        size = 150
        show_wild_pokemon(game, size, message)
        #reset
        game["wild_pokemon"] = None
        game["cards_until_wild"] = bell_curve(15, 4)
        game["pokeballs"] = 0
        game["pokeballs_needed"] = 0
    else:
        tooltip(f'You threw a Pokeball at {wild_pokemon}!')
