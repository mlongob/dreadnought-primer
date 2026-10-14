## Practice

Each puzzle below sets up a board and asks for the right play. Work it out before you open the answer: the reasoning matters more than the card you pick. Each puzzle assumes you've read the matchup it comes from. In the PDF, each answer starts on the next page, so you can solve the board before you turn it. The board is drawn the way MTGO shows it, with your opponent at the top. Cards with an eye are known to the other player — a card in their hand that you have seen, or a card in yours that they have. Tapped cards are turned sideways, attacking creatures have a red arrow under them, face-down cards are ones you haven't seen, and a number on a card is its counters. Spells and abilities on the stack sit in the band across the middle, leaning toward the player who put them there, with the top of the stack on the right; the bar below shows the turn and the current step, with the arrow pointing at the player whose turn it is.

### Puzzle 1: the Sligh race

{puzzle}
turn = 12
active = "you"
phase = "main1"
[them]
life = 19
library = 47
hand = ["?"]
lands = ["Mountain", "Mountain", "Mishra's Factory"]
permanents = ["Jackal Pup", "Jackal Pup", "Mogg Fanatic"]
graveyard = ["Bloodstained Mire", "Goblin Cadets", "Lightning Bolt", "Overload", "Incinerate", "Lightning Bolt"]
[you]
life = 7
library = 46
hand = ["Phyrexian Dreadnought", "Stifle", "Counterspell"]
lands = ["Island", "Island", "Island"]
permanents = ["Phyrexian Dreadnought"]
graveyard = ["Opt", "Portent", "Island", "Foil", "Stifle", "Hydroblast", "Daze"]
{/puzzle}

Game two against Sligh. Your Dreadnought came down last turn and can attack. They have one card in hand; assume whatever they draw next turn is a Mountain. What's the play?

{answer}
Attack with the Dreadnought. Then, in your second main phase, cast the other Dreadnought without Stifle and sacrifice the tapped one to its trigger. Keep the last two Islands up for Counterspell.

**Why attack.** They are at nineteen, so the Dreadnought needs two hits, and at seven life against a deck full of Bolts and Fireblasts every turn you give them is another draw aimed at you. The attack puts them at seven, or not far above it if they chump: the Dreadnought tramples over a blocker, and whatever blocks comes out of their attack.

**Why you need a blocker.** Once the Dreadnought is tapped, their board is lethal on its own: two Jackal Pups, the Fanatic and an animated Factory swing for seven, and sacrificing the Fanatic adds one more. Something has to be untapped on their turn.

**Read their card.** A Sligh player holding one card this late is most likely holding a finisher, a Fireblast or another burn spell waiting for your life total to drop into range, an answer to the Dreadnought, an Overload or a Mogg Salvage they didn't want to fire into your untapped Counterspell, or a Ball Lightning kept in after sideboarding and waiting for the third Mountain. Each of those is lethal unless you make the right play, so you have to play around all of them.

**The tempting blocker.** The second Dreadnought, with Stifle on its trigger. That spends two of your three Islands and strands Counterspell in your hand. The blocker stops one attacker and you go to one, and their card is free to finish you: a burn spell to the face, or Overload or Mogg Salvage on the blocker to let the whole board through.

**The play.** The second Dreadnought's trigger asks for twelve power of creatures, and the tapped Dreadnought has exactly that. Sacrifice it, and for one mana you have swapped a tapped Dreadnought for an untapped one with Counterspell still up. On their turn the Counterspell meets their one card, whether that's a burn spell, an Overload, a Salvage, a Ball Lightning or a Threaten, and the Dreadnought blocks. With one blocker the most they can get through is six, the Fanatic included, and you are at seven. If it blocks a Jackal Pup, the Pup's own trigger deals the twelve damage to them, but it doesn't kill them on the spot: the trigger goes on the stack, and they can respond with whatever they have left, a burn spell or the Fanatic's sacrifice. That is why the Counterspell matters even here: with their card countered, the Fanatic only takes you to one, and then the trigger resolves and the game is over. Most of the time they won't attack with the Pups at all, and the Dreadnought swings for the win next turn. The Stifle stays in hand too, and with two Islands open it takes the Fanatic's sacrifice if their card turns out to be a land.

If they respond to the trigger by destroying either Dreadnought, that is the spell to counter.

**Doing nothing is an option.** Not attacking at all also survives: the untapped Dreadnought blocks a Pup or the Factory, Counterspell takes their card, and Stifle takes the Fanatic. It isn't the best play — it leaves them at nineteen and gives them another turn of draws, where the swap gives you the same defense and puts them a turn from dead — but it is a reasonable choice. What doesn't work is attacking and keeping all three Islands up for Stifle and Counterspell: their attack alone is seven, and you are at seven. Nor does walling with both Dreadnoughts: not attacking and casting the second with Stifle leaves one Island, and a single burn spell for three to your face, followed by the whole board into your two blockers, gets the last points through.
{/answer}

### Puzzle 2: the Siege-Gang swing

{puzzle}
turn = 12
active = "them"
phase = "begin-combat"
[them]
life = 6
library = 45
hand = []
lands = ["Mountain", "Mountain", "Mountain", "Mountain", "Mountain", "Forest"]
permanents = ["Goblin Piledriver", "Siege-Gang Commander", "Goblin token", "Goblin token"]
graveyard = ["Wooded Foothills", "Goblin Warchief", "Wooded Foothills", "Goblin Lackey", "Goblin Tinkerer", "Skirk Prospector", "Naturalize"]
[you]
life = 7
library = 48
hand = ["Vision Charm", "Stifle", "Stifle"]
lands = ["Island", "Island (tapped)", "Island (tapped)", "Island (tapped)"]
permanents = ["Phyrexian Dreadnought"]
graveyard = ["Stifle", "Daze", "Counterspell", "Essence Flare"]
{/puzzle}

Game two against Goblins. They have moved to combat, and none of their Goblins is summoning sick. What do you do?

{answer}
Vision Charm their Mountains into Islands now, at the beginning of combat. If they attack, block the Piledriver with the Dreadnought, and keep both Stifles for your turn.

**Count it first.** If they attack with everything, the Piledriver's trigger makes it a 7/2, with three other Goblins beside it. Protection from blue doesn't stop the Dreadnought, which is colorless, from blocking it, and it has to: anything else lets it through. That leaves four damage from the Siege-Gang and the tokens. Then the Siege-Gang finishes it. Each shot costs two mana, one of it red, and sacrifices a Goblin for two damage, and after damage every Goblin that has already hit you is ammunition. Five Mountains and a Forest are three shots; your one Island Stifles one of them, and four plus four is eight. You are at seven.

