import numpy as np
from tkinter import *

canvas_size = 800
token_size = canvas_size / 10
x_color = 'red'
o_color = 'blue'


class tictactoe():
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.window.bind('<Button-1>', self.event_handler)
        self.canvas = Canvas(self.window, width=canvas_size, height=canvas_size)
        self.canvas.pack()

        self.board_grid()
        self.x_turn = True
        self.gameboard = np.zeros(shape=(3, 3))

        self.x_points = 0
        self.o_points = 0
        self.tie_points = 0
        self.tie = False
        self.x_won = False
        self.o_won = False

        self.x_start = True
        self.restart = False
        self.gameover = False

    def board_grid(self):
        for i in range(2):
            self.canvas.create_line(0, (i + 1) * canvas_size / 3, canvas_size, (i + 1) * canvas_size / 3)
            self.canvas.create_line((i + 1) * canvas_size / 3, 0, (i + 1) * canvas_size / 3, canvas_size)

    def grid_to_pixel(self, grid_value):
        return (canvas_size / 3) * np.array(grid_value, dtype=int) + canvas_size / 6

    def pixel_to_grid(self, pixel_value):
        return np.array(np.array(pixel_value) // (canvas_size / 3), dtype=int)

    def is_marked(self, grid_value):
        return not self.gameboard[grid_value[0]][grid_value[1]] == 0

    def draw_O(self, grid_value):
        pixel_value = self.grid_to_pixel(grid_value)
        self.canvas.create_oval(pixel_value[0] - token_size, pixel_value[1] - token_size,
                                pixel_value[0] + token_size, pixel_value[1] + token_size, width=50,
                                outline=o_color)

    def draw_X(self, grid_value):
        pixel_value = self.grid_to_pixel(grid_value)
        self.canvas.create_line(pixel_value[0] - token_size, pixel_value[1] - token_size,
                                pixel_value[0] + token_size, pixel_value[1] + token_size, width=50,
                                fill=x_color)
        self.canvas.create_line(pixel_value[0] - token_size, pixel_value[1] + token_size,
                                pixel_value[0] + token_size, pixel_value[1] - token_size, width=50,
                                fill=x_color)

    def gameover_screen(self):
        self.canvas.delete("all")
        if self.x_won:
            self.x_points += 1
            text = 'X won!'
            color = x_color
        elif self.o_won:
            self.o_points += 1
            text = 'O won!'
            color = o_color
        else:
            self.tie_points += 1
            text = 'Tie!'
            color = 'orange'

        self.canvas.create_text(canvas_size / 2, canvas_size / 3, font=("Purisa", 100), fill=color, text=text)

        score_text = 'Player X: ' + str(self.x_points) + '\n'
        score_text += 'Player O: ' + str(self.o_points) + '\n'
        score_text += 'Tie: ' + str(self.tie_points)
        self.canvas.create_text(canvas_size / 2, canvas_size * 0.75, font=("Purisa", 40), fill='green', text=score_text)
        self.restart = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(canvas_size / 2, canvas_size * 0.1, font="Purisa", fill="gray", text=score_text)

    def is_winner(self, player):
        player = -1 if player == 'X' else 1
        for i in range(3):
            if (self.gameboard[i][0] == self.gameboard[i][1] == self.gameboard[i][2] == player) or (self.gameboard[0][i] == self.gameboard[1][i] == self.gameboard[2][i] == player):
                return True
            if (self.gameboard[0][0] == self.gameboard[1][1] == self.gameboard[2][2] == player) or (self.gameboard[0][2] == self.gameboard[1][1] == self.gameboard[2][0] == player):
                return True
        return False

    def is_tie(self):
        row, col = np.where(self.gameboard == 0)
        tie = False
        if len(row) == 0:
            tie = True
        return tie

    def is_gameover(self):
        self.x_won = self.is_winner('X')
        if not self.x_won:
            self.o_won = self.is_winner('O')
        if not self.o_won:
            self.tie = self.is_tie()
        gameover = self.x_won or self.o_won or self.tie

        if self.x_won:
            print('X won!')
        if self.o_won:
            print('O won!')
        if self.tie:
            print('Tie!')

        return gameover

    def play_again(self):
        self.board_grid()
        self.x_start = not self.x_start
        self.x_turn = self.x_start
        self.gameboard = np.zeros(shape=(3, 3))

    def event_handler(self, event):
        pixel_value = [event.x, event.y]
        grid_value = self.pixel_to_grid(pixel_value)

        if not self.restart:
            if self.x_turn:
                if not self.is_marked(grid_value):
                    self.draw_X(grid_value)
                    self.gameboard[grid_value[0]][grid_value[1]] = -1
                    self.x_turn = not self.x_turn
            else:
                if not self.is_marked(grid_value):
                    self.draw_O(grid_value)
                    self.gameboard[grid_value[0]][grid_value[1]] = 1
                    self.x_turn = not self.x_turn
            if self.is_gameover():
                self.gameover_screen()
        else:
            self.canvas.delete("all")
            self.play_again()
            self.restart = False


game_instance = tictactoe()
game_instance.window.mainloop()
