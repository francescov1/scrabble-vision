from random import shuffle
from gameplay.word_rank import word_rank

"""
Scrabble Game
Classes:
Tile - keeps track of the tile letter and value
Rack - keeps track of the tiles in a player's letter rack
Bag - keeps track of the remaining tiles in the bag
Word - checks the validity of a word and its placement
Board - keeps track of the tiles' location on the board
"""
#Keeps track of the score-worth of each letter-tile.
LETTER_VALUES = {"A": 1,
                 "B": 3,
                 "C": 3,
                 "D": 2,
                 "E": 1,
                 "F": 4,
                 "G": 2,
                 "H": 4,
                 "I": 1,
                 "J": 8,
                 "K": 5,
                 "L": 1,
                 "M": 3,
                 "N": 1,
                 "O": 1,
                 "P": 3,
                 "Q": 10,
                 "R": 1,
                 "S": 1,
                 "T": 1,
                 "U": 1,
                 "V": 4,
                 "W": 4,
                 "X": 8,
                 "Y": 4,
                 "Z": 10,
                 "#": 0}

class Tile:
    """
    Class that allows for the creation of a tile. Initializes using an uppercase string of one letter,
    and an integer representing that letter's score.
    """
    def __init__(self, letter, letter_values):
        #Initializes the tile class. Takes the letter as a string, and the dictionary of letter values as arguments.
        self.letter = letter.upper()
        if self.letter in letter_values:
            self.score = letter_values[self.letter]
        else:
            self.score = 0

    def get_letter(self):
        #Returns the tile's letter (string).
        return self.letter

    def get_score(self):
        #Returns the tile's score value.
        return self.score

class Bag:
    """
    Creates the bag of all tiles that will be available during the game. Contains 98 letters and two blank tiles.
    Takes no arguments to initialize.
    """
    def __init__(self):
        #Creates the bag full of game tiles, and calls the initialize_bag() method, which adds the default 100 tiles to the bag.
        #Takes no arguments.
        self.bag = []
        self.initialize_bag()

    def add_to_bag(self, tile, quantity):
        #Adds a certain quantity of a certain tile to the bag. Takes a tile and an integer quantity as arguments.
        for i in range(quantity):
            self.bag.append(tile)

    def initialize_bag(self):
        #Adds the intiial 100 tiles to the bag.
        global LETTER_VALUES
        self.add_to_bag(Tile("A", LETTER_VALUES), 9)
        self.add_to_bag(Tile("B", LETTER_VALUES), 2)
        self.add_to_bag(Tile("C", LETTER_VALUES), 2)
        self.add_to_bag(Tile("D", LETTER_VALUES), 4)
        self.add_to_bag(Tile("E", LETTER_VALUES), 12)
        self.add_to_bag(Tile("F", LETTER_VALUES), 2)
        self.add_to_bag(Tile("G", LETTER_VALUES), 3)
        self.add_to_bag(Tile("H", LETTER_VALUES), 2)
        self.add_to_bag(Tile("I", LETTER_VALUES), 9)
        self.add_to_bag(Tile("J", LETTER_VALUES), 1)
        self.add_to_bag(Tile("K", LETTER_VALUES), 1)
        self.add_to_bag(Tile("L", LETTER_VALUES), 4)
        self.add_to_bag(Tile("M", LETTER_VALUES), 2)
        self.add_to_bag(Tile("N", LETTER_VALUES), 6)
        self.add_to_bag(Tile("O", LETTER_VALUES), 8)
        self.add_to_bag(Tile("P", LETTER_VALUES), 2)
        self.add_to_bag(Tile("Q", LETTER_VALUES), 1)
        self.add_to_bag(Tile("R", LETTER_VALUES), 6)
        self.add_to_bag(Tile("S", LETTER_VALUES), 4)
        self.add_to_bag(Tile("T", LETTER_VALUES), 6)
        self.add_to_bag(Tile("U", LETTER_VALUES), 4)
        self.add_to_bag(Tile("V", LETTER_VALUES), 2)
        self.add_to_bag(Tile("W", LETTER_VALUES), 2)
        self.add_to_bag(Tile("X", LETTER_VALUES), 1)
        self.add_to_bag(Tile("Y", LETTER_VALUES), 2)
        self.add_to_bag(Tile("Z", LETTER_VALUES), 1)
        # self.add_to_bag(Tile("#", LETTER_VALUES), 2)
        shuffle(self.bag)

    def take_from_bag(self):
        #Removes a tile from the bag and returns it to the user. This is used for replenishing the rack.
        return self.bag.pop()

    def get_remaining_tiles(self):
        #Returns the number of tiles left in the bag.
        return len(self.bag)

