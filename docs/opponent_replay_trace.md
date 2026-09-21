# Opponent Replay Trace

Purpose: reconstruct the exact hour-by-hour opening used by the winning
opponent in a real ranked match, from the recorded replay, so it can be
replicated in `main.py` later. This is different from a determinism check
against our own agent -- there is only one recorded seed here
(`replays/110311259.json`, local only, not tracked in git), so nothing below
is confirmed to generalize across seeds. It is a single, concrete example of
a stronger opening to learn from and adapt, not a verified-deterministic
script the way our own agent's early days are.

Match: `Yendrew Y` (us, player 0) vs `Alua Аkhmetkali` (player 1, the
opponent traced below). Final money 90253 vs 140537 -- a real loss. See
`docs/experiment-log.md` ("Replay-informed opening study") for the earlier
mid-game analysis of this same match.

Positions are `(x, y)`; hands are listed in `farm["hands"]` order (hand 0
first). All data below is the opponent's (player index 1) own recorded
observation/action stream, extracted directly from the replay JSON -- not a
local re-simulation.

Do not implement any single day in isolation. The opponent's plan is
already visibly progressive (pasture construction starts on day 1, before
any animal is placed in the new pastures), so an early day's script only
makes sense together with the days that complete what it starts.

**Reading the hour-by-hour tables below**: the position shown for a given
hour already reflects that hour's own action having been applied -- e.g.
`H21 farmer=EAST` with position `(3,4)` means the farmer moved from
`(2,4)` (its position at `H20`) to `(3,4)`, not that it was at `(3,4)` when
it chose `EAST`. This was confirmed while investigating the `DROP` action
below (see `docs/mechanics.md`, "Observation/action pairing"). It doesn't
change any of the sequencing or tile-assignment facts recorded here, but
matters if you're reconstructing exact per-hour positions for a scripted
implementation.

## Day 0

Opens with 5 hands (not our 4), 2 Cows, 2 Sheep, 12 Melon, and **7 Wheat**
planted as a crop (not just bought as feed) -- matching the "common
high-ranking template" already noted in `docs/current_roadmap.md`'s
top-player replay study.

End-of-day-0 tile state (NW quadrant; 23 of 25 tiles used, `(4,2)` and
`(2,4)` still empty):

- Cows: `(4,4)`, `(4,3)` -- same positions our own agent uses.
- Sheep: `(3,4)`, `(3,3)` -- same positions our own agent uses.
- Wheat (7 tiles, all watered): `(0,0) (1,0) (2,0) (0,1) (1,1) (0,2) (0,3)`
- Melon (12 tiles, all watered): `(3,0) (4,0) (2,1) (3,1) (4,1) (1,2) (2,2)
  (3,2) (1,3) (2,3) (0,4) (1,4)`

Hour-by-hour actions (farmer / hand0 / hand1 / hand2 / hand3 / hand4 / market):

```text
H00 farmer=PASS                                                                                    market=[]
H01 farmer=PASS                                                                                    market=BUY_PRODUCT WHEAT 10, SELL WHEAT 10
H02 farmer=NORTH                                                                                   market=SELL WHEAT 13, BUY_PRODUCT WHEAT 5, HIRE x5, BUY_ANIMAL COW 2, BUY_ANIMAL SHEEP 2
H03 farmer=SOUTH            h0=PICKUP COW   h1=PASS      h2=NORTH     h3=NORTH     h4=PICKUP COW    market=[]
H04 farmer=PICKUP SHEEP     h0=NORTH        h1=PASS      h2=NORTH     h3=NORTH     h4=BUILD_PASTURE market=[]
H05 farmer=PICKUP WHEAT     h0=BUILD_PASTURE h1=PASS     h2=NORTH     h3=NORTH     h4=PLACE COW     market=[]
H06 farmer=NORTH            h0=PLACE COW    h1=PASS      h2=NORTH     h3=WEST      h4=CARE          market=[]
H07 farmer=WEST             h0=NORTH        h1=PASS      h2=NORTH     h3=WEST      h4=PICKUP SHEEP  market=BUY_SEED MELON 2
H08 farmer=BUILD_PASTURE    h0=NORTH        h1=PASS      h2=PLANT MELON h3=PLANT MELON h4=PICKUP WHEAT market=BUY_SEED MELON 1
H09 farmer=PLACE SHEEP      h0=PLANT MELON  h1=PASS      h2=WATER     h3=WATER     h4=WEST          market=[]
H10 farmer=FEED             h0=WATER        h1=PASS      h2=WEST      h3=NORTH     h4=BUILD_PASTURE market=BUY_SEED MELON 1
H11 farmer=CARE             h0=WEST         h1=PASS      h2=PLANT MELON h3=WEST    h4=PLACE SHEEP   market=BUY_SEED MELON 2
H12 farmer=WEST             h0=PLANT MELON  h1=PASS      h2=WATER     h3=PLANT MELON h4=FEED         market=BUY_SEED MELON 1
H13 farmer=PLANT MELON      h0=WATER        h1=PASS      h2=WEST      h3=WATER     h4=CARE          market=BUY_SEED WHEAT 1
H14 farmer=WATER            h0=SOUTH        h1=PASS      h2=PLANT WHEAT h3=WEST    h4=WEST          market=BUY_SEED WHEAT 1
H15 farmer=WEST             h0=WEST         h1=PASS      h2=WATER     h3=PLANT WHEAT h4=WEST         market=BUY_SEED MELON 3
H16 farmer=PLANT MELON      h0=PLANT MELON  h1=PASS      h2=WEST      h3=WATER     h4=PLANT MELON   market=BUY_SEED WHEAT 1
H17 farmer=WATER            h0=WATER        h1=PASS      h2=PLANT WHEAT h3=WEST    h4=WATER         market=BUY_SEED WHEAT 1
H18 farmer=PASS             h0=WEST         h1=PASS      h2=WATER     h3=PLANT WHEAT h4=WEST         market=BUY_SEED MELON 2
H19 farmer=PASS             h0=PLANT MELON  h1=PASS      h2=PASS      h3=WATER     h4=PLANT MELON   market=[]
H20 farmer=PASS             h0=WATER        h1=PASS      h2=PASS      h3=NORTH     h4=WATER         market=BUY_SEED WHEAT 1
H21 farmer=PASS             h0=WEST         h1=PASS      h2=PASS      h3=PLANT WHEAT h4=NORTH        market=BUY_SEED WHEAT 2
H22 farmer=PASS             h0=PLANT WHEAT  h1=PASS      h2=PASS      h3=WATER     h4=PLANT WHEAT   market=[]
H23 farmer=PASS             h0=WATER        h1=PASS      h2=PASS      h3=PASS      h4=WATER         market=[]
```

