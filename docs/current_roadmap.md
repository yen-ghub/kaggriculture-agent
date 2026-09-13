# Competitive Agent Roadmap

Read this document before selecting or implementing the next performance
experiment. Detailed completed and rejected results belong in
`docs/experiment-log.md`; confirmed game rules belong in `docs/mechanics.md`.

## Current frozen baseline

`baselines/hand5_goose_v1.py`

The active strategy in `main.py` should be compared against this baseline until
a newer candidate passes the evaluation gates below.

Current characteristics:

- Three unlocked quadrants: NW, NE, and SW. Do not assume a fourth-quadrant
  purchase is useful.
- 68 managed tiles: all 25 NW, all 25 NE, and 18 of 25 SW.
- Four hands initially, eight after NE expansion, and eleven after SW expansion.
- Two Cows and two Sheep established on day 0.
- One additional Sheep starts on day 4 and another on day 11.
- Two expansion Cows start with the NE expansion.
- Conditional NE Geese start on day 8. Hand 5 owns the Goose at `(6, 4)` and
  the farmer owns the Goose at `(6, 3)`.
- Conditional four-animal SW plans may be mixed, all-Cow, or all-Sheep and are
  locked after establishment.
- One Melon wave, with ten opening Melon plants in the current day-0 livestock
  design.
- Idle hands and the farmer collect Fertilizer; selected premium crops use it
  when the projected return clears the value margin.
- Endgame liquidation and the NE Wheat overflow buffer are active.

Latest frozen validation against NE Wheat buffer v1:

- 30 wins, 0 losses, and 10 ties over 20 mirrored seeds.
- 87.5% match score with zero errors.
- Average money: 96,657.8 versus 94,590.7, a lead of 2,067.1.
- Average harvests: 376.9.
- Average sales: 270.0 Wheat, 52.5 Carrots, 60.0 Melons, 205.5
  Strawberries, 2.0 Tomatoes, 57.0 Eggs, 154.2 Milk, 135.8 Wool, and
  225.1 Fertilizer.
- Average leftovers: 2.7 Wheat and zero for every other tracked product.

## Top-player replay study

Five public replays in `replays/` were inspected. The higher-scoring agents in
those games were Mengfei Li, Subramanya N, feel the agi, QQ Farming, and
Xiangyu Liu. Both seats were inspected because the opposing strategies also
contain useful routing evidence.

### Findings shared by all five

- Every agent worked all 75 tiles in NW, NE, and SW at least once.
- No agent purchased the fourth quadrant.
- Land expansion alone was not the differentiator. The important differences
  were complete use of purchased land, livestock scale and composition, and
  daily staffing/routing.
- Animal composition reacted strongly to the revealed shop sequence.

Our current agent worked exactly 68 tiles in a controlled replay-seed run. The
seven SW tiles never included in its route are:

```python
(3, 8), (4, 8),
(0, 9), (1, 9), (2, 9), (3, 9), (4, 9)
```

### Common high-ranking template

Three of the five agents used nearly the same core build:

- Day 0: two Cows, two Sheep, five hands, twelve Melons, and seven Wheat.
- Additional Cows around days 2--4.
- NE unlocked during day 6 and SW during day 11.
- More shop-aware animals added progressively from days 6--12.
- Peak livestock was approximately 17--19 animals.
- Normal staffing was around eleven hands, with some workload-dependent days at
  twelve or thirteen.
- A broadly fixed crop skeleton was combined with adaptive animal composition.

This is evidence of a strategy family, not proof that every individual action
is optimal. Replay action tapes are market-sensitive: when replayed against a
different opponent, later recorded actions may become inefficient or invalid.

### Alternative top strategies

- Xiangyu Liu used a cattle-heavy branch: approximately nine Cows, three Sheep,
  one Goose, twelve hands, and earlier SW expansion. This was the only static
  replay tape that beat the current live agent on its recorded seed.
- QQ Farming used fewer hands and a more diversified crop plan, including much
  more Tomato and Carrot production and six Geese in a Pet Cafe-heavy market.
- These alternatives support shop-aware strategy branching rather than one
  globally fixed livestock mix.

## Prioritized experiments

### P0 — Complete SW coverage

This is the immediate next experiment.

Hypothesis: the seven already-purchased but unmanaged SW tiles can produce more
value than the incremental labour and seed cost. This is the only major
structural behaviour shared by all five replay agents and missing from ours.

Initial candidate design:

1. Extend `THIRD_QUADRANT_ROUTE` from 18 to all 25 SW tiles by adding the seven
   coordinates listed above.
2. Add a twelfth hand whose local route consists of those seven tiles.
3. Use Wheat as the default crop on the new route for the first experiment.
4. Leave livestock thresholds, existing crop targets, land timing, sale rules,
   and the first eleven hand assignments unchanged.
