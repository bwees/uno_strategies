from strategy_switch_colors import sim
import random

w = []
for i in range(40):
    pID = random.randint(0, 3)
    w.append(sim(pID).player_id == pID)
print(w.count(True))