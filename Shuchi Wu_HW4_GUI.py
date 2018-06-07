# Shuchi Wu
# Homework 4
# CPS 300

######################################################################################
# In this homework, we implement a "Hangman" game with Python. The GUI functions are #
# implemented with graphics library.                                                 # 
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

# Import the graphics library
from graphics import *

########################### This part is unchanged from Lab 12 #######################
# This function converts the list sofar into a string.
def stringify (sofar):
    return ''.join(sofar)

# The getGuess() function has been deleted since it may conflict with GUI.
# Instead, you will find a guess() in the below part.
# Please refer to HW4_nonGUI.py for the detail of getGuess() function.

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

# This function sets up the basic construction of the game GUI window.
# Only permanent components will be set up in this function.
def setUpWindow (window):
    window.setBackground("pink")
    # Prepare the title.
    titleText = Text(Point(500,50), "Welcome to Hangman")
    titleText.setFill("purple")
    titleText.setSize(36)
    titleText.setStyle("bold")
    titleText.draw(window)
    # Prepare the instruction to solve.
    inviteText0 = Text(Point(238,180), "Do you want to solve it? (Enter Y to solve):")
    inviteText0.setFill("purple")
    inviteText0.setSize(20)
    inviteText0.draw(window)
    # Prepare the balance window title.
    balanceText = Text(Point(97,300), "Prize Pool:")
    balanceText.setFill("purple")
    balanceText.setSize(20)
    balanceText.draw(window)
    # Prepare the answer sofar title.
    answerText = Text(Point(112,350), "Puzzle Status:")
    answerText.setFill("purple")
    answerText.setSize(20)
    answerText.draw(window)
    # Prepare the input instruction.
    inputText = Text(Point(162,400), "Please guess a character:")
    inputText.setFill("purple")
    inputText.setSize(20)
    inputText.draw(window)

# This function prints current status of prize and answer which is updating in main().
# Return objects prizeText and answerText.
def status (window, prize, answer):
    # Display current prize pool.
    prizeText = Text(Point(350,300), prize)
    prizeText.setSize(20)
    prizeText.draw(window)
    # Display current answer status.
    answerText = Text(Point(399,350), stringify(answer))
    answerText.setSize(20)
    answerText.draw(window)
    # return prizeText and answerText for undraw commands in main()
    return prizeText, answerText

# This function asks if user like to solve in one time guess. Default is "N".
# Return True if user like to solve, otherwise return False.
def solveAsk (window):
    entryInvite = Entry(Point(550, 180), 8)
    entryInvite.setText("N")
    entryInvite.draw(window)
    # Print a click instruction guiding user to click mouse to continue.
    clickHint = Text(Point(750, 180), "Click mouse to continue.")
    clickHint.setFill("purple")
    clickHint.setSize(20)
    clickHint.draw(window)
    # Get the first letter of user's input.
    window.getMouse()
    play = entryInvite.getText().upper()[0]
    # Hide the click instruction after click to avoid user confusing.
    clickHint.undraw()
    # Check ther user's decision.
    if play == 'Y':
        return True
    else:
        return False

# This function will be called if user choose to solve puzzle.
# It will prepare an entry place and instruction, and return the entry.
def solveEntry(window):
    # Print entry instruction.
    instructionText = Text(Point(133, 220), "Enter your answer:")
    instructionText.setFill("purple")
    instructionText.setSize(20)
    instructionText.draw(window)
    # Prepare an entry place.
    # Default is "Input Here" to avoid empty entry.
    userAnswer = Entry(Point(350, 220), 20)
    userAnswer.setText("Input Here")
    userAnswer.draw(window)
    # Print a click instruction guiding user to click mouse to continue.
    clickHint = Text(Point(650, 220), "Click mouse to submit answer.")
    clickHint.setFill("purple")
    clickHint.setSize(20)
    clickHint.draw(window)
    # Get and return the input.
    window.getMouse()
    answer = userAnswer.getText()
    # Hide the click instruction after click to avoid user confusing.
    clickHint.undraw()
    return answer

