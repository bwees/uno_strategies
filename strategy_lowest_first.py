from uno import UnoGame, COLORS
import random
import matplotlib.pyplot as plt

my_id = 0

def sim():
    game = UnoGame(4)
    while game.is_active:
        player = game.current_player
        player_id = player.player_id
                
        if player.can_play(game.current_card):
            if player_id == my_id:

                playable_colors = []

                # I'm the current player, do cool strategy
                for i, card in enumerate(player.hand):
                    if game.current_card.playable(card):
                        if card.color != "black":
                            playable_colors.append(card)
                
                # remove any cards that have a string as card type
                playable_colors = [card for card in playable_colors if type(card.card_type) != str]

                if playable_colors == []:
                    # no playable colors, play black
                    for i, card in enumerate(player.hand):
                        if game.current_card.playable(card):
                            if card.color == 'black':
                                new_color = random.choice(COLORS)
                            else:
                                new_color = None
                            game.play(player=player_id, card=i, new_color=new_color)
                            break
                else:
                    # sort colors by smallest card type
                    playable_colors.sort(key=lambda x: x.card_type)
                    # play lowest color
                    card_i = player.hand.index(playable_colors[0])
                    game.play(player=player_id, card=card_i, new_color=None)


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

win_rates = []
for i in range(1000):
    w = []
    for i in range(100):
        w.append(sim().player_id)
    win_rates.append(w.count(0) / len(w))

# dump win rates to file, one item per line
with open('results/highest_first.txt', 'w') as f:
    for i in win_rates:
        f.write(str(i) + '\n')

