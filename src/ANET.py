import random
from typing import Tuple
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense
from keras import Input
from keras.activations import softmax
from keras.models import Sequential, load_model
import matplotlib.pyplot as plt

import parameters as pm


class ANET:
    """Actor netwok"""

    def __init__(self) -> None:
        self.model = self._build()
        self.epsilon = pm.EPSILON
        self.loss = []

    def _build(self) -> Sequential:

        input_dimension = pm.INPUT_DIMENSION
        hidden_dimesions = pm.HIDDEN_DIMENSIONS
        output_dimension = pm.OUTPUT_DIMENSION

        model = Sequential()
        model.add(Input(shape=(input_dimension, )))

        for dim in hidden_dimesions:
            model.add(Dense(dim, activation=pm.ACTIVATION_FUNC))

        model.add(Dense(output_dimension, activation=softmax))

        model.compile(
            optimizer=pm.OPTIMIZER(learning_rate=pm.LEARNING_RATE),
            loss=pm.LOSS
        )

        model.summary()
        return model

    def choose_softmax(self, state: Tuple[int], valid_actions: Tuple[int]) -> int:
        state = np.reshape(state, (1, -1))
        actions = self.model.predict(state, verbose=0)
        actions *= np.array(valid_actions)
        actions = actions[0]
        actions *= 1 / sum(actions)  # Normalizing
        return np.random.choice(range(pm.NUMBER_OF_ACTIONS), size=1, p=actions)[0]

    def choose_greedy(self, state: Tuple[int], valid_actions: Tuple[int]) -> int:
        state = np.reshape(state, (1, -1))
        actions = self.model.predict(state, verbose=0)
        actions *= np.array(valid_actions)
        return np.argmax(actions)

    def choose_uniform(self, state, valid_actions: Tuple[int]):
        if sum(valid_actions) == 0:
            print(valid_actions)
        valid_actions = np.array(valid_actions, dtype=np.float64)
        valid_actions *= 1/sum(valid_actions)
        return np.random.choice(range(pm.NUMBER_OF_ACTIONS), size=1, p=valid_actions)[0]

    def choose_epsilon_greedy(self, state: Tuple[int], valid_actions: Tuple[int]):
        if random.random() < self.epsilon:
            return self.choose_uniform(state, valid_actions)
        return self.choose_greedy(state, valid_actions)

    def save(self, dir: str, name: str):
        self.model.save(f"{dir}/{name}", overwrite=True)

    def load(self, path: str):
        self.model = load_model(path, compile=False)

    def visualize_loss(self):
        plt.plot(self.loss)
        plt.show()

    def fit(self, episode: np.ndarray) -> None:
        X, Y = episode[:, :pm.INPUT_DIMENSION], episode[:,
                                                        pm.INPUT_DIMENSION:]

        print(X)
        print(Y)
        log = self.model.fit(X, Y, batch_size=pm.BATCH_SIZE)

        self.loss.append(log.history["loss"])

        self.epsilon *= pm.EPSILON_DECAY
