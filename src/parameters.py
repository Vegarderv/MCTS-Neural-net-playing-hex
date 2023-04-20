
from keras.activations import relu, tanh, sigmoid, linear # noqa
from keras.losses import mse  
from keras.optimizers import Adam, RMSprop, SGD, Adagrad

# TOPP
DIRECTORY = "models_3"
G = 10
VISUALIZE = False

# RL
EPISODES = 20
M = 3
SAVE_INTERVALS = [EPISODES / (M - 1) * i for i in range(M)]

# MCTS
ITER = 200
MAX_MS = 1

# Game world
GAME = "HexGame"
LEDGE_BOARD = [0, 0, 1, 1, 0, 2, 1, 0, 0, 1]
SIZE = 3 if GAME == "HexGame" else len(LEDGE_BOARD)
NUMBER_OF_ACTIONS = SIZE ** 2 if GAME == "HexGame" else int((SIZE ** 2 - SIZE) / 2) + 1

TIME_SHOW = 1
 
# ANET
INPUT_DIMENSION = SIZE ** 2 + 1 if GAME == "HexGame" else SIZE + 1
HIDDEN_DIMENSIONS = (64, 32)
OUTPUT_DIMENSION = NUMBER_OF_ACTIONS
ACTIVATION_FUNC = relu
LEARNING_RATE = 0.1
OPTIMIZER = Adam
LOSS = mse
BATCH_SIZE = 6
EPSILON = 0.2
EPSILON_DECAY = 1