**Why now.** The Charm leaves them no red mana for the rest of the turn; the Forest can pay for the generic part of a shot but not the red. Mana empties at the end of each step, not when a spell resolves, so they can respond by tapping the Mountains and floating the red mana, but cast now, that mana is gone before attackers are declared. Any shot they want this turn has to be fired now, before attackers are declared, and each one sacrifices a Goblin that then won't attack and won't count for the Piledriver. They can't have both the combat damage and the shots. Aimed at you, the most they get is six, and you are at one. Aimed at the Dreadnought, whatever they sacrifice also comes off the Piledriver it has to get past, and the shots and the block together come nowhere near twelve.

**If they keep the Goblins.** Then they attack without the shots: block the Piledriver, take four, go to three. The shots wait for your turn, when the Mountains are Mountains again, but you untap first: four Islands and two Stifles against three shots. One gets through and you are at one. Stifle counters the ability, not its cost, so every shot still sacrifices a Goblin. Holding the Goblins back to block doesn't save them either: at six, they can't soak up enough of a twelve-power trampler.

**Why not wait for the attack.** Charm in response to the Piledriver's trigger and they float the mana, let the trigger resolve, and spend it before blocks: three shots at the Dreadnought, and it still has to block the 7/2, so it dies. Charm after blockers and the blocked Piledriver becomes a free shot: that is eight, and you are dead. Stifling the trigger shrinks the Piledriver to a 1/2 but leaves them all their red mana: block the Siege-Gang and they fire three shots before damage, seven in all; block anything else and the Siege-Gang shoots after damage.
{/answer}

### Puzzle 3: racing the Elephants

{puzzle}
turn = 17
active = "them"
phase = "attackers"
[them]
life = 13
library = 43
hand = []
lands = ["Forest", "Forest (tapped)", "Plains (tapped)", "Gemstone Mine [1]", "City of Brass"]
permanents = ["Mox Diamond", "Sylvan Library", "Werebear (tapped) (attacking)", "Nimble Mongoose (tapped) (attacking)", "Elephant token (tapped) (attacking)", "Elephant token (tapped) (attacking)"]
graveyard = ["Windswept Heath", "Treetop Village", "Hidden Gibbons", "Aura of Silence", "Meddling Mage", "Pyroblast", "Naturalize"]
[you]
life = 7
library = 39
hand = ["Island", "Essence Flare", "Counterspell", "Impulse", "Chain of Vapor"]
lands = ["Island", "Island", "Island", "Island (tapped)", "Island (tapped)"]
permanents = ["Phyrexian Dreadnought"]
graveyard = ["Annul", "Opt", "Gush", "Portent", "Back to Basics", "Essence Flare", "Counterspell", "Vision Charm", "Gush", "Counterspell"]
{/puzzle}

Game two against 4C Terrageddon, the Meddling Mage build. They have just attacked with everything. What do you do, this turn and next?

{answer}
Block the Werebear. Chain of Vapor an Elephant token, and Counterspell the copy when they sacrifice a land to point it at the Dreadnought. Take six and go to one. Then, on your turn, Essence Flare your own Dreadnought and swing for fourteen.

**Count their attack.** Thirteen power is coming: the Werebear is a 4/4 with threshold, the Mongoose and the Elephants 3/3s. Blocking alone stops four of it, and nine kills you. So something else has to leave combat, and Chain is the only way. The Mongoose has shroud, so it can't be the target, and the block and the Chain have to take out the Werebear and an Elephant: block the Mongoose or an Elephant instead and seven gets through, which is exactly lethal.

**Why the token.** Chaining the Werebear and blocking an Elephant also leaves you at one, but the Werebear goes back to their hand, not away. They recast it after combat, and on your turn it is an untapped 4/4 standing in front of the Dreadnought. A token that leaves the battlefield simply stops existing.

**The copy.** Chain lets them sacrifice a land to copy it, and the copy goes straight at the Dreadnought. The copy is a spell, and Counterspell counters it. That is what the Counterspell is held for here.

**Why you can't stay home.** At one, with the Mongoose and an Elephant left, their next attack kills you: one blocker against two attackers. And a twelve-power Dreadnought into thirteen life doesn't end it. But everything that attacked you this turn is still tapped on yours, and the Werebear is dead, so nothing can block. Essence Flare is +2/+0: the Dreadnought swings as a 14/12, and the −0/−1 counters it would pick up from your next upkeep on mean nothing to twelve toughness. Thirteen life, fourteen damage.
{/answer}

### Puzzle 4: the Therapy that ends it

{puzzle}
turn = 11
active = "them"
phase = "main1"
[[stack]]
card = "Ravenous Rats"
by = "them"
ability = "Target opponent discards a card."
kind = "triggered"
target = "You"
[them]
life = 20
library = 48
hand = ["?", "?"]
lands = ["Swamp", "Swamp", "Swamp", "Swamp (tapped)", "Swamp (tapped)"]
permanents = ["Ravenous Rats"]
graveyard = ["Dark Ritual", "Hypnotic Specter", "Diabolic Edict", "Cabal Therapy"]
[you]
life = 20
library = 43
hand = ["Phyrexian Dreadnought (seen)", "Flash of Insight", "Phyrexian Dreadnought", "Phyrexian Dreadnought (seen)"]
lands = ["Island", "Island", "Island", "Island"]
graveyard = ["Daze", "Opt", "Stifle", "Phyrexian Dreadnought", "Counterspell", "Impulse", "Portent", "Opt", "Impulse"]
{/puzzle}

Game one against Moneyball Black. They have just cast Ravenous Rats, and its trigger is on the stack. Their Cabal Therapy, now in their graveyard, showed them your hand earlier: of the cards you hold now, they have seen the two Dreadnoughts with the eye. What do you do?

{answer}
Discard the Flash of Insight to the Rats. When they flash back Cabal Therapy by sacrificing the Rats and name the Dreadnought, flash back the Flash in response: exile all eight blue cards in your graveyard, look at the top eight, and take a Counterspell or the Thwart to counter the Therapy.

**What's coming.** The Rats are the body for Therapy's flashback. Their first Therapy showed them two Dreadnoughts, so the flashback names it, and it takes all three in your hand; the fourth is already in your graveyard. If that Therapy resolves, the game is over.

