import json

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


with open("profile.json", 'r') as f:
    games = json.load(f)['games']

print(json.dumps(games, indent=4))

for game in games:
    rounds = game['rounds']
    if len(rounds) > 1:
        for i in range(1, len(rounds)):
            last_pl_pick = rounds[i - 1]['player_pick']
            pl_pick = rounds[i]['player_pick']
            match last_pl_pick:
                case "PAPER":
                    after_paper[pl_pick] += 1
                case "STONE":
                    after_stone[pl_pick] += 1
                case "SHEARS":
                    after_shears[pl_pick] += 1
                    
print(max(after_stone, key=after_stone.get))
        


