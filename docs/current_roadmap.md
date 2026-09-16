# Competitive Agent Roadmap

Read this document before selecting or implementing the next performance
experiment. Detailed completed and rejected results belong in
`docs/experiment-log.md`; confirmed game rules belong in `docs/mechanics.md`.

## Current frozen baseline

`baselines/staged_cow_v1.py`

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
- When at least two Milk-demand shops are visible, one staged Cow may be added
  at `(1, 4)` after the NE Cows are established and the existing crop clears.
  Hand 1 owns its setup and service as part of the NW Sheep circuit.
- Conditional NE Geese start on day 8. Hand 5 owns the Goose at `(6, 4)` and
  the farmer owns the Goose at `(6, 3)`.
- Conditional four-animal SW plans may be mixed, all-Cow, or all-Sheep and are
  locked after establishment.
- One Melon wave, with twelve opening Melon plants in the current day-0 livestock
  design.
- Idle hands and the farmer collect Fertilizer; selected premium crops use it
  when the projected return clears the value margin.
- Endgame liquidation and the NE Wheat overflow buffer are active.

Latest frozen validation against Twelve Melon opening v1:

- 10 wins, 0 losses, and 30 ties over 20 mirrored seeds.
- 62.5% match score with zero errors.
- Average money: 97,501.4 versus 96,841.4, a lead of 660.0.
- Average harvests: 368.7.
- Average sales: 185.8 Wheat, 42.1 Carrots, 72.0 Melons, 198.8
  Strawberries, 2.6 Tomatoes, 49.0 Eggs, 159.4 Milk, 138.4 Wool, and
  233.8 Fertilizer.
- Average leftovers: 3.0 Wheat and zero for every other tracked product.
- A five-seed regression against Day-0 livestock v1 finished 10W--0L with a
  5,332.2 average lead and zero errors.

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

### P0 — Complete SW coverage — rejected

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

Outcome:

- The permanent twelfth-hand candidate worked all seven tiles and raised average
  harvests to 397.6, but lost all ten mirrored five-seed matches. It averaged
  2,568.4 coins behind because the twelfth hand costs 144 coins every day after
  SW unlock; the extra Wheat did not repay that recurring cost.
- Splitting all seven tiles across the existing three SW hands also failed,
  finishing 4W--6L and averaging 803.7 coins behind. Average harvests reached
  only 377.6, essentially unchanged from the 376.9 frozen result, showing that
  the existing hands lack spare service capacity.
- Rebalancing the existing four-animal SW crop routes from 6/8 to 7/7 also
  failed its five-seed screen. Moving the geographically adjacent `(2, 7)`
  tile produced 4W--2L--4T but averaged 137.0 coins behind; equal tile counts
  displaced higher-value Strawberry, Carrot, and Fertilizer work with Wheat.
- Do not pursue permanent full-SW Wheat coverage again without a materially
  different labour model. The conditional-hire and six-tile variants are
  lower-priority P3 workload experiments, not the immediate next step.

### P1 — Staged shop-aware livestock ladder

The first safe stage is accepted; continue one stage at a time.

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

First-stage finding:

- A day-4 additional Cow at `(1, 3)` was rejected after a five-seed screen:
  4W--6L, 40.0% match score, and an average deficit of 3,715.2 coins.
- The tile was too far from the farmer's existing animal circuit. More
  importantly, limited day-4 cash caused the Cow to displace the scheduled
  day-4 Sheep in the setup queue until day 6. The extra daily feed, care, and
  travel load then produced a compounding loss despite additional Milk.
- Any next livestock-ladder attempt must preserve the day-4 Sheep, use a tile
  adjacent to the established service circuit, and prove there is enough cash
  and labour capacity before activation. Do not retry `(1, 3)`.

Accepted Cow stage:

- A Cow at `(1, 4)` is activated only when at least two Milk-demand shops are
  visible, after both NE expansion Cows are established and the tile's current
  crop has cleared. Hand 1 owns setup and daily service along its existing NW
  Sheep circuit.
- The initial one-shop trigger was too broad: on seed 2 it gained 21 Milk and
  15 Fertilizer but displaced 23 Carrots, 15 Wheat, and two Strawberries, in
  addition to its purchase and feed cost.
