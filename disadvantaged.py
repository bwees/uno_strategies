from tqdm import tqdm
from uno import UnoGame, COLORS
import random
import matplotlib.pyplot as plt


def sim(my_id):
    game = UnoGame(4)
    while game.is_active:
        player = game.current_player
        player_id = player.player_id
                
        if player.can_play(game.current_card):
            # I'm not the current player, do random strategy
            for i, card in enumerate(player.hand):
                if game.current_card.playable(card):
                    if card.color == 'black':
                        new_color = random.choice(COLORS)
                    else:
                        new_color = None
                    game.play(player=player_id, card=i, new_color=new_color)
                    break
        else:
            game.play(player=player_id, card=None)

    return game.winner

if __name__ == '__main__':

    win_rates = []
    for i in tqdm(range(1000)):
        w = []
        for i in range(100):
            pID = 3
            w.append(sim(pID).player_id == pID)
        win_rates.append(w.count(True) / len(w))

    # dump win rates to file, one item per line
    with open('results/p_3.txt', 'w') as f:
        for i in win_rates:
            f.write(str(i) + '\n')