**Why discard the Flash.** The Rats make you discard, but you choose. A Dreadnought saves nothing, because the Therapy takes the other two. The Flash is the card they can't strip: in the graveyard its flashback costs two mana plus blue cards you already have, so eight cards cost you two Islands, and the other two are left for Counterspell. Thwart is free, returning three Islands.

**Why not cast it now.** Cast from hand, Flash costs X plus two, so your four Islands look at two cards and leave nothing to cast what you find. And it can't be flashed back in response to the Rats trigger: it only reaches the graveyard when the trigger resolves. The moment is the Therapy on the stack.

**What else could stop it.** Foil needs an Island in your hand, and you have none. Daze is no good while they have three Swamps open to pay for it.

**Playing to your outs.** Of the eight, take a Counterspell or the Thwart if one is there. Failing that, take a Gush: return the two tapped Islands and draw two, and with Islands in hand any Foil you draw counters the Therapy, as does a Counterspell off the two Islands still untapped. Failing that, take an Opt, or the Peek, and cast it off one untapped Island to dig for a Thwart, which still has four Islands to return, or a Gush into Foil. It isn't a lock, but every one of those outs exists only because the Flash came from the graveyard: cast from hand, the same four Islands would have bought two cards and no mana to use them.
{/answer}

### Puzzle 5: the Replenish on the stack

{puzzle}
turn = 15
active = "them"
phase = "main1"
storm = 2
[[stack]]
card = "Replenish"
by = "them"
[them]
life = 11
library = 38
hand = []
lands = ["Island", "Adarkar Wastes", "Island (tapped)", "Plains (tapped)", "Ancient Tomb (tapped)"]
permanents = ["Attunement"]
graveyard = ["Abeyance", "Opalescence", "Parallax Wave", "Intuition", "Replenish", "Fact or Fiction", "Mana Leak", "Seal of Cleansing", "Decree of Silence", "Frantic Search", "Intuition", "Adarkar Wastes", "Plains", "Attunement", "Frantic Search"]
[you]
life = 20
library = 33
hand = ["Brain Freeze", "Stifle", "Vision Charm"]
lands = ["Island", "Island", "Island", "Island", "Island"]
permanents = []
graveyard = ["Opt", "Daze", "Portent", "Opt", "Impulse", "Counterspell", "Island", "Phyrexian Dreadnought", "Foil", "Portent", "Gush", "Daze", "Opt", "Peek", "Portent", "Vision Charm", "Impulse", "Opt", "Portent"]
{/puzzle}

Game one against Replenish. They cast Frantic Search, untapped their lands and put Replenish on the stack, with Opalescence, Parallax Wave and Decree of Silence in their graveyard. What do you do?

{answer}
Vision Charm yourself, milling your own top four, to find a Flash of Insight: neither copy is in your graveyard, so both are in your library. If the Charm misses, Brain Freeze yourself as well. When a Flash turns up, flash it back, exiling every blue card in your graveyard, eighteen or more, and take the card that answers the Replenish with the mana you have left.

**What resolving costs you.** Replenish brings back the lock: Decree counters the next three spells you cast, Wave exiles whatever you block with, and Opalescence makes creatures of every enchantment they have — Wave a 4/4, Decree an 8/8, the Seal and both Attunements 2/2 and 3/3s. The Attunement already in play hits you this turn, and next turn they swing for twenty: you are dead in two turns.

**Why not mill them.** It looks like a Brain Freeze turn, with two spells already cast, but there isn't enough storm. The Freeze now mills nine; Charm their library first and the two mill sixteen of thirty-eight. Once Replenish resolves, Decree counters your spells; storm copies still resolve, but your turn starts the count again. Stifle has nothing to hit: Replenish is a spell.

**Playing to your outs.** The Flash is the only card that answers the Replenish from where you stand, and the graveyard is the only place you can afford to cast it from: two mana, with the blue cards already there paying for X — most of your library after the Charm, all of it after the Freeze. After the Charm, four Islands pay for the flashback and a Counterspell. After the Charm and the Freeze, two Islands pay for the flashback alone, and only the Thwart can be cast. If the Flash shows no counter you can cast, take a Gush. After the Freeze the Flash has seen your whole library, so you choose the order the rest goes back in: put a Foil on top, the Gush draws it, and the two Islands it returns pay for it. And whenever the Flash has seen your whole library, set up the next turns while you order it: a Dreadnought to draw next, with the Stifle in your hand to enable it, and a Counterspell or a Foil behind it for their next Replenish. At eleven life, one swing ends the game. Together the Charm and the Freeze find an answer about two times in three; nothing else in your hand finds one at all.
{/answer}

### Puzzle 6: what the Peek showed

{puzzle}
turn = 7
active = "you"
phase = "main1"
[them]
life = 20
library = 50
hand = ["Wrath of God", "Island", "Mana Leak", "Decree of Justice", "Plains", "Wrath of God", "Adarkar Wastes"]
lands = ["Island", "Plains", "Coastal Tower (tapped)"]
[you]
life = 20
library = 49
hand = ["Counterspell", "Phyrexian Dreadnought", "Gush", "Stifle", "Portent", "Daze", "Vision Charm"]
lands = ["Island", "Island", "Island"]
graveyard = ["Peek"]
{/puzzle}

Game one against Landstill. At the end of their last turn you Peeked at their hand. It's your main phase, you haven't played a land this turn and have none in hand, and you haven't committed a Dreadnought yet. What's the plan for the next few turns?

{answer}
Tap two Islands for mana, Gush by returning those two, and play one of them back as your land for the turn. Then Portent them, and cast the Dreadnought with Vision Charm as the enabler, keeping an Island untapped. Daze the Mana Leak whenever it comes. Next turn swing for twelve, and keep Counterspell up for the Wrath.

**Gush first.** Float the mana from two Islands before you return them, and the Gush costs you nothing this turn: two more cards, and with your land drop still unused, one of the Islands goes straight back down. You commit with four mana instead of three, and two more cards to protect it with.

**Read the hand.** A Mana Leak, two Wraths, and a Plains for their fourth land: next turn they can Wrath. The Coastal Tower came in tapped, so they have exactly two lands open now — a Mana Leak, with nothing left to pay for Daze.

