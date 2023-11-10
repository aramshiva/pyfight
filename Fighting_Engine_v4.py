"""
Fighting_Engine_v4
AUTHOR: ARAM SHIVA (aram.sh)
DESCRIPTION: A text based fighting engine.
REQUIREMENTS: pygame 1.9.2
USAGE: fight(monstertable, paramaters)
AVALIABLE PARAMATERS:
--cancorrupt - Allows a low chance for monster's to corrupt and do more damage. - Recommended
--showmenu - Shows a menu that can allow people to play and view stats. WIP - Not Recommended
--nomoods - Disables monsters having moods - Not Recommended
--oneweapon - Disables weapons module to have one static weapon. - Not Recommended

TODO:
Balance gameplay mechanics: Adjust damage calculations and monster stats to ensure fair gameplay and avoid situations where fights become too easy or too difficult.
"""
# Importing Python Modules
import copy
import random
import sys
import pygame
import base64
import json
pygame.init()

# Defining Styling
def bold(message):
    bold = {
    'A': '𝗔', 'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚', 'H': '𝗛', 'I': '𝗜', 'J': '𝗝', 'K': '𝗞', 'L': '𝗟',
    'M': '𝗠', 'N': '𝗡', 'O': '𝗢', 'P': '𝗣', 'Q': '𝗤', 'R': '𝗥', 'S': '𝗦', 'T': '𝗧', 'U': '𝗨', 'V': '𝗩', 'W': '𝗪', 'X': '𝗫', 'Y': '𝗬', 'Z': '𝗭',
    'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳', 'g': '𝗴', 'h': '𝗵', 'i': '𝗶', 'j': '𝗷', 'k': '𝗸', 'l': '𝗹',
    'm': '𝗺', 'n': '𝗻', 'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿', 's': '𝘀', 't': '𝘁', 'u': '𝘂', 'v': '𝘃', 'w': '𝘄', 'x': '𝘅', 'y': '𝘆', 'z': '𝘇',
    '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'
    }
    result=""
    for char in message:
        if char in bold: result += bold[char]
        else: result += char
    return result
def boldprint(message):
    print(bold(message))
def boldinput(message):
    input(bold(message))

# Lists and Dictonaries
YourStats = {"damage": 5, "health": 50} # Declares Player Stats
monstertable = [ 
    {"name":"Monster #1", "attack":"punches you!", "health":50, "damage":5, "weight":10},
    {"name":"Monster #2", "attack":"kicks you!", "health":50, "damage":5, "weight":10},
    {"name":"Monster #3", "attack":"fights you!", "health":50, "damage":5, "weight":10}
    # Name Of Monster      Monster Attack          Health       Damage      Weight
] # Table of Monsters
moves = ["FIGHT", "FRIEND"] # Avaliable Moves
weapons = [
    {"name":"Maple Sword", "multiplier":0.2},
    {"name":"Flaming Blade", "multiplier":3},
] # Weapons you can use. Damage is a multiplier on your base damage
mood = [
    {"name":"calm", "multiplier":0.3},
    {"name":"Annoyed", "multiplier":1},
    {"name":"ANGRY", "multiplier":1.1},
    {"name":"FURIOUS", "multiplier":1.2},
    {"name":"INFURIATED", "multiplier":1.4},
    {"name":"ENRAGED", "multiplier":1.5},
    {"name":"INFLAMED", "multiplier":1.75},
    {"name":"FUMING", "multiplier":2},
]

# Functions
def clearscreen(): print("\n" * 500)
def menu():
    global moves,monstertable,moves,YourStats
    while True:
        clearscreen()
        homeselector = input("\n\n\n\nPLAY\nVIEW STATS\nSAVE GAME\nLOAD SAVE\nEnter the option you would like to go to!")
        if homeselector == "PLAY": break
        elif homeselector == "SAVE GAME":
            clearscreen()
            save = []
            save += [weapons]
            save += [moves]
            save += [monstertable]
            save += [YourStats]
            print(bold("This is your save slot, save it to play later.\n") + str(base64.b64encode(json.dumps(save).encode('utf-8'))))
        elif homeselector == "LOAD SAVE":
            clearscreen()
            save = list(json.loads(base64.b64decode(input("Please enter your save slot:")).decode('utf-8')))
            weapon = save[0]
            moves = save[1]
            monstertable = save[2]
            YourStats = save[3]
            print("LOADED SAVE SLOT!")
        input("Press ENTER to continue")
def monsterfinder(monstertable): # Adds weight to randomness on monstertable
    monster = copy.deepcopy(random.choice(monstertable))
    tweight = 0
    for monster in monstertable: tweight += monster["weight"]
    rtweight = random.randint(0, tweight)
    tweight = 0
    for monster in monstertable:
        tweight += monster["weight"]
        if rtweight < tweight: return copy.deepcopy(monster)
