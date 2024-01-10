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
    """
    Функция постепенного вывода текста (эффект печати).
    """
    
    
    # Последовательный посимвольный вывод строки при помощи цикла for и задержки (time.sleep()).
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.08)
    print()
    
def exportData(data):
    """
    Функция для экспорта данных в json файл.
    """
    
    # Открытие файла и обновление profile.json.
    with open("profile.json", 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Перечисления (библиотека Enum) обеспечивают удобство в использовании и улучшают читаемость кода.
class Result(Enum): 
    """
    Класс Result представляет результаты игры (победа, ничья, поражение).
    """
    
    
    WIN = 1
    DRAW = 0
    LOSE = -1

class Choice(Enum):
    """
    Класс Choice представляет возможные варианты выбора игрока (камень, ножницы, бумага).
    """
    
    
    STONE = 0
    SHEARS = 1
    PAPER = 2


@dataclass
class Round:
    """
    Дата-Класс для представления результатов отдельного раунда.
    """
    result: Result
    player_pick: Choice
    ai_pick: Choice

    def to_json(self) -> dict:
        """
        Функция совмещения данных раунда в словарь для поддержки эскпорта в json.
        """
        
        
        return {
            "result": self.result.name,
            "player_pick": self.player_pick.name,
            "ai_pick": self.ai_pick.name
        }
        

class Player(ABC):
    """
    Абстрактный класс, описывающий игроков: Пользователя и ИИ.
    """
    
    
    @abstractmethod
    def getPick(self) -> Choice:
        pass

class AiPlayer(Player):
    """
    Класс для представления компьютерного игрока.
    Наследует абстрактный класс игрока.
    """
    
    
    def __init__(self):
        pass

    def getPick(self, pl_pick, data) -> Choice:
        """
        Функция, описывающая алгоритм выбора хода компьютером.
        Опирается на статистику игрока:
            Начиная с 2 раунда выбирает победный предмет над предметом, который игрок чаще всего выбирал
            после своего предыдущего выбора.
            
            Например: 
            После камня игрок чаще всего выбирал бумагу, поэтому компьютер выберет ножницы.
            
            В 1 раунде компьютер выбирает ход наугад (при помощи библиотеки random и метода choice).
        """
        
        
        games = data['games']
        # Если данных достаточно (сыгранных игр больше 3), учитывая их выполняем алгоритм поиска наилучшего хода.
        if len(games) > 3:
        # Словари, хранящие о частоте выбора одного предмета после другого.
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
            # Цикл для заполнения словарей по данным из файла profile.json.
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
                else:
                    return random.choice(list(Choice))                
            # Проверка условий выбора и поиск самого частого элемента в определенном словаре.
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
            # Выбор победного предмета, над тем, который чаще всего выбирает игрок (нашли его в верхнем match-case).      
            match pl_often_pick:
                case "PAPER":
                    return Choice.SHEARS
                case "STONE":
                    return Choice.PAPER
                case "SHEARS":
                    return Choice.STONE
        # Если данных недостаточно (сыгранных игр не больше 3), компьютер случайно выбирает предмет.
        else:
            return random.choice(list(Choice))

class User(Player):
    """
    Класс для представления пользователя (человека).
    Наследует абстрактный класс игрока.
    """
    

    def __init__(self, data):
        
        
        self.data = data
        self.username = self.data['username']

    def getPick(self) -> Choice:
        """
        Функция выбора предмета игроком.
        """
        
        
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
        """
        Функция установки нового имени пользователя.
        """
        
        
        new_username = input("Введи желаемое имя пользователя: ")
        self.data['username'] = new_username
        exportData(self.data)
        animatePrint(f"Имя пользователя {new_username} успешно установлено.")
        animatePrint("\nВыходим в меню......")
        

class Game:
    """
    Класс для управления ходом игры и подсчета результатов.
    Сама игра состоит из раундов/раунда.
    """
    
    
    def __init__(self, player, ai, data):
        
        
        self.rounds: List[Round] = []
        self.player = player
        self.ai = ai
        self.data = data

    def start(self, round_count):
        """
        Функция старта игры и контроля над ней.
        """
        
        rounds_pl = 0
        rounds_ai = 0
        result_game = 0
        
        # Цикл для создания раундов и прохождения по ним во время игры.
        for i in range(round_count):
            animatePrint("....Начало нового раунда....\n")
            time.sleep(0.5)
            player_pick = self.player.getPick()
            # Если игра состоит из 1 раунда, алгоритм наилучшего хода для компьютера не запускается.
            if round_count == 1:
                ai_pick = random.choice(list(Choice))
            # Если игра состоит не из 1 раунда, создаем переменную в которую ложим наилучший выбор для компьютера.
            else:
                ai_pick = self.ai.getPick(player_pick, self.data)
            # Проверки условий для вычисления исхода раунда: Победа, поражение, ничья.
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
            # Вспомогательный вывод для пользователя, в зависимости от исхода раунда.
            match round_result.name:
                case "WIN":
                    animatePrint("Вы выиграли в этом раунде.")
                case "DRAW":
                    animatePrint("Ничья в этом раунде.")
                case "LOSE":
                    animatePrint("Вы проиграли в этом раунде.")
            # Создание обьекта класса Round и форматирование данных.
            round = Round(round_result, player_pick, ai_pick)
            round_data = round.to_json()
            self.rounds.append(round_data)
        animatePrint("==== Статистика игры ====\n")
        # Вспомогательный вывод для пользователя, в зависимости от исхода игры.
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
        # Экспорт данных игры и раундов в ней.
        return { 
            "result": result_game.name,
            "rounds": self.rounds
            }
    
class App:

    """
    Основной Класс для управления приложением, включая загрузку данных, вывод статистики и меню выбора действий.
    """
    
    
    def __init__(self):
        
        
        self.loadData()
        self.player = User(self.data)
        self.ai = AiPlayer()

    def loadData(self):
        """
        Функция импорта данных в приложение.
        """
        
        with open("profile.json", "r") as f:
            self.data = json.load(f)

    def startGame(self):
        """
        Функция создания и запуска игры.
        """
        
        
        game = Game(self.player, self.ai, self.data)
        # Меню выбора кол-во раундов в игре.
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
        # Инициализация полученных данных завершившейся игры и обработка их.
        data_game = game.start(answer['count'])
        self.data['games'].append(data_game)
        self.data['count_game'] += 1
        match data_game['result']:
            case "WIN":
                self.data['wins'] += 1
            case "LOSE":
                self.data['loses'] += 1
        # Обновление данных в profile.json  
        exportData(self.data)
        
        self.showCommandMenu()
        
    def resetStat(self):
        """
        Функция сброса profile.json к его стандартному виду.
        """
        
        # Инициализация стандарт вида в виде словаря для перевода в json файл.
        default_data = {
            "username": "None",
            "count_game": 0,
            "wins": 0,
            "loses": 0,
            "pcy": 0,
            "games": []
        }
        
        exportData(default_data)
        f = open("profile.json")
        f.close()
        animatePrint("Статистика была успешно сброшена")
        animatePrint("\nВыходим в меню......")

    def showStat(self):
        """
        Функция просмотра статистики пользователя(Человека).
        """
        
        
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
        """
        Функция отображения вкладки настройки, контроль настроек.
        """
        
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
        """Функция выхода из приложения"""
        animatePrint("Выход")

    def showCommandMenu(self):
        """
        Функция отображения и взаимодействия визуала с методами приложения.
        """
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
    app.showCommandMenu()