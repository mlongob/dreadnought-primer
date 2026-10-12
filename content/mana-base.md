## Mana base: the one-land keep

Seventeen Islands and eleven cantrips means you will keep one-land hands, and the deck is built to survive them. Two Islands is the deck's operating level: Counterspell, Impulse and Gush all turn on at two, and once Gush is live you are past the point where screw decides the game. Missing the third and fourth land drop is fine against aggro and combo; it matters against control, where Foil, Thwart and Flash want the extra mana.

{cards: Island | Portent | Opt | Peek}
**The one-land keep.** From a seven with one Island, the question is the second land by your second land drop. A one-lander has one mana a turn, so it's one cantrip a turn, and the order matters. The chance of the second Island, by what you cast on turns one and two:

| Cantrips in the one-land hand | Second Island by turn 2, on the play | On the draw |
|---|---|---|
| None | 35% | 62% |
| Peek | 57% | 75% |
| Opt | 71% | 83% |
| Opt and Peek | 79% | 87% |
| Opt and Opt | 85% | 90% |
| Portent | 86% | 91% |
| Portent and Peek | 90% | 93% |
| Portent and Opt | 93% | 95% |

How the numbers are made, so you can check them: a one-land seven leaves a library of 53 cards with 16 Islands and whatever Portents, Opts and the Peek aren't in your hand. Peek sees one card. Opt sees two, because the scry bottoms anything that isn't an Island before the draw — not a second Opt, not a Portent; only the land is kept. Portent sees three, puts an Island on top if there is one and shuffles if there isn't, and its draw arrives at the beginning of the next upkeep — on your turn-one cast that is the opponent's upkeep, so the card is in hand before your turn-two draw step.

Plan A is one cantrip on turn one, Portent if you have it, and the Island in hand when turn two's main phase begins. If that misses, the table also counts one recovery, which costs you tempo: a second Opt or Peek, drawn or held, cast in your turn-two main phase so the land is played at once — a turn spent not holding Counterspell and not casting the Dreadnought. A turn-two Portent is never that recovery, since its draw can't arrive in time. Each line was checked by exact enumeration and by simulation, and the two agree.

Three things fall out. Portent is the best single cantrip for finding land by a margin, because it sees three cards and the shuffle gives it two more random looks when they miss. Peek helps less than Opt and far less than Portent, because it cycles without choosing. With Opt and Peek together you Opt first: the scry filters what Peek then draws blind, and Peek stays in hand for the turn its information matters. And with Portent and Opt in hand you always Portent first. Opt first leaves Portent's draw arriving a turn late, so by the turn-two drop that line is no better than Opt alone, 71% on the play against 93% the right way round. A second Portent adds nothing by turn two for the same reason.

So a one-lander with Portent and a Dreadnought is a keep, a one-lander with Opt and a Dreadnought is a keep on the draw, and a one-lander with neither is a mulligan, however good the rest looks.

