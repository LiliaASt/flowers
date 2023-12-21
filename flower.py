import os
import requests


def creating_folder(name: str) -> None:
    if not os.path.isdir(name):
        os.mkdir(name)
        print("The folder has been created")
    else:
        print("The folder already exists")

