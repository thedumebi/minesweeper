import random
import re

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # create the board
        self.board = self.make_new_board()
        self.assign_values_to_board()

        # initialize a set to keep track of which locations we've uncovered
        # we'll save (row, col) tuples into this set
        self.dug = set() #if we dig at 0, 1 then self.dug = {(0,1)}

    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        #plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1) #return a random integer N such that a <= N <= b
            row = loc // self.dim_size #we want the number of times dim_size goes into loc to tell us the row
            col = loc % self.dim_size #we want the remainder to tell us what index in that row to look

            if board[row][col] == "*":
                # this means we've actually planted a bomb there already so continue going
                continue

            board[row][col] = "*" #plant the bomb
            bombs_planted += 1
        
        return board

    def assign_values_to_board(self):
        # assign a number 0-8 for all empty spaces, which represents how many neighbouring bombs there are.
        for r in range (self.dim_size):
            for c in range (self.dim_size):
                if self.board[r][c] == "*":
                    # if it's a bomb, we don't want to do anything.
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        # iterate through each of the neihbouring positions and sum number of bombs
        # top left: (row-1, col-1)
        # top middle: (row-1, col)
        # top right: (row-1, col+1)
        # left: (row, col-1)
        # right: (row, col+1)
        # bottom left: (row+1, col-1)
        # bottom middle: (row+1, col)
        # bottom right: (row+1, col+1)

        # make sure we don't go out if bounds

        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    # our original location, don't check
                    continue
                if self.board[r][c] == "*":
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
        # dig at that location
        # return true if successful dig, false if bomb dug

        # a few scenarios:
        # hit a bomb -> game over
        # dig at a location near a bomb -> finish dig
        # dig at a location with no neighboring bombs -> recursively dig neighbors

        self.dug.add((row, col)) #keep track that we dug here

        if self.board[row][col] == "*":
            return False
        elif self.board[row][col] > 0:
            return True

        # self.board[row][col] == 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue #don't dig where you've already dug
                self.dig(r, c)

        # if our initial dig didnt hit a bomb, we should not hit a bomb here
        return True

    def __str__(self):
        # if you call print in this object, it'll print what this function returns
        # return a string that shows the board to the player

        # first create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = " "

        # put together the board representation in a string
        string_rep = ""
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = "   "
        cells = []
        for idx, col in enumerate(indices):
            format = "%-" + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += "  ".join(cells)
        indices_row += " \n"

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f"{i} |"
            cells = []
            for idx, col in enumerate(row):
                format = "%-" + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += " |".join(cells)
            string_rep += " |\n"

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + "-"*str_len + "\n" + string_rep + "-"*str_len

        return string_rep

def play(dim_size=10, num_bombs=10):
    # step 1: create the board and plant the bombs
    board = Board(dim_size, num_bombs)

    # step 2: show the user the board and ask for where they want to dig
    # step 3a: if location is a bomb, show game over message
    # step 3b: if location is not a bomb, dig recursively until each square is at least next to a bomb
    # step 4: repeat steps 2 and 3a/b until there are no more places to dig -> victory!

    safe = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        #0,0 or 0, 0 or 0,   0
        user_input = re.split(",(\\s)*" ,input("where would you like to dig? Input as row,col: \n")) #0, 5
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try again")
            continue

        if (row, col) in board.dug:
            print("You have already dug here")
            continue
        
        # if it's valid, we dig
        safe = board.dig(row, col)
        if not safe:
            # dug a bomb
            break

    if safe:
        print("CONGRATULATIONS!!! YOU ARE VICTORIOUS!")
    else:
        print("SORRY, GAME OVER :(")
        # reveal the whole board
    board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
    print(board)


if __name__ == "__main__":
    play()
