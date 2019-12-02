def get_letter_group(letters, direction, col, row):
    return {'letters': letters, 
            'direction': direction, 
            'col': col, 
            'row': row,
            'length': len(letters)}

def get_ltr_groups(word_indx, board, playable, direction):
    i = 0
    while i < len(word_indx):
        col = word_indx[i][1]
        row = word_indx[i][0]
        letters = [board[row][col].strip()]
        if i == len(word_indx) - 1:
            letter_group = get_letter_group(letters, direction, col, row)
            playable.append(letter_group)
            break
        if direction == 'd':
            nxt = row + 1
            group = col
            order = [0, 1]
        else:
            nxt = col + 1
            group = row
            order = [1, 0]
        for j in range(i + 1, len(word_indx)):
            if word_indx[j][order[0]] == nxt and word_indx[j][order[1]] == group:
                if direction == 'd':
                    letters.append(board[nxt][col].strip())
                else:
                    letters.append(board[row][nxt].strip())
                nxt += 1
                if j == len(word_indx) - 1:
                    i = j + 1
            else:
                i = j
                break
        letter_group = get_letter_group(letters, direction, col, row)
        playable.append(letter_group)
    return playable

# given the current state of the board find all viable tiles to play a word around 
# (ex. a tile without tiles on its left or right, or top and bottom)
def word_position(board):
    word_indx = []
    playable = []
    for i in range(0, len(board)):
        for j in range(0, len(board)):
            if board[i][j][0].isspace() and not board[i][j][1].isspace():
                word_indx.append([i, j])
    playable = get_ltr_groups(word_indx, board, playable, 'r')
    word_indx = sorted(word_indx, key=lambda x: x[1])
    return get_ltr_groups(word_indx, board, playable, 'd')
