from pyfiglet import Figlet
from board import *
import re


class Title:
    def __init__(self, art_style="chunky"):
        self.f = Figlet(font=art_style)
        self.title = self.f.renderText("TicTacToe").strip()
        self.line = self.title.count("\n") + 1
        self.length = (len(self.title) - self.line) // self.line + 1

    def print_center(self, str):
        raw_str = self.break_color_code(str)
        side_space = (self.length - len(raw_str)) // 2
        print(" " * side_space + str)

    def show(self):
        print(self.title)

    def render(self, *messages, warning=None):
        print("=" * self.length)
        self.show()
        print()
        print("=" * self.length)
        print()
        for msg in messages:
            self.print_center(msg)
        if warning:
            print("\033[31m", end="")
            self.print_center(warning)
            print("\033[0m", end="")
        print("-" * self.length)

    def break_color_code(self, str: str) -> str:
        """
        str : strings, could include ansii color code escape
        return only string without color code
        """
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        return ansi_escape.sub("", str)


class GameScreen:
    def __init__(self, size):
        # the default screen length is 60
        self.length = max([60, size * 7 + size + 1])

    def print_center(self, str):
        raw_str = self.break_color_code(str)
        side_space = (self.length - len(raw_str)) // 2
        print(" " * side_space + str)

    def print_center_with_edge(self, str: str, left: str = "", right: str = "") -> None:
        raw_str = self.break_color_code(str)
        raw_right = self.break_color_code(right)
        raw_left = self.break_color_code(left)
        left_space = (self.length - len(raw_str) - len(raw_right) - len(raw_left)) // 2
        right_space = (
            self.length - len(raw_str) - len(raw_right) - len(raw_left) - left_space
        )
        print(left + " " * left_space + str + " " * right_space + right)

    def render(
        self,
        board: Board,
        info: str = None,
        message: str = None,
        error: str = None,
        congrats: str = None,
    ) -> None:
        """
        board : Board
        message : message should be shown
        error : error should be shown

        Given the board, pretty print the board and
        other ornaments
        """
        # top ornament
        print("-" * self.length)
        self.print_center_with_edge("\033[1mTicTacToe\033[0m", "OXOX", "XOXO")
        print("-" * self.length)
        print()

        # board
        side_board_space = (self.length - (board.size * 7 + board.size + 1)) // 2
        print(" " * side_board_space, end="")
        board_str = board.__str__().replace("\n", "\n" + " " * side_board_space)
        print(board_str)
        print()

        # message
        if message:
            message = f"\033[2m{message}\033[0m"
            self.print_center(message)
            print()

        # error
        if error:
            self.print_center("⚠️  \033[31m" + error + "\033[0m ⚠️")
            print()
        print("-" * self.length)
        self.print_center_with_edge(info, "OXOX", "XOXO")
        print("-" * self.length)

        # congratulation
        if congrats:
            print()
            for str in congrats.split("\n"):
                self.print_center(str)
            print()
            print("-" * self.length)

    def break_color_code(self, str: str) -> str:
        """
        str : strings, could include ansii color code escape
        return only string without color code
        """
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        return ansi_escape.sub("", str)


if __name__ == "__main__":
    # title = Title("rounded")
    # title.render("A CS50P FINAL PROJECT",
    #              "github.com/wstypr/tictactoe"," ",
    #              "<< PRESS ENTER TO START >>")

    size = 5
    board = Board(size)
    gamescreen = GameScreen(size)

    gamescreen.render(board, error="⚠️  There is an error", message="This is a message")

    # text = "\033[31mhello\033[0m"
    # print(gamescreen.break_color_code(text))
