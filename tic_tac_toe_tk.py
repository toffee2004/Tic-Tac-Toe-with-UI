#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tic-Tac-Toe GUI (Tkinter)
- Modes: Player vs Player, Player vs Computer (unbeatable AI via minimax)
- Single file, no extra dependencies
"""
import tkinter as tk
from tkinter import messagebox

CELL_SIZE = 110
PADDING = 14
FONT_BTN = ("Segoe UI", 28, "bold")
FONT_STATUS = ("Segoe UI", 12, "bold")
BG = "#0f172a"      # slate-900
FG = "#e2e8f0"      # slate-200
ACCENT = "#22c55e"  # green-500
ACCENT2 = "#38bdf8" # sky-400
DISABLED = "#64748b" # slate-500

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe (Tkinter)")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.mode = tk.StringVar(value="pve")  # "pvp" or "pve"
        self.current = "X"
        self.board = [""] * 9
        self.game_over = False

        # Layout
        self._build_menu()
        self._build_board()
        self._build_status()

        self._update_status()

        # If AI starts (optional toggle), keep human X by default
        # self.current = "O"; self.root.after(300, self.ai_move)

    # ----- UI Build -----
    def _build_menu(self):
        top = tk.Frame(self.root, bg=BG)
        top.grid(row=0, column=0, sticky="ew", padx=PADDING, pady=(PADDING, 0))

        lbl = tk.Label(top, text="Mode:", bg=BG, fg=FG, font=("Segoe UI", 11))
        lbl.pack(side="left")

        r1 = tk.Radiobutton(top, text="Player vs Computer", variable=self.mode, value="pve",
                            bg=BG, fg=FG, selectcolor=BG, activebackground=BG,
                            activeforeground=FG, highlightthickness=0, font=("Segoe UI", 11),
                            command=self.reset)
        r1.pack(side="left", padx=(8, 0))

        r2 = tk.Radiobutton(top, text="Player vs Player", variable=self.mode, value="pvp",
                            bg=BG, fg=FG, selectcolor=BG, activebackground=BG,
                            activeforeground=FG, highlightthickness=0, font=("Segoe UI", 11),
                            command=self.reset)
        r2.pack(side="left", padx=12)

        self.btn_reset = tk.Button(top, text="Reset", command=self.reset,
                                   bg=ACCENT, fg="#0b1220", bd=0, relief="flat",
                                   activebackground=ACCENT2, activeforeground="#07101d",
                                   font=("Segoe UI", 11, "bold"), padx=10, pady=6,
                                   cursor="hand2")
        self.btn_reset.pack(side="right")

    def _build_board(self):
        board_frame = tk.Frame(self.root, bg=BG, bd=0, highlightthickness=0)
        board_frame.grid(row=1, column=0, padx=PADDING, pady=PADDING)

        self.buttons = []
        for r in range(3):
            for c in range(3):
                idx = r * 3 + c
                b = tk.Button(board_frame, text="", width=3, height=1,
                              font=FONT_BTN, bg="#111827", fg=FG, activebackground="#0b1220",
                              activeforeground=FG, bd=0, relief="flat",
                              cursor="hand2",
                              command=lambda i=idx: self.on_click(i))
                b.grid(row=r, column=c, padx=6, pady=6, ipadx=18, ipady=12, sticky="nsew")
                self.buttons.append(b)

        # Expand grid cells evenly (nice spacing)
        for i in range(3):
            board_frame.grid_columnconfigure(i, weight=1, minsize=CELL_SIZE)
            board_frame.grid_rowconfigure(i, weight=1, minsize=CELL_SIZE)

    def _build_status(self):
        bottom = tk.Frame(self.root, bg=BG)
        bottom.grid(row=2, column=0, sticky="ew", padx=PADDING, pady=(0, PADDING))

        self.status = tk.Label(bottom, text="", bg=BG, fg=FG, font=FONT_STATUS, anchor="w")
        self.status.pack(side="left")

    # ----- Core Game Logic -----
    def on_click(self, i):
        if self.game_over or self.board[i] != "":
            return

        # Human move
        self.board[i] = self.current
        self._render()
        winner = self._check_winner()
        if winner or self._is_full():
            self._end_game(winner)
            return

        # Switch player
        self.current = "O" if self.current == "X" else "X"
        self._update_status()

        # AI move if PvE and it's O's turn
        if self.mode.get() == "pve" and self.current == "O" and not self.game_over:
            self.root.after(200, self.ai_move)

    def ai_move(self):
        # Unbeatable AI using minimax with simple heuristics
        best_score = -float("inf")
        best_move = None
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = self._minimax(is_maximizing=False, alpha=-float("inf"), beta=float("inf"))
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i

        if best_move is not None:
            self.board[best_move] = "O"
            self._render()
            winner = self._check_winner()
            if winner or self._is_full():
                self._end_game(winner)
                return
            self.current = "X"
            self._update_status()

    def _minimax(self, is_maximizing, alpha, beta):
        winner = self._check_winner()
        if winner == "O":
            return 10
        elif winner == "X":
            return -10
        elif self._is_full():
            return 0

        if is_maximizing:
            best = -float("inf")
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = "O"
                    score = self._minimax(False, alpha, beta)
                    self.board[i] = ""
                    best = max(best, score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
            return best
        else:
            best = float("inf")
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = "X"
                    score = self._minimax(True, alpha, beta)
                    self.board[i] = ""
                    best = min(best, score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            return best

    def _check_winner(self):
        lines = [
            (0,1,2),(3,4,5),(6,7,8), # rows
            (0,3,6),(1,4,7),(2,5,8), # cols
            (0,4,8),(2,4,6)          # diags
        ]
        for a,b,c in lines:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def _is_full(self):
        return all(cell != "" for cell in self.board)

    def _end_game(self, winner):
        self.game_over = True
        if winner:
            self.status.configure(text=f"{winner} thắng! Nhấn Reset để chơi lại.", fg=ACCENT)
            # highlight winning line
            self._highlight_win(winner)
        else:
            self.status.configure(text="Hoà! Nhấn Reset để chơi lại.", fg=ACCENT2)

        # disable remaining buttons
        for i, b in enumerate(self.buttons):
            if self.board[i] == "":
                b.configure(state="disabled", fg=DISABLED)

    def _highlight_win(self, winner):
        # Recompute winning line to highlight
        lines = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for a,b,c in lines:
            if self.board[a] == self.board[b] == self.board[c] == winner:
                for idx in (a,b,c):
                    self.buttons[idx].configure(fg=ACCENT if winner == "X" else ACCENT2)
                break

    def _render(self):
        for i, b in enumerate(self.buttons):
            b.configure(text=self.board[i])
            if self.board[i] != "":
                b.configure(state="disabled")
        self._update_status()

    def _update_status(self):
        if self.game_over:
            return
        if self.mode.get() == "pve":
            turn_text = "Bạn (X)" if self.current == "X" else "Máy (O)"
        else:
            turn_text = f"Lượt của {self.current}"
        self.status.configure(text=f"Chế độ: {'PvsE' if self.mode.get() == 'pve' else 'PvsP'}  •  {turn_text}",
                              fg=FG)

    def reset(self):
        self.board = [""] * 9
        self.current = "X"
        self.game_over = False
        for b in self.buttons:
            b.configure(text="", state="normal", fg=FG)
        self._update_status()

def main():
    root = tk.Tk()
    app = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()
