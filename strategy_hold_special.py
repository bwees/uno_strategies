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
            if player_id == my_id:

                playable_colors = []

                # get the next player's card count
                next_card_count = len(game._player_cycle.view_next().hand)

                # I'm the current player, do cool strategy
                for i, card in enumerate(player.hand):
                    if game.current_card.playable(card):
                        if next_card_count == 1:
                            if "+" in str(card.card_type) or "reverse" in str(card.card_type) or "skip" in str(card.card_type):
                                playable_colors.append(card)
                        elif "+" not in str(card.card_type) and "reverse" not in str(card.card_type) and "skip" not in str(card.card_type):
                            playable_colors.append(card)
                
                if playable_colors == []:
                    # no playable colors, play random
                    for i, card in enumerate(player.hand):
                        if game.current_card.playable(card):
                            if card.color == 'black':
                                new_color = random.choice(COLORS)
                            else:
                                new_color = None
                            game.play(player=player_id, card=i, new_color=new_color)
                            break
                else:
                    # pick random card to play
                    card = random.choice(playable_colors)
                    # play highest color
                    card_i = player.hand.index(card)
                    if card.color == 'black':
                        new_color = random.choice(COLORS)
                    else:
                        new_color = None
                    game.play(player=player_id, card=card_i, new_color=new_color)


            else:
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
            pID = random.randint(0, 3)
            w.append(sim(pID).player_id == pID)
        win_rates.append(w.count(True) / len(w))

    # dump win rates to file, one item per line
    with open('results/hold_plus_lookahead.txt', 'w') as f:
        for i in win_rates:
            f.write(str(i) + '\n')

