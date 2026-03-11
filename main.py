import threading
from driver import get_driver
import config
import tkinter as tk
from tkinter import simpledialog

driver_ready = threading.Event()


def start_driver():
    get_driver()
    driver_ready.set()


t = threading.Thread(target=start_driver)
t.start()


def color(text):
    return "\033[32m" + text + "\033[0m"


def openMenu():
    if config.defaultOption == 0:
        inputValue = simpledialog.askstring(
            "\nSelect an option\n",
            "0 - Visualizar chamados (admin)\n"
            + "1 - Abrir & Fechar\n"
            + "2 - Abrir\n"
            + "3 - Fechar (automatico)\n"
            + "4 - Fechar (manual)\n"
            + "5 - Avaliar\n"
            + "6 - Fechar\n",
        )
    else:
        inputValue = config.defaultOption

    driver_ready.wait()  # aguarda navegador estar pronto

    from menu import selectMenuOptions

    selectMenuOptions(inputValue)


openMenu()