def fight(monstertable, param): # Pass Monster Table and runs fighting script and passes params
    if "--showmenu" in param: menu()
    print(YourStats)
    lastusedweapon = {"name":""}
    clearscreen()
    monster = monsterfinder(monstertable)
    if "--cancorrupt" in param:
        Corrupted = False
        if random.randint(1, 10) == 1:
            Corrupted = True
            boldprint("CORRUPTED!\nCorrupted mobs do more damage!\n")
            monster["name"] = bold("CORRUPTED " + (monster["name"].upper()))
            monster["damage"] *= random.randint(2, 3)
    print("You stumbled upon a " + monster["name"] + "!")
    print("They have " + str(monster["health"]) + " health and " + str(monster["damage"]) + " damage!")
    Fight = True
    Turn = True
    while Fight: # Fight Loop
        if Turn:
            usedweapon = False
            print("Its your turn to go!")
            print()
            print("You have multiple moves avaliable")
            for avmove in moves: print(avmove)
            move = input("What is your move?")
            if move == "FIGHT" and move in moves: # Fight Move
                if "--oneweapon" not in param:
                    if lastusedweapon["name"] != "":
                        if input("Do you want to reuse " + weapon["name"] + "?\ny/n") == "y":
                            damagedone = copy.deepcopy(YourStats["damage"]) * weapon["multiplier"]
                            monster["health"] -= damagedone
                            usedweapon = True
                            print("You attack with " + weapon["name"] + " dealing " + str(damagedone) + " damage to " + monster["name"] + "\n" + monster["name"] + " is now at " + str(monster["health"]) + " health remaining")
                        else: pass
                    if not usedweapon:
                        clearscreen()
                        print("You can use any of the following weapons: ")
                        for weapon in weapons: print(weapon["name"])
                        weaponmove = input("\nWhat do you want to attack with?")
                        clearscreen()
                        for weapon in weapons:
                            if weaponmove == weapon["name"]:
                                lastusedweapon = weapon
                                damagedone = copy.deepcopy(YourStats["damage"]) * weapon["multiplier"]
                                monster["health"] -= damagedone
                                print("You attack with " + weapon["name"] + " dealing " + str(damagedone) + " damage to " + monster["name"] + "\n" + monster["name"] + " is now at " + str(monster["health"]) + " health remaining")
                else:
                    damagedone = YourStats["damage"]
                    monster["health"] -= damagedone
                    print("You attack dealing " + str(damagedone) + " damage to " + monster["name"] + "\n" + monster["name"] + " is now at " + str(monster["health"]) + " health remaining")
            elif move == "FRIEND" and move in moves:
                clearscreen()
                if random.randint(1, 10) == 1:
                    print("VICTORY!\nYou tamed " + monster["name"] + "!")
                    monster["health"] = 0
                    break
                else: print("It doesn't work and it is apparent that you have wasted a move")
            else:
                clearscreen()
                raise Expection(("\n" * 300) + "𝗘𝗥𝗥𝗢𝗥!\n\nMove Type Not Recongnized!")
                sys.exit()
            pygame.time.wait(2000)
            Turn = False
        if monster["health"] <= 0:
            clearscreen()
            print(random.choice(["VICTORY!", "WINNER!", "YOU WON!", "YA WON!"]) + "\n\n\tGood Job!")
            pygame.time.wait(1000)
            clearscreen()
            Fight = False
        else:
            clearscreen()
            if "--nomoods" in param: angrylevel = {"name":"", "multiplier":1}
            else: angrylevel = copy.deepcopy(random.choice(mood)) # Picks a random mood.
            monsterattack = monster["damage"] * angrylevel["multiplier"]
            YourStats["health"] -= monsterattack
            print("\n" + monster["name"] + " " + monster["attack"])
            print(angrylevel["name"] + " " + monster["name"] + " does " + str(monsterattack) + " damage\n\tYou are left at " + str(YourStats["health"]) + " health")
            pygame.time.wait(2000)
            clearscreen()
            print("\n\n\n\n\n\n")
            print(monster["name"] + " has " + str(monster["health"]) + " health and " + str(monster["damage"]) + " damage!")
            Turn = True
        if YourStats["health"] <= 0:
            clearscreen()
            raise Exception(("\n" * 500) + random.choice(["You died", "Ya Died", "Arr Matey looks like your dead!", "EEK! YOU DIED!"]) + "\n\nThanks for playing!")
# Code    
fight(monstertable, "--cancorrupt --showmenu")
