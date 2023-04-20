from game.game import Game, Action
import random
import copy


class Ledge(Game):
    def __init__(self) -> None:
        super().__init__()
        # self.state = self._create_state()
        self.state = [1, 0, 0, 0, 1, 0, 0, 0, 0, 2]
        self.winning_move = (0, -1)

    def _create_state(self) -> list[int]:
        board = [0 for i in range(20)]
        board[random.randrange(1, 20)] = 2
        for i, tile in enumerate(board):
            if random.random() > 0.5 and tile != 2:
                board[i] = 1
        return board

    def get_actions(self) -> list['LedAction']:
        actions: list['LedAction'] = []
        if self.state[0] != 0:
            actions.append(LedAction(0, -1))
        for i, tile in enumerate(self.state):
            if tile == 0 or i == 0:
                continue
            prev_index = i - 1
            while self.state[prev_index] == 0 and prev_index >= 0:
                actions.append(LedAction(i, prev_index))
                prev_index -= 1
        return actions

    def do_action(self, action: 'LedAction'):
        if action.coin == 0:
            self.state[0] = 0
        else:
            self.state[action.coin], self.state[action.move_to] = self.state[action.move_to], self.state[action.coin]

    def do_rollout(self) -> int:
        i = 0
        game_copy = copy.deepcopy(self)
        while True:
            action = random.choice(game_copy.get_actions())
            if action.move_to == -1 and game_copy.state[0] == 2:
                if i % 2 == 0:
                    return 1
                else:
                    return -1
            game_copy.do_action(action)
            i += 1

    def is_finished(self) -> bool:
        return not 2 in self.state

    def get_winning_move(self):
        return self.winning_move
    
    def create_action(self, no: int) -> "LedAction":
        if no == 0:
            return LedAction(0, -1)
        for i in range(1, no + 1):
            for j in range(i):
                if i * (i - 1) / 2 + j + 1 == no:
                    return Action(i, j)


class LedAction(Action):
    def __init__(self, coin: int, move_to: int) -> None:
        self.coin = coin
        self.move_to = move_to

    def get_info(self):
        return (self.coin, self.move_to)
    
    def get_action_no(self):
        if self.move_to == -1:
            return 0
        return self.coin * (self.coin - 1) / 2 + self.move_to + 1
 
    
