import sys
import random

acc_elo = {}

def update_ranking(p1, p2, real_score):
    # update elo[p1] and elo[p2] according to real match result between p1 and p2
    # according to: https://en.wikipedia.org/wiki/Elo_rating_system
    
    Q_a = 10 ** (elo[p1] / 400)
    Q_b = 10 ** (elo[p2] / 400)
    
    
    E_a = Q_a / (Q_a + Q_b)  # expected scores according to current ranking
    E_b = Q_b / (Q_a + Q_b)  
    
    K_a = 800 / (n_of_games[p1] + 1)  # one match tournament
    K_b = 800 / (n_of_games[p2] + 1)  # one match tournament
    
    elo[p1] = elo[p1] + K_a * (real_score - E_a)
    elo[p2] = elo[p2] + K_b * (-real_score - E_b)
    
    n_of_games[p1] += 1
    n_of_games[p2] += 1


game = sys.argv[1]

results = []

MAX_POINT = 8


players = set()

for x in open(game):
    L = x.split()
    if len(L) != 3:
        continue
    p1 = L[0]
    p2 = L[1]
    
    players.update([p1, p2])
    
    won,tied,lost = map(int, L[2].split('-'))
    
    matches = won+tied+lost
    
    won  = round(100 * won / matches)
    tied = round(100 * tied / matches)
    lost = round(100 * lost / matches)
    
    
    
    for i in range(won):
        results.append( (p1, p2, +1) )
    
    for i in range(tied):
        results.append( (p1, p2, 0) )

    for i in range(lost):
        results.append( (p1, p2, -1) )
    
for p in players:
    acc_elo[p] = 0

for run in range(1000):
    random.shuffle(results)
    elo = {}  
    n_of_games = {}  
    for p in players:
        elo[p] = 400
        n_of_games[p] = 0
                
    for a, b, r in results:
        update_ranking(a, b, r)

    for p in players:
        acc_elo[p] += elo[p]

min_val = acc_elo['desdemona']
max_val = max(acc_elo.values())

    
    
for p in sorted(acc_elo, key=acc_elo.get, reverse=True):
    print (p, MAX_POINT *  (acc_elo[p]- min_val) / (max_val - min_val))
         
    
    
        
            
