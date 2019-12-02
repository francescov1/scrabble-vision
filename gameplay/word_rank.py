from itertools import combinations
from bisect import bisect_left
from gameplay.word_position import word_position
import gameplay.scrabble as scrabble

# TODO incorperate blank tiles, randomly breaks probably should look into that

# Load words from the anagram text file
def load_vars():
    f = open("gameplay/anadict.txt", 'r')
    ana_dict = f.read().split('\n')
    f.close()
    return ana_dict

# Find anagrams of all possible combanations of the rack,
# always including a letter on the board
def find_words(rack, ana_dict, board_ltr):
    rack = ''.join(sorted(rack))
    found_words = []
    for i in range(1, len(rack)+1):
        for comb in combinations(rack, i):
            if board_ltr != '':
                comb = tuple(board_ltr) + comb
            ana = ''.join(sorted(comb))
            j = bisect_left(ana_dict, ana)
            if j == len(ana_dict):
                continue
            words = ana_dict[j].split()
            if words[0] == ana:
                for word in words[1:]:
                    if word.find(board_ltr) != -1:
                        found_words.append(word)
    return found_words

# Given a playable word calculate location to place the fist letter
def get_word(word, word_info, board, player):
    board_ltr = ''.join(word_info['letters'])
    board_ltr = board_ltr.lower().strip()
    ltr_split = word.split(board_ltr)
    row = word_info['row']
    col = word_info['col']
    # In the case of the first turn where there aren't words to play around
    if len(ltr_split[0]) == len(word):
        ltr_split[0] = ''
    # On all other turns position the starting letter such that
    # the letters already on the board line up with the word
    else:
        if word_info['direction'] == 'r':
            col = col - len(ltr_split[0])
        elif word_info['direction'] == 'd':
            row = row - len(ltr_split[0])
    return scrabble.Word(word, [row, col], player, word_info['direction'], board)

#  Find list of playable words given a list of valid positions
#  returns list of words sorted by highest score
def get_top_words(playable, board, rack, players, player, round_number):
    ana_dict = load_vars()
    scored = []
    for info in playable:
        # Check to see if it is the first turn (no board letters to play around)
        if board[7][7] == ' * ':
            board_ltr = ''
        else:
            board_ltr = ''.join(info['letters']).lower().strip()
        found_words = set(find_words(rack, ana_dict, board_ltr))
        # put word objects
        for word in found_words:
            word_obj = get_word(word, info, board, players[player])
            check = word_obj.check_word(round_number, players)
            if check == True:
                score = word_obj.calculate_word_score()
                scored.append({'word': word_obj, 'score': score})
    return sorted(scored, key=lambda k: k['score'], reverse=True)

# Given a players rack and the board find the highest scoring valid
# word to play and return information needed to play
def word_rank(rack, board, round_number, players, player):
    mod_rack = rack.split(", ").copy()
    mod_rack = [x.lower() for x in mod_rack]
    playable = word_position(board)
    scored = get_top_words(playable, board, mod_rack, players, player, round_number)
    return scored[0]['word']