**Why the Charm.** Charmed, the Dreadnought is phased out through their turn and comes back in your untap step, ready to swing; the Wrath they can cast next turn has nothing to hit, whatever mana you have left. With the Gush's extra mana, Stifle and an Island held for the Charm would also survive it, but the Charm in response to a Wrath is a card you spend on their timing; enabling with it spends the same card on yours.

**Why the Portent.** The Peek told you everything except what they draw. Portent sets the two draws that matter, before your first swing and before your second: put a Swords, a Disenchant, a Humility or a Fact or Fiction third, or shuffle if more than one is there — cycling the Decree draws them one card deeper. And if they spend the Mana Leak on the Portent, let it go: they are tapped out, the Dreadnought and the Charm resolve untouched, and the Daze stays in your hand.

**The next turns.** Swing for twelve. On their turn they have one Wrath they can cast; Counterspell it, and swing again for the game.
{/answer}

### Puzzle 7: the top three

{puzzle}
turn = 12
active = "you"
phase = "main1"
[[stack]]
card = "Portent"
by = "you"
target = "Opponent"
[choice]
label = "Portent: put them back in any order, or shuffle"
cards = ["Swords to Plowshares", "Terravore", "Forest"]
[them]
life = 17
library = 47
hand = []
lands = ["Forest", "Forest", "Plains", "Plains", "Brushland"]
permanents = ["Mox Diamond", "Oath of Druids", "Sphere of Resistance (phased out)"]
graveyard = ["Windswept Heath", "Forest", "Sylvan Library", "Thermokarst", "Winter's Grasp"]
[you]
life = 20
library = 47
hand = ["Impulse", "Phyrexian Dreadnought", "Brain Freeze", "Vision Charm", "Phyrexian Dreadnought"]
lands = ["Island", "Island", "Island (tapped)"]
graveyard = ["Island", "Daze", "Island", "Vision Charm"]
{/puzzle}

Game one against GW Oath Ponza. At the end of their turn you Vision Charmed their Sphere of Resistance, so it is phased out for your turn. Your Portent is resolving on their library. In what order do you put them back, or do you shuffle? And what's your plan?

{answer}
Put them back with the Forest on top, then the Swords, then the Terravore. Cast the Dreadnought and enable it with your second Vision Charm. Next turn swing for twelve. On their following upkeep, let the Oath trigger resolve, and swing again for the game.

**Do it while the Sphere is away.** With the Sphere in play, the Dreadnought and an enabler cost four, and you have three Islands: that is why it had to go. It phases back in at their untap step. This turn the Dreadnought and the Charm cost one each, as the Portent did; from their turn on, every spell costs one more.

**Why the Charm.** Charmed, the Dreadnought is phased out through their next upkeep, and the Oath only triggers when they control fewer creatures than you: with the Dreadnought gone, they don't. There is no trigger to fight, and the first swing lands before any Terravore exists.

**Let the second trigger resolve.** On their following upkeep the Dreadnought is back and the Oath triggers, and you want it to: the Oath reveals cards until it finds a creature and puts the rest into their graveyard, so it reveals the Swords first, throws it away, and finds the Terravore — the Oath mills their own answer. Terravore counts the land cards in all graveyards, and nothing the Oath revealed was a land, so it counts only what is already there: their Windswept Heath and the Forest they discarded to Mox Diamond, and your two Islands. A 4/4. It can block the Dreadnought, but twelve trample over a 4/4 is eight, and the first swing has put them at five.

**Why that order.** The Forest on top is their next draw, harmless. The Swords anywhere they would draw it before your second swing costs you the Dreadnought: on top they draw it next turn, and behind the Terravore the Oath stops before reaching it and they draw it after. Second, between the Forest and the Terravore, is the one place the Oath reveals it and throws it away. The Terravore on top would be drawn and cast in time to block your first swing, and worse comes after: once it dies blocking, the Oath triggers again with nothing known left to find. It reveals the Swords and the Forest, then digs through unknown cards, milling every land on the way into the graveyard, and whatever creature it finds, another Terravore above all, can arrive bigger than the Dreadnought. Don't shuffle either: this order is a sequence you can win with, and a shuffle hands their next draw and the Oath's reveal to forty-seven unknown cards.

**What's left.** One unknown draw after the Oath, which you can't control. And the Oath is optional: if they decline it, they draw the Swords. That is the gamble in the line, and a free Terravore is a hard trigger to turn down.
{/answer}

### Puzzle 8: the counter war

{puzzle}
turn = 19
active = "them"
phase = "main1"
storm = 4
[[stack]]
card = "Psychatog"
by = "them"
[[stack]]
card = "Counterspell"
by = "you"
target = "Psychatog"
[[stack]]
card = "Counterspell"
by = "them"
target = "Counterspell"
[them]
life = 19
library = 26
hand = ["?", "?", "?"]
lands = ["Island", "Island", "Swamp", "Island (tapped)", "Island (tapped)", "Island (tapped)", "Island (tapped)", "Island (tapped)", "Swamp (tapped)", "Underground River (tapped)"]
graveyard = ["Polluted Delta", "Opt", "Impulse", "Accumulated Knowledge", "Island", "Smother", "Gush", "Swamp", "Psychatog", "Accumulated Knowledge", "Island", "Swamp", "Island", "Fact or Fiction", "Duress", "Counterspell", "Accumulated Knowledge", "Island", "Impulse"]
[you]
life = 20
library = 32
hand = ["Counterspell", "Brain Freeze"]
lands = ["Island", "Island", "Island", "Island", "Island", "Island", "Island (tapped)", "Island (tapped)"]
graveyard = ["Opt", "Portent", "Impulse", "Opt", "Vision Charm", "Counterspell", "Portent", "Flash of Insight", "Peek", "Vision Charm", "Opt", "Counterspell", "Portent", "Impulse", "Vision Charm", "Opt", "Portent"]
{/puzzle}

Game two against Psychatog. They cast Psychatog and you countered it; in response they cast Impulse, then countered your Counterspell. What do you do?

{answer}
Don't counter back. Let their Counterspell resolve: your Counterspell goes to the graveyard, and the Psychatog is still on the stack. Flash back Flash of Insight, exiling the seventeen blue cards now in your graveyard, and look for your second Brain Freeze. If it is there, cast both Freezes, for thirty-nine cards against a library of twenty-six, before the Tog resolves. If it isn't, counter the Psychatog with the Counterspell in your hand.

