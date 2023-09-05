from players import *


class Tile:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.tile = [
            "|-------|",
            "|       |",
            f"| \033[2m({self.row},{self.col})\033[0m |",
            "|       |",
            "|-------|",
        ]
        self.type = Tile.BLANK

    def set_o(self):
        self.tile = [
            "|-------|",
            "|  \033[31;1mOOO\033[0m  |",
            "|  \033[31;1mO O\033[0m  |",
            "|  \033[31;1mOOO\033[0m  |",
            "|-------|",
        ]
        self.type = Tile.O

    def set_x(self):
        self.tile = [
            "|-------|",
            "|  \033[33;1mX X\033[0m  |",
            "|   \033[33;1mX\033[0m   |",
            "|  \033[33;1mX X\033[0m  |",
            "|-------|",
        ]
        self.type = Tile.X

    def set_o_highlight(self):
        self.tile = [
            "|-------|",
            "|\033[41;1m  OOO  \033[0m|",
            "|\033[41;1m  O O  \033[0m|",
            "|\033[41;1m  OOO  \033[0m|",
            "|-------|",
        ]

    def set_x_highlight(self):
        self.tile = [
            "|-------|",
            "|\033[43;1m  X X  \033[0m|",
            "|\033[43;1m   X   \033[0m|",
            "|\033[43;1m  X X  \033[0m|",
            "|-------|",
        ]

    def set_clear(self):
        self.tile = [
            "|-------|",
            "|       |",
            "|       |",
            "|       |",
            "|-------|",
        ]

    def set_red(self):
        self.tile = [
            "|-------|",
            "|\033[41m       \033[0m|",
            "|\033[41m       \033[0m|",
            "|\033[41m       \033[0m|",
            "|-------|",
        ]

    def highlight(self):
        if self.type == Tile.O:
            self.set_o_highlight()
        else:
            self.set_x_highlight()

    def __str__(self):
        return "\n".join(self.tile)

    @classmethod
    def render_row(cls, *args):
        if len(args) == 1:
            return args[0].tile
        else:
            res = args[0].tile.copy()

            for col in args[1:]:
                for i in range(len(res)):
                    res[i] = res[i][:-1]
                    res[i] += col.tile[i]
            return res

    @classmethod
    def print_row(cls, *args):
        row = Tile.render_row(*args)
        print("\n".join(row))

    BLANK = 0
    O = "O"
    X = "X"


class Board:
    def __init__(self, size: int):
        self.size = size
        self.tiles = {}
        for row in range(size):
            for col in range(size):
                self.tiles[str(row) + str(col)] = Tile(row, col)

        # create winning pattern
        self.winning_pattern = []
        # > winning pattern: straight row
        for row in range(size):
            pattern = []
            for col in range(size):
                pattern.append(str(row) + str(col))
            self.winning_pattern.append(pattern)
        # > winning pattern: straight col
        for col in range(size):
            pattern = []
            for row in range(size):
                pattern.append(str(row) + str(col))
            self.winning_pattern.append(pattern)
        # > winning pattern: diagonal left bottom right up
        pattern = []
        for rowcol in range(size):
            pattern.append(str(rowcol) + str(rowcol))
        self.winning_pattern.append(pattern)
        # > winning pattern: diagonal left up right bottom
        pattern = []
        for rowcol in reversed(range(size)):
            pattern.append(str(rowcol) + str(size - 1 - rowcol))
        self.winning_pattern.append(pattern)

        # define possible move
        self.possible_move = []
        for row in range(size):
            for col in range(size):
                self.possible_move.append(str(row) + str(col))

    def __str__(self):
        board_string = ""
        for row in range(self.size):
            one_row = []
            for col in range(self.size):
                one_row.append(self.tiles[str(row) + str(col)])
            one_row = Tile.render_row(*one_row)
            if row != self.size - 1:
                one_row[0] = ""
            board_string = "\n".join(one_row) + board_string
        return board_string

    def set_tile(self, player: Player, move: str) -> None:
        """
        move = string of coordinate rowcol, ex: "12" means row:1 col:2
        set the according tile to Tile O
        """
        if move not in self.tiles.keys():
            raise ValueError("Invalid move")
        elif player.type == "O":
            self.tiles[move].set_o()
        elif player.type == "X":
            self.tiles[move].set_x()

    def highlight_winning_pattern(self, player: Player, move: str):
        for pattern in self.winning_pattern:
            win_pattern = True
            for mv in pattern:
                if self.tiles[mv].type != player.type:
                    win_pattern = False
                    break

            if win_pattern:
                for mv in pattern:
                    self.tiles[mv].highlight()

    def show_easter_egg(self):
        pattern = [
            "00",
            "01",
            "02",
            "04",
            "05",
            "06",
            "10",
            "11",
            "15",
            "16",
            "20",
            "26",
            "60",
            "63",
            "66",
        ]
        for tile in self.tiles:
            if tile in pattern:
                self.tiles[tile].set_clear()
            else:
                self.tiles[tile].set_red()


if __name__ == "__main__":
    board = Board(7)
    board.show_easter_egg()
    print(board)
