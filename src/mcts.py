from typing import Tuple
import math
import random
import time
from typing import List

import numpy as np
import parameters as pm
from game.game import Game, Action
import copy


class Node:

    def __init__(self, game: 'Game', action: 'Action', parent_node: 'Node', depth: int) -> None:
        self.t: int = 0
        self.n: int = 0
        self.children: list['Node'] = []
        self.S: int = 2
        self.depth = depth
        self.game = copy.deepcopy(game)
        self.action = action
        self.parent_node = parent_node
        self.is_winning_state = False
        self.score = 0

    def _node_expansion(self):
        for action in self.game.get_actions():
            new_game = copy.deepcopy(self.game)
            new_game.do_action(action)
            new_node = Node(new_game, action, self, self.depth + 1)
            if action.get_info() == self.game.get_winning_move():
                new_node.is_winning_state = True
                new_node.score = 1 if self.depth % 2 == 0 else -1
            self.children.append(new_node)

    def tree_search(self, N, you = 0) -> tuple['Node', int]:
        if self.game.is_finished():
            return (self, 1 if self.game.get_winner() == you else -1)
        if self.n == 0:
            return (self, 1)
        if len(self.children) == 0:
            return (self, 2)
        child = sorted(self.children, key=lambda x: float(
            "inf") if x.n == 0 else x.t / x.n + self.S * math.log(N/x.n))[-1]
        return child.tree_search(N)

    def backpropegate_result(self, result: int):
        self.n += 1
        if result not in [-1, 1]:
            print("WAAA")
        self.t += result
        if self.parent_node != None:
            self.parent_node.backpropegate_result(result)

    def prune(self, action: 'Action') -> 'Node':
        if len(self.children) == 0:
            self._node_expansion()
        right_children = list(
            filter(lambda x: x.action.get_info() == action.get_info(), self.children))
        if len(right_children) == 0:
            raise Exception("Grr")
        return right_children[0]

    def get_distribution(self) -> List[float]:
        children_as_action_no = {child.action.get_action_no(): child for child in self.children}
        output = []
        for i in range(pm.NUMBER_OF_ACTIONS):
            if i in children_as_action_no:
                output.append(children_as_action_no[i].n / self.n)
            else:
                output.append(0.0)
        return output



class MCTS():
    def __init__(self, game: 'Game', parent_node: 'Node' = None, you = 0) -> None:
        self.max_iter = pm.ITER
        if parent_node == None:
            self.parent_node = Node(game, None, None, 0)
            self.game = copy.deepcopy(game)
        else:
            self.parent_node = parent_node
            self.game = copy.deepcopy(parent_node.game)
        self.you = you

    def _tree_search(self, chooser_func):
        node, action = self.parent_node.tree_search(self.parent_node.n, self.you)
        if action == 0:
            result = node.score
            self._backpropegation(result, node)
        elif action == 1:
            self._do_rollout(node, chooser_func)
        elif action == 2:
            self._expand_node(node)

    def _do_rollout(self, node: 'Node', chooser_func):
        # TODO: FIX THIS
        if chooser_func == None:
            chooser_func = choose_uniform
        
        game_copy = copy.deepcopy(node.game)

        while game_copy.is_finished() != True:
            actions = game_copy.get_actions()
            action_nums = [action.get_action_no() for action in actions]
            action_nums = [1 if i in action_nums else 0 for i in range(pm.NUMBER_OF_ACTIONS)]
            state = game_copy.get_state()
            action_num = chooser_func(state, action_nums)
            action = game_copy.get_action(action_num)
            game_copy.do_action(action)
        

        result = 1 if game_copy.get_winner() == self.you else -1

        self._backpropegation(result, node)

    def _backpropegation(self, result: 'int', node: 'Node'):
        node.backpropegate_result(result)

    def _expand_node(self, node: 'Node'):
        node._node_expansion()
    
    def get_distribution(self) -> List[float]:
        return self.parent_node.get_distribution()

    def run(self, chooser_func = None) -> tuple[Action, Node]:
        i = 0
        timed = time.time()
        while i < pm.ITER  and time.time() - timed < pm.MAX_MS: 
            self._tree_search(chooser_func)
            i += 1
        actions = self.parent_node.children
        random.shuffle(actions)
        actions = sorted(actions, key=lambda x: float(
            "inf") if x.n == 0 else x.t / x.n)
        if len(actions) == 0:
            # print(self.game.board)
            move = self.game.get_actions()[0]
        else:
            move = actions[-1].action
        next_node = self.parent_node.prune(move)
        return move, next_node


def choose_uniform(state, valid_actions: Tuple[int]):
        valid_actions = np.array(valid_actions, dtype=np.float64)
        valid_actions *= 1/sum(valid_actions)
        return np.random.choice(range(pm.NUMBER_OF_ACTIONS), size=1, p=valid_actions)[0]