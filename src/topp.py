import os
import parameters as pm
from ANET import ANET
from game.hex import HexGame
from game.yeOldGold import Ledge
from mcts import MCTS, Node
from hex_pygame import run
from pathlib import Path

class TOPP:

    def __init__(self) -> None:
        self.models = {}
        self.score = {}
        self._add_models()
    

    def _add_models(self) -> None:
        models = list(os.listdir(pm.DIRECTORY))
        models = sorted(models, reverse=True)
        for filename in models:
            f = os.path.join(pm.DIRECTORY, filename)
            anet = ANET()
            anet.load(f)
            self.models[filename] = anet
            self.score[filename] = [0, 0]
    
    def play_round_robin(self, visualize = False) -> None:
        for i, (k, v) in enumerate(self.models.items()):
            for i2, (k2, v2) in enumerate(self.models.items()):
                if i2 not in range(i + 1, len(self.models)):
                    continue
                print(f"Player {k} vs player {k2}")
                for g in range(pm.G):
                    if g % 2 == 0:
                        score, game = hex_match(v, v2)
                        if score == 0:
                            print(f"Player {k} beats player {k2}")
                            self.score[k][1] += 1
                        else:
                            print(f"Playa {k2} beats player {k}")
                            self.score[k2][1] += 1
                    else:
                        score, game = hex_match(v2, v)
                        if score == 1:
                            print(f"Player {k} beats player {k2}")
                            self.score[k][1] += 1
                        else:
                            print(f"Playa {k2} beats player {k}")
                            self.score[k2][1] += 1
                    self.score[k][0] += 1
                    self.score[k2][0] += 1
                    if visualize:
                        run(game)

                    
    
    def display_scores(self) -> None:
        for key, value in self.score.items():
            print(f"{key}'s score: {value[1] / value[0]}")



def hex_match(p1: ANET, p2: ANET) -> tuple[int, "HexGame"]:
    turn = 0
    game = HexGame() if pm.GAME == "HexGame" else Ledge()
    while not game.is_finished():
        actions = game.get_actions()
        action_nums = [action.get_action_no() for action in actions]
        action_nums = [1 if i in action_nums else 0 for i in range(pm.NUMBER_OF_ACTIONS)]
        state = game.get_state()
        if turn % 2 == 0:
            action_num = p1.choose_softmax(state, action_nums)
        else:
            action_num = p2.choose_softmax(state, action_nums)
        action = game.get_action(action_num)
        game.do_action(action)
        turn += 1
    return game.get_winner(), game


if __name__ == "__main__":
    topp = TOPP()
    topp.play_round_robin(visualize=pm.VISUALIZE)
    topp.display_scores()