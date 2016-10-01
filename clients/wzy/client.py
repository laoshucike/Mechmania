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

# Game map that you can use to query 
gameMap = GameMap()

# global vars
targetpriority = ["Sorcerer", "Enchanter", "Wizard", "Assassin", "Druid", "Archer", "Paladin", "Warrior"]
naima = ["Paladin", "Druid"]

# --------------------------- SET THIS IS UP -------------------------
teamName = "wzy"
# ---------------------------------------------------------------------

# Set initial connection data
def initialResponse():
# ------------------------- CHANGE THESE VALUES -----------------------
    return {'TeamName': teamName,
            'Characters': [
                {"CharacterName": "Druid",
                 "ClassId": "Archer"},
                {"CharacterName": "Archer",
                 "ClassId": "Archer"},
                {"CharacterName": "Warrior",
                 "ClassId": "Archer"},
            ]}
# ---------------------------------------------------------------------

def archer_func(myself, enemy, enemys, ally):

    global targetpriority, naima


#    outofsight = True;
    if enemy.in_range_of(myself, gameMap):
        outofsight = False

    sumX = 0
    sumY = 0
    for oneenemy in enemys:
        sumX += oneenemy.position[0]
        sumY += enemy.position[1]
    averX = (int)(sumX/3)
    averY = (int)(sumY/3)

    if myself.attributes.health > myself.attributes.maxHealth * 0.5:  # higher than 0.5 * maxhealth , fight!!!!!
        target = None
        if myself.in_range_of(enemy, gameMap):  #fight or cast
                target = enemy
        if target != None:
            if myself.casting is None:              #cast
                cast = False
                for abilityId, cooldown in myself.abilities.items():
                    # Do I have an ability not on cooldown
                    if cooldown == 0 and int(abilityId) == 2:
                        # If I can, then cast it
                        ability = game_consts.abilitiesList[int(abilityId)]
                        # Get ability
                        return {
                            "Action": "Cast",
                            "CharacterId": myself.id,
                            # Am I buffing or debuffing? If buffing, target myself
                            "TargetId": target.id if ability["StatChanges"][0]["Change"] < 0 else myself.id,
                            "AbilityId": int(abilityId)
                        }
                        cast = True
                        break

                if not cast:                  # Was I able to cast something? Either wise attack
                    return {
                        "Action": "Attack",
                        "CharacterId": myself.id,
                        "TargetId": target.id,
                    }

        else:       #move to enemy
            return{
                "Action": "Move",
                "CharacterId": myself.id,
                "TargetId": enemy.id,
            }
    
    else:                                                               #blood < 0.5
        if myself.attributes.stunned == -1 or myself.attributes.rooted == -1:
            if myself.abilities[0] == 0:       #burst - break crowd control with a long cooldown
                return {
                    "Action": "Cast",
                    "CharacterId": myself.id,

                    "TargetId": myself.id,
                    "AbilityId": int(0)
                }
            else :                          #whatever
                return {
                    "Action": "Move",
                    "CharacterId": myself.id,
                    "TargetId": ally[0].id,
                }
        elif myself.abilities[12] == 0:
                return {
                    "Action": "Cast",
                    "CharacterId": myself.id,

                    "TargetId": myself.id,
                    "AbilityId": int(12)
                }
        else:                                #run!!!!!!!!!!!
            '''
            if (ally[0].classId in naima):          #run to naima
                if ally[0].position == myself.position:     #fight with naima
                    if myself.in_range_of(enemy, gameMap):
                        return {
                            "Action": "Attack",
                            "CharacterId": myself.id,
                            "TargetId": target.id,
                        }
                    else:                               #stay
                        return {
                            "Action": "Move",
                            "CharacterId": myself.id,
                            "TargetId": ally[0].id,
                        }
                else:                                   #move to naima
                    return {
                        "Action": "Move",
                        "CharacterId": myself.id,
                        "TargetId": ally[0].id,
                    }

            if (ally[1].classId in naima):          #run to naima
                if ally[1].position == myself.position:     #fight with naima
                    if myself.in_range_of(enemy, gameMap):
                        return {
                        "Action": "Attack",
                        "CharacterId": myself.id,
                        "TargetId": target.id,
                        }
                    else:                               #stay
                        return {
                            "Action": "Move",
                            "CharacterId": myself.id,
                            "TargetId": ally[1].id,
                        }
                else:                                   #move to naima
                    return {
                        "Action": "Move",
                        "CharacterId": myself.id,
                        "TargetId": ally[1].id,
                    }

            if (ally[2].classId in naima):          #run to naima
                if ally[2].position == myself.position:     #fight with naima
                    if myself.in_range_of(enemy, gameMap):
                        return {
                            "Action": "Attack",
                            "CharacterId": myself.id,
                            "TargetId": target.id,
                        }
                    else:                               #stay
                        return {
                            "Action": "Move",
                            "CharacterId": myself.id,
                            "TargetId": ally[2].id,
                        }
                else:                                   #move to naima
                    return {
                        "Action": "Move",
                        "CharacterId": myself.id,
                        "TargetId": ally[2].id,
                    }
            
            '''
            nextplace = copy.deepcopy(myself.position)  #no naima

            nextplace_arr = list(nextplace)

            speed = myself.attributes.movementSpeed
            if speed == 1:                                      #speed 1

                if averX < nextplace_arr[0] and averY < nextplace_arr[1]:
                    if nextplace_arr[0] == 4 and nextplace_arr[1] == 4:
                        if myself.in_range_of(enemy, gameMap):
                            return {
                                "Action": "Attack",
                                "CharacterId": myself.id,
                                "TargetId": enemy.id,
                            }
                        else:
                            return {
                                "Action": "Move",
                                "CharacterId": myself.id,
                                "Location": nextplace_arr
                            }
                    elif nextplace_arr[0] == 4:
                        nextplace_arr[1] = nextplace_arr[1] + 1

                    else:
                        nextplace_arr[0] = nextplace_arr[0] + 1
                        if ((nextplace_arr[0] == 3 and nextplace_arr[1] == 1) or (nextplace_arr[0] == 1 and nextplace_arr[1] == 3) or (nextplace_arr[0] == 3 and nextplace_arr[1] == 3) or (nextplace_arr[0] == 1 and nextplace_arr[1] == 1)):
                            nextplace_arr[0] -= 1
                            nextplace_arr[1] = nextplace_arr[1] + 1


                elif averX < nextplace_arr[0] and averY > nextplace_arr[1]:
                    if nextplace_arr[0] == 4 and nextplace_arr[1] == 0:
                        if myself.in_range_of(enemy, gameMap):
                            return {
                                "Action": "Attack",
                                "CharacterId": myself.id,
                                "TargetId": enemy.id,
                            }
                        else:
                            return {
                                "Action": "Move",
                                "CharacterId": myself.id,
                                "Location": nextplace_arr
                            }
                    elif nextplace_arr[0] == 4:
                        nextplace_arr[1] = nextplace_arr[1] - 1
                    else:
                        nextplace_arr[0] = nextplace_arr[0] + 1
                        if ((nextplace_arr[0] == 3 and nextplace_arr[1] == 1) or (nextplace_arr[0] == 1 and nextplace_arr[1] == 3) or (nextplace_arr[0] == 3 and nextplace_arr[1] == 3) or (nextplace_arr[0] == 1 and nextplace_arr[1] == 1)):
                            nextplace_arr[0] -= 1
                            nextplace_arr[1] = nextplace_arr[1] - 1

                elif averX > nextplace_arr[0] and averY < nextplace_arr[1]:
                    if nextplace_arr[0] == 0 and nextplace_arr[1] == 4:
                        if myself.in_range_of(enemy, gameMap):
                            return {
                                "Action": "Attack",
                                "CharacterId": myself.id,
                                "TargetId": enemy.id,
                            }
                        else:
                            return {
                                "Action": "Move",
                                "CharacterId": myself.id,
                                "Location": nextplace_arr
                            }
                    elif nextplace_arr[0] == 0:
                        nextplace_arr[1] = nextplace_arr[1] + 1
                    else:
                        nextplace_arr[0] = nextplace_arr[0] - 1
                        if ((nextplace_arr[0] == 3 and nextplace_arr[1] == 1) or (nextplace_arr[0] == 1 and nextplace_arr[1] == 3) or (nextplace_arr[0] == 3 and nextplace_arr[1] == 3) or (nextplace_arr[0] == 1 and nextplace_arr[1] == 1)):
                            nextplace_arr[0] += 1
                            nextplace_arr[1] = nextplace_arr[1] + 1

                else:
                    if nextplace_arr[0] == 0 and nextplace_arr[1] == 0:
                        if myself.in_range_of(enemy, gameMap):
                            return {
                                "Action": "Attack",
                                "CharacterId": myself.id,
                                "TargetId": enemy.id,
                            }
                        else:
                            return {
                                "Action": "Move",
                                "CharacterId": myself.id,
                                "Location": nextplace_arr
                            }
                    elif nextplace_arr[0] == 0:
                        nextplace_arr[1] = nextplace_arr[1] - 1
                    else:
                        nextplace_arr[0] = nextplace_arr[0] - 1
                        if ((nextplace_arr[0] == 3 and nextplace_arr[1] == 1) or (nextplace_arr[0] == 1 and nextplace_arr[1] == 3) or (nextplace_arr[0] == 3 and nextplace_arr[1] == 3) or (nextplace_arr[0] == 1 and nextplace_arr[1] == 1)):
                            nextplace_arr[0] += 1
                            nextplace_arr[1] = nextplace_arr[1] - 1

            else:                       #speed 2
                if averX < myself.position[0]:
                    if myself.position[0] == 3:
                        nextplace_arr[0] += 1
                        nextplace_arr[1] += 1
                    elif nextplace_arr[0] == 4:
                        nextplace_arr[1] = min(nextplace_arr[1] + 2, 4)
                    else:
                        nextplace_arr[0] = min(nextplace_arr[0] + 2, 4)

                else:
                    if nextplace_arr[0] == 1:
                        nextplace_arr[0] -= 1
                        nextplace_arr[1] -= 1
                    elif nextplace_arr[0] == 0:
                        nextplace_arr[1] = max(nextplace_arr[1] - 2, 0)
                    else:
                        nextplace_arr[0] = max(nextplace_arr[0] - 2, 0)
            return {
                "Action": "Move",
                "CharacterId": myself.id,
                "Location": nextplace_arr
            }
            print "doomed"

