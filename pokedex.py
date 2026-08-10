from pathlib import Path

from aqt import mw, gui_hooks
from aqt.qt import QDialog, QLabel, QVBoxLayout, QMovie, QSize

#load pokedex characters
def show_pokedex(game):
    dialog = QDialog(mw)
    dialog.setWindowTitle("My Pokedex")

    layout = QVBoxLayout(dialog)
    layout.addWidget(QLabel("Your Pokemon:"))

    owned_pokemon = game.get("collection", [])
    movies = []

    if not owned_pokemon:
        layout.addWidget(QLabel("You don't own any Pokemon yet."))

    for pokemon in owned_pokemon:
        #display pokemon name and level
        name = pokemon["name"]
        level = pokemon["level"]
        layout.addWidget(QLabel(f"{name} - Level {level}"))

        #pair pokemon with gif
        gif_label = QLabel()
        gif_path = Path(__file__).parent / "gifs" / f"{name}.gif"
        movie = QMovie(str(gif_path))

        movie.setScaledSize(QSize(150, 150))
        layout.addWidget(gif_label)
        gif_label.setMovie(movie)

        #play gif
        movies.append(movie)
        movie.start()


    dialog.exec()

#when pokedex clicked
def open_pokedex():
    from .hooks import game
    show_pokedex(game)

#add pokedex button
def add_pokedex_link(links, toolbar): # links = list on toolbar, toolbar = toolbar object
    link = toolbar.create_link(
        "pokedex",
        "Pokedex",
        open_pokedex,
        tip="Pokedex",
        id="pokedex",
    )
    links.append(link)

    # mw.form.menuTools.addAction(action) add to toolbar instead
gui_hooks.top_toolbar_did_init_links.append(add_pokedex_link)
    