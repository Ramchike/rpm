import json
import time
from abc import abstractmethod
from abc import ABC
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List
import inquirer


class Choice(Enum):
    STONE = 0
    SHEARS = 1
    PAPER = 2

@dataclass
class Round:
    winner: "Player"
    player_pick: Choice
    ai_pick: Choice

    def to_json(self) -> dict:
        return {
            "winner": self.winner,
            "player_pick": self.player_pick,
            "ai_p`ick": self.ai_pick
        }


class Player(ABC):

    @abstractmethod
    def getPick(self) -> Choice:
        pass

class AiPlayer(Player):

    def __init__(self, game: "Game"):
        self.game = game

    def getPick(self) -> Choice:
        pass

class User(Player):

    def getPick(self) -> Choice:
        choices = inquirer.List('choice', 
            message = "Ваш ход",
            choices = [
                ("Камень", Choice.STONE),
                ("Ножницы", Choice.SHEARS),
                ("Бумага", Choice.PAPER)
            ]
        )
        answer = inquirer.prompt([choices])
        answer['choice']()

class Game:

    def __init__(self):
        self.ai = AiPlayer(self)
        self.rounds: List[Round] = []

class App:

    def __init__(self):

        self.loadData()

    def loadData(self):
        with open("profile.json", "r") as f:
            self.data = json.load(f)

    def startGame(self):
        print("game")

    def showStat(self):
        print("stat")

    def showSettings(self):
        print("settings")
    
    def exitApp(self):
        print("exit")

    def showStartMenu(self):

        print("""


        ██████╗░░█████╗░░█████╗░██╗░░██╗  ██████╗░░█████╗░██████╗░███████╗██████╗░
        ██╔══██╗██╔══██╗██╔══██╗██║░██╔╝  ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
        ██████╔╝██║░░██║██║░░╚═╝█████═╝░  ██████╔╝███████║██████╔╝█████╗░░██████╔╝
        ██╔══██╗██║░░██║██║░░██╗██╔═██╗░  ██╔═══╝░██╔══██║██╔═══╝░██╔══╝░░██╔══██╗
        ██║░░██║╚█████╔╝╚█████╔╝██║░╚██╗  ██║░░░░░██║░░██║██║░░░░░███████╗██║░░██║
        ╚═╝░░╚═╝░╚════╝░░╚════╝░╚═╝░░╚═╝  ╚═╝░░░░░╚═╝░░╚═╝╚═╝░░░░░╚══════╝╚═╝░░╚═╝

        ░██████╗██╗░░██╗███████╗░█████╗░██████╗░░██████╗
        ██╔════╝██║░░██║██╔════╝██╔══██╗██╔══██╗██╔════╝
        ╚█████╗░███████║█████╗░░███████║██████╔╝╚█████╗░
        ░╚═══██╗██╔══██║██╔══╝░░██╔══██║██╔══██╗░╚═══██╗
        ██████╔╝██║░░██║███████╗██║░░██║██║░░██║██████╔╝
        ╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░

        """)

        self.showCommandMenu()

    def showCommandMenu(self):

        commands = inquirer.List('command', 
            message = "Выбор команды",
            choices = [
                ("Начать игру", self.startGame),
                ("Посмотреть статистику", self.showStat),
                ("Настройки", self.showSettings),
                ("Выйти", self.exitApp)
            ]
        )
        answer = inquirer.prompt([commands])
        answer['command']()


if __name__ == "__main__":

    app = App()
    app.showStartMenu()