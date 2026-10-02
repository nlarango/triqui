import tkinter as tk
from tkinter import messagebox
import random

class TriquiGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 ¡TRIQUI! 🎮")
        self.root.geometry("600x700")
        self.root.configure(bg="#2C3E50")

        # Variables del juego
        self.board = [""] * 9
        self.human = "X"
        self.ai = "O"
        self.current_player = self.human
        self.game_over = False
        self.wins_human = 0
        self.wins_ai = 0
        self.draws = 0

        # Colores vibrantes
        self.colors = {
            "bg_main": "#2C3E50",
            "bg_button": "#ECF0F1",
            "bg_hover": "#BDC3C7",
            "x_color": "#E74C3C",
            "o_color": "#3498DB",
            "empty": "#ECF0F1",
            "text": "#2C3E50"
        }

        self.setup_ui()

    def setup_ui(self):
        # Título
        title_frame = tk.Frame(self.root, bg=self.colors["bg_main"])
        title_frame.pack(pady=20)

        title = tk.Label(
            title_frame,
            text="🎮 ¡TRIQUI! 🎮",
            font=("Arial", 40, "bold"),
            bg=self.colors["bg_main"],
            fg="#F39C12"
        )
        title.pack()

        subtitle = tk.Label(
            title_frame,
            text="¡El Juego del Tres en Raya!",
            font=("Arial", 16),
            bg=self.colors["bg_main"],
            fg="#ECF0F1"
        )
        subtitle.pack()

        # Panel de estadísticas
        stats_frame = tk.Frame(self.root, bg="#34495E", relief=tk.RAISED, bd=2)
        stats_frame.pack(pady=10, padx=20, fill=tk.X)

        stats_label = tk.Label(
            stats_frame,
            text="📊 MARCADOR",
            font=("Arial", 12, "bold"),
            bg="#34495E",
            fg="#F39C12"
        )
        stats_label.pack()

        stats_content_frame = tk.Frame(stats_frame, bg="#34495E")
        stats_content_frame.pack(pady=5)

        self.stats_text = tk.Label(
            stats_content_frame,
            text=f"Tú: {self.wins_human}  |  Computadora: {self.wins_ai}  |  Empates: {self.draws}",
            font=("Arial", 12),
            bg="#34495E",
            fg="#ECF0F1"
        )
        self.stats_text.pack()

        # Tablero
        board_frame = tk.Frame(self.root, bg=self.colors["text"], relief=tk.RAISED, bd=3)
        board_frame.pack(pady=20, padx=20)

        self.buttons = []
        for i in range(9):
            row = i // 3
            col = i % 3

            btn = tk.Button(
                board_frame,
                text="",
                font=("Arial", 36, "bold"),
                width=6,
                height=2,
                bg=self.colors["empty"],
                fg=self.colors["text"],
                activebackground=self.colors["bg_hover"],
                relief=tk.RAISED,
                bd=3,
                command=lambda idx=i: self.on_button_click(idx)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(btn)

        # Panel de mensajes
        message_frame = tk.Frame(self.root, bg=self.colors["bg_main"])
        message_frame.pack(pady=10)

        self.message_label = tk.Label(
            message_frame,
            text="¡Tu turno! (X)",
            font=("Arial", 14, "bold"),
            bg=self.colors["bg_main"],
            fg="#2ECC71"
        )
        self.message_label.pack()

        # Botones de control
        button_frame = tk.Frame(self.root, bg=self.colors["bg_main"])
        button_frame.pack(pady=15)

        new_game_btn = tk.Button(
            button_frame,
            text="🔄 Nuevo Juego",
            font=("Arial", 12, "bold"),
            bg="#27AE60",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=2,
            command=self.new_game
        )
        new_game_btn.pack(side=tk.LEFT, padx=10)

        reset_btn = tk.Button(
            button_frame,
            text="🔁 Reiniciar Marcador",
            font=("Arial", 12, "bold"),
            bg="#E74C3C",
            fg="white",
            padx=20,
            pady=10,
            relief=tk.RAISED,
            bd=2,
            command=self.reset_score
        )
        reset_btn.pack(side=tk.LEFT, padx=10)

    def on_button_click(self, index):
        if not self.game_over and self.board[index] == "" and self.current_player == self.human:
            self.board[index] = self.human
            self.update_button(index)

            # Verificar si el humano ganó
            if self.check_winner(self.human):
                self.end_game(f"¡🎉 ¡GANASTE! 🎉\nFelicidades, ¡lo hiciste muy bien!")
                self.wins_human += 1
                return

            # Verificar empate
            if self.is_board_full():
                self.end_game("🤝 ¡EMPATE! Ambos jugamos bien.")
                self.draws += 1
                return

            # Turno de la IA
            self.current_player = self.ai
            self.message_label.config(text="🤖 La computadora está pensando...", fg="#3498DB")
            self.root.after(500, self.ai_move)

    def ai_move(self):
        # Estrategia de IA: Minimax simple con un poco de aleatoriedad
        best_score = float('-inf')
        best_move = None

        # Primero, intentar ganar
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = self.ai
                if self.check_winner(self.ai):
                    best_move = i
                    self.board[i] = ""
                    break
                self.board[i] = ""

        # Si no puede ganar, bloquear al humano
        if best_move is None:
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = self.human
                    if self.check_winner(self.human):
                        best_move = i
                        self.board[i] = ""
                        break
                    self.board[i] = ""

        # Si no, tomar el centro
        if best_move is None and self.board[4] == "":
            best_move = 4

        # Si no, tomar una esquina
        if best_move is None:
            corners = [0, 2, 6, 8]
            available_corners = [c for c in corners if self.board[c] == ""]
            if available_corners:
                best_move = random.choice(available_corners)

        # Si no, tomar cualquier casilla disponible
        if best_move is None:
            available = [i for i in range(9) if self.board[i] == ""]
            best_move = random.choice(available)

        # Hacer el movimiento de la IA
        self.board[best_move] = self.ai
        self.update_button(best_move)

        # Verificar si la IA ganó
        if self.check_winner(self.ai):
            self.end_game("😢 La computadora ganó.\n¡Pero tú puedes hacerlo mejor!")
            self.wins_ai += 1
            return

        # Verificar empate
        if self.is_board_full():
            self.end_game("🤝 ¡EMPATE! Ambos jugamos bien.")
            self.draws += 1
            return

        # Volver al turno del humano
        self.current_player = self.human
        self.message_label.config(text="¡Tu turno! (X)", fg="#2ECC71")

    def update_button(self, index):
        btn = self.buttons[index]
        player = self.board[index]

        if player == self.human:
            btn.config(text="X", fg=self.colors["x_color"], state=tk.DISABLED)
        elif player == self.ai:
            btn.config(text="O", fg=self.colors["o_color"], state=tk.DISABLED)

    def check_winner(self, player):
        # Combinaciones ganadoras
        winning_combos = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]

        for combo in winning_combos:
            if all(self.board[i] == player for i in combo):
                return True
        return False

    def is_board_full(self):
        return all(cell != "" for cell in self.board)

    def end_game(self, message):
        self.game_over = True
        self.message_label.config(text=message, fg="#F39C12")
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        self.update_stats()

    def new_game(self):
        self.board = [""] * 9
        self.current_player = self.human
        self.game_over = False

        for btn in self.buttons:
            btn.config(text="", state=tk.NORMAL, bg=self.colors["empty"])

        self.message_label.config(text="¡Tu turno! (X)", fg="#2ECC71")

    def reset_score(self):
        response = messagebox.askyesno(
            "Reiniciar",
            "¿Estás seguro de que quieres reiniciar el marcador?"
        )
        if response:
            self.wins_human = 0
            self.wins_ai = 0
            self.draws = 0
            self.update_stats()
            self.new_game()

    def update_stats(self):
        self.stats_text.config(
            text=f"Tú: {self.wins_human}  |  Computadora: {self.wins_ai}  |  Empates: {self.draws}"
        )

if __name__ == "__main__":
    root = tk.Tk()
    game = TriquiGame(root)
    root.mainloop()