**The count.** Four spells have been cast this turn: their Impulse, the Psychatog, your Counterspell and theirs. The Flash makes five. The first Freeze is then six instances, eighteen cards; the second counts the first and is seven, twenty-one. Thirty-nine, thirteen more than they have.

**Why not counter back.** It doesn't keep the Tog off the table: they have three cards and three lands open, and another Counterspell or a Foil puts it back on course. And it doesn't win: two of your six Islands go on the Counterspell, and what is left buys the Flash and one Freeze, twenty-one cards, five short. With two more Psychatogs in their library, holding this one off only buys a turn; the mill is how the game ends.

**Why let their counter resolve first.** It puts your countered Counterspell in the graveyard, one more blue card for the Flash to exile: seventeen cards seen instead of sixteen. And the Psychatog is still on the stack while you look, so nothing is given up yet.

**What they can do about it.** If they counter the Flash, they have spent a counter and a card on it, and the Tog is still on the stack with your Counterspell and four Islands behind it. If the Flash resolves and finds the Freeze, they can't stop the mill: three cards and three lands counter two copies at most, a Counterspell and a Foil, and six cards off thirty-nine still leaves thirty-three.

**Playing to your outs.** Both your other Freezes are among your thirty-two cards, and the Flash sees seventeen of them. It misses both only when all seventeen come from the thirty other cards, about one time in five, so it finds a Freeze about four times in five. When it misses, it almost always shows a Gush: take it, and its two draws come from the fifteen cards you haven't seen, a Freeze about a quarter of the time. That adds about one game in twenty. If nothing turns up, Counterspell the Psychatog with the one in your hand, and keep the Freeze rather than fire it short: a partial mill only feeds the Togs still in their library.
{/answer}

### Puzzle 9: before the Confinement lands

{puzzle}
turn = 27
active = "them"
phase = "main1"
storm = 7
[[stack]]
card = "Solitary Confinement"
by = "them"
[[stack]]
card = "Argothian Enchantress"
by = "them"
ability = "Draw a card."
kind = "triggered"
[[stack]]
card = "Enchantress's Presence"
by = "them"
ability = "Draw a card."
kind = "triggered"
[[stack]]
card = "Enchantress's Presence"
by = "them"
ability = "Draw a card."
kind = "triggered"
[them]
life = 19
library = 25
hand = ["?", "?", "?"]
lands = ["Forest", "Forest", "Serra's Sanctum (tapped)", "Forest (tapped) + Wild Growth", "Forest (tapped) + Fertile Ground", "Plains (tapped)", "Plains (tapped)", "Brushland (tapped)"]
permanents = ["Argothian Enchantress", "Enchantress's Presence", "Enchantress's Presence", "Exploration", "Sterling Grove", "Mirri's Guile", "Elephant Grass", "Seal of Cleansing", "Sylvan Library"]
graveyard = ["Xantid Swarm", "Abeyance", "Opalescence", "Forest", "Seal of Cleansing", "Plains", "Replenish", "Xantid Swarm", "Abeyance", "Opalescence", "Plains", "Forest"]
[you]
life = 20
library = 30
hand = ["Opt", "Brain Freeze", "Gush"]
lands = ["Island", "Island", "Island", "Island", "Island", "Island", "Island"]
graveyard = ["Opt", "Portent", "Island", "Island", "Foil", "Essence Flare", "Counterspell", "Gush", "Portent", "Vision Charm", "Stifle", "Impulse", "Island", "Annul", "Foil", "Essence Flare", "Counterspell", "Gush", "Opt", "Flash of Insight"]
{/puzzle}

Game two against Enchantress. They have spent their turn casting seven spells, and the last is a Solitary Confinement, with the draw triggers from their three Enchantress effects above it on the stack. What do you do?

{answer}
Pounce now. Dig for Stifles first — two if the mana and the cards allow — then Brain Freeze them, Stifle any Gaea's Blessing trigger, and let their own Enchantress triggers finish the job. Tap two Islands for mana and Gush them back to your hand, cast Opt, and flash back Flash of Insight; then Freeze with whatever Stifles you have found.

**The count.** Seven spells have been cast this turn; your Gush, Opt and Flash make ten. One Freeze is then eleven instances, thirty-three cards, against a library of twenty-five. And the draw triggers sit below anything you cast: once the Freeze has emptied their library they resolve, they draw from an empty library, and they lose.

**Play around the Blessing.** You haven't seen one, but after sideboarding they bring Gaea's Blessing, and most lists bring two. A Blessing put into the graveyard from the library shuffles the whole graveyard back in, every card the Freeze has milled with it, and a Freeze that empties their library is certain to mill any that are in it. So each one needs a Stifle, and you have none in hand.

**Dig cheapest first.** Seven Islands pay for exactly this: Opt one, the Flash two, the Freeze two, and a Stifle for each Blessing. The Gush costs nothing if you tap the two Islands it returns for mana first and spend that mana before the phase ends. Three Stifles are left in your library: the Gush's two cards, the Opt and the Flash's eighteen find at least one nearly every time, and two about a third of the time.

**Why now, whatever you find.** Once the Confinement resolves they have shroud, and the Freeze can't target them; Sterling Grove gives their other enchantments shroud, so a single Chain of Vapor can't bounce it either. The other line is to dig for a counter for the Confinement instead, but a counter spent there is one you don't have for the next Opalescence or Replenish, and those are what kill you. The storm is here now, they are short of white mana for an Abeyance with only Forests open, and their own triggers will finish them: Freeze with one Stifle if one is all you have, and with none if it comes to that.
{/answer}
{/answer}

### Puzzle 10: the Squirrel army

{puzzle}
turn = 13
active = "you"
phase = "main1"
[them]
life = 15
library = 46
hand = []
lands = ["Mountain", "Karplusan Forest", "Karplusan Forest (tapped)", "Forest (tapped)", "Gaea's Cradle (tapped)"]
permanents = ["Deranged Hermit", "Squirrel token", "Squirrel token", "Squirrel token", "Squirrel token", "Llanowar Elves", "Fyndhorn Elves", "Wirewood Symbiote"]
graveyard = ["Llanowar Elves", "Priest of Titania", "Nantuko Vigilante", "Anger", "Survival of the Fittest"]
[you]
life = 12
library = 45
hand = ["Flash of Insight", "Powder Keg", "Island"]
lands = ["Island", "Island", "Island", "Island"]
permanents = ["Phyrexian Dreadnought"]
graveyard = ["Daze", "Opt", "Counterspell", "Chain of Vapor", "Counterspell", "Portent", "Stifle"]
{/puzzle}

