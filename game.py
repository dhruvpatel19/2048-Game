import random
from tkinter import Frame, Label, CENTER

import operations
import constants as c


class Board(Frame):
    def __init__(self):
        Frame.__init__(self)
        global score
        global high_score
        score = 0
        with open("scores.txt", "r") as f:
            high_score = int(f.read())
        self.grid()
        self.master.title('2048 - A TKinter Game')
        self.master.bind("<Key>", self.key_down)

        self.commands = {c.KEY_UP: operations.move_up, c.KEY_DOWN: operations.move_down,
                         c.KEY_LEFT: operations.move_left, c.KEY_RIGHT: operations.move_right,
                         c.KEY_UP_ALT: operations.move_up, c.KEY_DOWN_ALT: operations.move_down,
                         c.KEY_LEFT_ALT: operations.move_left, c.KEY_RIGHT_ALT: operations.move_right}

        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        self.label = Label(self, text="Your Score: " + str(score) + "            Your High Score: " + str(high_score), bg="white", justify=CENTER, font=("Verdana", 18, "bold"), width = 53, height=2)
        self.label.grid()

        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR_GAME,
                           width=c.SIZE, height=c.SIZE)
        background.grid()

        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(background, bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                             width=c.SIZE / c.GRID_LEN,
                             height=c.SIZE / c.GRID_LEN)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING,
                          pady=c.GRID_PADDING)
                t = Label(master=cell, text="",
                          bg=c.BACKGROUND_COLOR_CELL_EMPTY,
                          justify=CENTER, font=c.FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def gen(self):
        return random.randint(0, c.GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = operations.new_game(4)
        self.history_matrixs = list()
        self.matrix = operations.make_two(self.matrix)
        self.matrix = operations.make_two(self.matrix)

    def update_grid_cells(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(
                        text="", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(
                        new_number), bg=c.BACKGROUND_COLOR_DICT[new_number],
                        fg=c.CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def key_down(self, event):
        global score
        global high_score
        key = repr(event.keysym)
        if key == c.KEY_UNDO and len(self.history_matrixs) > 1:
            self.matrix = self.history_matrixs.pop()
            self.update_grid_cells()
            print('back on step total step:', len(self.history_matrixs))
        elif key in self.commands:
            self.matrix, done, pts = self.commands[repr(event.keysym)](self.matrix)
            if done:
                self.matrix = operations.make_two(self.matrix)
                # record last move
                self.history_matrixs.append(self.matrix)
                self.update_grid_cells()
                done = False
                if operations.game_status(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text="Win!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                if operations.game_status(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(
                        text="You", bg=c.BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(
                        text="Lose!", bg=c.BACKGROUND_COLOR_CELL_EMPTY)

            score += pts
            self.label["text"] = "Your Score: " + str(score) + "            Your High Score: " + str(high_score)

        def high_score_1(self):
            global score
            global high_score
            if score > high_score:
                with open("scores.txt", "w") as f:
                    f.write(str(score))
                f.close()

        high_score_1(self)

    def generate_new(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2



game_board = Board()