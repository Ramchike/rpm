import json
import random
import time
import inquirer

from abc import abstractmethod
from abc import ABC
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List
from math import trunc


def animatePrint(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.08)
    print()

class Result(Enum):
    WIN = 1
    DRAW = 0
    LOSE = -1

class Choice(Enum):
    STONE = 0
    SHEARS = 1
    PAPER = 2

@dataclass
class Round:
    result: Result
    player_pick: Choice
    ai_pick: Choice

    def to_json(self) -> dict:
        return {
            "result": self.result.name,
            "player_pick": self.player_pick.name,
            "ai_pick": self.ai_pick.name
        }

class Player(ABC):

    @abstractmethod
    def getPick(self) -> Choice:
        pass

class AiPlayer(Player):

    def __init__(self):
        pass

    def getPick(self) -> Choice:
        return random.choice(list(Choice))

class User(Player):

    def __init__(self, username, balance):
        self.username = username
        self.balance = balance

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
        return answer['choice']
    
    def editUserName(self) -> str:
        self.username = input("Введи желаемое имя пользователя: ")
        return self.username

class Game:

    def __init__(self, player, ai):
        self.rounds: List[Round] = []
        self.player = player
        self.ai = ai

    def start(self, round_count):
        result_game = 0
        for i in range(round_count):
            player_pick = self.player.getPick()
            ai_pick = self.ai.getPick()
            if player_pick == ai_pick:
                round_result = Result.DRAW
            elif (player_pick.value == 0 and ai_pick.value == 1) or (player_pick.value == 1 and ai_pick.value == 2) or (player_pick.value == 2 and ai_pick.value == 0):
                round_result = Result.WIN
                result_game += 1
            else:
                round_result = Result.LOSE
                result_game += -1
            print(round_result.name)
            round = Round(round_result, player_pick, ai_pick)
            round_data = round.to_json()
            self.rounds.append(round_data)
        if result_game >= 1:
            result_game = Result.WIN
        elif result_game == 0:
            result_game = Result.DRAW
        else:
            result_game = Result.LOSE
        return { 
            "result": result_game.name,
            "money_win": 0,
            "rounds": self.rounds
            }
    
class App:

    def __init__(self):
        self.loadData()
        self.player = User(self.data['username'], self.data['money'])
        self.ai = AiPlayer()

    def loadData(self):
        with open("profile.json", "r") as f:
            self.data = json.load(f)

    def startGame(self):
        game = Game(self.player, self.ai)
        count_rounds = inquirer.List('count', 
        message = "Выберите Кол-во раундов",
        choices = [
            ("1", 1),
            ("3", 3),
            ("5", 5),
            ("10", 10),
            ("Выйти", self.exitApp())
        ]
    )
        answer = inquirer.prompt([count_rounds])
        data_game = game.start(answer['count'])
        print(data_game)
        print(json.dumps(data_game, indent=1))

    def showStat(self):
        data = self.data
        animatePrint(f"Имя пользователя: {data['username']}")
        animatePrint(f"Количество игр: {data['count_game']}")
        animatePrint(f"Побед: {data['wins']}")
        animatePrint(f"Поражений: {data['loses']}")
        animatePrint(f"Процент побед: {trunc((data['wins'] / data['count_game']) * 100)}%")
        animatePrint(f"Монет: {data['money']}")
        animatePrint("История игр:")
    def showSettings(self):
        print("settings")
        settings = inquirer.List('setting', 
        message = "Настройки:",
        choices = [
            ("Поменять имя пользователя", self.player.editUserName),
            ("Выбрать тему", 1)
        ]
    )
        answer = inquirer.prompt([settings])
        answer['setting']()
    
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