#  CPS 300 (Python Programming): HW 5
#  Shuchi Wu
#  
#  This file contains the beginning of a program to simulate turns 
#  in the dice game Yahtzee.

from random import *

#
#  displayDice (dice)
#
#  The list dice contains the results of most recent roll of the dice.
#
#  The function displayDie prints out the number rolled for each individual die.
#
#  In the future, this function could be replaced with a more visual
#  representation of dice.
#

def displayDice (dice):
    for i in range(len(dice)):
        print (dice[i],end=" ")
    print ("\n")

#
#  The list dice contains the results of most recent roll of the dice.
#
#  This function simulates a possible reroll of the dice: the user is prompted
#  for which dice should be kept and which should be re-rolled.
#
#  This function makes use of the function yesOrNo, which must be written.
#

def reroll (dice):
    for i in range(len(dice)):
        ans = yesOrNo ("Keeping die #{0} (value: {1})? (Y/N) ".format(i,dice[i]))
        if (ans != True):
            dice[i] = rollOneDie()

#  rollAllDice (dice)
#
#  This function simulates the rolling portion of a turn, returning
#  the final values in the list dice.
#
#  Initially, all dice are rolled.  The results are displayed, and
#  the user is given the option to re-roll at most twice (for a total
#  of three rolls).
#
#  This function makes use of the functions yesOrNo and reroll, both 
#  of which must be written.

def rollAllDice (dice):
    for i in range(len(dice)):
        dice[i] = rollOneDie()

    print("\nYour roll: ")
    displayDice(dice) 

 
   # Can re-roll at most twice */
    if yesOrNo("Do you want to re-roll? (Y/N) "):
        reroll(dice)
        print("\nYour roll: ")
        displayDice(dice)
 
        if yesOrNo("Do you want to re-roll? (Y/N) "):
            reroll(dice)
            print("\nYour roll: ")

#############################################################################
#  Function definitions from Lab 14

# Part 1: rollOneDie

def rollOneDie ():
    return randint(1,6)

# Part 2: yesOrNo

def yesOrNo (prompt):
    ch = input (prompt)
    resp = (ch != "" and ch[0].lower() == 'y')
    return resp

# Part 3: countUp

def countUp (val, dice):
    return dice.count(val)

# Part 4: displayPoints

def displayPoints (str,pts):
    print ("Points for",str+":",pts)
    
# Part 5: upperSection

def upperSection (val,freq):
    return freq[val]*val

#############################################################################
# Functions for Homework 5

# Function 1: Returns the number of points that freq allows for three of a kind 
#   (i.e., either 0 or the total of the dice).
# Originally I wrote a helper function for Function 1 and 2 to calculate the
#   total points. But it has a nested for-loop when threeOfAkind or fourOfAKind.
# I'd like to avoid nested for-loop, so I changed my design that only loops
#   one time and does checking and calculating at the same time.

def threeOfAKind (freq):
    points = 0
    # Total points could get
    threeFlag = False
    # Flag keeps tracking of threeOfAKind  
    for index in range (7):
        # index of freq is 0 to 6
        points += upperSection (index, freq)
        # Go through the freq list and accumulate total points
        if freq[index] >= 3:
        	# Note: fourOfAKind and yahtzee are also threeOfAKind
            threeFlag = True
        # Update the flag of threeOfAKind
    if threeFlag:
        return points
    else:
        return 0

# Function 2: Returns the number of points that freq allows for four of a kind 
#   (i.e., either 0 or the total of the dice).
# This function designs in the same way of threeOfAKind.

def fourOfAKind (freq):
    points = 0
    # Total points could get
    fourFlag = False
    # Flag keeps tracking of fourOfAKind  
    for index in range (7):
        # index of freq is 0 to 6
        points += upperSection (index, freq)
        # Go through the freq list and accumulate total points
        if freq[index] >= 4:
        	# Note: yahtzee is also fourOfAKind
            fourFlag = True
        # Update the flag of threeOfAKind
    if fourFlag:
        return points
    else:
        return 0

# Function 3: Returns the number of points that freq allows for a full house
#   (i.e., either 0 or 25).
#   This design only maps the freq one time, which keeps [2,3] [3,2] [2,2] and [5],
#   and in the end use if-condition to kick out [2,2].