# Determine actions to take on a given turn, given the server response
def processTurn(serverResponse):

# --------------------------- CHANGE THIS SECTION -------------------------
    # Setup helper variables
    actions = []
    myteam = []
    enemyteam = []
    # Find each team and serialize the objects
    for team in serverResponse["Teams"]:
        if team["Id"] == serverResponse["PlayerInfo"]["TeamId"]:
            for characterJson in team["Characters"]:
                character = Character()
                character.serialize(characterJson)
                myteam.append(character)
        else:
            for characterJson in team["Characters"]:
                character = Character()
                character.serialize(characterJson)
                enemyteam.append(character)


# ------------------ You shouldn't change above but you can ---------------
    #if (targetpriority.index(enemyteam[0]) > targetpriority.index(enemyteam[1])):
    #    enemyteam[1], enemyteam[0] = enemyteam[y], enemyteam[x]

#    print map(lambda en: en.classId, enemyteam)
    enemyteam = sorted(enemyteam, key=lambda en: targetpriority.index(en.classId))
#    print map(lambda en: en.classId, enemyteam)

    # Choose a target
    target = None
    for character in enemyteam:
        if not character.is_dead():
            target = character
            break

    # If we found a target
    if target:
        for character in myteam:
            if (character.classId == "Archer"):
                action = archer_func(character, target, enemyteam, myteam)
                if action is None:
                    print "hahh no action returned"
                actions.append(action)
            else: 
            # If I am in range, either move towards target
                if character.in_range_of(target, gameMap):
                    # Am I already trying to cast something?
                    if character.casting is None:
                        cast = False
                        for abilityId, cooldown in character.abilities.items():
                            # Do I have an ability not on cooldown
                            if cooldown == 0:
                                # sIf I can, then cast it
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