5. Extend any internal hand-cost table for the twelfth Fibonacci hire cost.

Trace checks:

- The twelfth hand is hired only after SW unlock.
- All seven tiles are dug, planted, watered, harvested, and replanted.
- The new hand does not steal SW livestock work or duplicate another hand's
  target.
- No market-order overflow, seed starvation, shed overflow, or endgame
  leftovers are introduced.
- Record idle, movement, and productive actions for the twelfth hand.

If a permanent twelfth hand fails economically, test these fallbacks in order:

1. Hire it only on days with actionable work on its route.
2. Split the seven tiles across the existing three SW hands.
3. Use six tiles with one compact route and leave the worst tile unmanaged.

### P1 — Staged shop-aware livestock ladder

Start only after P0 is accepted or rejected.

Hypothesis: the current animal-heavy branches generally top out around 12--14
animals, and lighter shop scenarios use fewer, leaving profitable demand
unserved. The replay strategy family commonly reaches 17--19 animals by adding
livestock progressively rather than creating one large late branch.

Design direction:

- Prefer additional NW/NE livestock positions that are close to existing
  service routes; do not automatically consume more SW crop land.
- Add one stage at a time and measure its marginal return.
- First test one additional Cow around day 2, then a second around day 3 or 4.
- After NE unlock, choose Cow, Sheep, or Goose stages from the revealed Milk,
  Wool, and Egg demand.
- Target roughly 16--18 total animals only when service capacity, feed, and cash
  reserves support them.
- Assign ownership before placement so every animal has exactly one farmer or
  hand responsible for setup, feed, care, harvest, return, and Fertilizer.

Do not copy a full replay build order at once. Earlier experiments show that
animal profit disappears when setup interrupts Melon liquidation, land buying,
or crop service.

### P2 — Recover the twelve-Melon opening

The common replay template financed twelve Melons alongside four day-0 animals
and five hands. Our current day-0 livestock opening reduced Melons from twelve
to ten, which is a known revenue cost.

Investigate the opening order and cash flow before changing the target. Look
for cheaper hiring order, unnecessary seed/product reserves, avoidable travel,
or purchases that can wait until the first Wheat income. The experiment passes
only if all four initial animals are serviced and twelve Melons are planted in
time without delaying NE expansion.

### P3 — Workload-aware hand count

Top replay agents vary daily hiring rather than holding one fixed count for the
whole game. After the full-SW test, measure whether hands 11--13 should be hired
according to actionable tiles and livestock workload. Avoid optimizing this
from assumed route size alone; use actual idle/productive-action traces.

### P4 — Strategy-family branching

Build a small portfolio after the production foundation is stronger:

- Livestock-heavy branch for strong Milk/Wool/Egg demand.
- Cattle-heavy branch for early multiple Milk-demand shops.
- Goose/diversified-crop branch for repeated Pet Cafe and Tomato demand.
- Crop-heavy default when animal demand is weak.

Branch inputs should include the unlocked-shop prefix, current market prices,
opponent crop/animal counts, cash runway, and remaining production cycles. Once
a capital-intensive branch establishes its structures, lock the decision unless
replacement is impossible.

## Deprioritized directions

- Fourth-quadrant expansion: none of the five replay agents used it, while all
  fully exploited the first three quadrants.
- Unconditional extra SW livestock: earlier results were highly seed-sensitive
  and sometimes displaced more valuable crops.
- Earlier Geese without workload sharing: day-7/day-8 farmer-only versions lost
  crop output and liquidity. The Hand 5 split is the retained solution.
- Broad early liquidation to avoid shed overflow: it diverted hands from more
  valuable field work. Prefer harvest staggering and targeted product returns.
- Large multi-variable changes: they make failures impossible to attribute.

## Evaluation protocol

For every candidate:

1. Freeze the current accepted strategy as a baseline before editing.
2. Change one strategic variable or one tightly coupled package.
3. Trace at least one normal seed and the relevant known stress seeds.
4. Run five mirrored seeds against the direct predecessor.
5. If promising, run twenty mirrored seeds against the direct predecessor.
6. Run a small multi-opponent regression against recent frozen baselines.
7. Check errors, money, match score, harvests, product mix, leftovers, shed
   overflow, animal service, idle actions, and position asymmetry.
8. Record accepted and rejected results in `docs/experiment-log.md`.
9. Update this roadmap: remove completed work from P0, promote the next item,
   and preserve any newly discovered constraint.

Do not accept a candidate solely because it beats a nearly identical baseline.
Prefer a positive average lead, no systematic paired-seed regressions, zero
errors, and evidence that the gain survives at least one strategically
different opponent.

## Next action

Implement and trace **P0 — Complete SW coverage** before pursuing another
livestock, crop-target, or timing tweak.
