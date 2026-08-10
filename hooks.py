from pathlib import Path

from aqt import gui_hooks, mw
from aqt.qt import QDialog, QLabel, QMovie, QVBoxLayout, QTimer, QSize

from .starters import choose_starter


SAVE_NAME = "pokeanki_game5"


evolutions = {
    "Bulbasaur": "Ivysaur",
    "Ivysaur": "Venusaur",
    "Charmander": "Charmeleon",
    "Charmeleon": "Charizard",
    "Squirtle": "Wartortle",
    "Wartortle": "Blastoise",
}


# load previous progress
game = mw.col.get_config(SAVE_NAME, {})

# if no saved progress:
if not game:
    starter = choose_starter()

    if starter:
        game = {"pokemon": starter, "level": 1, "cards": 0}
        mw.col.set_config(SAVE_NAME, game)


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

    # move to the bottom-right corner
    dialog.show()
    screen = dialog.screen().availableGeometry()
    popup = dialog.frameGeometry()

    x = screen.right() - popup.width() - 20
    y = screen.bottom() - popup.height() - 20
    dialog.move(x, y)

    QTimer.singleShot(time, dialog.accept)

    dialog.exec()


def on_card_answered(reviewer, card, ease):
    if not game:
        return

    game["cards"] += 1

    # level up after every 5 cards
    if game["cards"] % 5 == 0:
        game["level"] += 1

        # evolve at levels 10 and 15
        if game["level"] in (10, 15) and game["pokemon"] in evolutions:
            old_pokemon = game["pokemon"]
            game["pokemon"] = evolutions[old_pokemon]
            message = f'{old_pokemon} evolved into {game["pokemon"]}!'
            show_pokemon_message(2000, message, game["pokemon"])

        else:
            message = f'{game["pokemon"]} reached level {game["level"]}!'
            show_pokemon_message(1500, message, game["pokemon"])

    mw.col.set_config(SAVE_NAME, game)


gui_hooks.reviewer_did_answer_card.append(on_card_answered)
