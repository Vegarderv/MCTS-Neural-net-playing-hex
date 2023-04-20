import random
from typing import List
import parameters as pm
import numpy as np
from ANET import ANET
from mcts import MCTS, Node
from game.hex import HexGame


class RL:
    def __init__(self) -> None:
        self.game = HexGame()
        self.buffer = np.empty((0, pm.INPUT_DIMENSION + pm.NUMBER_OF_ACTIONS))
        self.ANET = ANET()

    def _run_episode(self):
        self.game.reset()
        node_1 = None
        node_2 = None

        while self.game.is_finished() != True:
            if self.game.turn % 2 == 0:
                ai = MCTS(self.game, node_1, self.game.turn % 2)
                action, node_1 = ai.run(self.ANET.choose_epsilon_greedy)
                if node_2 != None:
                    node_2 = node_2.prune(action)
            
                
            else:
                ai = MCTS(self.game, node_2, self.game.turn % 2)
                action, node_2 = ai.run(self.ANET.choose_epsilon_greedy)
                node_1 = node_1.prune(action)
            
            target_dist = ai.get_distribution()
            self._add_to_buffer(self.game.get_state(), target_dist)

            self.game.do_action(action)

            print("Action done!")
            print("New board state:")
            print(self.game.board)
            print()

        self.ANET.fit(self._get_buffer_sample())
    
    def _add_to_buffer(self, state: List[int], distribution: List[float]):
        instance = np.array([state + distribution], dtype=np.float32)
        self.buffer = np.append(self.buffer, instance, axis=0)
    
    def _get_buffer_sample(self):
        size = min(self.buffer.shape[0], pm.BATCH_SIZE)
        return self.buffer[np.random.choice(self.buffer.shape[0], size, replace=False), :]
    
    def run(self):
        self.ANET.save(pm.DIRECTORY, f"anet_0")
        for episode in range(pm.EPISODES):
            print(f"Episode number {episode + 1}", end="\n\n")
            self._run_episode()
            if (episode + 1) in pm.SAVE_INTERVALS:
                self.ANET.save(pm.DIRECTORY, f"anet_{str(episode + 1)}")
        self.ANET.visualize_loss()

             


