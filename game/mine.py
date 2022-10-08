"""
Implementation of command-line minesweeper by Kylie Ying

YouTube Kylie Ying: https://www.youtube.com/ycubed
Twitch KylieYing: https://www.twitch.tv/kylieying
Twitter @kylieyying: https://twitter.com/kylieyying
Instagram @kylieyying: https://www.instagram.com/kylieyying/
Website: https://www.kylieying.com
Github: https://www.github.com/kying18
Programmer Beast Mode Spotify playlist: https://open.spotify.com/playlist/4Akns5EUb3gzmlXIdsJkPs?si=qGc4ubKRRYmPHAJAIrCxVQ

Project specs, files, code all over the place? Start using Backlog for efficient management!! There is a free tier: https://cutt.ly/ehxImv5
"""
import pickle
import random
import re

# lets create a board object to represent the minesweeper game
# this is so that we can just say "create a new board object", or
# "dig here", or "render this game for this object"
from base.base import BaseFunc


class Board:
    def __init__(self, dim_size, num_bombs):
        # let's keep track of these parameters. they'll be helpful later
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # let's create the board
        # helper function!
        self.board = self.make_new_board()  # plant the bombs
        self.assign_values_to_board()

        # initialize a set to keep track of which locations we've uncovered
        # we'll save (row,col) tuples into this set
        self.dug = set()  # if we dig at 0, 0, then self.dug = {(0,0)}
        self.safe = True

    def make_new_board(self):
        # construct a new board based on the dim size and num bombs
        # we should construct the list of lists here (or whatever representation you prefer,
        # but since we have a 2-D board, list of lists is most natural)

        # generate a new board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        # this creates an array like this:
        # [[None, None, ..., None],
        #  [None, None, ..., None],
        #  [...                  ],
        #  [None, None, ..., None]]
        # we can see how this represents a board!

        # plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size ** 2 - 1)  # return a random integer N such that a <= N <= b
            row = loc // self.dim_size  # we want the number of times dim_size goes into loc to tell us what row to look at
            col = loc % self.dim_size  # we want the remainder to tell us what index in that row to look at

            if board[row][col] == '*':
                # this means we've actually planted a bomb there already so keep going
                continue

            board[row][col] = '*'  # plant the bomb
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        # now that we have the bombs planted, let's assign a number 0-8 for all the empty spaces, which
        # represents how many neighboring bombs there are. we can precompute these and it'll save us some
        # effort checking what's around the board later on :)
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # if this is already a bomb, we don't want to calculate anything
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        # let's iterate through each of the neighboring positions and sum number of bombs
        # top left: (row-1, col-1)
        # top middle: (row-1, col)
        # top right: (row-1, col+1)
        # left: (row, col-1)
        # right: (row, col+1)
        # bottom left: (row+1, col-1)
        # bottom middle: (row+1, col)
        # bottom right: (row+1, col+1)

        # make sure to not go out of bounds!

        num_neighboring_bombs = 0
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if r == row and c == col:
                    # our original location, don't check
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
        # dig at that location!
        # return True if successful dig, False if bomb dug

        # a few scenarios:
        # hit a bomb -> game over
        # dig at location with neighboring bombs -> finish dig
        # dig at location with no neighboring bombs -> recursively dig neighbors!

        self.dug.add((row, col))  # keep track that we dug here

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        # self.board[row][col] == 0
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if (r, c) in self.dug:
                    continue  # don't dig where you've already dug
                self.dig(r, c)

        # if our initial dig didn't hit a bomb, we *shouldn't* hit a bomb here
        return True

    def __str__(self):
        # this is a magic function where if you call print on this object,
        # it'll print out what this function returns!
        # return a string that shows the board to the player

        # first let's create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = '  '

        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '*   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += ' '.join(cells)  # 第一排
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size) - 3
        string_rep = indices_row + '-' * str_len + '\n' + string_rep + '-' * str_len

        return string_rep


# play the game
def play(wechat, room_wxid, from_wxid, dim_size=10, num_bombs=10):
    # Step 1: create the board and plant the bombs
    board = Board(dim_size, num_bombs)

    # Step 2: show the user the board and ask for where they want to dig
    # Step 3a: if location is a bomb, show game over message
    # Step 3b: if location is not a bomb, dig recursively until each square is at least
    #          next to a bomb
    # Step 4: repeat steps 2 and 3a/b until there are no more places to dig -> VICTORY!
    safe = True

    # ckd write
    f = open('ceshi.pickle', 'wb')
    pickle.dump(board, f)
    f.close()
    print(board)
    BaseFunc().send_textmsg(wechat, room_wxid, from_wxid, str(board), str(board))

    tip = '你想从哪里开始扫呢？ \n请输入行数和列数（例如2,4）:'
    BaseFunc().send_textmsg(wechat, room_wxid, from_wxid, tip, tip)
    # fs = open('ceshi.pickle', 'rb')
    # objFromPickle = pickle.load(fs)
    # print('打印对象本身:', objFromPickle)
    # print('打印对象类型:', type(board))


def plays(wechat, to_wxid, msg, bf):
    try:
        fs = open('ceshi.pickle', 'rb')
        board = pickle.load(fs)
        # print('打印对象本身:', board)
        # print('plays')
        fs.close()
        while len(board.dug) < board.dim_size ** 2 - board.num_bombs:
            # print(type(board))

            # print('send msg')
            # 0,0 or 0, 0 or 0,    0
            user_input = re.split(',(\\s)*', msg)  # '0, 3'
            row, col = int(user_input[0]), int(user_input[-1])
            if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
                error = '无效参数，请重试。'
                wechat.send_text(to_wxid, error)
                return

            # if it's valid, we dig
            board.safe = board.dig(row, col)
            print(board)
            # ckd write
            wechat.send_text(to_wxid, str(board))
            f = open('ceshi.pickle', 'wb')
            pickle.dump(board, f)
            f.close()
            if not board.safe:
                # dug a bomb ahhhhhhh
                break  # (game over rip)
            tip = '你想从哪里开始扫呢？ \n请输入行数和列数（例如2,4）: '
            wechat.send_text(to_wxid, tip)
            return

        # 2 ways to end loop, lets check which one
        if board.safe:
            win = '恭喜！！！ 你赢啦!'
            print(win)
            wechat.send_text(to_wxid, win)
            bf.into_mine_signal = True
            bf.mine_signal = False
        else:
            failure = 'SORRY GAME OVER :('
            print(failure)
            wechat.send_text(to_wxid, failure)
            # let's reveal the whole board!
            board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
            print(board)
            wechat.send_text(to_wxid, str(board))
            bf.into_mine_signal = True
            bf.mine_signal = False
    except Exception as e:
        print(e)
        wechat.send_text(to_wxid, str(e))
        wechat.send_text(to_wxid, '请重试')
        return

#
# if __name__ == '__main__':  # good practice :)
#     play(1, 1, 1)
#     plays()