- The two-shop version leaves nonqualifying seeds behaviorally unchanged. Its
  twenty-seed direct gate produced 10W--0L--30T and a 660.0 average lead, then
  won 10--0 against Day-0 livestock v1 with a 5,332.2 average lead.
- Frozen as `baselines/staged_cow_v1.py`.

Do not copy a full replay build order at once. Earlier experiments show that
animal profit disappears when setup interrupts Melon liquidation, land buying,
or crop service.

### P2 — Recover the twelve-Melon opening — accepted candidate

The common replay template financed twelve Melons alongside four day-0 animals
and five hands. Our current day-0 livestock opening reduced Melons from twelve
to ten, which is a known revenue cost.

Investigate the opening order and cash flow before changing the target. Look
for cheaper hiring order, unnecessary seed/product reserves, avoidable travel,
or purchases that can wait until the first Wheat income. The experiment passes
only if all four initial animals are serviced and twelve Melons are planted in
time without delaying NE expansion.

Outcome:

- Feed Wheat carried by hands was omitted from the market stock calculation,
  causing the agent to rebuy Wheat immediately after a hand picked it up.
  Counting all carried Wheat and sizing the reserve from outstanding animal
  setup/feed work recovered enough opening cash for two more Melon seeds.
- The day-4 Sheep tile is now cleared but left unplanted, and the day-0 Carrot
  and Wheat seed buffers are deferred. A seed-1 trace confirmed twelve Melons
  and all four initial animals by day 1, the third Sheep at day 4 hour 7, and NE
  at day 7 hour 2. The Sheep and NE milestones exactly match the frozen
  baseline.
- The final 20-seed mirrored gate against Hand 5 Goose v1 produced 38W--2L,
  95.0% match score, zero errors, and a 1,752.8 average-money lead. Five-seed
  regressions won 10--0 against both Locked SW livestock v1 and Day-0 livestock
  v1.
- Frozen as `baselines/twelve_melon_opening_v1.py`.

### P3 — Workload-aware hand count

Top replay agents vary daily hiring rather than holding one fixed count for the
whole game. After the full-SW test, measure whether hands 11--13 should be hired
according to actionable tiles and livestock workload. Avoid optimizing this
from assumed route size alone; use actual idle/productive-action traces.

Initial five-seed workload audit:

- Hand 11 is not generally redundant after SW unlock: 41.3% of its submitted
  actions were productive, 47.1% were movement, and only 11.6% were passes.
- Hands 9 and 10 were similarly active, at 44.1% and 50.7% productive. Reducing
  the permanent eleven-hand count would therefore abandon useful work.
- Pressure is episodic. All hands were still busy at the end of several SW
  expansion and crop-cycle days, particularly day 11 and days 20--25, while
  many ordinary days ended with spare actions.
- First candidate: add a twelfth surge hand only when live actionable work on
  Hand 11's six-tile SW route exceeds that hand's remaining daily capacity.
  Split those six tiles 3/3 while the helper is active; do not add unmanaged SW
  land in this experiment. Include the twelfth daily hire cost of 144 coins.

Outcome:

- The loose capacity trigger was rejected. It hired on ordinary recurring-crop
  cycles and produced only 4W--4L--2T over five mirrored seeds, with a 51.0-coin
  average lead. The helper often accelerated work Hand 11 would have completed
  anyway, so its 144-coin daily cost was not consistently recovered.
- Requiring at least a six-action estimated backlog removed the regressions but
  was too narrow to retain. Over twenty mirrored seeds it produced 2W--0L--38T
  and an 8.8-coin average lead, triggering only on seed 1. A five-seed check
  against Hand 5 Goose v1 was exactly unchanged from the frozen baseline,
  providing no evidence that the P3 gain generalized to another matchup.
- Keep eleven hands as the fixed post-SW count. Do not retry a twelfth hand from
  route workload alone; revisit only with a broader whole-farm scheduler that
  can prove incremental work would otherwise miss its profitable deadline.

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

Continue **P1 — Staged shop-aware livestock ladder** with one additional
demand-aware stage. Audit a Sheep or Goose position adjacent to an established
service circuit, assign its owner before placement, and preserve the accepted
Cow stage, day-4 Sheep, land timing, and normal crop schedule on nonqualifying
seeds.
