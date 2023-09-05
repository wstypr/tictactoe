from collections import Counter
from random import shuffle, choice


class Player:
    def __init__(self, name: str, type: str):
        """
        name = name of player
        type = 'O' or 'X'
        """
        self.name = name
        self.player_winning_patterns = []
        self.type = type

    def get_move(self, *args):
        return input("Type <row,col> : ")

    def add_player_winning_pattern(self, pattern):
        self.player_winning_patterns.append(pattern)

    def remove_player_winning_pattern(self, move):
        for win_pattern in self.player_winning_patterns.copy():
            if move in win_pattern:
                self.player_winning_patterns.remove(win_pattern)

    def is_winning(self, move):
        for pattern in self.player_winning_patterns.copy():
            if move in pattern:
                pattern.remove(move)
                if len(pattern) == 0:
                    return True
        return False

    def say_congrats(self):
        congratulations = [
            f"Victory unlocked for {self.name}! \nCongrats on your epic tictactoe triumph!",
            f"Game over, victory achieved! \nWell played, champion {self.name}!",
            f"You've conquered the virtual realm {self.name}! \nCongratulations on your tictactoe win!",
            f"Level complete {self.name}! \nYour tictactoe skills are truly impressive. \nCongratulations!",
            f"The winner is you {self.name}! \nCongratulations on your tictactoe game victory!",
            f"Mission accomplished!, {self.name} \nYour tictactoe prowess is unmatched. \nCongrats!",
            f"Tictactoe domination achieved, {self.name}! \nCongrats on your well-deserved win!",
            f"You've proven yourself as the ultimate player. \nCongratulations, {self.name}!",
            f"Winner winner, virtual dinner! \nCongrats on your tictactoe success, {self.name}!",
            f"Game on, game won! \nCongratulations on your fantastic victory, {self.name}!",
        ]
        return choice(congratulations)

    def say_draw(self):
        draws = [
            "In the world of tictactoe, \nsometimes a draw is just as thrilling. \nWell done to both players for an intense showdown!",
            "Two forces equally matched, \nresulting in a draw. \nCongratulations on your valiant effort!",
            "Neither victory nor defeat, but a hard-fought draw. \nYour tictactoe talents are truly balanced and impressive!",
            "When the game ends in a tie, \nit's a testament to your tictactoe excellence. \nCongratulations on a well-deserved draw!",
            "The battle was fierce, the outcome undecided. \nA draw that highlights your dedication and skill. \nGreat job!",
        ]
        return choice(draws)


class Computer(Player):
    def __init__(self, name, type):
        super().__init__(name, type)

    def get_move(self, win_patterns, opponent, available_moves) -> str:
        # FIRST MOVE OPTION
        # check self winning patterns
        # if there is a pattern needs final step, immediately return to win
        for pattern in self.player_winning_patterns:
            if len(pattern) == 1:
                return pattern[0]

        # SECOND MOVE OPTION
        # check opponent winning patterns
        # if there is a pattern with final step, immediately return to block opponent winning move
        opponent_win_patterns = opponent.player_winning_patterns
        for pattern in opponent_win_patterns:
            if len(pattern) == 1:
                return pattern[0]

        # THIRD MOVE OPTION
        # collect all possible move from winning pattern and player winning pattern
        possible_moves = []
        for pattern in win_patterns:
            for move in pattern:
                possible_moves.append(move)
        for pattern in self.player_winning_patterns:
            for move in pattern:
                possible_moves.append(move)
        for move in available_moves:
            possible_moves.append(move)
        # tally the moves
        # return the highest chance of win
        shuffle(possible_moves)
        possible_moves = Counter(possible_moves)
        move = possible_moves.most_common(1)[0][0]
        return move

    def say_congrats(self):
        congratulations = [
            "In the game of tictactoe, \none must taste both victory and defeat. \nKeep playing and learning!",
            "Defeat is just a stepping stone towards improvement. \nYour next win is right around the corner!",
            "Even champions experience setbacks. \nYour skills will only grow stronger from this moment on.",
            "Remember, \nevery loss is an opportunity to refine your strategies. \nKeep your head up and keep playing!",
            "Though the victory slipped away this time, \nyour determination and sportsmanship shine brightly. \nOnward to more matches!",
        ]
        return choice(congratulations)
