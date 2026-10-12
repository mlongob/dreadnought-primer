import random
N = 400000
# Deck: 17 Island, 4 Portent, 4 Opt, 1 Peek; other cards are blanks for this purpose
# (Impulse costs two and can't be cast off one land).

def library(hand_cantrips):
    cnt = {'P': 4, 'O': 4, 'K': 1}
    for c in hand_cantrips:
        cnt[c] -= 1
    lib = ['L'] * 16 + ['P'] * cnt['P'] + ['O'] * cnt['O'] + ['K'] * cnt['K']
    lib += ['x'] * (53 - len(lib))
    random.shuffle(lib)
    return lib

CANTRIPS = ('P', 'O', 'K')

def cast_opt(L, hand, turn):
    # scry 1: keep a land. On turn one keep an Opt if we hold nothing castable (two looks on turn two);
    # bottom everything else. On turn two bottom every non-land: nothing drawn now is castable in time.
    top = L[0]
    if top == 'L':
        pass
    elif turn == 1 and top == 'O' and not any(c in CANTRIPS for c in hand):
        pass
    else:
        L.append(L.pop(0))
    return L.pop(0)

def cast_portent(L):
    top = L[:3]
    if 'L' in top:
        i = top.index('L'); L.insert(0, L.pop(i))
    else:
        random.shuffle(L)

def run(hand_cantrips, onplay):
    hits = 0
    for _ in range(N):
        L = library(hand_cantrips)
        hand = list(hand_cantrips)
        found = False
        pending = False  # a Portent draw due at the next upkeep
        # Turn 1
        if not onplay:
            c = L.pop(0)
            if c == 'L': found = True
            elif c in CANTRIPS: hand.append(c)
        if not found:
            # cast one cantrip: Portent > Opt > Peek
            for pref in ('P', 'O', 'K'):
                if pref in hand:
                    hand.remove(pref)
                    if pref == 'P':
                        cast_portent(L); pending = True
                    elif pref == 'O':
                        c = cast_opt(L, hand, 1)
                        if c == 'L': found = True
                        elif c in CANTRIPS: hand.append(c)
                    else:
                        c = L.pop(0)
                        if c == 'L': found = True
                        elif c in CANTRIPS: hand.append(c)
                    break
        # opponent's turn: the Portent draw
        if pending:
            c = L.pop(0); pending = False
            if c == 'L': found = True
            elif c in CANTRIPS: hand.append(c)
        # Turn 2: natural draw, then a cantrip that can still find the drop this turn
        if not found:
            c = L.pop(0)
            if c == 'L': found = True
            elif c in CANTRIPS: hand.append(c)
        if not found:
            for pref in ('O', 'K'):
                if pref in hand:
                    hand.remove(pref)
                    if pref == 'O':
                        c = cast_opt(L, hand, 2)
                    else:
                        c = L.pop(0)
                    if c == 'L': found = True
                    break
        if found: hits += 1
    return hits / N

rows = [('Nothing', ''), ('Peek', 'K'), ('Opt', 'O'), ('Portent', 'P'),
        ('Opt and Peek', 'OK'), ('Opt and Opt', 'OO'), ('Portent and Peek', 'PK'),
        ('Portent and Opt', 'PO'), ('Portent and Portent', 'PP')]
random.seed(11)
N = 1000000
print(f"{'hand':22s} {'play':>6s} {'draw':>6s}")
for name, hc in rows:
    print(f"{name:22s} {run(hc, True)*100:6.0f} {run(hc, False)*100:6.0f}")
