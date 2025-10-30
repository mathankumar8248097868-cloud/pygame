import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []

        for i in range(9):
            button = tk.Button(self.window, text="", width=10, height=3, command=lambda x=i: self.button_click(x))
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)

    def button_click(self, index):
        if self.board[index] == "":
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.window.quit()
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.window.quit()
            self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        win_conditions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for a, b, c in win_conditions:
            if self.board[a] == self.board[b] == self.board[c] != "":
                return True
        return False

    def run(self):
        self.window.mainloop()

game = TicTacToe()
game.run()
