import chess.pgn
import time
import sys
import math

# name of pgn file : number of games stored
games = {'allgames_2010.pgn': 20374965,
         'allgames2000_2013.pgn': 569560,
         'allgames2000_2017.pgn': 395300,
         '2017games_rating2600.pgn': 5000}

gamefile = list(games.keys())[3]

pgn = open(gamefile)
counter = 0
starttime = time.time()
train = []
# final training data will have the format:

#  [
# [[position1], [position2]],
# [[position2], [position3],
# ...]

# each position is a 64-element list of numbers(each element can be from 1-12 for each of the pieces) indicating what piece is in the square
#dict to convert letter from FEN notation to numerical values
convert = {

    'p': 1,
    'n': 2,
    'b': 3,
    'r': 4,
    'q': 5,
    'k': 6,
    'P': 7,
    'N': 8,
    'B': 9,
    'R': 10,
    'Q': 11,
    'K': 12


}

#progress bar with ETA. only used in full file testing, and did not affect time taken
def progressBar(value, endvalue, time1, time2, bar_length=20):
    percent = float(value) / endvalue
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\rProgress: [{0}] {1}% ".format(arrow + spaces, int(round(percent * 100))))
    seconds = ((time2 - time1) / (percent)) - (time2-time1)
    sys.stdout.write("ETA: {} minutes and {:0.0f} seconds".format(math.floor(seconds / 60), seconds % 60))
    sys.stdout.flush()

#------------ test for one game ------------

# game = chess.pgn.read_game(pgn) #open first game
# board = game.board() #set the game board
# for i, move in enumerate(game.mainline()):
#     position = []
#     train.append([])
#     fenposition = board.fen().split(' ', 1)[0] #only select first part of FEN indicating positions
#     for char in fenposition:
#         if char.isalpha(): #if the character is a letter, it's a piece, so use dict to convert to number
#             position.append(convert[char])
#         elif char.isdigit(): #if the character is number, it's spaces, so add 0s
#             position.extend([0] * int(char))
#     print(fenposition) #FEN representation of position
#     print(position) #Converted representation of position
#     train[i].append(position) #appending to training data
#     if i > 0:
#         train[i-1].append(position)

#     board.push(move) #go to next position

# print('\ntraining data: {}'.format(train))
# print('time to process: {} seconds'.format(time.time() - starttime))

#------------ test for full file ------------

while True:
    game = chess.pgn.read_game(pgn)
    if game is None:
        break
    counter += 1
    progressBar(counter, games[gamefile], starttime, time.time())

    board = game.board()
    for i, move in enumerate(game.main_line()):
        position = []
        train.append([])
        fenposition = board.fen().split(' ', 1)[0]
        for letter in fenposition:
            if letter.isalpha():
                position.append(convert[letter])
            elif letter.isdigit():
                position.extend([0] * int(letter))

        train[i].append(position)
        if i > 0:
            train[i - 1].append(position)

        board.push(move)


print("\n {} games processed in {} seconds".format(counter, time.time()-starttime))