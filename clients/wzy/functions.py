def archer_func(myself, enemy, enemys):

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
        if myself.in_range_of(enemy, gameMap):
                target = enemy

        if target != None:
            return {
                "Action": "Attack",
                "CharacterId": myself.id,
                "TargetId": target.id,
            }

        else:
            return{
                "Action": "Move",
                "CharacterId": myself.id,
                "TargetId": enemy.id,
            }
    
    else:

        if myself.attributes.stunned == -1 or myself.attributes.rooted == -1:
            if myself.abilities[0] == 0:       #burst - break crowd control with a long cooldown

                return {
                    "Action": "Cast",
                    "CharacterId": myself.id,

                    "TargetId": myself.id,
                    "AbilityId": 0
                }
        elif myself.abilities[2] == 0:
                return {
                    "Action": "Cast",
                    "CharacterId": myself.id,

                    "TargetId": myself.id,
                    "AbilityId": 2
                }
        else:       #run!!!!!!!!!!!


            nextplace = copy.deepcopy(myself.position)

            nextplace_arr = list(nextplace)

            speed = myself.attributes.movementSpeed
            if speed == 1:

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

            else:
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
#            print nextplace_arr[0]
#            print nextplace_arr[1]

            return {
                "Action": "Move",
                "CharacterId": myself.id,
                "Location": nextplace_arr
            }