End money: 16.

Notes:

- **Hand 1 (index 1) does nothing all day.** It moves from its spawn tile to
  `(5, 4)` (a shed-access tile) at hour 2 and then `PASS`es every remaining
  hour. This looks like a real inefficiency in the opponent's own script,
  not something to copy -- they won this match despite it, not because of it.
- Buys and sells Wheat as a product in the same early hours (`BUY_PRODUCT
  WHEAT 10` then `SELL WHEAT 10` at H01; `SELL WHEAT 13` + `BUY_PRODUCT
  WHEAT 5` at H02). Net effect and intent are not yet understood -- flag for
  a dedicated look before copying any part of this pattern.
- Plants both Wheat and Melon on day 0 (unlike our agent, which only plants
  Melon on day 0). Melon planting is interleaved with Wheat planting rather
  than batched.
- Cow and Sheep pasture positions are identical to our own agent's
  (`(4,4)`, `(4,3)` for Cows; `(3,3)`, `(3,4)` for Sheep).

## Day 1

Only 3 new hands hired (down from 5 on day 0) -- hiring is clearly
budget-driven, not a fixed daily count.

Start-of-day-1 state matches end-of-day-0 exactly (as expected). End-of-day-1
tile state:

- Same 2 Cows, 2 Sheep, 7 Wheat, 12 Melon tiles as day 0, **plus two new
  empty pastures** at `(4,2)` and `(2,4)` -- built this day but not yet
  occupied by an animal.
- All 7 Wheat tiles re-watered (`watered_today = True`).
- **All 12 Melon tiles left un-watered** this day (`watered_today = False`).
  Melon doesn't harvest until day 10 and only turns to weed after 2
  consecutive missed waterings, so skipping one day is safe; the opponent
  is prioritizing Wheat (4-day maturity, already being cycled for cash)
  over Melon this day.

Hour-by-hour actions (farmer / hand0 / hand1 / hand2 / market):

```text
H00 farmer=PASS                                                                     market=[]
H01 farmer=PICKUP WHEAT                                                             market=HIRE x3
H02 farmer=NORTH            h0=WEST          h1=NORTH        h2=NORTH               market=[]
H03 farmer=WEST             h0=PICKUP WHEAT  h1=PICKUP WHEAT h2=WEST                market=[]
H04 farmer=FEED             h0=NORTH         h1=FEED         h2=WEST                market=[]
H05 farmer=CARE             h0=FEED          h1=CARE         h2=WEST                market=[]
H06 farmer=COLLECT_FERTILIZER h0=CARE        h1=COLLECT_FERTILIZER h2=BUILD_PASTURE market=[]
H07 farmer=SOUTH            h0=COLLECT_FERTILIZER h1=PLACE FERTILIZER h2=NORTH      market=SELL FERTILIZER 1, BUY_PRODUCT WHEAT 3
H08 farmer=EAST             h0=SOUTH         h1=NORTH        h2=WEST                market=BUY_PRODUCT WHEAT 1
H09 farmer=PLACE FERTILIZER h0=PLACE FERTILIZER h1=NORTH     h2=WEST                market=SELL FERTILIZER 2
H10 farmer=PASS             h0=PASS          h1=BUILD_PASTURE h2=WATER              market=BUY_PRODUCT WHEAT 1
H11 farmer=PASS             h0=PASS          h1=SOUTH        h2=NORTH               market=[]
H12 farmer=PASS             h0=PASS          h1=SOUTH        h2=WATER               market=BUY_PRODUCT WHEAT 1
H13 farmer=PASS             h0=PASS          h1=PICKUP WHEAT h2=NORTH               market=[]
H14 farmer=PASS             h0=PASS          h1=WEST         h2=EAST                market=BUY_PRODUCT WHEAT 1
H15 farmer=PASS             h0=PASS          h1=FEED         h2=WATER               market=[]
H16 farmer=PASS             h0=PASS          h1=COLLECT_FERTILIZER h2=WEST          market=BUY_PRODUCT WHEAT 1
H17 farmer=PASS             h0=PASS          h1=CARE         h2=WATER               market=[]
H18 farmer=PASS             h0=PASS          h1=PASS         h2=NORTH               market=[]
H19 farmer=PASS             h0=PASS          h1=PASS         h2=WATER               market=[]
H20 farmer=PASS             h0=PASS          h1=PASS         h2=EAST                market=[]
H21 farmer=PASS             h0=PASS          h1=PASS         h2=WATER               market=[]
H22 farmer=PASS             h0=PASS          h1=PASS         h2=EAST                market=[]
H23 farmer=PASS             h0=PASS          h1=PASS         h2=WATER               market=[]
```

