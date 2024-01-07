import json
import time
from abc import abstractmethod
from abc import ABC
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List
from pick import pick, Option

with open("profile.json", "r") as f:
    profile = json.load(f)

class Choice(Enum):
    STONE = 0
    SHEARS = 1
    PAPER = 2

    @staticmethod
    def byName(self, name: str) -> Optional["Choice"]:
        match name:
            case "Камень": return Choice.STONE
            case "Ножницы": return Choice.SHEARS
            case "Бумага": return Choice.PAPER

class Winner(Enum):
    User = 0
    Ai = 1
    Draw = 2

@dataclass
class Round:
    winner: Winner
    player_pick: Choice
    ai_pick: Choice

    def to_json(self) -> dict:
        return {
        "winner": self.winner,
        "player_pick": self.player_pick,
        "ai_pick": self.ai_pick
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

    def __init__(self, money: int):
        self.money = money

    def getPick(self) -> Choice:
        options = [
            Option("Камень", Choice.STONE),
            Option("Ножницы", Choice.SHEARS),
            Option("Бумага", Choice.PAPER)
        ]
        selected, index = pick(options, "Ваш ход, выберите предмет \U0001f600")
        return selected.value

class App:
    def __int__(self):
        pass

    def loadData(self):
        with open("profile.json", "r") as f:
            data = json.load(f)
        return data

    def get_stats(self):
        data = App.loadData(self)
        return print(json.dumps(data, indent=4))

    def start():
        commands = [
            Option("  Начать игру", Game.start()),
            Option("  Посмотреть статистику", App.get_stats()),
            Option("  Настройки"),
            Option("  Выйти")
        ]
        command, index = pick(commands, "Добро пожаловать в игру КАМЕНЬ НОЖНИЦЫ БУМАГА:")
        return command.value

class Game:

    def __init__(self):
        self.ai = AiPlayer(self)
        self.rounds: List[Round] = []

        self.loadData()

    def loadData(self):
        with open("profile.json", "r") as f:
            data = json.load(f)

    def exportData(self):
        self.rounds_data = [round.to_json() for round in self.rounds]

    def start(self):
        pass

def hello():
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
    load_elements = [" ", "=", "==", "===", "====", "=====", "======", "=======", "========", "=========", "=========="]

    print("Загрузка игры...")

    for i in range(len(load_elements)):
        progress = load_elements[i]
        percentage = i * 10
        print(f"[{progress}] {percentage}%")
        time.sleep(0.5)  # Задержка для плавности анимации


App.start()
