from random import randint

CORES = {"t_red": "\033[31m", "t_green": "\033[32m", "t_normal": "\033[37m"}


def green_print(mensage):
    print(CORES["t_green"] + mensage + CORES["t_normal"])


def red_print(mensage):
    print(CORES["t_red"] + mensage + CORES["t_normal"])


class Player:
    def __init__(self, name, mark):
        self.name = name
        self.mark = mark

    def __str__(self):
        return f"name: {self.name}\tmark: {self.mark}"


class Board:
    def __init__(self) -> None:
        self.board = [[" " for _ in range(3)] for _ in range(3)]

    def display(self):
        for row_index in range(len(self.board)):
            for cell_index in range(len(self.board[row_index])):
                if self.board[row_index][cell_index] == "X":
                    print(CORES["t_green"], end="")
                else:
                    print(CORES["t_red"], end="")

                print(f" {self.board[row_index][cell_index]} ", end="")
                print(CORES["t_normal"], end="")
                if not cell_index == len(self.board) - 1:
                    print("|", end="")
            print()
            if not row_index == len(self.board) - 1:
                print("---+---+---")

    def is_full(self):
        for row in self.board:
            for cell in row:
                if cell == " ":
                    return False
        return True

    def place_mark(self, row, col, mark):
        if self.board[row][col] == " ":
            self.board[row][col] = mark
            return True
        return False

    def is_winner(self, player):
        return (
            self.check_rows(player.mark)
            or self.check_columns(player.mark)
            or self.check_diagonals(player.mark)
        )

    def check_rows(self, mark):
        for row in self.board:
            if self.is_row_full(row, mark):
                return True
        return False

    def check_columns(self, mark):
        for col in range(3):
            if self.is_column_full(col, mark):
                return True
        return False

    def check_diagonals(self, mark):
        return self.is_left_diagonal_full(mark) or self.is_right_diagonal_full(mark)

    def is_row_full(self, row, mark):
        for cell in row:
            if cell != mark:
                return False
        return True

    def is_column_full(self, col, mark):
        for row in range(3):
            if self.board[row][col] != mark:
                return False
        return True

    def is_left_diagonal_full(self, mark):
        for i in range(3):
            if self.board[i][i] != mark:
                return False
        return True

    def is_right_diagonal_full(self, mark):
        for i in range(3):
            if self.board[i][2 - i] != mark:
                return False
        return True


class Game:
    def __init__(self) -> None:
        self.board = Board()
        self.players = [Player("Jogador", "X"), Player("Computador", "O")]
        self.current_player_index = randint(0, 1)

    def switch_player(self):
        self.current_player_index += 1

    def get_current_player(self):
        return self.players[self.current_player_index % 2]

    def get_valid_input(self, prompt):
        while True:
            try:
                value = int(input(prompt))
                if value in [1, 2, 3]:
                    return value - 1
                else:
                    red_print(
                        "Valor inválido! por favor, selecione um numero entre 1 e 3."
                    )
            except ValueError:
                red_print("Valor inválido! por favor, selecione um numero valido.")

    def run(self):
        print("""
  \033[31mJ\033[0m \033[32mO\033[0m \033[33mG\033[0m \033[34mO\033[0m
    \033[35mD\033[0m \033[36mA\033[0m
 \033[37mV\033[0m \033[31mE\033[0m \033[32mL\033[0m \033[33mH\033[0m \033[34mA\033[0m
        """)

        try:
            while True:
                self.board.display()
                player = self.get_current_player()

                if player.mark == "X":
                    green_print(f"vez do {player.name}")
                else:
                    red_print(f"vez do {player.name}")

                while True:
                    if player.mark == "X":
                        row = self.get_valid_input("Selecione uma linha entre 1 e 3: ")
                        column = self.get_valid_input(
                            "Selecione uma coluna entre 1 e 3: "
                        )
                    else:
                        row = randint(0, 2)
                        column = randint(0, 2)

                    if self.board.place_mark(row, column, player.mark):
                        row += 1
                        column += 1
                        if player.mark == "X":
                            green_print(
                                f"{player.mark} marcado na linha {row} coluna {column}"
                            )
                        else:
                            red_print(
                                f"{player.mark} marcado na linha {row} coluna {column}"
                            )
                        break
                    else:
                        if player.mark == "X":
                            red_print(
                                "Essa celula já está ocupada, por favor escolha outra linha e coluna."
                            )

                if self.board.is_winner(player):
                    self.board.display()
                    print(f"{player.name} ganhou!")
                    break
                if self.board.is_full():
                    self.board.display()
                    print("deu velha!")
                    break

                self.switch_player()
        except KeyboardInterrupt:
            green_print("\nSaindo o jogo da velha...")


game = Game()
game.run()