def fullHouse (freq):
    fullHouseFlag = []
    # Flag list to collect freq count that equals 2,3 and 5
    for count in freq:
        if count == 3 or count == 2 or count == 5:
            fullHouseFlag.append(count)
            # Push into fullHouseFlag when count qualifies
    if fullHouseFlag == [2,3] or fullHouseFlag == [3,2] or fullHouseFlag == [5]:
        # Note: this method kicks out the situation of [2,2]
        return 25
    else:
        return 0

# Function 4: Returns the number of points that freq allows for a small straight
#   (i.e., either 0 or 30).
# The design idea is: small straight only has three situations: 1,2,3,4; 2,3,4,5;
#   and 3,4,5,6, which means the counts on these indexes are not zero.
#   So we just need to check if the freq list hits any of these three situations.

def smallStraight (freq):
    for index in [1,2,3]:
        if freq[index] != 0 and freq[index + 1] != 0 and freq[index + 2] !=0\
        and freq[index + 3] !=0: # This line is too long, so breaked.
            return 30
    return 0

# Funtion 5: Returns the number of points that freq allows for a large straight 
#   (i.e., either 0 or 40).
# Large straight only has two possibilities: 1,2,3,4,5 or 2,3,4,5,6.
#   which means freq is [0,1,1,1,1,1,0] or [0,0,1,1,1,1,1].

def largeStraight (freq):
    if freq[1:] == [1,1,1,1,1,0] or freq[1:] == [0,1,1,1,1,1]:
        return 40
    else:
        return 0

# Function 6: Returns the number of points that freq allows for chance 
#   (i.e., total of all dice).
# Calculate the total points directly.
# Indeed this function can be used as helper function in Function 1 and 2,
#   but I choose not to do so to avoid nested for-loops.

def chance (freq):
    points = 0
    for index in range (7):
        # index of freq is 0 to 6
        points += upperSection (index, freq)
    return points

# Function 7: Returns the number of points that freq allows for yahtzee
#   (i.e., 0 or 50).
# Yahtzee only needs to check if there is 5 in freq list.

def yahtzee (freq):
    if 5 in freq:
        return 50
    else:
        return 0

# This is a helper function for Function 8 and Function 9 below,
#   which calculate points of all seven functions (from threeOfAKind to yahtzee),
#   and return a points list. The max point must be in this list.

def sevenFunctions (freq):
    pointsList = []
    pointsList.append(threeOfAKind(freq))
    pointsList.append(fourOfAKind(freq))
    pointsList.append(fullHouse(freq))
    pointsList.append(smallStraight(freq))
    pointsList.append(largeStraight(freq))
    pointsList.append(chance(freq))
    pointsList.append(yahtzee(freq))
    return pointsList

# Function 8: Returns the maximum number of points that can be received for freq
# This function will call the helper function: sevenFunctions to biggest points.

def maximizePoints (freq):
    maxPoints = 0
    pointsList = sevenFunctions (freq)
    for point in pointsList:
        if point > maxPoints:
            maxPoints = point
    return maxPoints

# Function 9: Returns the name of strategy corresponds to the maximizePoints.
# Since the helper function: sevenFunctions returns a list of points and the sequence
#    is fixed: threeOfAKind, fhourOfAKind, fullHouse, smallStraight, largeStraight
#    chance and yahtzee. I will ultilize this list to print names of strategy 
#    corresponds to the maximizePoints.

def maxCategories (freq):
    maxPoints = maximizePoints (freq)
    pointsList = sevenFunctions (freq)
    nameList = ["Three of a kind", "Four of a kind", "Full house", "Small straight",\
        "Large straight", "Chance", "Yahtzee"] # This line is too long, so breaked.
    # Note: the nameList and pointsList have the same sequence so can share index    
    print ("Maximum points can be received from these categories:")
    for index in range(len(pointsList)):
       if pointsList[index] == maxPoints:
           print (nameList[index])

#############################################################################
#  main -- the heart of the program 
#
#  There are two arrays here:
#
#      dice[5], which contains the results of a turn's dice roll
#         (e.g., each dice[i] is the roll of a separate die)
#
#      freq[7]: indicates how many dice came up with a given value
#          freq[1] is the number of ones rolled
#          freq[2] is the number of twos rolled
#               etc.
#
#      Example: Suppose the dice rolled were  5 3 6 6 2
#          dice[0] = 5   dice[1] = 3   dice[2] = 6   etc
#
#          freq[1] = freq[4] = 0   freq[5] = freq[3] = freq[2] = 1
#          freq[6] = 2