Game one against Elves. Your Dreadnought came down last turn and can attack; you have just drawn a Powder Keg and haven't played your land. Their Deranged Hermit came down on their last turn. What's your plan, for this turn and theirs?

{answer}
Play the Island and the Keg, leave the Keg at zero — no fuse counter in your upkeep, and don't crack it — and attack. Crack it only when not cracking would kill you or your Dreadnought: in response to a block that would kill it, or to an attack that would kill you.

**Their engine.** Survival is gone, but Anger is already in their graveyard, and with their Mountain every creature they have has haste. Deranged Hermit is an Elf, so once a turn Wirewood Symbiote can return it to their hand, and five mana recasts it for four fresh Squirrels — hasty, and 2/2 while a Hermit is out. That is the only way they make more tokens, and one Keg at zero kills every token on the battlefield.

**Why not crack it now.** It kills four Squirrels, and they make four more next turn: the Symbiote bounces the Hermit in response to its echo trigger, so there is no echo to pay, and they recast it. Four hasty 2/2 Squirrels, the Hermit and their three other creatures are twelve damage, your Dreadnought is tapped from attacking, and you are at twelve.

**If they block with everything.** Four 2/2 Squirrels, the Hermit and their three other creatures have twelve power, exactly enough to kill the Dreadnought. After blockers are declared, crack the Keg: the Squirrels die, and the Dreadnought kills everything that blocked it and tramples over — the Symbiote can save the Hermit by bouncing it, and it changes nothing. With no creatures left, Gaea's Cradle makes no mana, and their four other lands can't pay five for the Hermit. Your next swing is lethal — unless they draw a fifth land, and even then four Squirrels and a Hermit can't kill you from twelve.

**If they don't block.** Twelve takes them to three. On their turn, if they bounce and recast the Hermit and swing with everything, crack the Keg once attackers are declared: all eight Squirrels die, you take four from the rest, and the Symbiote has been used for the turn. If they pay the echo instead and swing with everything, crack the Keg on the attack all the same; after combat they can recast the Hermit for four fresh blockers, and the Symbiote untaps one more on your turn — it works once in each player's turn. That wall has eleven toughness and eleven power: the Dreadnought survives it, kills all of it, and tramples one over. They have nothing left, and the next swing ends it. And if their attack wouldn't kill you, don't crack it: take the damage, and crack it after they block your next swing.

**If they chump.** A single Squirrel in front of the Dreadnought soaks two, and ten takes them to five. Next turn, if their attack can't kill you, let it through and keep the Keg; your next swing, with the Keg cracked after blocks, tramples over whatever is left.

**The lesson.** Cracking the Keg now looks like value: four Squirrels for one card. But a Keg on the table is a threat they have to play around, and while it sits there untouched it shapes every attack and every block they make; once it is cracked, it shapes nothing. Hold it until it answers the board that would kill you.

**Never at one.** The Dreadnought's mana value is one: a fuse counter in your upkeep turns the Keg into a way to kill your own Dreadnought.
{/answer}

### Puzzle 11: the race against Survival

{puzzle}
turn = 7
active = "them"
phase = "main1"
[[stack]]
card = "Volrath's Shapeshifter"
by = "them"
[[stack]]
card = "Impulse"
by = "you"
[choice]
label = "Impulse: put one into your hand"
cards = ["Chain of Vapor", "Counterspell", "Vision Charm", "Island"]
[them]
life = 3
library = 47
hand = ["Phyrexian Devourer", "Triskelion"]
lands = ["City of Brass (tapped)", "Gemstone Mine (tapped) [1]", "Underground River (tapped)", "Llanowar Wastes (tapped)"]
permanents = ["Survival of the Fittest", "Birds of Paradise (tapped)"]
graveyard = ["Duress", "Birds of Paradise", "Squee, Goblin Nabob", "Palinchron"]
[you]
life = 20
library = 49
hand = ["Island", "Powder Keg", "Island"]
lands = ["Island", "Island (tapped)", "Island (tapped)"]
permanents = ["Phyrexian Dreadnought (tapped)"]
graveyard = ["Counterspell", "Opt", "Stifle"]
{/puzzle}

Game one against Full English Breakfast. They mulliganed to six, and their first-turn Duress took your Counterspell; your Dreadnought came down on your second turn and has hit them once. Two turns ago Survival of the Fittest turned a Birds of Paradise into Squee and Squee into a Triskelion; this turn it turned the returning Squee into Palinchron and the Palinchron into Phyrexian Devourer, and they have tapped out to cast Volrath's Shapeshifter. In response you cast Impulse, and it shows you Chain of Vapor, Counterspell, Vision Charm and an Island. Which do you take, and what do you do next?

{answer}
Take the Vision Charm, and with your last Island Charm their library while the Shapeshifter is still on the stack. One mana left means one play: the Charm is the one that wins, and the Chain isn't. The Counterspell would answer the Shapeshifter outright, but it costs two, and you have one Island left.

**What they have set up.** The Shapeshifter has the text of the top card of their graveyard while that card is a creature, and the top card is Palinchron. It enters as a Palinchron, and its trigger untaps their lands. With that mana Survival does the rest: the Devourer in their hand goes to the graveyard, the Shapeshifter becomes a Devourer and grows as they exile their library, and discarding the Triskelion in their hand turns it into a Triskelion with every one of those counters to shoot you with. You are at twenty, and that is the kill.

**What the Charm does.** Four cards from their library go on top of the Palinchron. If none of them is a creature, the Shapeshifter enters as itself; if any is, they choose which of the four goes on top, and it enters as that creature. It can't be a Palinchron, so most of the time the untap never happens; the exception is below.

**Why that wins.** Without the untap they are tapped out. The kill needs two more payments — a green for Survival to discard the Devourer, then a green or the Shapeshifter's two to discard the Triskelion — and nothing of theirs makes the mana for both before their next untap step. (A Shapeshifter that enters as a Wall of Roots makes one green, but discarding either 1/1 to Survival leaves it a 1/0 with the Wall's counter on it, and it dies.) Your Dreadnought swings before that untap step comes. Whatever the Shapeshifter has become can block, but it would need ten toughness to keep twelve trampling damage from killing them: they are at three.