class Rack:
    """
    Creates each player's 'dock', or 'hand'. Allows players to add, remove and replenish the number of tiles in their hand.
    """
    def __init__(self, rack):
        #Initializes the player's rack/hand. Takes the bag from which the racks tiles will come as an argument.
        self.rack = rack
        #self.bag = bag
        #self.initialize()

    def add_to_rack(self, bag):
        #Takes a tile from the bag and adds it to the player's rack.
        self.rack.append(bag.take_from_bag())

    def initialize(self, bag):
        #Adds the initial 7 tiles to the player's hand.
        for i in range(7):
            self.add_to_rack(bag)

    def get_rack_str(self):
        #Displays the user's rack in string form.
        return "".join(self.rack)

    def get_rack_arr(self):
        #Returns the rack as an array of tile instances
        return self.rack

    def remove_from_rack(self, tile):
        #Removes a tile from the rack (for example, when a tile is being played).
        self.rack.remove(tile)

    def get_rack_length(self):
        #Returns the number of tiles left in the rack.
        return len(self.rack)

    def replenish_rack(self, bag):
        #Adds tiles to the rack after a turn such that the rack will have 7 tiles (assuming a proper number of tiles in the bag).
        while self.get_rack_length() < 7 and bag.get_remaining_tiles() > 0:
            self.add_to_rack(bag)

class Player:
    """
    Creates an instance of a player. Initializes the player's rack, and allows you to set/get a player name.
    """
    def __init__(self, bag, rack):
        #Intializes a player instance. Creates the player's rack by creating an instance of that class.
        #Takes the bag as an argument, in order to create the rack.
        self.name = ""
        self.rack = rack
        self.score = 0

    def set_name(self, name):
        #Sets the player's name.
        self.name = name

    def get_name(self):
        #Gets the player's name.
        return self.name

    def get_rack_str(self):
        #Returns the player's rack.
        return self.rack.get_rack_str()

    def get_rack_arr(self):
        #Returns the player's rack in the form of an array.
        return self.rack.get_rack_arr()

    def increase_score(self, increase):
        #Increases the player's score by a certain amount. Takes the increase (int) as an argument and adds it to the score.
        self.score += increase

    def get_score(self):
        #Returns the player's score
        return self.score

