from fractions import Fraction
from functools import lru_cache
from math import comb

# Library multiset: L lands, P Portent, O Opt, K Peek, X blanks. Hand: counts of P,O,K.
# Phases: 't1' (turn-one actions), 'opp' (opponent upkeep: pending Portent draw), 't2draw', 't2cast'.
# A card bottomed by Opt's scry is out of reach by turn two, so it leaves the multiset.

def draw_outcomes(L, P, O, K, X):
    N = L + P + O + K + X
    for kind, n in (('L', L), ('P', P), ('O', O), ('K', K), ('X', X)):
        if n:
            yield kind, Fraction(n, N)

@lru_cache(maxsize=None)
def prob(L, P, O, K, X, hP, hO, hK, phase, pending):
    """Probability of finding a land by the turn-two land drop from this state."""
    if phase == 't1':
        # cast one cantrip: Portent > Opt > Peek
        if hP:
            # Portent: top three contain a land with prob 1 - C(nonL,3)/C(N,3); else shuffle (state unchanged)
            N = L + P + O + K + X
            p_land = 1 - Fraction(comb(N - L, 3), comb(N, 3)) if N >= 3 else Fraction(1 if L else 0)
            # if a land is found it is drawn at the opponent's upkeep: certain land
            rest = peek(L, P, O, K, X, hP - 1, hO, hK, 't2draw')  # the delayed draw still happens after a miss
            return p_land + (1 - p_land) * rest
        if hO:
            return opt(L, P, O, K, X, hP, hO - 1, hK, 't2draw', 1)
        if hK:
            return peek(L, P, O, K, X, hP, hO, hK - 1, 't2draw')
        return prob(L, P, O, K, X, hP, hO, hK, 't2draw', False)
    if phase == 'opp':
        return prob(L, P, O, K, X, hP, hO, hK, 't2draw', False)
    if phase == 't2draw':
        total = Fraction(0)
        for kind, p in draw_outcomes(L, P, O, K, X):
            if kind == 'L':
                total += p
            else:
                nxt = dict(L=L, P=P, O=O, K=K, X=X); nxt[kind] -= 1
                h = dict(hP=hP, hO=hO, hK=hK)
                if kind in 'POK': h['h' + kind] += 1
                total += p * prob(nxt['L'], nxt['P'], nxt['O'], nxt['K'], nxt['X'], h['hP'], h['hO'], h['hK'], 't2cast', False)
        return total
    if phase == 't2cast':
        # a turn-two Portent cannot deliver by the drop; Opt or Peek can
        if hO:
            return opt(L, P, O, K, X, hP, hO - 1, hK, 'end', 2)
        if hK:
            return peek(L, P, O, K, X, hP, hO, hK - 1, 'end')
        return Fraction(0)
    if phase == 'end':
        return Fraction(0)
    raise ValueError(phase)

def peek(L, P, O, K, X, hP, hO, hK, nxt_phase):
    total = Fraction(0)
    for kind, p in draw_outcomes(L, P, O, K, X):
        if kind == 'L':
            total += p
        else:
            c = dict(L=L, P=P, O=O, K=K, X=X); c[kind] -= 1
            h = dict(hP=hP, hO=hO, hK=hK)
            if kind in 'POK': h['h' + kind] += 1
            total += p * prob(c['L'], c['P'], c['O'], c['K'], c['X'], h['hP'], h['hO'], h['hK'], nxt_phase, False)
    return total

def opt(L, P, O, K, X, hP, hO, hK, nxt_phase, turn):
    # scry 1: see the top card
    total = Fraction(0)
    for kind, p in draw_outcomes(L, P, O, K, X):
        if kind == 'L':
            total += p  # keep and draw it
            continue
        c = dict(L=L, P=P, O=O, K=K, X=X); c[kind] -= 1
        keep = turn == 1 and kind == 'O' and not (hP or hO or hK)  # keep an Opt on turn one if nothing else is castable
        if keep:
            h = dict(hP=hP, hO=hO, hK=hK); h['h' + kind] += 1
            total += p * prob(c['L'], c['P'], c['O'], c['K'], c['X'], h['hP'], h['hO'], h['hK'], nxt_phase, False)
        else:
            # bottom it (out of reach), then draw the next card
            total += p * peek(c['L'], c['P'], c['O'], c['K'], c['X'], hP, hO, hK, nxt_phase)
    return total

def start(hand, onplay):
    hP, hO, hK = hand.count('P'), hand.count('O'), hand.count('K')
    L, P, O, K = 16, 4 - hP, 4 - hO, 1 - hK
    X = 53 - L - P - O - K
    if onplay:
        return prob(L, P, O, K, X, hP, hO, hK, 't1', False)
    # on the draw: natural draw first
    return peek(L, P, O, K, X, hP, hO, hK, 't1')

rows = [('None', ''), ('Peek', 'K'), ('Opt', 'O'), ('Portent', 'P'), ('Opt and Peek', 'OK'),
        ('Opt and Opt', 'OO'), ('Portent and Peek', 'PK'), ('Portent and Opt', 'PO')]
print(f"{'hand':20s} {'play':>7s} {'draw':>7s}")
for name, h in rows:
    print(f"{name:20s} {float(start(h, True))*100:7.1f} {float(start(h, False))*100:7.1f}")
