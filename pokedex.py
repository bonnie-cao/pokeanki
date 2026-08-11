from pathlib import Path

from aqt import gui_hooks, mw
from aqt.qt import (
    QDialog,
    QLabel,
    QMovie,
    QPushButton,
    QSize,
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
)

#load pokedex characters
def show_pokedex(game, save_name):
    #FORMATTING
    dialog = QDialog(mw)
    dialog.resize(750, 500)
    dialog.setWindowTitle("My Pokedex")
    layout = QVBoxLayout(dialog)

    layout.addWidget(QLabel("Your Pokemon:"))

    # make scrollable
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_content = QWidget()
    pokemon_grid = QGridLayout(scroll_content) # put a grid in the scrollable area
    scroll_area.setWidget(scroll_content)

    layout.addWidget(scroll_area)

    

    #get info, store gifs
    owned_pokemon = game.get("collection", [])
    movies = []

    columns = 3
    pokemon_per_page = 12
    current_page = 0

    # page controls
    page_buttons = QHBoxLayout()
    previous_button = QPushButton("Previous")
    page_label = QLabel()
    next_button = QPushButton("Next")

    page_buttons.addWidget(previous_button)
    page_buttons.addWidget(page_label)
    page_buttons.addWidget(next_button)

    layout.addLayout(page_buttons)


    # save selected active pokemon
    def select_pokemon(index):
        game["active"] = index #turn selected pokemon (index) active
        mw.col.set_config(save_name, game)
        dialog.accept()

    #stop previous page's gifs
    def clear_page():
        for movie in movies:
            movie.stop()

        movies.clear()

        while pokemon_grid.count():
            item = pokemon_grid.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()


    #show current page
    def show_page():
        clear_page()

        total_pages=max(
            1,
            (len(owned_pokemon) + pokemon_per_page - 1)
            // pokemon_per_page,
        )

        start = current_page * pokemon_per_page
        end = start + pokemon_per_page

        page_pokemon = owned_pokemon[start:end]

        if not page_pokemon:
            pokemon_grid.addWidget(
                QLabel("You don't own any Pokemon yet."),
                0,
                0,
            )

        #assigning index per pokemon
        for position, pokemon in enumerate(page_pokemon):
            index = start + position
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

            movie.setParent(gif_label)
            movie.setScaledSize(QSize(150, 150))

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
            row = position // columns
            column = position % columns
            pokemon_grid.addWidget(pokemon_panel, row, column)


        page_label.setText(
                f"Page {current_page + 1} of {total_pages}"
            )

        previous_button.setEnabled(current_page > 0)
        next_button.setEnabled(current_page < total_pages - 1)

    def previous_page():
            nonlocal current_page
            if current_page > 0:
                current_page -= 1
                show_page()

    def next_page():
        nonlocal current_page

        total_pages = max(
            1,
            (len(owned_pokemon) + pokemon_per_page - 1)
            // pokemon_per_page,
        )

        if current_page < total_pages - 1:
            current_page += 1
            show_page()

    previous_button.clicked.connect(previous_page)
    next_button.clicked.connect(next_page)

    #page one
    show_page()
    dialog.exec()

    # stop gifs when pokedex closes
    for movie in movies:
        movie.stop()



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
