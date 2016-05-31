
import argparse
from tkinter import Frame, Tk, Canvas, Button, BOTH, TOP, BOTTOM


BOARDS = ['debug', 'n00b', 'l33t', 'error']     #  Available sudoku boards
MARGIN = 20     #  Pixels around the board
SIDE = 50       #  Width of every board cell
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9      #  Width and Height of the entire board


class SudokuError(Exception):
    '''
        Appplication Specific Error code is here...
    '''

    pass


def parse_arguments():
    '''
        Parses arguments of the form:
            sudoku.py <board Name>
        where <board Name> must be in `BOARD` list
    '''
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--board', help='Desired Board Name', type=str, choices=BOARDS, required=True)

    args = vars(arg_parser.parse_args())
    return args['board']


class SudokuBoard(object):
    '''
        Sudoku Board representation...
    '''

    def __init__(self, board_file):
        self.board = self.__create_board(board_file)

    def __create_board(self, board_file):

        board = []

        for eachLine in board_file:
            line = eachLine.strip()
            if len(line) != 9:
                board = []
                raise SudokuError('Each line should contain 9 characters in Sudoku')

            board.append([])

            for c in line:
                if not c.isdigit():
                    raise SudokuError('Only characters accepted for the sudoku puzzle are from 0-9')

                board[-1].append(int(c))

        if len(board) != 9:
            raise SudokuError('Each Sudoku puzzle must of 9 line...')

        return board


class SudokuGame(object):
    '''
        This class is responsible for storing the state of the board and decide wheather the user has solved the game or not...
    '''

    def __init__(self, board_file):
        self.board_file = board_file
        self.start_game = SudokuBoard(board_file).board


    def start(self):
        self.game_over = False
        self.puzzle = []

        for i in range(9):
            self.puzzle.append([])
            for j in range(9):
                self.puzzle[i].append(self.start_game[i][j])


    def check_win(self):
        for row in range(9):
            if not self.__check_row(row):
                return False

        for column in range(9):
            if not self.__check_column(column):
                return False

        for row in range(3):
            for column in range(3):
                if not self.__check_square(row, column):
                    return False

        self.game_over = True

        return True

    def __check_block(self, block):
        return set(block) == set(range(1,10))

    def __check_row(self, row):
        return self.__check_block(self.puzzle[row])

    def __check_column(self, column):
        return self.__check_block([self.puzzle[row][column] for row in range(9)])

    def __check_square(self, row, column):
        return self.__check_block([
            self.puzzle[r][c]
            for r in range(row*3, (row+1)*3)
            for c in range(column*3, (column+1)*3)
        ])


class SudokuUI(Frame):
    '''
        The class responsible to create the Sudoku UI and interact with the User and accept the inputs from the User and
        run the game logic to verify the inputs of the user has led the user to win or loose the game...
    '''
    def __init__(self, parent, game):
        self.game = game
        self.parent = parent
        super(SudokuUI, self).__init__()


        self.row = 0
        self.column = 0

        self.__initUI()

    def __initUI(self):
        assert isinstance(self.parent, Tk)
        self.parent.title('Sudoku')
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        self.clear_button = Button(self, text='Clear Answers', command=self.__clear_answers)
        self.clear_button.pack(fill=BOTH, side=BOTTOM)

        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind('<Button-1>', self.__cell_clicked)
        self.canvas.bind('<Key>', self.__key_pressed)

    def __draw_grid(self):
        '''
            Draws the 3x3 grid separated by blue lines
        '''
        for i in range(10):
            color = 'blue' if i%3 == 0 else 'grey'
            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete('numbers')
        for i in range(9):
            for j in range(9):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.start_game[i][j]
                    color = 'black' if answer == original else 'sea green'
                    self.canvas.create_text(x, y, text=answer, tags='numbers', fill=color)

    def __clear_answers(self):
        self.game.start()
        self.canvas.delete('victory')
        self.__draw_puzzle()

    def __cell_clicked(self, event):
        if self.game.game_over:
            return

        x, y = event.x, event.y
        if(MARGIN < x < WIDTH - MARGIN and MARGIN < y <HEIGHT - MARGIN):
            self.canvas.focus_set()

            row, col = (y - MARGIN)/SIDE, (x - MARGIN)/SIDE
            if (row, col) == (self.row, self.column):
                self.row, self.column = -1, -1
            else:
                self.row, self.column = row, col

        self.__draw_cursor()

    def __draw_cursor(self):
        self.canvas.delete('cursor')
        if self.row >= 0 and self.column >= 0:
            x0 = MARGIN + self.column * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.column + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1

            self.canvas.create_rectangle(x0, y0, x1, y1, outline='red', tags='cursor')

    def __key_pressed(self, event):
        if self.game.game_over:
            return
        if self.row >= 0 and self.column >= 0 and event.char in '1234567890':
            self.game.puzzle[int(self.row)][int(self.column)] = int(event.char)
            self.row, self.column = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()
            if self.game.check_win():
                self.__draw_victory()

    def __draw_victory(self):
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(x0, y0, x1, y1, tags='victory', fill='dark orange', outline='orange')

        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(x, y, text='You Win!!!', fill='white', font=('Arial', 32), tags='winner')


if __name__ == '__main__':
    board_name = parse_arguments()

    with open('%s.sudoku' % board_name, 'r') as board_file:
        game = SudokuGame(board_file)
        game.start()

        root = Tk()
        SudokuUI(root, game)

        root.geometry('%dx%d' % (WIDTH, HEIGHT + 40))
        root.mainloop()