End money: 107.

Notes:

- Hand 1 (`(4,2)`) and hand 2 (`(2,4)`) each build one new empty pasture on
  day 1 -- these are staged ahead of the animals that will occupy them
  (matches the full-match trace showing Cow count rising to 3 by day 2 and
  4 by day 4). This is a materially different pattern from our own agent,
  which builds a pasture and places its animal in the same short window.
- Hand 0 and the farmer each run one FEED/CARE cycle early (the existing 2
  Cows and 2 Sheep, one cycle each -- unclear yet which unit owns which
  animal type; needs a longer trace to disambiguate, unlike our own agent
  where the farmer clearly owns Cows and hand 0 clearly owns Sheep).
- Farmer and hand 0 both collect and place Fertilizer, then sell it in two
  small batches (`SELL FERTILIZER 1` then `SELL FERTILIZER 2`).
- Several `BUY_PRODUCT WHEAT 1` orders appear spread through the day
  (H07, H08, H10, H12, H14, H16) alongside hand 2's Wheat-tile watering --
  possibly a feed-stock top-up tied to watering progress rather than a
  single batched purchase like our own agent uses.
- Farmer goes idle after hour 9; hand 0 goes idle after hour 10. Only hand 2
  (the Wheat-watering hand) stays active through hour 23.

## Day 2

Closes the gap left by tracing day 3 first: this is where the 3rd Cow
(staged as an empty pasture on day 1) gets placed. Only 4 hands hired.

Start-of-day-2 state matches end-of-day-1 exactly. End-of-day-2 tile state:

- Same 2 Cows, 2 Sheep, 7 Wheat, 12 Melon as before, **plus the 3rd Cow now
  placed at `(4,2)`** (the pasture built on day 1). The pasture at `(2,4)`
  is still empty.
- All 7 Wheat and all 12 Melon tiles re-watered (`watered_today = True`) --
  unlike day 1, which skipped Melon.

Hour-by-hour actions (farmer / hand0 / hand1 / hand2 / market):

```text
H00 farmer=PASS                                                                     market=[]
H01 farmer=PICKUP WHEAT 4                                                           market=SELL FERTILIZER 1, HIRE x4
H02 farmer=FEED             h0=PASS         h1=NORTH        h2=NORTH                market=[]
H03 farmer=CARE             h0=PASS         h1=WEST         h2=NORTH                market=SELL WHEAT 2
H04 farmer=COLLECT_FERTILIZER h0=PASS       h1=WEST         h2=NORTH                market=[]
H05 farmer=NORTH            h0=PASS         h1=WEST         h2=NORTH                market=[]
H06 farmer=FEED             h0=PASS         h1=WEST         h2=WEST                market=[]
H07 farmer=CARE             h0=PASS         h1=WATER        h2=WATER                market=[]
H08 farmer=COLLECT_FERTILIZER h0=PASS       h1=EAST         h2=NORTH                market=[]
H09 farmer=WEST             h0=PASS         h1=WATER        h2=WATER                market=[]
H10 farmer=FEED             h0=PASS         h1=NORTH        h2=WEST                market=[]
H11 farmer=CARE             h0=PASS         h1=WATER        h2=WATER                market=[]
H12 farmer=COLLECT_FERTILIZER h0=PASS       h1=NORTH        h2=WEST                market=[]
H13 farmer=SOUTH            h0=PASS         h1=WATER        h2=HARVEST              market=BUY_SEED WHEAT 1
H14 farmer=FEED             h0=PASS         h1=EAST         h2=PLANT WHEAT          market=[]
H15 farmer=CARE             h0=PASS         h1=WATER        h2=WATER                market=BUY_SEED WHEAT 1
H16 farmer=COLLECT_FERTILIZER h0=PASS       h1=SOUTH        h2=PLANT WHEAT          market=[]
H17 farmer=EAST             h0=PASS         h1=WATER        h2=WATER                market=[]
H18 farmer=PLACE FERTILIZER 4 h0=PASS       h1=WEST         h2=HARVEST              market=SELL FERTILIZER 4, BUY_ANIMAL COW 1, BUY_SEED WHEAT 1
H19 farmer=PICKUP COW       h0=PASS         h1=WEST         h2=PLANT WHEAT          market=[]
H20 farmer=NORTH            h0=PASS         h1=WATER        h2=PASS                 market=[]
H21 farmer=NORTH            h0=NORTH        h1=NORTH        h2=SOUTH                market=[]
H22 farmer=PLACE COW        h0=WATER        h1=PASS         h2=EAST                 market=[]
H23 farmer=CARE             h0=PASS         h1=PASS         h2=WATER                market=[]
```

End money: 222.

Notes:

- **Hand 0 is idle all day again** (`PASS` at `(5, 4)` every hour after
  hour 1) -- same wasted-hand pattern as day 0's hand 1. This recurs on
  roughly every other day so far (days 0 and 2), not every day (days 1 and
  3 had all hands active); worth checking whether it correlates with hand
  count or something else once more days are traced.
- The **farmer** (not a hand) buys, picks up, walks to, and places the 3rd
  Cow directly (`BUY_ANIMAL COW 1` H18, `PICKUP COW` H19, `NORTH` x2,
  `PLACE COW` H22, `CARE` H23) -- a different responsibility split from day
  3's 4th Cow, which a **hand** carried and was still walking toward when
  the day ended.

## Day 3