**Why not the Chain.** There is no moment when it stops them. It can't touch the Shapeshifter while it is a spell, so its useful targets are Survival and, once the Shapeshifter has resolved, the Shapeshifter itself, and neither stops them. Chain Survival and the Palinchron untaps their four lands, enough to recast Survival, discard the Devourer and discard the Triskelion this turn; they can even sacrifice a land to copy the Chain onto your Dreadnought. Chain the Shapeshifter with its trigger on the stack and the lands still untap; they recast it, and it enters as a Palinchron again. Wait until the untap has happened and Chain the Shapeshifter, and they kill you in response: the mana is theirs and the Triskelion is already in their hand, so the whole kill fits in before the Chain resolves.

**The risk.** They order the four milled cards, so a creature among them that helps them goes on top: a Karmic Guide brings the Palinchron back and untaps their lands after all. Nothing in your hand answers that, but without the Charm you are dead this turn, so it is the play.
{/answer}

### Puzzle 12: the quiet turn

{puzzle}
turn = 10
active = "you"
phase = "main1"
[them]
life = 18
library = 47
hand = ["Armageddon", "Pyroblast", "Call of the Herd"]
lands = ["Forest (tapped)", "Treetop Village (tapped)", "Battlefield Forge", "Rishadan Port (tapped)", "Tranquil Thicket (tapped)"]
permanents = ["Terravore"]
graveyard = ["Windswept Heath", "Tranquil Thicket", "Sylvan Library", "Secluded Steppe"]
[you]
life = 20
library = 47
hand = ["Phyrexian Dreadnought", "Phyrexian Dreadnought", "Stifle", "Vision Charm", "Back to Basics", "Annul"]
lands = ["Island", "Island", "Island", "Island", "Island"]
permanents = []
graveyard = ["Annul", "Peek"]
{/puzzle}

Game two against Naya Terrageddon. They mulliganed to six. Your Peek at the end of their turn showed you their hand. What do you do?

{answer}
Cast a Dreadnought and Stifle its trigger. When they Pyroblast the Stifle, let the Dreadnought go: don't Charm it. (Leading with the Charm instead of the Stifle is the same bait; keep whichever is left for the second Dreadnought.) Cast Back to Basics with your last three Islands, and next turn cast the second Dreadnought with the Charm.

**What they have set up.** Terravore counts every land card in every graveyard, and three are there already: it is a 3/3. They spent their turn putting it down, not on Armageddon, because Armageddon with nothing on the table wins nothing. Next turn they untap, cast it, and every land on the table goes to the graveyard: their five, your five, and the Terravore is at least a 13/13. That beats a Dreadnought, and you have no lands left to rebuild with.

**Why Back to Basics wins.** Their mana is a Forest and four nonbasics. Under Back to Basics the nonbasics don't untap, and the Treetop Village, the Rishadan Port and the Tranquil Thicket are tapped already; only the Forest untaps. The Battlefield Forge is the only one left, and it is their only red and their only white. Once they tap it for the Pyroblast, they have the Forest and nothing else: no Armageddon, no blast, no Call of the Herd. Next turn the second Dreadnought comes down with the Charm to protect it, and there is very little they can do about it.

**Why the Dreadnought first.** Back to Basics into an open Forge and a known Pyroblast is countered, and a blast still in their hand would destroy it later anyway, so the blast has to go before it lands. The Dreadnought is the card they can't let resolve. They haven't seen Back to Basics, and from their side a 12/12 with Stifle behind it could be followed by a Gush in response to Armageddon or by another answer. The blast goes on the Stifle, and the Forge is tapped.

**Why not save it.** The Charm saves the Dreadnought, but it leaves you two Islands, one short of Back to Basics. They untap, Armageddon resolves, and a 13/13 beats the Dreadnought. A Dreadnought on the table is worth less than the lock: under Back to Basics the second one is far safer next turn. Casting the second Dreadnought with the Charm this turn, instead of Back to Basics, loses the same way.

**Why not Back to Basics first.** They blast it, and you are back to sticking a Dreadnought that Armageddon beats.

**The risk.** A player who reads the board and keeps the blast lets the Dreadnought resolve, then counters Back to Basics, and Armageddon wins. Most won't: they can't see your hand. After the lock, a Naturalize or a Disenchant off the top needs a basic land or a fetch to go with it, and they have no land in hand, so it takes two good draws, and by then the Dreadnought should have done its work.
{/answer}

### Puzzle 13: three cards deep

{puzzle}
turn = 10
active = "you"
phase = "main2"
[[stack]]
card = "Portent"
by = "you"
target = "Opponent"
[choice]
label = "Portent: put them back in any order, or shuffle"
cards = ["Naturalize", "Armageddon", "Disenchant"]
[them]
life = 7
library = 47
hand = ["Pyroblast", "Pyroblast"]
lands = ["Forest (tapped)", "Tranquil Thicket (tapped)", "Rith's Grove (tapped)", "Rishadan Port (tapped)"]
permanents = ["Terravore"]
graveyard = ["Windswept Heath", "Tranquil Thicket", "Sylvan Library", "Secluded Steppe", "Tranquil Thicket", "Swords to Plowshares"]
[you]
life = 20
library = 47
hand = ["Vision Charm", "Island"]
lands = ["Island (tapped)", "Island (tapped)", "Island", "Island", "Island"]
permanents = ["Phyrexian Dreadnought (tapped)"]
graveyard = ["Annul", "Stifle", "Counterspell", "Peek"]
{/puzzle}

Game two against Naya Terrageddon. They mulliganed to five. Your Peek earlier this turn showed you their hand, and your Dreadnought has just hit them. Your Portent shows you the top three cards of their library. How do you put them back, or do you shuffle?

{answer}
Put Armageddon on top; the other two can go in any order. Then, in their upkeep, Vision Charm Lairs into Islands to make their Rith's Grove tap only for blue.

**Where the game is.** They are at seven. Next turn your Dreadnought attacks again; if the Terravore blocks, eight trample over, and they are dead. Each of the three cards would save them. Naturalize and Disenchant kill the Dreadnought. Armageddon makes the Terravore a 13/13 — the four lands in the graveyards, their four and your five — and it walls the Dreadnought and then kills it. You can stop only one of them, and it isn't the obvious one.

