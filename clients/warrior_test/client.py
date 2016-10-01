#!/usr/bin/python2
import socket
import json
import os
import random
import sys
from socket import error as SocketError
import errno
sys.path.append("../..")
import src.game.game_constants as game_consts
from src.game.character import *
from src.game.gamemap import *

targetpriority = ["Sorcerer", "Enchanter", "Wizard", "Assassin", "Druid", "Archer", "Paladin", "Warrior"]
naima = ["Paladin", "Druid"]
HP = [0,0,0,0,0,0]
hurt = [False, False, False, False,False,False]
# Game map that you can use to query 
gameMap = GameMap()

# --------------------------- SET THIS IS UP -------------------------
teamName = "yongshi"
# ---------------------------------------------------------------------

'''
myself -- character obj

'''


def warrier_function(myself, enemylist):
    action = None
    lowestHP = 2000
    enemy = None
    for target in enemylist:
        if target.is_dead():
            continue
        if HP[int(target.id) - 1] < lowestHP:
            lowestHP = HP[int(target.id) - 1]
            enemy = target
    
    if myself.in_range_of(enemy, gameMap):
        if myself.casting is None:
            cast = False
            for abilityId, cooldown in myself.abilities.items():
                if cooldown == 0 and abilityId == 1:
                    ability = game_consts.abilitiesList[int(abilityId)]
                    action = {
                        "Action" : "Cast",
                        "CharacterId":myself.id,
                        "TargetId":enemy.id if ability["StatChanges"][0]["Change"] < 0 else myself.id,
                        "AbilityId":1                            
                    }
                    cast = True
                    break
                if hurt[int(myself.id -1)] == True and cooldown == 0 and abilityId == 15:
                    ability = game_consts.abilitiesList[int(abilityId)]

                    action = {
                               "Action" : "Cast",
                               "CharacterId":myself.id,
                               "TargetId":enemy.id if ability["StatChanges"][0]["Change"] < 0 else myself.id,
                               "AbilityId":15                            
                           }
                    cast = True
                    break
            if not cast:
                action = {
                    "Action": "Attack",
                    "CharacterId": myself.id,
                    "TargetId": enemy.id,
                }
    else: # Not in range, move towards
        action = {
            "Action": "Move",
            "CharacterId": myself.id,
            "TargetId": enemy.id,
        }
    return action




# Set initial connection data
def initialResponse():
# ------------------------- CHANGE THESE VALUES -----------------------
    return {'TeamName': teamName,
            'Characters': [
                {"CharacterName": "W1",
                 "ClassId": "Warrior"},
                {"CharacterName": "W2",
                 "ClassId": "Warrior"},
                {"CharacterName": "W3",
                 "ClassId": "Warrior"},
            ]}
# ---------------------------------------------------------------------

# Determine actions to take on a given turn, given the server response
def processTurn(serverResponse):
# --------------------------- CHANGE THIS SECTION -------------------------
    # Setup helper variables
    actions = []
    myteam = []
    enemyteam = []
    # Find each team and serialize the objects
    for team in serverResponse["Teams"]:

        i = 0
        if team["Id"] == serverResponse["PlayerInfo"]["TeamId"]:
            for characterJson in team["Characters"]:
                character = Character()
                character.serialize(characterJson)
                myteam.append(character)
                if HP[int(team["Characters"][i]["Id"]) - 1] > int(team["Characters"][i]["Attributes"]["Health"]):
                    hurt[int(team["Characters"][i]["Id"] - 1)] = True
                else: 
                    hurt[int(team["Characters"][i]["Id"] - 1)] = False
                HP[int(team["Characters"][i]["Id"]) -1] = int(team["Characters"][i]["Attributes"]["Health"])

                i+=1

        else:
            for characterJson in team["Characters"]:
                character = Character()
                character.serialize(characterJson)
                enemyteam.append(character)
                if HP[int(team["Characters"][i]["Id"]) -1] > int(team["Characters"][i]["Attributes"]["Health"]):
                    hurt[int(team["Characters"][i]["Id"])-1] = True
                else: 
                    hurt[int(team["Characters"][i]["Id"])-1] = False
                HP[int(team["Characters"][i]["Id"]) - 1] = int(team["Characters"][i]["Attributes"]["Health"])

                i+=1
# ------------------ You shouldn't change above but you can ---------------

    # Choose a target
    target = None
    for character in enemyteam:
        if not character.is_dead():
            target = character
            break

    # If we found a target
    if target:
        #print myteam
        for character in myteam:
            if character.classId == 'Warrior':
                action = warrier_function(character, enemyteam)
                if not action == None:
                    actions.append(action)
            # If I am in range, either move towards target
            if character.in_range_of(target, gameMap):
                # Am I already trying to cast something?
                if character.casting is None:
                    cast = False
                    for abilityId, cooldown in character.abilities.items():
                        # Do I have an ability not on cooldown
                        if cooldown == 0:
                            # If I can, then cast it
                            ability = game_consts.abilitiesList[int(abilityId)]
                            # Get ability
                            actions.append({
                                "Action": "Cast",
                                "CharacterId": character.id,
                                # Am I buffing or debuffing? If buffing, target myself
                                "TargetId": target.id if ability["StatChanges"][0]["Change"] < 0 else character.id,
                                "AbilityId": int(abilityId)
                            })
                            cast = True
                            break
                    # Was I able to cast something? Either wise attack
                    if not cast:
                        actions.append({
                            "Action": "Attack",
                            "CharacterId": character.id,
                            "TargetId": target.id,
                        })
            else: # Not in range, move towards
                actions.append({
                    "Action": "Move",
                    "CharacterId": character.id,
                    "TargetId": target.id,
                })

    # Send actions to the server
    return {
        'TeamName': teamName,
        'Actions': actions
    }
# ---------------------------------------------------------------------

# Main method
# @competitors DO NOT MODIFY
if __name__ == "__main__":
    # Config
    conn = ('localhost', 1337)
    if len(sys.argv) > 2:
        conn = (sys.argv[1], int(sys.argv[2]))

    # Handshake
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(conn)

    # Initial connection
    s.sendall(json.dumps(initialResponse()) + '\n')

    # Initialize test client
    game_running = True
    members = None

    # Run game
    try:
        data = s.recv(1024)
        while len(data) > 0 and game_running:
            value = None
            if "\n" in data:
                data = data.split('\n')
                if len(data) > 1 and data[1] != "":
                    data = data[1]
                    data += s.recv(1024)
                else:
                    value = json.loads(data[0])

                    # Check game status
                    if 'winner' in value:
                        game_running = False

                    # Send next turn (if appropriate)
                    else:
                        msg = processTurn(value) if "PlayerInfo" in value else initialResponse()
                        s.sendall(json.dumps(msg) + '\n')
                        data = s.recv(1024)
            else:
                data += s.recv(1024)
    except SocketError as e:
        if e.errno != errno.ECONNRESET:
            raise  # Not error we are looking for
        pass  # Handle error here.
    s.close()
