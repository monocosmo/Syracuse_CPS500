# Shuchi Wu
# Homework 4
# CPS 300

######################################################################################
# In this homework, we implement a "Hangman" game with Python.                       #
# This is a non-GUI version (Problem 1 and Problem 2).                               #
#                                                                                    #
# Game rules:                                                                        #
# 1. The game starts with a prize pool of $1500.                                     #
# 2. The game ends when the prize decrements to $0 or below $0.                      #
# 3. Each time the user guesses a letter, that balance is reuced by                  #
#    either $100 (if the letter is in the puzzle and hadn't been guessed)            #
#    or $150 (if the letter is not in the puzzle, or if it had been guessed)         #
#                                                                                    #
# Note: Rule #2 is ambiguous when prize reaches $50 and only one letter unsolved,    #
# because the user may "win" the game with a prize of -$50. To solve this problem,   #
# I decided to give the user one more chance to guess at prize $50, and whenever     #
# the prize goes below $0, the system will adjust the residual prize to $0. So the   #
# user can "win" the game with a prize of $0 (instead of "strange" -$50).            #
#                                                                                    #
# My previous design is to kick the user out when prize reaches $100 to avoid -$50   #
# situation, but the user may feel "angry" when they see still $50 left but been     #
# kicked out (although it is reasonable).                                            #
######################################################################################

########################### This part is unchanged from Lab 12 #######################
# This function converts the list sofar into a string.
def stringify (sofar):
    return ''.join(sofar)

# This function prompts user for character, reads it, and
#    ensures what is sent back is a single character.
def getGuess ():
    ch = input ("Guess a char: ")
    while ch == '':
        print("Error: please enter a char.")
        ch = input ("Guess a char: ")
    # only return one uppered character (even if user entered more)
    return ch[0].upper ()

# This function copies non-letter characters from orig into sofar.
def setup (sofar,orig):
    for i in range(len(orig)):
        if not orig[i].isalpha():
            sofar[i] = orig[i]
 
# This function updates the list sofar to reflect the guess ch:
#    if the i-th element of orig is ch, then the
#    i-th element of sofar should be made ch.
def update (sofar,orig,ch):
    for i in range(len(orig)):
        if orig[i] == ch:
            sofar[i] = orig[i]
    
# This function determines whether the list sofar is an accurate
#    representation of the string orig.
#    Return True if they have the same values (and same length)
#    Return False otherwise
def compare (sofar, orig):
    for i in range(len(sofar)):
        if sofar[i] != orig[i]:
            return False
    return True

#################################### New functions ###################################
# This function appends input to the list of guessed chracters.
# Note: Input will be appended no matter guessed or not, and won't affect the result.
def updateGuessed (guessed, ch):
    guessed.append(ch)

# This function asks if user like to solve in one time guess.
# Return True if user like to solve, otherwise return False.
def solveAsk ():
    userInput = input("Do you want to solve it? (Enter Y to solve)")
    while userInput == '':
        print("Error: please enter something.")
        userInput = input("Do you want to solve it? (Enter Y to solve)")
    if userInput.upper()[0] == 'Y':
	    return True
    else:
	    return False

#################################### Main function ###################################
# Basic idea:
# 1. Set up answer and prize, initiate guessed record and solved status.
# 2. Ask if the user want to solve (make a one time guess).
# 3. If not, ask the user for a guess (input to guess one character).
# 4. Check if the input is in puzzle or guessed.
# 5. Update the guessed record and the answer with input.
# 6. Update the prize.
# 7. When out of while-loop, print the conclusion.
def main ():
    phrase = "Magical Mystery Word".upper ()

    # Make sure answer is exactly as long as phrase, but make it
    # mutable  (i.e., a list).
    answer = ['-'] * len (phrase)

    # Have all nonalphabetic characters show up in answer string.
    setup (answer, phrase)

    # Initiate prize, solved status and guessed list.
    prize = 1500
    solved = False
    guessed = []

    while not solved and prize > 0:
        # Let the user know the current prize pool and current guess status.
        print("\nYou have $", prize)
        print ("\nCurrent status: ", stringify(answer))
        
        # Check if the user wants to solve in one time guess.
        if solveAsk ():
            # If the user like to solve, ask for an input.
            # In this case, answer will not go through regular update process.
            answer = input("Enter your answer: ")
            
            if answer.upper() == phrase.upper():
            	# set solved to True to get out of loop.
            	solved = True
            else:
            	# set prize to zero to get out of loop.
            	prize = 0
        else:
        # If user like to contunue guessing character by character, call getGuess().
            ch = getGuess ()

            # Check if input is in puzzle or guessed and update prize.
            if ch in phrase and (ch not in guessed):
            # If the letter is in the puzzle and hadn’t been guessed
                prize = prize - 100
            else:
            # If the letter is not in the puzzle, or if it had been guessed
                prize = prize - 150

            # Transfer the negative prize amount to $0.
            if prize < 0:
                prize = 0

            # Update the guessed record and the answer with input.
            update(answer,phrase,ch)
            updateGuessed(guessed,ch)

            # Determine whether puzzle has been solved
            solved = compare (answer,phrase)

    # We're out of the loop, and ready to declare victory/defeat
    if solved:
        print ("\nCongratulations!")
        print ("Your prize is: ",prize)
    else:
        print ("\nSorry, better luck next time.")
        print ("The answer was: ", phrase)

# Run the game.
main()
