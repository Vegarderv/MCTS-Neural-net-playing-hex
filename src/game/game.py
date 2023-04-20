from typing import List


class Game:
    def __init__(self) -> None:
        pass

    def do_rollout(self) -> int:
        pass

    def get_actions(self) -> list['Action']:
        pass

    def do_action(self, action: 'Action'):
        pass

    def is_finished(self) -> bool:
        pass

    def get_winning_move(self):
        pass

    def get_action(self, no: int):
        pass

    def get_state(self) -> List[int]:
        pass

    def get_winner(self) -> int:
        pass

    def reset(self):
        pass

class Action:
    def __init__(self) -> None:
        pass

    def get_info(self):
        pass

    def get_action_no(self):
        pass