def main ():
    dice = [0]*5    # dice[i] is the value on die #i
    freq = [0]*7    # freq[v] is how many dice came up with value v
    
    # set seed if you want reproducible dice rolls
    #    (keep next line commented out if you don't)
    # seed (12345678)


    # roll each of the dice exactly once
    rollAllDice (dice)

    # display the results of the rolls
    displayDice (dice)

    # get the frequencies
    for i in range(1,7):
        freq[i] = countUp(i,dice);
        
    # Calculate the points for the upper section of the scorecard
    displayPoints ("Aces/Ones", upperSection (1,freq))
    displayPoints ("Deuces/Twos", upperSection (2,freq))
    displayPoints ("Threes", upperSection (3,freq))
    displayPoints ("Fours", upperSection (4,freq))
    displayPoints ("Fives", upperSection (5,freq))
    displayPoints ("Sixes", upperSection (6,freq))

    # Calculate the points for the upper section of the scorecard
    displayPoints ("Three of a Kind", threeOfAKind(freq))
    displayPoints ("Four of a Kind", fourOfAKind(freq))
    displayPoints ("Full House", fullHouse(freq))
    displayPoints ("Small Straight", smallStraight(freq))
    displayPoints ("Large Straight", largeStraight(freq))
    displayPoints ("Chance", chance(freq))
    displayPoints ("Yahtzee", yahtzee(freq))
    print ("Maximum points possible: ",maximizePoints(freq))
    maxCategories (freq)

##############################################################################
##                              Shell Interaction
##
##>>> main()
##
##Your roll: 
##1 6 6 4 5 
##
##Do you want to re-roll? (Y/N) y
##Keeping die #0 (value: 1)? (Y/N) n
##Keeping die #1 (value: 6)? (Y/N) y
##Keeping die #2 (value: 6)? (Y/N) y
##Keeping die #3 (value: 4)? (Y/N) y
##Keeping die #4 (value: 5)? (Y/N) y
##
##Your roll: 
##3 6 6 4 5 
##
##Do you want to re-roll? (Y/N) n
##3 6 6 4 5 
##
##Points for Aces/Ones: 0
##Points for Deuces/Twos: 0
##Points for Threes: 3
##Points for Fours: 4
##Points for Fives: 5
##Points for Sixes: 12
##Points for Three of a Kind: 0
##Points for Four of a Kind: 0
##Points for Full House: 0
##Points for Small Straight: 30
##Points for Large Straight: 0
##Points for Chance: 24
##Points for Yahtzee: 0
##Maximum points possible:  30
##Maximum points can be received from these categories:
##Small straight
##>>> main()
##
##Your roll: 
##1 3 5 5 6 
##
##Do you want to re-roll? (Y/N) y
##Keeping die #0 (value: 1)? (Y/N) n
##Keeping die #1 (value: 3)? (Y/N) 
##Keeping die #2 (value: 5)? (Y/N) y
##Keeping die #3 (value: 5)? (Y/N) y
##Keeping die #4 (value: 6)? (Y/N) y
##
##Your roll: 
##5 5 5 5 6 
##
##Do you want to re-roll? (Y/N) y
##Keeping die #0 (value: 5)? (Y/N) y
##Keeping die #1 (value: 5)? (Y/N) y
##Keeping die #2 (value: 5)? (Y/N) y
##Keeping die #3 (value: 5)? (Y/N) y
##Keeping die #4 (value: 6)? (Y/N) no
##
##Your roll: 
##5 5 5 5 6 
##
##Points for Aces/Ones: 0
##Points for Deuces/Twos: 0
##Points for Threes: 0
##Points for Fours: 0
##Points for Fives: 20
##Points for Sixes: 6
##Points for Three of a Kind: 26
##Points for Four of a Kind: 26
##Points for Full House: 0
##Points for Small Straight: 0
##Points for Large Straight: 0
##Points for Chance: 26
##Points for Yahtzee: 0
##Maximum points possible:  26
##Maximum points can be received from these categories:
##Three of a kind
##Four of a kind
##Chance
##>>> 
