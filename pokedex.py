from pathlib import Path

from aqt import gui_hooks, mw
from aqt.qt import QDialog, QLabel, QMovie, QPushButton, QSize, QScrollArea, QVBoxLayout, QGridLayout, QWidget

#load pokedex characters
def show_pokedex(game, save_name):
    #FORMATTING
    dialog = QDialog(mw)
    dialog.resize(750, 500)
    dialog.setWindowTitle("My Pokedex")
    layout = QVBoxLayout(dialog)

    # make scrollable
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_content = QWidget()
    pokemon_grid = QGridLayout(scroll_content) # put a grid in the scrollable area
    scroll_area.setWidget(scroll_content)
    
    layout.addWidget(QLabel("Your Pokemon:"))
    layout.addWidget(scroll_area)


    #get info, store gifs
    owned_pokemon = game.get("collection", [])
    movies = []

    columns = 3

    # save selected active pokemon
    def select_pokemon(index):
        game["active"] = index #turn selected pokemon (index) active
        mw.col.set_config(save_name, game)
        dialog.accept()

    if not owned_pokemon:
        layout.addWidget(QLabel("You don't own any Pokemon yet."))

    #assigning index per pokemon
    for index, pokemon in enumerate(owned_pokemon):
        name = pokemon["name"]
        level = pokemon["level"]
        #display pokemon name and level
        pokemon_panel = QWidget()
        panel_layout = QVBoxLayout(pokemon_panel)

        panel_layout.addWidget(QLabel(f"{name} - Level {level}"))

        #pair pokemon with gif
        gif_label = QLabel()
        gif_path = Path(__file__).parent / "gifs" / f"{name}.gif"
        movie = QMovie(str(gif_path))
        movie.setScaledSize(QSize(150, 150))

        #play gif
        gif_label.setMovie(movie)
        panel_layout.addWidget(gif_label)
        movies.append(movie)
        movie.start()

        #choose active pokemon
        select_button = QPushButton("Equip Pokemon")

        if index == game["active"]:
            select_button.setEnabled(False) #can't click button for active pokemon
        else:
            #select pokemon according to index
            select_button.clicked.connect(
                lambda checked=False, selected=index: select_pokemon(selected)
            )

        panel_layout.addWidget(select_button)
        #number of rows
        row = index // columns
        column = index % columns
        pokemon_grid.addWidget(pokemon_panel, row, column)

    dialog.exec()

#when pokedex clicked
def open_pokedex():
    from .hooks import SAVE_NAME, game #load progress
    show_pokedex(game, SAVE_NAME) #apply progress

#add pokedex button
def add_pokedex_link(links, toolbar):
    link = toolbar.create_link(
        "pokedex",
        "Pokedex",
        open_pokedex,
        tip="Pokedex",
        id="pokedex",
    )
    links.append(link)


gui_hooks.top_toolbar_did_init_links.append(add_pokedex_link)