# This function will be called when the user choose to guess chracater by character.
# It will return the first letter of user's entry.
def guess(window):
    # Prepare the guess entry window.
    # Default is "*Input Here*", the "*" is to avoid mis-entering.
    entryGuess = Entry(Point(420, 400), 10)
    entryGuess.setText("*Input Here*")
    entryGuess.draw(window)
    # Print a click instruction guiding user to click mouse to continue.
    clickHint = Text(Point(730, 400), "Please enter a guess before clicking mouse to continue.")
    clickHint.setFill("purple")
    clickHint.setSize(20)
    clickHint.draw(window)
    # Parse the first character of input into main function.
    window.getMouse()
    ch = entryGuess.getText()[0].upper()
    # Hide the click instruction after click to avoid user confusing.
    clickHint.undraw()
    return ch

# These two functions print the final messages.
# Since the if-condition on prize must be implemented in main, I devide the final
# massage printing into two functions.

# Win message
def win (window, prize):
    winLine1 = Text(Point(120, 450), "Congratulations!")
    winLine1.setFill("purple")
    winLine1.setSize(20)
    winLine1.draw(window)
    winLine2 = Text(Point(112, 480), "Your prize is $")
    winLine2.setFill("purple")
    winLine2.setSize(20)
    winLine2.draw(window)
    winLine3 = Text(Point(252, 480), prize)
    winLine3.setFill("purple")
    winLine3.setSize(20)
    winLine3.draw(window)

# Lose message
def lose (window, orig):
    loseLine1 = Text(Point(168, 450), "Sorry, better luck next time.")
    loseLine1.setFill("purple")
    loseLine1.setSize(20)
    loseLine1.draw(window)
    loseLine2 = Text(Point(122, 480), "The answer was:")
    loseLine2.setFill("purple")
    loseLine2.setSize(20)
    loseLine2.draw(window)
    loseLine3 = Text(Point(412, 480), orig)
    loseLine3.setFill("purple")
    loseLine3.setSize(20)
    loseLine3.draw(window)

# This function is to print exit message guiding user to close game window.
def exit (window):
    exitText = Text(Point(251, 530), "Exit. Thanks for playing. Click mouse to close.")
    exitText.setFill("purple")
    exitText.setSize(20)
    exitText.draw(window)
    window.getMouse()
    window.close()

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

    # Open a GUI window.
    gameWindow = GraphWin("Hangman", 1000, 550)

    # Set up permanent components (non-user-interact part) in the GUI.
    setUpWindow(gameWindow)

    while not solved and prize > 0:
        # Print current status of prize and answer.
        # Note: two text objects are returned, to be undrawed later.
        prizeText, answerText = status (gameWindow, prize, answer)

        # Check if the user wants to solve the puzzle.
        if solveAsk(gameWindow):
            # if the user chooses to solve, get the entry.
            answer = solveEntry(gameWindow)
            if answer.upper() == phrase.upper():
                # set solved to True to get out of loop.
                solved = True
            else:
                # set prize to zero to get out of loop.
                prize = 0
        else:
            ch = guess(gameWindow)
             # Check if input is in puzzle or guessed and update prize.
            if ch in phrase and (ch not in guessed):
                # If the letter is in the puzzle and hadn’t been guessed
                prize = prize - 100
            else:
                # If the letter is not in the puzzle, or if it had been guessed
                prize = prize - 150

            # Convert the negative prize amount to $0.
            if prize < 0:
                prize = 0

            # Update the guessed record and the answer with input.
            update(answer,phrase,ch)
            updateGuessed(guessed,ch)

            # Erase the prize and answer information to make place for next round loop.
            prizeText.undraw()
            answerText.undraw()

            # Determine whether puzzle has been solved
            solved = compare (answer,phrase)

    # We're out of the loop, and ready to declare victory/defeat
    # Call subroutine win() and lose() to print results.
    if solved:
        win (gameWindow, prize)
    else:
        lose (gameWindow, phrase)

    # Close the game window
    exit (gameWindow)

# Run the game
main()
