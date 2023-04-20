from mcts import MCTS
from yeOldGold import Ledge

p1_win = 0
p2_win = 0

for i in range(100):
    game = Ledge()
    i = 0
    node1 = None
    node2 = None

    while not game.is_finished():
        # print("Game state: ")
        print(game.state)
        #print("\nAvailable moves: ")
        #for j, action in enumerate(game.get_actions()):
        #    print(f"Action {j}: Coin: {action.coin} to: {action.move_to}")
        if i % 2 == 0:
            """move = int(input("What move will you do?\n"))
            game.do_action(game.get_actions()[move])"""
        #    print("AI 1 is thinking...")
            ai = MCTS(game, 2000, node1)
            move, node1 = ai.run()
        #    print(f"AI does action: Coin: {move.coin} to: {move.move_to}")
            game.do_action(move)
            if node2 != None:
                node2 = node2.prune(move)


        else:
         #   print("AI 2 is thinking...")
            ai = MCTS(game, 500, node2)
            move, node2 = ai.run()
         #   print(f"AI does action: Coin: {move.coin} to: {move.move_to}")
            game.do_action(move)
            node1 = node1.prune(move)
        
        i += 1

    if i % 2 == 1:
        p1_win += 1
    else:
        p2_win += 1

    print("-_____________________________________________-")

print(f"p1 winrate: {p1_win / (p1_win + p2_win)}")