**The ruling.** On the Planeshift printing the type line just says "Land", but the text box makes Rith's Grove a Lair as well, and today's Oracle text puts it on the type line: "Land — Lair". Lair is a land type, just as Island and Forest are. Vision Charm's third mode reads "Choose a land type and a basic land type": the first type can be any land type, not only a basic one. Name Lair and Island, and until end of turn every Lair on the table is an Island. It loses its own ability and taps only for blue.

**Why Armageddon.** Their Rith's Grove is their only white and their only red. Charm the Lairs into Islands in their upkeep, and either way Armageddon can't be cast. If they blast the Charm, they have to tap the Grove for the red, and their white goes with it; the Grove stays tapped until their next untap step, so they have no red or white on your turn either. If they float the white in response, it empties at the end of the upkeep, before they have even drawn the Armageddon. If they let the Charm resolve, the Grove taps for blue until the end of their turn, and on your turn they hold two Pyroblasts that can't touch a colorless Dreadnought. It attacks, and they are dead.

**Why not Naturalize.** It costs green, and they have green in the Forest and the Thicket as well as the Grove; the Thicket has no land type for the Charm to name, and one Charm can't cover the rest. Charm the Dreadnought in response to phase it out, and they blast the Charm with the Grove: the Dreadnought dies. The blasts in their hand are why the Charm is only half an answer here.

**Why not Disenchant.** It needs the Grove's white, so they can't Disenchant and blast in the same turn, but they don't need to. Cast on their own turn, you would phase the Dreadnought out in response and it would phase back in at your untap step, so they wait for your turn and Disenchant at the beginning of combat. Charm the Dreadnought in response, and it phases out and misses the attack, and next turn they draw the Armageddon or the Naturalize. Charm Lairs into Islands in their upkeep instead, and they let it resolve: at the end of their turn the Grove is a Lair again, untapped, and the Disenchant comes on your turn with the Charm already spent.

**Why not shuffle.** Their deck is full of answers to the Dreadnought, and a shuffle trades a certain win for a random card. Charming them to mill four throws all three away too, but it spends the Charm, and their next draw is just as random.
{/answer}

### Puzzle 14: five cards, two piles

{puzzle}
turn = 16
active = "you"
phase = "end"
[[stack]]
card = "Fact or Fiction"
by = "them"
[choice]
label = "Fact or Fiction: separate them into two piles"
cards = ["Meddling Mage", "Disenchant", "Swords to Plowshares", "Counterspell", "Island"]
[them]
life = 20
library = 41
hand = []
lands = ["Island (tapped)", "Plains (tapped)", "Adarkar Wastes (tapped)", "Island (tapped)", "Coastal Tower (tapped)", "Plains (tapped)", "Island (tapped)", "Plains (tapped)"]
permanents = ["Meddling Mage (tapped) (naming Phyrexian Dreadnought)"]
graveyard = ["Disenchant", "Fact or Fiction", "Mana Leak", "Counterspell"]
[you]
life = 14
library = 43
hand = ["Phyrexian Dreadnought", "Counterspell", "Stifle", "Vision Charm"]
lands = ["Island", "Island (tapped)", "Island (tapped)", "Island (tapped)", "Island (tapped)", "Island (tapped)"]
permanents = ["Powder Keg [1]"]
graveyard = ["Stifle", "Phyrexian Dreadnought", "Counterspell", "Opt", "Impulse", "Counterspell"]
{/puzzle}

Game two against UW Web Control. At the end of your turn they cast Fact or Fiction. You countered it, they Mana Leaked your Counterspell, you paid, and they countered it. How do you split the five cards?

{answer}
Keep the Disenchant away from the Meddling Mage and the Counterspell: Disenchant, Swords to Plowshares and Island in one pile; Meddling Mage and Counterspell in the other. The Swords and the Island can go on either side; the Disenchant can't.

{cards: Disenchant | Swords to Plowshares | Island}

{cards: Meddling Mage | Counterspell}

**Your plan.** Their Mage names the Dreadnought, and your Keg is the way past it. In your upkeep it goes to two, you crack it, and every Mage on the table dies: Meddling Mage costs two. Then the Dreadnought comes down with the Stifle, and the Counterspell and the Vision Charm are left to protect it: the Dreadnought is an artifact, so the Charm can phase it out in response to a Swords or a Disenchant. You have one Island until then; everything untaps before your upkeep.

**Their plan is the Keg.** The Disenchant isn't really an answer to the Dreadnought here: it is the answer to the Keg. Cast on their own turn, it meets your Charm, and the Keg phases back in at your untap step in time to tick. On its own, it has to wait for your upkeep, in response to the Keg's trigger, and there it meets your Counterspell. (The Charm would save the Keg there too, but a phased-out Keg misses the upkeep and comes back a full turn later, with the Mage still on the table.) Alone, the Disenchant loses; it must not get help.

**Why not with the Mage.** On their turn the new Mage names Vision Charm, and the Disenchant goes on the Keg: your one Island can't cast the Counterspell. Charm the Keg in response to the Mage instead, and they Disenchant it in response to the Charm.

**Why not with the Counterspell.** On their turn the Disenchant goes on the Keg, your Charm answers, and their Counterspell counters the Charm.

**If they take Disenchant, Swords and Island.** Every line has an answer:

- Disenchant on the Keg on their turn: your one Island Charms it. It phases back in at your untap step, ticks to two in your upkeep, and you crack it. The Dreadnought comes down with the Stifle, and the Counterspell is left for the Swords.
- Disenchant on the Keg in your upkeep, in response to its trigger: your Counterspell counters it, and you crack the Keg. The Dreadnought comes down with the Stifle, and the Charm is left for the Swords.
- Disenchant once the Keg has its second counter: crack the Keg in response, and the Mage dies before the Disenchant resolves.
- Both saved for the Dreadnought: the Keg kills the Mage, the Stifle takes the trigger, and the Swords and the Disenchant meet your Counterspell and your Charm, one each.

**If they take Meddling Mage and Counterspell.** The new Mage can name what it likes: it dies to the Keg with the first one, before you cast anything it could name, and their Counterspell can't stop the Keg, because cracking it is an ability. After that their Counterspell meets yours, the Stifle takes the trigger, and the Charm is spare.

**The natural splits lose.** Isolate the Swords, the cheap answer to the Dreadnought, and the Mage, the Disenchant and the Counterspell go together. Isolate the Mage, the card that looks like the lock, and the Disenchant goes with the Counterspell.

**The risk.** They draw a card next turn, and a second counter or a second answer to the Keg off the top can still beat you.
{/answer}
