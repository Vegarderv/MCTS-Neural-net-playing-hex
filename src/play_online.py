import RLSystem, mcts
from game import hex
import parameters as pm


# Import and override the `handle_get_action` hook in ActorClient
from ActorClient import ActorClient
class MyClient(ActorClient):


    def handle_series_start( self, unique_id, series_id, player_map, num_games, game_params):
        """Called at the start of each set of games against an opponent
        Args:
        unique_id (int): your unique id within the tournament
        series_id (int): whether you are player 1 or player 2
        player_map (list): (inique_id, series_id) touples for both players
        num_games (int): number of games that will be played
        game_params (list): game-specific parameters.
        Note:
        > For the qualifiers, your player_id should always be "-200",
        but this can change later
        > For Hex, game params will be a 1-length list containing
        the size of the game board ([board_size])
        """
        self.logger.info(
        'Series start: unique_id=%s series_id=%s player_map=%s num_games=%s'
        ', game_params=%s',
        unique_id, series_id, player_map, num_games, game_params,
        )
        self.you = series_id - 1
        pm.SIZE = game_params[0]
    
    def handle_game_start(self, start_player):
        """Called at the beginning of of each game
        Args:
        start_player (int): the series_id of the starting player (1 or 2)
        """
        self.logger.info('Game start: start_player=%s', start_player)

    def handle_get_action(self, state):
        game = hex.HexGame(state[1:])
        game.turn = state[0] - 1
        actor = mcts.MCTS(game, None, you=state[0] - 1)
        action, node = actor.run()
        return action.y, action.x
    
    def handle_game_over(self, winner, end_state):
        """Called after each game
        Args:
        winner (int): the winning player (1 or 2)
        end_stats (tuple): final board configuration
        Note:
        > Given the following end state for a 5x5 Hex game
        state = [
        2, # Current player is 2 (doesn't matter)
        0, 2, 0, 1, 2, # First row
        0, 2, 1, 0, 0, # Second row
        0, 0, 1, 0, 0, # ...
        2, 2, 1, 0, 0,
        0, 1, 0, 0, 0
        ]
        > Player 1 has won here since there is a continuous
        path of ones from the top to the bottom following the
        neighborhood description given in `handle_get_action`
        """
        self.logger.info('Game over: winner=%s end_state=%s', winner, end_state)

    def handle_series_over(self, stats):
        """Called after each set of games against an opponent is finished
        Args:
        stats (list): a list of lists with stats for the series players
        Example stats (suppose you have ID=-200, and playing against ID=999):
        [
        [-200, 1, 7, 3], # id=-200 is player 1 with 7 wins and 3 losses
        [ 999, 2, 3, 7], # id=+999 is player 2 with 3 wins and 7 losses
        ]
        """
        self.logger.info('Series over: stats=%s', stats)
    
    def handle_tournament_over(self, score):
        """Called after all series have finished
        Args:
        score (float): Your score (your win %) for the tournament
        """
        self.logger.info('Tournament over: score=%s', score)

# Initialize and run your overridden client when the script is executed
if __name__ == '__main__':
    client = MyClient(auth="682b655be1b046918aa9094672a14a29")
    client.run()

    
"682b655be1b046918aa9094672a14a29"