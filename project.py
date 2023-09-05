from display import *
from players import *
from board import Board
from os import system, name


def main():
    # CONSTANT VARIABLE
    MIN_BOARD_SIZE = 3
    MAX_BOARD_SIZE = 7

    # TITLE SCREEN
    title = Title()
    clear_screen()
    title.render(
        "A CS50P FINAL PROJECT",
        "github.com/wstypr/tictactoe",
        "",
        "<< PRESS ENTER TO START >>",
    )
    input()

    while True:
        # MAIN GLOBAL VARIABLE
        warning = None  # warning shown in game screen
        message = None  # message shown in game screen
        turn = 0  # game turn counter
        winning_pattern = None  # possible winning patterns based on board size
        available_move = None  # possible moves based on board size
        is_draw = False  # state control if the game is draw
        play_again = False  # state control if the game will be played again
        warning = None

        # BOARD SIZE PROMPT
        while True:
            clear_screen()
            title.render(
                "SELECT BOARD SIZE",
                f"<< {MIN_BOARD_SIZE} - {MAX_BOARD_SIZE} >>",
                "",
                warning=warning,
            )
            try:
                size = get_board_size(
                    MIN_BOARD_SIZE, MAX_BOARD_SIZE, input("Board size: ")
                )
                warning = None
                break
            except ValueError:
                warning = f"⚠️  Size must be number between {MIN_BOARD_SIZE} - {MAX_BOARD_SIZE} ⚠️"

        # GAME MODE PROMPT
        while True:
            clear_screen()
            title.render(
                "SELECT MODE",
                " ",
                "<< 1 >> Player1  VS  Player2 ",
                "<< 2 >> Player   VS  Computer",
                "<< 3 >> Computer VS  Player  ",
                "",
                warning=warning,
            )
            try:
                mode = get_game_mode(input("Game mode: "))
                warning = None
                break
            except ValueError:
                warning = "⚠️  Game mode must be number between 1 - 3 ⚠️"

        # CREATE BOARD
        board = Board(size)
        winning_pattern = board.winning_pattern.copy()
        available_move = board.possible_move

        # CREATE GAMESCREEN
        gamescreen = GameScreen(size)

        # CREATE PLAYERS
        match mode:
            case 1:
                player1 = Player("Player 1", "O")
                player2 = Player("Player 2", "X")
            case 2:
                player1 = Player("Player", "O")
                player2 = Computer("Computer", "X")
            case 3:
                player1 = Computer("Computer", "O")
                player2 = Player("Player", "X")

        # GAME START
        # define player turn
        while True:
            if turn % 2 == 0:
                player, opponent = player1, player2
            else:
                player, opponent = player2, player1

            # show the board
            clear_screen()
            gamescreen.render(board, f"{player.name} Turn", message, warning)

            # prompt for player's move
            try:
                warning = None
                move = get_move(
                    available_move,
                    player.get_move(winning_pattern, opponent, available_move),
                )
            except ValueError:
                warning = "Invalid Move"
                continue
            register_move(move, player, opponent, board, winning_pattern)
            message = f"{player.name} last move: {move[0]},{move[1]}"

            if player.is_winning(move):
                win_msg = player.say_congrats()
                break

            if len(available_move) == 0:
                is_draw = True
                draw_msg = player.say_draw()
                break

            # increment turn
            turn += 1

        # render draw or winning screen
        while True:
            clear_screen()
            if is_draw:
                gamescreen.render(board, "DRAW !!!", message, warning, draw_msg)
            elif size == 7 and isinstance(opponent, Computer):
                board.show_easter_egg()
                gamescreen.render(
                    board,
                    f"{player.name.upper()} WIN !!!",
                    message,
                    warning,
                    player,
                    win_msg,
                )
            else:
                board.highlight_winning_pattern(player, move)
                gamescreen.render(
                    board, f"{player.name.upper()} WIN !!!", message, warning, win_msg
                )

            # prompt for playing again
            try:
                if get_play_again(input("Play again <y/n> : ")):
                    play_again = True
                    break
                else:
                    play_again = False
                    break
            except ValueError:
                warning = "Invalid Input"

        if not play_again:
            break

    clear_screen()
    title.render("Thanks For Playing")


# HELPER FUNCTIONS ========================================================
def clear_screen() -> None:
    """
    clear the screen to prepare for next render
    """
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")


def get_board_size(min_size: int, max_size: int, user_input: str) -> int:
    """
    min_size = minimum board size allowed
    max_size = maximum board size allowed
    user_input = string of user input

    return the int of chosen board size as long as it meets the criteria
    if not, raise error
    """
    size = int(user_input)
    if size in range(min_size, max_size + 1):
        return size
    else:
        raise ValueError


def get_game_mode(user_input: str) -> int:
    """
    user_input = string of user input

    return integer of mode number if it meets criteria
    if not raise ValueError

    there are 3 modes available
    """
    mode = int(user_input)
    if mode in range(1, 4):
        return mode
    else:
        raise ValueError


def get_move(available_move: list[str], user_input: str) -> str:
    move = user_input.replace(",", "").replace(" ", "")
    if move not in available_move:
        raise ValueError("Invalid Move")
    else:
        available_move.remove(move)
        return move


def register_move(
    move,
    player: Player,
    opponent: Player,
    board: Board,
    winning_pattern: list[list[str]],
) -> None:
    # check the winning pattern, if the move exist, put the pattern on player winning pattern
    for pattern in winning_pattern.copy():
        if move in pattern:
            player.add_player_winning_pattern(pattern.copy())
            winning_pattern.remove(pattern)

    # remove opponent winning pattern if it contains current move
    opponent.remove_player_winning_pattern(move)

    # update board
    board.set_tile(player, move)


def get_play_again(user_input: str) -> bool:
    user_input = user_input.lower()
    if user_input in ["y", "yes"]:
        return True
    elif user_input in ["n", "no"]:
        return False
    else:
        raise ValueError("Invalid Input")


if __name__ == "__main__":
    main()