5 hands hired again (back up from day 1's 3), matching the earlier
full-match summary's `hires_by_day` for the opponent: `{0: 5, 1: 3, 2: 4,
3: 5, ...}`.

Start-of-day-3 state (see the Day 2 gap note above): 3 Cows (`(4,4)`,
`(4,3)`, `(4,2)`), 2 Sheep, 7 Wheat, 12 Melon, one still-empty pasture at
`(2,4)`. All crop tiles start the day unwatered (`w: False` for everything,
including the Wheat that was watered by end of day 1 -- watered state
resets every day as expected).

Hour-by-hour actions (farmer / hand0 / hand1 / hand2 / hand3 / hand4 / market):

```text
H00 farmer=PASS                                                                                        market=[]
H01 farmer=PICKUP WHEAT 3                                                                              market=HIRE x5
H02 farmer=WEST             h0=NORTH        h1=NORTH        h2=NORTH        h3=NORTH        h4=NORTH   market=[]
H03 farmer=FEED             h0=WEST         h1=NORTH        h2=NORTH        h3=WEST         h4=NORTH   market=SELL WHEAT 1
H04 farmer=CARE             h0=WEST         h1=NORTH        h2=NORTH        h3=WEST         h4=NORTH   market=[]
H05 farmer=COLLECT_FERTILIZER h0=WEST       h1=NORTH        h2=NORTH        h3=WEST         h4=NORTH   market=[]
H06 farmer=NORTH            h0=WATER        h1=WEST         h2=WEST         h3=WEST         h4=WEST    market=[]
H07 farmer=FEED             h0=WEST         h1=WEST         h2=WATER        h3=WATER        h4=WEST    market=[]
H08 farmer=CARE             h0=WATER        h1=WEST         h2=NORTH        h3=HARVEST      h4=WEST    market=BUY_SEED WHEAT 1
H09 farmer=COLLECT_FERTILIZER h0=SOUTH      h1=WATER        h2=WATER        h3=PLANT WHEAT  h4=WATER   market=SELL WHEAT 3
H10 farmer=NORTH            h0=WATER        h1=HARVEST      h2=WEST         h3=WATER        h4=HARVEST market=BUY_SEED WHEAT 2
H11 farmer=EAST             h0=WEST         h1=PLANT WHEAT  h2=WATER        h3=NORTH        h4=PLANT WHEAT market=[]
H12 farmer=FEED             h0=WATER        h1=WATER        h2=SOUTH        h3=WATER        h4=WATER   market=[]
H13 farmer=CARE             h0=PASS         h1=NORTH        h2=WATER        h3=HARVEST      h4=SOUTH   market=BUY_SEED WHEAT 1
H14 farmer=COLLECT_FERTILIZER h0=PASS       h1=WATER        h2=SOUTH        h3=PLANT WHEAT  h4=WATER   market=[]
H15 farmer=SOUTH            h0=PASS         h1=SOUTH        h2=WATER        h3=WATER        h4=SOUTH   market=[]
H16 farmer=SOUTH            h0=PASS         h1=SOUTH        h2=SOUTH        h3=NORTH        h4=WATER   market=[]
H17 farmer=PLACE FERTILIZER 3 h0=PASS       h1=SOUTH        h2=SOUTH        h3=WATER        h4=WEST    market=SELL FERTILIZER 3, BUY_ANIMAL COW 1
H18 farmer=COLLECT_FERTILIZER h0=PASS       h1=SOUTH        h2=EAST         h3=NORTH        h4=WATER   market=[]
H19 farmer=PLACE FERTILIZER   h0=PASS       h1=EAST         h2=CARE         h3=WATER        h4=PASS    market=SELL FERTILIZER 1
H20 farmer=CARE             h0=PASS         h1=EAST         h2=PASS         h3=PASS         h4=PASS    market=[]
H21 farmer=NORTH            h0=PASS         h1=EAST         h2=PICKUP COW   h3=PASS         h4=PASS    market=[]
H22 farmer=COLLECT_FERTILIZER h0=PASS       h1=PLACE WHEAT  h2=WEST         h3=PASS         h4=PASS    market=SELL WHEAT 1
H23 farmer=CARE             h0=PASS         h1=PASS         h2=WEST         h3=PASS         h4=PASS    market=[]
```

End money: 280.

During day 3:

- **Wheat harvesting begins.** Three `HARVEST` actions occur (hand 3 at
  H08, hands 1 and 4 at H10) against Wheat tiles planted on day 0 -- i.e.
  harvested at **age 3**, one day earlier than our own agent's day-4 Wheat
  harvest rule (`docs/mechanics.md` notes the 4-day rule is a strategy
  choice, not a hard mechanic). Only 3 of the 7 day-0 Wheat tiles are
  harvested this day; the other 4 are presumably harvested age-3 as well
  but on tiles not yet reached by hour 23, or were planted at a slightly
  later hour on day 0 and are not yet age 3 -- needs the exact per-tile
  `planted_day` to confirm, not just the aggregate crop count.
- A 4th Cow is bought (`BUY_ANIMAL COW 1` at H17) and picked up (`PICKUP
  COW` at H21), and hand 2 (at `(3,4)`) immediately starts moving toward
  the empty `(2,4)` pasture (`WEST` at H22, H23) -- but does **not** reach
  or place it before hour 23. The Cow is carried overnight; matches the
  full-match summary showing 4 Cows established by day 4.
- Fertilizer is collected, placed, and sold in two more small batches
  (`SELL FERTILIZER 3` then `SELL FERTILIZER 1`), continuing the day-1
  pattern.
- One `SELL WHEAT` order appears early (H03, before anything is harvested
  that day -- likely selling Wheat carried over from day 1/2) and another
  late (H22, presumably from the day's own harvest).
- End-of-day-3 grid: same 23 used tiles as day 1 (3 Cows, 2 Sheep, 7 Wheat,
  12 Melon), all now re-watered, plus the still-empty `(2,4)` pasture and
  the 4th Cow in hand 2's backpack rather than placed.

## Day 4

Only 4 hands hired again. This is where the 4th Cow (bought and carried
overnight at the end of day 3) finally gets placed -- and it happens at
**hour 0**, before day 4's own hires even spawn: `hand_actions` at H00 is
`[PASS, PASS, PLACE COW, PASS, PASS]` (5 entries -- day 3's last hand roster,
completing its carried-over action) with hand index 2 placing the Cow at
`(2,4)`. This is the first sign that a day boundary is not a hard action
cutoff for a unit that already has a queued placement.

Start-of-day-4 state: all 25 NW tiles now occupied -- **4 Cows, 2 Sheep, 7
Wheat, 12 Melon, zero empty tiles**. This is the full 25-tile NW quadrant
fully committed by day 4.

Hour-by-hour actions (farmer / hand0 / hand1 / hand2 / hand3 / market):

```text
H00 farmer=PASS                                    h?=PLACE COW (day-3 hand roster, index 2)          market=[]
H01 farmer=PICKUP WHEAT 5                                                                              market=SELL FERTILIZER 1, HIRE x4
H02 farmer=FEED             h0=NORTH        h1=NORTH        h2=NORTH        h3=NORTH                   market=[]
H03 farmer=CARE             h0=WEST         h1=NORTH        h2=NORTH        h3=NORTH                   market=[]
H04 farmer=COLLECT_FERTILIZER h0=WEST       h1=NORTH        h2=NORTH        h3=NORTH                   market=[]
H05 farmer=NORTH            h0=CARE         h1=NORTH        h2=WEST         h3=WEST                    market=SELL WHEAT 2
H06 farmer=FEED             h0=SOUTH        h1=NORTH        h2=WEST         h3=WEST                    market=[]
H07 farmer=CARE             h0=CARE         h1=WEST         h2=WATER        h3=WEST                    market=[]
H08 farmer=COLLECT_FERTILIZER h0=NORTH      h1=WEST         h2=NORTH        h3=WEST                    market=[]
H09 farmer=WEST             h0=NORTH        h1=WEST         h2=EAST         h3=WATER                   market=[]
H10 farmer=FEED             h0=EAST         h1=WATER        h2=WATER        h3=HARVEST                 market=BUY_SEED WHEAT 1
H11 farmer=COLLECT_FERTILIZER h0=CARE       h1=HARVEST      h2=SOUTH        h3=PLANT WHEAT             market=BUY_SEED WHEAT 1
H12 farmer=COLLECT_FERTILIZER h0=SOUTH      h1=PLANT WHEAT  h2=COLLECT_FERTILIZER h3=WATER              market=[]
H13 farmer=SOUTH            h0=SOUTH        h1=WATER        h2=SOUTH        h3=NORTH                   market=BUY_PRODUCT WHEAT 1
H14 farmer=FEED             h0=WEST         h1=EAST         h2=SOUTH        h3=WATER                   market=[]
H15 farmer=COLLECT_FERTILIZER h0=WEST       h1=WATER        h2=PASS         h3=HARVEST                 market=BUY_PRODUCT WHEAT 1, BUY_SEED WHEAT 1
H16 farmer=COLLECT_FERTILIZER h0=CARE       h1=SOUTH        h2=PLACE FERTILIZER h3=PLANT WHEAT          market=SELL FERTILIZER 1
H17 farmer=WEST             h0=COLLECT_FERTILIZER h1=SOUTH  h2=PASS         h3=WATER                   market=BUY_PRODUCT WHEAT 1
H18 farmer=FEED             h0=PASS         h1=SOUTH        h2=PASS         h3=SOUTH                   market=[]
H19 farmer=PASS             h0=PASS         h1=SOUTH        h2=PASS         h3=SOUTH                   market=BUY_PRODUCT WHEAT 1
H20 farmer=COLLECT_FERTILIZER h0=PASS       h1=EAST         h2=PASS         h3=SOUTH                   market=[]
H21 farmer=EAST             h0=PASS         h1=EAST         h2=PASS         h3=WATER                   market=BUY_PRODUCT WHEAT 1
H22 farmer=EAST             h0=PASS         h1=DROP         h2=PASS         h3=PASS                    market=[]
H23 farmer=PLACE FERTILIZER 5 h0=PASS       h1=PASS         h2=PASS         h3=PASS                    market=SELL FERTILIZER 4, BUY_PRODUCT WHEAT 1
```

End money: 688.

Notes:

- The 4th Cow's placement at hour 0 (see above) means **a unit's queued
  action can still execute on the very first hour of the next day**, using
  that day's hour-0 observation. Any scripted implementation must account
  for this rather than assuming a clean day boundary.
- **Watering coverage drops noticeably**: only 7 of the 19 crop tiles show
  `watered_today = True` at end of day, versus full coverage on days 0-2.
  With 4 hands now managing 19 crop tiles plus 6 animals (up from 3 hands
  and fewer tiles/animals on day 2), hand capacity is visibly stretched --
  consistent with `docs/current_roadmap.md`'s P3 note that workload
  pressure is real and episodic, not evenly distributed.
- Hand 1 does a `DROP` action at H22, carrying 2 Wheat at a shed-access
  tile. Confirmed from inventory/shed deltas: the 2 Wheat successfully
  reaches the shed (shed Wheat +2), the same effective result as `PLACE`.
  See `docs/mechanics.md` ("Drop") for the full confirmed behavior,
  including where it differs for Fertilizer.
- Fertilizer collection, placement, and sale continues as an every-day
  pattern (`SELL FERTILIZER 4` at H23, the largest single batch so far).

## Day 5

First day with no pending structural work (all 25 NW tiles were already
committed by day 4) -- and the first sign of crop diversification. 3 hands
hired (`HIRE` submitted 4 times at H01/H02, but one submission at H02 is a
literal empty order `[]`, so only 3 actually hire; matches
`hand_positions` never exceeding 3 all day).

Start-of-day-5 state matches end-of-day-4. End-of-day-5 tile state:

- **4 of the 7 Wheat tiles are replaced with Strawberry**: `(2,0)`, `(1,1)`,
  `(0,2)`, `(0,3)` are now Strawberry; only `(0,0)`, `(1,0)`, `(0,1)` remain
  Wheat. Cows, Sheep, and all 12 Melon tiles are unchanged.
- 6 of the 7 remaining/converted crop tiles show `watered_today = True`;
  `(0,2)`'s new Strawberry plant is `False` (planted at hour 23, too late
  to water the same day).

Hour-by-hour actions (farmer / hand0 / hand1 / hand2 / hand3 / market):

```text
H00 farmer=PASS                                                                                market=SELL FERTILIZER 1
H01 farmer=WEST                                                                                market=SELL FERTILIZER 1, HIRE x3
H02 farmer=EAST             h0=PICKUP WHEAT 2 h1=PASS      h2=NORTH                             market=HIRE, [] (literal empty order)
H03 farmer=PICKUP WHEAT 2  h0=FEED         h1=WEST         h2=CARE         h3=NORTH             market=SELL WHEAT 2
H04 farmer=WEST            h0=CARE         h1=PICKUP WHEAT 2 h2=COLLECT_FERTILIZER h3=NORTH     market=[]
H05 farmer=FEED            h0=WEST         h1=NORTH        h2=WEST         h3=NORTH             market=[]
H06 farmer=CARE            h0=WEST         h1=FEED         h2=WEST         h3=NORTH             market=[]
H07 farmer=COLLECT_FERTILIZER h0=FEED      h1=CARE         h2=WEST         h3=WATER             market=[]
H08 farmer=WEST            h0=CARE         h1=NORTH        h2=WATER        h3=WEST              market=[]
H09 farmer=COLLECT_FERTILIZER h0=EAST      h1=FEED         h2=WEST         h3=WATER             market=[]
H10 farmer=NORTH           h0=EAST         h1=CARE         h2=WATER        h3=PASS              market=[]
H11 farmer=WATER           h0=NORTH        h1=COLLECT_FERTILIZER h2=NORTH  h3=PASS              market=BUY_SEED STRAWBERRY 2
H12 farmer=NORTH           h0=COLLECT_FERTILIZER h1=NORTH  h2=WATER        h3=PASS              market=[]
H13 farmer=WATER           h0=EAST         h1=NORTH        h2=HARVEST      h3=WATER             market=[]
H14 farmer=EAST            h0=SOUTH        h1=WATER        h2=PLANT STRAWBERRY h3=WEST          market=[]
H15 farmer=WATER           h0=DROP         h1=WEST         h2=WATER        h3=WATER             market=SELL FERTILIZER 1
H16 farmer=SOUTH           h0=PASS         h1=WATER        h2=EAST         h3=WEST              market=BUY_SEED STRAWBERRY 1
H17 farmer=FEED            h0=PASS         h1=WEST         h2=WATER        h3=WATER             market=BUY_SEED STRAWBERRY 1
H18 farmer=CARE            h0=PASS         h1=WATER        h2=NORTH        h3=HARVEST           market=[]
H19 farmer=COLLECT_FERTILIZER h0=PASS      h1=PASS         h2=WATER        h3=PLANT STRAWBERRY  market=[]
H20 farmer=EAST            h0=PASS         h1=HARVEST      h2=WEST         h3=WATER             market=[]
H21 farmer=SOUTH           h0=PASS         h1=PLANT STRAWBERRY h2=WATER    h3=WEST              market=[]
H22 farmer=DROP            h0=PASS         h1=WATER        h2=HARVEST      h3=WATER             market=SELL FERTILIZER 3
H23 farmer=PASS            h0=PASS         h1=WEST         h2=PLANT STRAWBERRY h3=NORTH         market=[]
```

End money: 810.

Notes:

- **Strawberry appears for the first time**, bought as `BUY_SEED
  STRAWBERRY` in three small batches (2, then 1, then 1 -- 4 seeds total,
  matching the 4 tiles converted). Each conversion follows the same
  micro-pattern: `HARVEST` the mature Wheat tile, then `PLANT STRAWBERRY`
  on the same tile in a later action -- Wheat is not simply left to expire,
  its tile is actively recycled.
- Wheat tiles are converted, **not Melon** -- consistent with Melon being
  a single-harvest crop not due until much later, while Wheat cycles
  quickly and was already producing repeat harvests by day 5.
- `DROP` recurs twice (hand 0 at H15 carrying 1 Fertilizer; farmer at H22
  carrying 3 Fertilizer), both from a shed-access tile. Confirmed from
  inventory/shed deltas: in both cases the Fertilizer is **destroyed**, not
  deposited -- the shed's Fertilizer count stays at 0 either side of the
  action. This is the opposite of day 4's Wheat case (see `docs/mechanics.md`,
  "Drop"). The `SELL FERTILIZER 1` order submitted the same step as H15's
  `DROP` therefore had nothing in the shed to sell. Do not treat `DROP` as
  a safe way to deposit Fertilizer if this pattern is ever adapted into
  `main.py` -- use `PLACE FERTILIZER` instead, which the opponent's own
  script uses successfully elsewhere (e.g. day 4 H23, day 5 H22).
- Hand 0 goes idle after hour 15 (`PASS` for the rest of the day); the
  other hands stay active through hour 23 -- less severe than the
  full-day-idle pattern on days 0 and 2, but the same underlying tendency
  for the schedule to run out of assigned work before the day count fills.
- One market order at H02 is a literal empty list (`[]`) submitted
  alongside a `HIRE` -- confirms `hand_positions` never exceeding 3 that
  hour despite 4 `HIRE`-shaped submissions across H01/H02; the empty order
  is presumably a no-op rather than a 4th successful hire.

## Day 6 -- NE quadrant unlock

The biggest single day so far. 7 hands hired (up from 3-5 on prior days).
NE unlocks mid-day and 20 of its 25 tiles are filled before hour 23.

**Note on grid coverage from this day onward**: the visual artifact and the
tile dumps below now cover the full NW+NE area (`x: 0-9, y: 0-4`), not just
NW's `x: 0-4`. Days 0-5 above were re-extracted with the same wider grid
for consistency (all still empty/`LOCKED` in the NE half, as expected).

Key events, in order:

- **H05**: farmer `HARVEST`s a Sheep (the first Wool harvest of the match).
- **H06**: `SELL WOOL 6` -- money jumps from 961 to 2246 in one step.
- **H07**: NE unlocks (`unlocked_quadrants` becomes `['NW', 'NE']`).
  Same step: `SELL WOOL 4`, `BUY_PRODUCT WHEAT 2`, `BUY_PRODUCT FERTILIZER
  1`, `BUY_LAND`, `BUY_ANIMAL COW 2`. Hand 0 `PLACE WOOL 6` (banking the
  harvested Wool from H05 into the shed for that same-step sale).
- **H07-H23**: the farmer walks the full NE quadrant east then north
  (`(5,4)` &rarr; `(9,4)` &rarr; `(9,0)`-ish path) while all 7 hands fan out
  across NE, building pastures and planting crops.

End-of-day-6 tile state -- NE quadrant (25 tiles, 20 used):

- **7 pasture tiles staged**: `(5,2)`, `(6,2)`, `(5,3)`, `(6,3)`, `(5,4)`,
  `(6,4)`, `(7,4)`. Only 2 are occupied (`(5,3)` and `(5,4)`, both Cow --
  matching the `BUY_ANIMAL COW 2` at H07); the other 5 are empty, staged
  for animals to be bought later. This is the same staged-pasture pattern
  seen on day 1, but at roughly 3x the scale.
- **13 crop tiles planted**, split between Wheat and Strawberry --
  **no Melon** in NE at all: `(5,0)` `(6,0)` `(7,0)` `(8,0)` Wheat;
  `(5,1)` `(6,1)` Strawberry, `(7,1)` Wheat; `(7,2)` `(8,2)` Strawberry;
  `(7,3)` `(8,3)` Strawberry; `(8,4)` `(9,4)` Strawberry.
- Remaining unused NE tiles: `(9,0)`, `(8,1)`, `(9,1)`, `(9,2)`, `(9,3)` --
  5 tiles left for a future day.
- NW side is unchanged from day 5 except normal daily re-watering.

Hour-by-hour actions (farmer / hand0..hand6 / market; `lands` shows
`unlocked_quadrants` for that hour):

```text
H00 lands=NW    farmer=PASS                                                                                                       market=[]
H01 lands=NW    farmer=NORTH                                                                                                      market=SELL FERTILIZER 2, HIRE x7
H02 lands=NW    farmer=WEST      h0=PICKUP WHEAT 2 h1=WEST      h2=NORTH     h3=WEST      h4=PICKUP WHEAT h5=WEST      h6=NORTH   market=[]
H03 lands=NW    farmer=HARVEST   h0=WEST      h1=PICKUP WHEAT h2=PICKUP WHEAT 2 h3=WEST   h4=FEED      h5=PICKUP WHEAT h6=PICKUP WHEAT market=[]
H04 lands=NW    farmer=EAST      h0=FEED      h1=NORTH     h2=WEST      h3=WEST      h4=CARE      h5=NORTH     h6=COLLECT_FERTILIZER market=[]
H05 lands=NW    farmer=SOUTH     h0=HARVEST   h1=FEED      h2=WEST      h3=NORTH     h4=WEST      h5=NORTH     h6=NORTH            market=[]
H06 lands=NW    farmer=DROP      h0=EAST      h1=CARE      h2=FEED      h3=NORTH     h4=CARE      h5=FEED      h6=COLLECT_FERTILIZER market=SELL WOOL 6
H07 lands=NW,NE farmer=EAST      h0=PLACE WOOL 6 h1=NORTH  h2=CARE      h3=WATER     h4=COLLECT_FERTILIZER h5=CARE h6=SOUTH        market=SELL WOOL 4, BUY_PRODUCT WHEAT 2, BUY_PRODUCT FERTILIZER 1, BUY_LAND, BUY_ANIMAL COW 2
H08 lands=NW,NE farmer=EAST      h0=EAST      h1=COLLECT_FERTILIZER h2=COLLECT_FERTILIZER h3=NORTH h4=EAST h5=EAST h6=PICKUP COW  market=SELL FERTILIZER 1, BUY_PRODUCT FERTILIZER 1
H09 lands=NW,NE farmer=EAST      h0=PICKUP COW h1=SOUTH    h2=EAST      h3=WATER     h4=EAST      h5=PASS      h6=EAST            market=SELL FERTILIZER 1, BUY_PRODUCT WHEAT 2
H10 lands=NW,NE farmer=NORTH     h0=BUILD_PASTURE h1=SOUTH h2=EAST      h3=PASS      h4=DROP      h5=BUILD_PASTURE h6=PLACE FERTILIZER 2 market=SELL FERTILIZER 3
H11 lands=NW,NE farmer=PASS      h0=PASS      h1=DROP      h2=PLACE FERTILIZER h3=PASS h4=WEST     h5=EAST      h6=NORTH           market=SELL FERTILIZER 2, BUY_SEED WHEAT 1
H12 lands=NW,NE farmer=PASS      h0=PLACE COW h1=NORTH     h2=WEST      h3=WATER     h4=WEST      h5=BUILD_PASTURE h6=BUILD_PASTURE market=[]
H13 lands=NW,NE farmer=PASS      h0=FEED      h1=NORTH     h2=NORTH     h3=NORTH     h4=WEST      h5=NORTH     h6=PLACE COW        market=BUY_PRODUCT WHEAT 3, BUY_SEED STRAWBERRY 2
H14 lands=NW,NE farmer=PASS      h0=CARE      h1=NORTH     h2=FEED      h3=WATER     h4=WEST      h5=PLANT STRAWBERRY h6=FEED      market=[]
H15 lands=NW,NE farmer=PASS      h0=EAST      h1=WATER     h2=CARE      h3=WEST      h4=WATER     h5=WATER     h6=CARE             market=BUY_PRODUCT WHEAT 3
H16 lands=NW,NE farmer=PLANT STRAWBERRY h0=BUILD_PASTURE h1=EAST h2=COLLECT_FERTILIZER h3=NORTH h4=NORTH h5=EAST h6=EAST          market=BUY_SEED STRAWBERRY 1, BUY_SEED WHEAT 2
H17 lands=NW,NE farmer=WATER     h0=EAST      h1=PLANT STRAWBERRY h2=NORTH h3=WATER    h4=WATER     h5=PLANT WHEAT h6=BUILD_PASTURE market=[]
H18 lands=NW,NE farmer=EAST      h0=BUILD_PASTURE h1=WATER h2=WATER     h3=HARVEST   h4=NORTH     h5=WATER     h6=EAST             market=[]
H19 lands=NW,NE farmer=PASS      h0=EAST      h1=NORTH     h2=NORTH     h3=WEST      h4=WATER     h5=NORTH     h6=NORTH            market=BUY_SEED STRAWBERRY 3, BUY_SEED WHEAT 1
H20 lands=NW,NE farmer=PLANT STRAWBERRY h0=PLANT STRAWBERRY h1=PLANT WHEAT h2=WATER h3=WATER h4=WEST h5=PLANT WHEAT h6=PLANT STRAWBERRY market=[]
H21 lands=NW,NE farmer=WATER     h0=WATER     h1=WATER     h2=NORTH     h3=HARVEST   h4=SOUTH     h5=WATER     h6=WATER            market=SELL WHEAT 9
H22 lands=NW,NE farmer=PASS      h0=EAST      h1=EAST      h2=WATER     h3=SOUTH     h4=SOUTH     h5=EAST      h6=EAST             market=BUY_SEED STRAWBERRY 2, BUY_SEED WHEAT 1
H23 lands=NW,NE farmer=PASS      h0=PLANT STRAWBERRY h1=PLANT WHEAT h2=EAST h3=WATER h4=WATER     h5=PLANT WHEAT h6=PLANT STRAWBERRY market=[]
```

End money: 824.

Notes:

- **NE is settled with Wheat and Strawberry, never Melon** -- Melon is a
  one-shot 10-day-maturity crop; starting it this late relative to remaining
  useful cycles is presumably not worthwhile, unlike the fast-cycling Wheat
  and the ongoing-yield Strawberry.
- **7 pasture tiles staged with only 2 occupied** mirrors day 1's pattern of
  building ahead of the animals that will fill them, but at more than
  triple the scale (7 slots vs. 2). This is a big standing commitment: 5
  empty pastures sit idle in NE by end of day 6.
- The first Wool sale (`SELL WOOL 6` then `SELL WOOL 4`, 10 Wool total)
  happens same-day as the NE unlock -- the farmer's harvest-and-sell timing
  for the existing 2 Sheep is not disrupted by the land purchase.
- `DROP` appears twice more (farmer H06, hand 1 H10/H11 -- carrying
  Fertilizer both times per the pattern in `docs/mechanics.md`); not
  re-verified per-instance here since the mechanic is already confirmed.
- Farmer's route this day is almost entirely movement (`EAST`/`NORTH`/
  `WATER`/`PASS`) with only one `PLANT STRAWBERRY` -- most of the
  construction and planting work is spread across the 7 hands, not the
  farmer.

## Implementation status

The day-5 Wheat-to-Strawberry conversion pattern above ("Package 1") was
translated into `main.py` as `early_nw_strawberry_phase_active` -- adapted
to whichever staple our own agent actually grows (Carrot, not Wheat; see
`docs/experiment-log.md`, "Opponent-replay-informed staged packages", for
why) rather than replayed literally. Accepted on a twenty-seed gate
(36W--4L, +1861.3 average lead) and frozen as
`baselines/early_nw_strawberry_v1.py`, now the current frozen baseline.
A 5th day-0 hand (from day 0's "5 hands, 7 Wheat" template) was
investigated and not implemented -- see the same experiment-log section for
why it doesn't add capacity in our architecture.

## Next

Trace day 7 next. Day 6 staged 5 empty NE pastures and left 5 NE tiles
unused -- day 7 should show whether those pastures get animals, whether the
remaining NE tiles get planted, and whether SW-quadrant land purchase
begins this early (our own agent doesn't unlock SW until day 11).
