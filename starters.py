from pathlib import Path

from aqt import mw
from aqt.qt import QDialog, QHBoxLayout, QIcon, QPushButton, QSize, QLabel, QVBoxLayout


def choose_starter():
    chosen = None
    dialog = QDialog(mw)
    layout = QVBoxLayout(dialog)
    title = QLabel("Choose your starter Pokemon!")
    layout.addWidget(title)
    button_layout = QHBoxLayout()
    layout.addLayout(button_layout)
    image_folder = Path(__file__).parent / "images"

    #update chosen pokemon
    def choose(name):
        nonlocal chosen
        chosen = name
        dialog.accept()

    #choosing pokemon
    def make_button(name):
        button = QPushButton(name) #display pokemon on button
        button.setIcon(QIcon(str(image_folder / f"{name}.png")))
        button.setIconSize(QSize(100, 100))
        button.clicked.connect(lambda: choose(name))
        return button

    button_layout.addWidget(make_button("Bulbasaur"))
    button_layout.addWidget(make_button("Charmander"))
    button_layout.addWidget(make_button("Squirtle"))

#wait for player to choose
    dialog.exec()
    return chosen
