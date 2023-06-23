import random
from itertools import product
import math

def flush(hand):
    print(hand)
    hand_suit = [s for r,s in hand]
    hand_number = sorted([r for r,s in hand])
    hand_number_r = sorted([r for r,s in hand],reverse=True)
    len_set_hand = len(set(hand_number))
    if len(set(hand_suit))==1:
        Straights = [i for i in range(hand_number[0],hand_number[0]+5)]
        if hand_number == Straights:
            return 9,'Straight flush'
        else: 
            return 6,'Flush'
    elif len_set_hand == 2:
        if hand_number[:4] == [hand_number[0]] * 4 or hand_number_r[:4] == [hand_number_r[0]] * 4:
            return 8,'Four of a kind'
        if hand_number[:3] == [hand_number[0]] * 3 and hand_number[3:] == [hand_number[3]] * 2 or \
            hand_number_r[:3] == [hand_number_r[0]] * 3 and hand_number_r[3:] == [hand_number_r[3]] * 2:
            return 7,'Full house'
    elif len_set_hand==5:
        Straights = [i for i in range(hand_number[0],hand_number[0]+5)]
        if hand_number == Straights:
            return 5,'Straight'
        else:
            return 1,'High card'
    elif len_set_hand==3:
        if hand_number[:3] == [hand_number[0]] * 3 or hand_number_r[:3] == [hand_number_r[0]] * 3 \
            or hand_number[1:4] == [hand_number[1]] * 3:
            return 4,'Three of a kind'
        if hand_number[:2] == [hand_number[0]] * 2 and hand_number[2:4] == [hand_number[2]] * 2 or \
            hand_number_r[:2] == [hand_number_r[0]] * 2 and hand_number_r[2:4] == [hand_number_r[2]] * 2 or\
            hand_number[:2] == [hand_number[0]] * 2 and hand_number[3:5] == [hand_number[3]] * 2 :
            return 3,'Two pair'
    elif len_set_hand ==4:
        return 2,'One pair'
    else:
        return 1,'High card'

def simulate_game(blotter_deck):
    figure_hand = random.sample(figure_deck, 5)
    blotter_hand = random.sample(blotter_deck, 5)
    
    figure_strength,figure_type = flush(figure_hand)
    blotter_strength,blotter_type = flush(blotter_hand)
    print('figure_strength:',figure_strength,figure_type)
    print('blotter_strength:',blotter_strength,blotter_type)

    if figure_strength > blotter_strength:
        return "Figure"
    elif figure_strength == blotter_strength:
        return "Figure"
    elif blotter_strength > figure_strength:
        return "Blotter"
    else:
        return 

suits = ['H', 'D', 'C', 'S']
figure_deck = [(value, suit) for value, suit in product(range(11, 15), suits)]
blotter_deck = [(value, suit) for value, suit in product(range(2, 11), suits)]
num_simulations = 100000
num_wins = 0
for i in range(num_simulations):
    result = simulate_game(blotter_deck)
    if result == "Blotter":
        num_wins += 1
print(f"Probability of Blotter winning: {num_wins/num_simulations:.4f}")

print('figure_deck:',math.comb(len(figure_deck), 5))
print('blotter_deck:',math.comb(len(blotter_deck), 5))