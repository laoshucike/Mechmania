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
                        if nextplace_arr[1] == 4:
                            nextplace_arr[1] -= 1 
                        else:
                            nextplace_arr[1] += 1
                    elif nextplace_arr[0] == 4:
                        if nextplace_arr[1] >= 2:
                            nextplace_arr[1] -= 2 
                        else:
                            nextplace_arr[1] += 2
                    else:
                        nextplace_arr[0] = min(nextplace_arr[0] + 2, 4)

                else:
                    if myself.position[0] == 1:
                        nextplace_arr[0] -= 1
                        if nextplace_arr[1] == 0:
                            nextplace_arr[1] += 1 
                        else:
                            nextplace_arr[1] -= 1
                    elif nextplace_arr[0] == 0:
                        if nextplace_arr[1] >= 2:
                            nextplace_arr[1] -= 2 
                        else:
                            nextplace_arr[1] += 2
                    else:
                        nextplace_arr[0] = max(nextplace_arr[0] - 2, 0)
                    '''
                    if nextplace_arr[0] == 1:
                        nextplace_arr[0] -= 1
                        nextplace_arr[1] -= 1
                    elif nextplace_arr[0] == 0:
                        nextplace_arr[1] = max(nextplace_arr[1] - 2, 0)
                    else:
                        nextplace_arr[0] = max(nextplace_arr[0] - 2, 0)
                    '''
            return {
                "Action": "Move",
                "CharacterId": myself.id,
                "Location": nextplace_arr
            }
