import json
import os
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
    
def exportData(data):
    
    
    with open("profile.json", 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

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

    def getPick(self, pl_pick, data) -> Choice:
        
        games = data['games']
        if len(games) > 3:
            
            after_paper = {
                "SHEARS": 0,
                "PAPER": 0,
                "STONE": 0
            }

            after_stone = {
                "SHEARS": 0,
                "PAPER": 0,
                "STONE": 0
            }

            after_shears = {
                "SHEARS": 0,
                "PAPER": 0,
                "STONE": 0
            }
            
            for game in games:
                rounds = game['rounds']
                if len(rounds) > 1:
                    for i in range(1, len(rounds)):
                        last_player_pick = rounds[i - 1]['player_pick']
                        player_pick = rounds[i]['player_pick']
                        match last_player_pick:
                            case "PAPER":
                                after_paper[player_pick] += 1
                            case "STONE":
                                after_stone[player_pick] += 1
                            case "SHEARS":
                                after_shears[player_pick] += 1
                
            match pl_pick.name:
                case "PAPER":
                    pick = max(after_paper, key=after_paper.get)
                    pl_often_pick = Choice[pick].name
                case "STONE":
                    pick = max(after_stone, key=after_stone.get)
                    pl_often_pick = Choice[pick].name
                case "SHEARS":
                    pick = max(after_shears, key=after_shears.get)
                    pl_often_pick = Choice[pick].name
            match pl_often_pick:
                case "PAPER":
                    return Choice.SHEARS
                case "STONE":
                    return Choice.PAPER
                case "SHEARS":
                    return Choice.STONE
        else:
            return random.choice(list(Choice))

class User(Player):
    

    def __init__(self, data):
        
        
        self.data = data
        self.username = self.data['username']
        self.balance = self.data['money']

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
        
        new_username = input("Введи желаемое имя пользователя: ")
        self.data['username'] = new_username
        exportData(self.data)
        animatePrint(f"Имя пользователя {new_username} успешно установлено.")
        animatePrint("\nВыходим в меню......")
        

class Game:

    def __init__(self, player, ai, data):
        
        
        self.rounds: List[Round] = []
        self.player = player
        self.ai = ai
        self.data = data

    def start(self, round_count):
        rounds_pl = 0
        rounds_ai = 0
        result_game = 0
        for i in range(round_count):
            animatePrint("....Начало нового раунда....\n")
            time.sleep(0.5)
            player_pick = self.player.getPick()
            if round_count == 1:
                ai_pick = random.choice(list(Choice))
            else:
                ai_pick = self.ai.getPick(player_pick, self.data)
            if player_pick == ai_pick:
                round_result = Result.DRAW
                rounds_ai += 1
                rounds_pl += 1
            elif (player_pick.value == 0 and ai_pick.value == 1) or (player_pick.value == 1 and ai_pick.value == 2) or (player_pick.value == 2 and ai_pick.value == 0):
                round_result = Result.WIN
                result_game += 1
                rounds_pl += 1
            else:
                round_result = Result.LOSE
                result_game += -1
                rounds_ai += 1
            match round_result.name:
                case "WIN":
                    animatePrint("Вы выиграли в этом раунде.")
                case "DRAW":
                    animatePrint("Ничья в этом раунде.")
                case "LOSE":
                    animatePrint("Вы проиграли в этом раунде.")
            round = Round(round_result, player_pick, ai_pick)
            round_data = round.to_json()
            self.rounds.append(round_data)
        animatePrint("==== Статистика игры ====\n")
        if result_game >= 1:
            result_game = Result.WIN
            animatePrint("      Результат: Победа")
        elif result_game == 0:
            result_game = Result.DRAW
            animatePrint("      Результат: Ничья")
        else:
            result_game = Result.LOSE
            animatePrint("      Результат: Поражение")
        animatePrint(f"      Общий счёт ВЫ : ИИ составил:  {rounds_pl} : {rounds_ai}")
        animatePrint("\nВыходим в меню......")
        time.sleep(2)
        return { 
            "result": result_game.name,
            "money_win": 0,
            "rounds": self.rounds
            }
    
class App:

    def __init__(self):
        
        
        self.loadData()
        self.player = User(self.data)
        self.ai = AiPlayer()

    def loadData(self):
        
        
        with open("profile.json", "r") as f:
            self.data = json.load(f)

    def startGame(self):
        
        
        game = Game(self.player, self.ai, self.data)
        count_rounds = inquirer.List('count', 
        message = "Выберите Кол-во раундов",
        choices = [
            ("1", 1),
            ("3", 3),
            ("5", 5),
            ("10", 10)
        ]
    )
        answer = inquirer.prompt([count_rounds])
        data_game = game.start(answer['count'])
        self.data['games'].append(data_game)
        self.data['count_game'] += 1
        match data_game['result']:
            case "WIN":
                self.data['wins'] += 1
            case "LOSE":
                self.data['loses'] += 1
        exportData(self.data)
        self.showCommandMenu()
        
    def resetStat(self):
        default_data = {
            "username": "None",
            "count_game": 0,
            "wins": 0,
            "loses": 0,
            "pcy": 0,
            "money": 0,
            "games": []
        }
        
        exportData(default_data)
        f = open("profile.json")
        f.close()
        animatePrint("Статистика была успешно сброшена")
        animatePrint("\nВыходим в меню......")

    def showStat(self):
        
        data = open("profile.json")
        data = json.load(data)
        if data['wins'] != 0:
            pcy = trunc((data['wins'] / data['count_game']) * 100)
        else:
            pcy = 0
        animatePrint("==== Статистика игрока ====\n")
        animatePrint(f"     Имя пользователя: {data['username']}")
        animatePrint(f"     Количество игр: {data['count_game']}")
        animatePrint(f"     Побед: {data['wins']}")
        animatePrint(f"     Поражений: {data['loses']}")
        animatePrint(f"     Процент побед: {pcy}%")
        animatePrint(f"     Монет: {data['money']}")
        animatePrint("\nВыходим в меню...")
        time.sleep(2)
        self.showCommandMenu()
        
    def showSettings(self):
        
        
        settings = inquirer.List('setting', 
        message = "Настройки",
        choices = [
            ("Поменять имя пользователя", self.player.editUserName),
            ("Сбросить статистику", self.resetStat)
        ]
    )
        answer = inquirer.prompt([settings])
        answer['setting']()
        self.showCommandMenu()
    
    def exitApp(self):
        print("exit")

    def showStartMenu(self):
        self.showCommandMenu()

    def showCommandMenu(self):
        os.system('cls')
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