class Board:
    """
    Creates the scrabble board.
    """
    def __init__(self):
        #Creates a 2-dimensional array that will serve as the board, as well as adds in the premium squares.
        self.board = [["   " for i in range(15)] for j in range(15)]
        self.add_premium_squares()
        self.board[7][7] = " * "

    def get_board(self):
        #Returns the board in string form.
        board_str = "   |  " + "  |  ".join(str(item) for item in range(10)) + "  | " + "  | ".join(str(item) for item in range(10, 15)) + " |"
        board_str += "\n   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
        board = list(self.board)
        for i in range(len(board)):
            if i < 10:
                board[i] = str(i) + "  | " + " | ".join(str(item) for item in board[i]) + " |"
            if i >= 10:
                board[i] = str(i) + " | " + " | ".join(str(item) for item in board[i]) + " |"
        board_str += "\n   |_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _|\n".join(board)
        board_str += "\n   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _"
        return board_str

    def add_premium_squares(self):
        #Adds all of the premium squares that influence the word's score.
        TRIPLE_WORD_SCORE = ((0,0), (7, 0), (14,0), (0, 7), (14, 7), (0, 14), (7, 14), (14,14))
        DOUBLE_WORD_SCORE = ((1,1), (2,2), (3,3), (4,4), (1, 13), (2, 12), (3, 11), (4, 10), (13, 1), (12, 2), (11, 3), (10, 4), (13,13), (12, 12), (11,11), (10,10))
        TRIPLE_LETTER_SCORE = ((1,5), (1, 9), (5,1), (5,5), (5,9), (5,13), (9,1), (9,5), (9,9), (9,13), (13, 5), (13,9))
        DOUBLE_LETTER_SCORE = ((0, 3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (6,2), (6,6), (6,8), (6,12), (7,3), (7,11), (8,2), (8,6), (8,8), (8, 12), (11,0), (11,7), (11,14), (12,6), (12,8), (14, 3), (14, 11))

        for coordinate in TRIPLE_WORD_SCORE:
            self.board[coordinate[0]][coordinate[1]] = "TWS"
        for coordinate in TRIPLE_LETTER_SCORE:
            self.board[coordinate[0]][coordinate[1]] = "TLS"
        for coordinate in DOUBLE_WORD_SCORE:
            self.board[coordinate[0]][coordinate[1]] = "DWS"
        for coordinate in DOUBLE_LETTER_SCORE:
            self.board[coordinate[0]][coordinate[1]] = "DLS"

    def place_word(self, word, location, direction, player, bag):
        #Allows you to play words, assuming that they have already been confirmed as valid.
        global premium_spots
        premium_spots = []
        direction.lower()
        word = word.upper()

        #Places the word going rightwards
        if direction.lower() == "r":
            for i in range(len(word)):
                if self.board[location[0]][location[1]+i] != "   ":
                    premium_spots.append((word[i], self.board[location[0]][location[1]+i]))
                self.board[location[0]][location[1]+i] = " " + word[i] + " "

        #Places the word going downwards
        elif direction.lower() == "d":
            for i in range(len(word)):
                if self.board[location[0]+i][location[1]] != "   ":
                    premium_spots.append((word[i], self.board[location[0]+i][location[1]]))
                self.board[location[0]+i][location[1]] = " " + word[i] + " "

    def board_array(self):
        #Returns the 2-dimensional board array.
        return self.board

class Word:
    def __init__(self, word, location, player, direction, board):
        self.word = word.upper()
        self.location = location
        self.player = player
        self.direction = direction.lower()
        self.board = board
        self.attached_words = []
        self.score = 0
        self.board_squares = []

    def check_word(self, round_number, players):
        #Checks the word to make sure that it is in the dictionary, and that the location falls within bounds.
        #Also controls the overlapping of words.

        dictionary = open('gameplay/dic.txt').read()

        current_board_ltr = ""
        needed_tiles = ""
        blank_tile_val = ""

        #Assuming that the player is not skipping the turn:
        if self.word != "":

            #Raises an error if the location of the word will be out of bounds.
            if self.location[0] > 14 or self.location[1] > 14 or self.location[0] < 0 or self.location[1] < 0 or (self.direction == "d" and (self.location[0]+len(self.word)-1) > 14) or (self.direction == "r" and (self.location[1]+len(self.word)-1) > 14):
                return False

            # TODO Fix blank tile function and program the bot to use them
            #Allows for players to declare the value of a blank tile.
            if "#" in self.word:
                while len(blank_tile_val) != 1:
                    blank_tile_val = input("Please enter the letter value of the blank tile: ")
                self.word = self.word[:self.word.index("#")] + blank_tile_val.upper() + self.word[(self.word.index("#")+1):]

            #Reads in the board's current values under where the word that is being played will go. Raises an error if the direction is not valid.
            if self.direction == "r":
                # Check for adjacent letters and add them to the word
                board_row = self.board[self.location[0]]
                col = self.location[1]
                end_ltrs = self.get_letters(board_row, col + len(self.word))
                start_ltrs = self.get_letters(board_row[::-1], 15 - col)
                if len(end_ltrs) > 0:
                    self.word = self.word + ''.join(end_ltrs)
                if len(start_ltrs) > 0:
                    self.word = ''.join(start_ltrs[::-1]) + self.word
                    self.location[1] -= len(self.word)

                for i in range(len(self.word)):
                    if self.board[self.location[0]][self.location[1]+i][1] == " " or self.board[self.location[0]][self.location[1]+i] == "TLS" or self.board[self.location[0]][self.location[1]+i] == "TWS" or self.board[self.location[0]][self.location[1]+i] == "DLS" or self.board[self.location[0]][self.location[1]+i] == "DWS" or self.board[self.location[0]][self.location[1]+i][1] == "*":
                        current_board_ltr += " "
                    else:
                        current_board_ltr += self.board[self.location[0]][self.location[1]+i][1]
            elif self.direction == "d":
                board_col = [x[self.location[1]] for x in self.board]
                row = self.location[0]
                end_ltrs = self.get_letters(board_col, row + len(self.word))
                start_ltrs = self.get_letters(board_col[::-1], 15 - row)
                if len(end_ltrs) > 0:
                    self.word = self.word + ''.join(end_ltrs)
                if len(start_ltrs) > 0:
                    self.word = ''.join(start_ltrs[::-1]) + self.word
                    self.location[0] -= len(self.word)

                for i in range(len(self.word)):
                    if self.board[self.location[0]+i][self.location[1]] == "   " or self.board[self.location[0]+i][self.location[1]] == "TLS" or self.board[self.location[0]+i][self.location[1]] == "TWS" or self.board[self.location[0]+i][self.location[1]] == "DLS" or self.board[self.location[0]+i][self.location[1]] == "DWS" or self.board[self.location[0]+i][self.location[1]] == " * ":
                        current_board_ltr += " "
                    else:
                        current_board_ltr += self.board[self.location[0]+i][self.location[1]][1]
            else:
                return "Error: please enter a valid direction."

            #Raises an error if the word being played is not in the official scrabble dictionary (dic.txt).
            if '\n' + self.word + '\n' not in dictionary:
                return "Please enter a valid dictionary word.\n"

            #Ensures that the words overlap correctly. If there are conflicting letters between the current board and the word being played, raises an error.
            for i in range(len(self.word)):
                if current_board_ltr[i] == " ":
                    needed_tiles += self.word[i]
                elif current_board_ltr[i] != self.word[i]:
                    # print("Current_board_ltr: " + str(current_board_ltr) + ", Word: " + self.word + ", Needed_Tiles: " + needed_tiles)
                    return "The letters do not overlap correctly, please choose another word."

            #If there is a blank tile, remove it's given value from the tiles needed to play the word.
            if blank_tile_val != "":
                needed_tiles = needed_tiles[needed_tiles.index(blank_tile_val):] + needed_tiles[:needed_tiles.index(blank_tile_val)]

            #Ensures that the word will be connected to other words on the playing board.
            if (round_number != 1 or (round_number == 1 and players[0] != self.player)) and current_board_ltr == " " * len(self.word):
                # print("Current_board_ltr: " + str(current_board_ltr) + ", Word: " + self.word + ", Needed_Tiles: " + needed_tiles)
                return "Please connect the word to a previously played letter."

            #Raises an error if the player does not have the correct tiles to play the word.
            for letter in needed_tiles:
                if letter not in self.player.get_rack_str() or self.player.get_rack_str().count(letter) < needed_tiles.count(letter):
                    return "You do not have the tiles for this word\n"

            #Ensures that first turn of the game will have the word placed at (7,7).
            if round_number == 1 and players[0] == self.player and self.location != [7,7]:
                return "The first turn must begin at location (7, 7).\n"

            # Check that new words formed that are attached to the word played are real
            attached_words, board_squares  = self.get_attached_words()
            for word_info in attached_words:
                word = '\n' + ''.join(word_info['word']) + '\n'
                if word not in dictionary:
                    return 'invalid word attached'

            self.attached_words = attached_words
            self.board_squares = board_squares
            return True

        #If the user IS skipping the turn, confirm. If the user replies with "Y", skip the player's turn. Otherwise, allow the user to enter another word.
        else:
            if input("Are you sure you would like to skip your turn? (y/n)").upper() == "Y":
                return True
            else:
                return "Please enter a word."

    # get letters that are apart of the attached word
    def get_letters(self, word_col, row):
        word = []
        space = False
        while not space and row >= 0 and row < 15:
            if len(word_col[row].strip()) == 1:
                word.append(word_col[row].strip())
                row += 1
            else:
                space = True
        return word

    # Get the score for the word that is attached to the played word
    def format_word(self, col, row, board, ltr):
        word_col = [x[col] for x in board]
        word_end = self.get_letters(word_col, row + 1)
        word_start = self.get_letters(word_col[::-1], 15 - row)
        word = word_start[::-1] + [ltr] + word_end
        return word

    # check the spaces on both sides of the word for letters
    def get_other_words(self, start, row, end, board, played_ltrs):
        global LETTER_VALUES
        words = []
        for square in played_ltrs:
            if self.direction == 'r':
                col = square['col']
            else:
                col = square['row']
            ltr_after = self.is_letter(board, row + 1, col)
            ltr_before = self.is_letter(board, row - 1, col)
            if ltr_after or ltr_before:
                word = self.format_word(col, row, board, square['ltr'])
                words.append({'word': word, 'ltr': square['ltr'], 'ltr_indx': [row, col], 'score': 0})
        return words

    #check if there is a letter on the square
    def is_letter(self, board, row, i):
        try:
            space = board[row][i].strip()
            is_ltr = len(space) == 1
        except IndexError:
            is_ltr = False
        return is_ltr

    def get_played_tiles(self, board):
        player_ltrs = []
        squares = []
        loc = self.location
        if self.direction == 'r':
            end = loc[1] + len(self.word) - 1
            squares = board[loc[0]][loc[1]:end + 1]
        else:
            end = loc[0] + len(self.word) - 1
            squares = board[loc[1]][loc[0]: end + 1]
        for i in range(len(squares)):
            if len(squares[i].strip()) == 1 and squares[i].strip() != "*":
                pass
            else:
                if self.direction == 'r':
                    player_ltrs.append({'ltr': self.word[i], 'row': loc[0], 'col': loc[1] + i, 'score': 0})
                else:
                    player_ltrs.append({'ltr': self.word[i], 'row': loc[0] + i, 'col': loc[1], 'score': 0})
        return player_ltrs, squares

    def get_attached_words(self):
        loc = self.location
        if self.direction == 'r':
            stat = loc[0]
            start = loc[1]
            board = self.board
        else:
            stat = loc[1]
            start = loc[0]
            board = [list(i) for i in zip(*self.board)]
        end = start + len(self.word) -1
        if end > 14 or end < 0 or loc[0] < 0  or loc[0] > 14 or loc[1] < 0 or loc[1] > 14:
            return 0 # change to invalid
        played_ltrs, squares = self.get_played_tiles(board)
        return self.get_other_words(start, stat, end, board, played_ltrs), squares

    # calculate the score of the word being played, as well as words that are attached
    def calculate_word_score(self):
        self.score = 0
        global LETTER_VALUES
        word_score = 0
        total_score = 0
        word_mult = 1
        board_ltrs = []

        for word in self.attached_words:
            row = word['ltr_indx'][0]
            col = word['ltr_indx'][1]
            ltr_sqr = self.board[row][col]
            for ltr in word['word']:
                word['score'] += LETTER_VALUES[ltr]
            if ltr_sqr == "TLS":
                word['score']+= LETTER_VALUES[word['ltr']] * 2
            elif ltr_sqr == "DLS":
                word['score'] += LETTER_VALUES[word['ltr']]

            if ltr_sqr == "DWS":
                word['score'] *= 2
            elif ltr_sqr == "TWS":
                word['score'] *= 3
            total_score += word['score']


        # calculate the score of the word being played
        if self.location == [7,7] and self.board[7][7][1] == '*':
            word_mult = 2

        for i in range(len(self.word)):
            if len(self.board_squares[i].strip()) == 1 and self.board_squares[i][1] != '*':
                board_ltrs.append(self.board_squares[i][1])
            if self.board_squares[i] == "TLS":
                word_score += LETTER_VALUES[self.word[i]] * 3
            elif self.board_squares[i] == "DLS":
                word_score += LETTER_VALUES[self.word[i]] * 2
            else:
                word_score += LETTER_VALUES[self.word[i]]
            if self.board_squares[i] == "DWS":
                word_mult *= 2
            elif self.board_squares[i] == "TWS":
                word_mult *= 3

        word_score *= word_mult
        total_score += word_score

        #fix
        if len(self.word) - len(board_ltrs) == 7:
            total_score += 50

        self.score = total_score
        return total_score

    def format_output(self, rack):
        moves = []
        rack = [char.upper() for char in rack]
        row = self.location[0]
        col = self.location[1]
        for i in range(len(self.word)):
            if self.direction == 'r':
                col = self.location[1] + i
            else:
                row = self.location[0] + i
            if len(self.board_squares[i].strip()) != 1:
                rack_pos = rack.index(self.word[i])
                rack[rack_pos] = ''
                moves.append({'ltr': self.word[i], 'rack_pos': rack_pos, 'board_pos': [row, col]})
        return moves

    def add_score(self):
        self.player.increase_score(self.score)

    def set_word(self, word):
        self.word = word

    def set_location(self, location):
        self.location = location

    def set_direction(self, direction):
        self.direction = direction

    def get_word(self):
        return self.word

class Game:
    """
    Creates an instance of a game. Initializes the board and players
    """
    def __init__(self, player_name, rack, board):
        self.board = board
        self.bag = Bag()
        self.round_number = 4
        self.skipped_turns = 0

        players = [Player(self.bag, rack), Player(self.bag, rack)]
        players[0].set_name(player_name)
        players[1].set_name("Bot")
        self.players = players
        self.current_player = 0

    def get_word_played(self, new_board):
        # if one letter found, need to figure out which direction word is going
        # if multiple letters, we know the direction
        old_board = self.board.board_array()
        for (i, row) in enumerate(old_board):
            for (j, letter) in enumerate(row):
                letter = letter.strip()
                if letter != new_board[i,j]:
                    # new letter
                    print("new letter \"" + letter + "\" at [" + str(i) + ", " + str(j) + "]")
                    #TODO: report new word

    def print_game(self):
        players = self.players
        print("\nRound " + str(self.round_number) + ": " + players[self.current_player].get_name() + "'s turn \n")
        print(self.board.get_board())

        print("\nLetter Racks")
        for player in players:
            print(player.get_name() + ": " + player.get_rack_str())

        print("\nScores")
        for player in players:
            print(player.get_name() + ": " + str(player.get_score()))

        print("")

    def get_board_data(self):
        return self.board.board_array()

    def bot_turn(self, player, rack):
        print('bot turn')
        word_to_play = word_rank(self.players[player].get_rack_str(), self.get_board_data(), self.round_number, self.players, player)
        output = word_to_play.format_output(self.players[player].get_rack_str())
        self.player_turn(word_to_play.word, word_to_play.location[0], word_to_play.location[1], word_to_play.direction)
        return output

    def is_ended(self):
        player = self.players[self.current_player]

        # TODO: logic for the second condition seems wrong
        #If the number of skipped turns is less than 6 and a row, and there are either tiles in the bag, or no players have run out of tiles, play the turn.
        #Otherwise, end the game.
        if (self.skipped_turns < 6) or (player.rack.get_rack_length() == 0 and self.bag.get_remaining_tiles() == 0):
            return False
        #If the number of skipped turns is over 6 or the bag has both run out of tiles and a player is out of tiles, end the game.
        else:
            return True


    # word [type string], col/row [type num], direction [r or d]
    def player_turn(self, word_to_play, row, col, direction):
        player = self.players[self.current_player]
        #Code added to let BESSIE pick a word to play
        location = []
        if (col > 14 or col < 0) or (row > 14 or row < 0):
            location = [-1, -1]
        else:
            location = [row, col]

        word = Word(word_to_play, location, player, direction, self.board.board_array())

        # return error, ask user to play different word
        word_valid = word.check_word(self.round_number, self.players)
        if (word_valid != True):
            print('INVALID WORD')
            return

        #If the user has confirmed that they would like to skip their turn, skip it.
        #Otherwise, plays the correct word and prints the board.
        if word.get_word() == "":
            print("Your turn has been skipped.")
            self.skipped_turns += 1
        else:
            word.calculate_word_score()
            word.add_score()
            self.board.place_word(word_to_play, location, direction, player, self.bag)
            self.skipped_turns = 0

        #Gets the next player.
        self.current_player += 1
        self.current_player %= 2
        if (self.current_player == 0):
            self.round_number += 1


    def end_game(self):
        #Forces the game to end when the bag runs out of tiles.
        highest_score = 0
        winning_player = ""
        for player in self.players:
            if player.get_score > highest_score:
                highest_score = player.get_score()
                winning_player = player.get_name()

        return "The game is over! " + player.get_name() + ", you have won!"
