# Competitive Agent Roadmap

Read this document before selecting or implementing the next performance
experiment. Detailed completed and rejected results belong in
`docs/experiment-log.md`; confirmed game rules belong in `docs/mechanics.md`.

## Current frozen baseline

`baselines/melon_early_return_v1.py`

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
- The early NE branch replaces the normal NE Goose branch with four compact
  livestock at `(6, 4)`, `(7, 4)`, `(6, 3)`, and `(7, 3)` whenever the first
  two shops signal any of: a Yarn Store (four Sheep), both shops demanding
  Milk (four Cows), or at least one Milk-demand shop with no Yarn and no Egg
  demand (four Cows). Hand 6 prebuilds their pastures on day 8 and establishes
  them in a batch on day 9; the SW four-animal branch remains inactive whenever
  this branch is selected.
- When at least two Milk-demand shops are visible, one staged Cow may be added
  at `(1, 4)` after the NE Cows are established and the existing crop clears.
  Hand 1 owns its setup and service as part of the NW Sheep circuit.
- Conditional NE Geese start on day 8 only when the early NE branch is not
  selected. Hand 5 owns the Goose at `(6, 4)` and the farmer owns the Goose
  at `(6, 3)`.
- Conditional four-animal SW plans may be mixed, all-Cow, or all-Sheep and are
  locked after establishment, active only when the early NE branch is not
  selected.
- One Melon wave, with twelve opening Melon plants in the current day-0 livestock
  design. On melon harvest day (day 10), Hands 1, 2, and 3 (the tile owners)
  harvest each Melon tile immediately once mature -- forfeiting the usual
  same-day watering bonus -- then return and sell before touching replanting
  or their other tiles, so the sale lands a full day ahead of the automatic
  overnight deposit and gets ahead of the opponent's own Melon sale in the
  shared market. This sells 60 Melon (12 tiles x 5) instead of 72 (12 x 6).
- Idle hands and the farmer collect Fertilizer; selected premium crops use it
  when the projected return clears the value margin.
- Endgame liquidation and the NE Wheat overflow buffer are active.

Latest frozen validation against Early NE single-Milk v1:

- 36 wins, 4 losses, and 0 ties over 20 mirrored seeds.
- 90.0% match score with zero errors.
- Average money: 97,749.4 versus 96,327.3, a lead of 1,422.1.
- Average harvests: 369.1.
- Average sales: 190.8 Wheat, 38.4 Carrots, 60.0 Melons, 196.6
  Strawberries, 1.8 Tomatoes, 41.4 Eggs, 169.7 Milk, 143.8 Wool, and
  234.3 Fertilizer.
- Average leftovers: 3.4 Wheat and zero for every other tracked product.
- Zero ties is expected: unlike the shop-conditional branches above, this
  change is unconditional and affects every seed, not a qualifying subset.
  Both losses (seeds 10 and 18) were thin (254 and 13 coins); a baseline
  isolation on seed 10 confirmed the mechanism works as intended (our day-10
  sale quoted 249.0/226.0 versus the opponent's day-11 quote of only 106.0)
  but the forfeited yield (60 versus 72 units) outweighs the price edge on
  that particular seed.
- Five-seed regressions (seeds 1--5) won 10W--0L against Locked SW livestock v1
  (+9,181.0) and Day-0 livestock v1 (+8,447.2), both with zero errors.

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
- A Carrot variant of the same permanent twelfth hand (same tiles, same SW-
  unlock hire timing, Carrot instead of Wheat) was retried and also rejected:
  a large, consistent loss across five seeds (roughly -6750 average),
  dwarfing the hire cost alone. Carrot's own revenue was actually fine (a net
  gain on the traced seed); the bulk of the loss came from knock-on effects
  on unrelated Milk, Wool, and Strawberry pricing via the shared market's
  order-list-position sensitivity (see the experiment log for the full
  breakdown). Any future twelfth-hand attempt on these tiles needs to verify
  it is not disturbing other products' market-list positions, not just check
  its own crop's economics.

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

Rejected Goose stage:

- A third Goose at `(7, 4)` was tested only when both of the first two shops
  demanded Eggs. Hand 5 owned it beside the existing `(6, 4)` Goose, and all
  nonqualifying seeds remained unchanged.
- The twenty-seed gate produced 4W--2L--34T, a 52.5% match score, and only a
  25.1 average-money lead. Seed 11 lost by 698 in both positions, meaning one
  of only three qualifying seeds regressed.
- Do not retry this third-Goose stage without a materially better capacity or
  market-value trigger. Additional Egg output alone did not reliably offset
  displaced crop and Wool work.

Accepted early-NE livestock relocation:

- Strong early demand is identified from the first two shops: at least one
  Yarn Store selects four Sheep, while two Milk-demand shops select four Cows.
  The animals use `(6, 4)`, `(7, 4)`, `(6, 3)`, and `(7, 3)`.
- Hand 6 owns the compact NE setup and service route. It builds all four
  pastures on day 8, then batches pickup and placement on day 9. Conditional
  NE Geese and the independent four-animal SW branch are suppressed only when
  this branch is active; nonqualifying seeds retain the predecessor behavior.
- The twenty-seed mirrored gate against Staged Cow v1 produced 10W--0L--30T,
  a 62.5% match score, zero errors, and a 968.5 average-money lead. The thirty
  exact ties confirm that nonqualifying seeds stayed isolated.
- Five-seed regressions won 10--0 against both Locked SW livestock v1
  (+5,996.0) and Day-0 livestock v1 (+6,227.4). Frozen as
  `baselines/early_ne_livestock_v1.py`.

Next P1 action:

- Test a second staged Cow at `(0, 4)` only under at least three visible
  Milk-demand shops, after the accepted `(1, 4)` Cow is established and the
  existing crop clears. Hand 1 should own both staged Cows along the same route.
- Reserve `(0, 4)` only after the three-shop condition is met. Preserve exact
  frozen-baseline behavior on nonqualifying seeds, and do not change land,
  Sheep, Goose, crop-target, or hiring schedules in this experiment.

Outcome:

- Rejected. The twenty-seed direct evaluation produced 0W--6L--34T (42.5%).
  It changed only seeds 8, 13, and 17, and lost both player positions on all
  three by 942, 1,860, and 1,045 coins respectively. The resulting average
  deficit was 192.4 coins across the full mirrored suite.
- A third Milk-demand shop does not repay the second Cow's purchase, feed, and
  Hand 1 service load at `(0, 4)`. Do not retry this tile/threshold combination
  as another isolated Cow stage.

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

First accepted branch-selection change:

- A branch scan across seeds 1--20 found the compact early-NE block sitting
  idle in crops on four seeds (1, 4, 8, 20) whose first two shops carried a
  Milk-demand signal but neither Yarn nor Egg demand -- a prefix the existing
  Yarn/double-Milk trigger did not cover, leaving those animals deferred to
  the weaker day-12 SW decision.
- The fix routes that prefix to the existing `EARLY_NE_ALL_COW_PLAN` with no
  change to tiles, timing, hand ownership, or the SW/Goose suppression rule.
- The twenty-seed mirrored gate against Early NE livestock v1 produced
  8W--0L--32T (60.0%) with zero errors and a 1,117.6 average lead; the 32 ties
  confirm isolation on nonqualifying seeds. Three five-seed regressions on
  seeds 1--5 were all zero-error, including a third pass against Early NE
  livestock v1 itself that reproduced the exact qualifying/nonqualifying split
  found in the twenty-seed gate.
- Accepted and frozen as `baselines/early_ne_single_milk_v1.py`.

## Melon same-day sale -- accepted (roadmap detour)

Requested outside the P0--P4 sequence, not a continuation of P4. The opening
twelve-Melon wave previously sold in full on day 11, via the automatic
overnight deposit, a full day after harvest day (day 10). The accepted change
has Hands 1, 2, and 3 (the tile owners) harvest each Melon tile immediately
once mature on day 10 -- skipping the usual same-day watering bonus, which
would otherwise double the action cost per tile and blow the day's 24-action
budget across all twelve tiles -- then return and sell before touching
replanting or their other tiles.

- Sells 60 Melon (12 x 5) same-day instead of 72 (12 x 6) a day later.
- Twenty-seed mirrored gate against Early NE single-Milk v1: 36W--4L--0T
  (90.0%), zero errors, 97,749.4 versus 96,327.3 (+1,422.1). Zero ties is
  expected since the change is unconditional, not shop-gated.
- A seed-10 isolation confirmed the mechanism: our day-10 sale quoted
  249.0/226.0 across its two batches versus the opponent's day-11 quote of
  106.0 for a larger single dump -- but the forfeited yield outweighs that
  price edge on the two losing seeds (10, 18; both thin, 254 and 13 coins).
- Five-seed regressions (seeds 1--5) won 10W--0L against Locked SW livestock v1
  (+9,181.0) and Day-0 livestock v1 (+8,447.2), both zero-error.
- Accepted and frozen as `baselines/melon_early_return_v1.py`, now the current
  frozen baseline.
- Recovering more of the forfeited yield was tried and rejected. Watering the
  lightest-loaded hand's Melon tiles (full four, or three of four to still
  make the same-day cutoff) both lost consistently (-194 and -319 to -322
  coins/seed) against the true predecessor. The mechanism: two of the three
  Melon-owning hands finish simultaneously at hour 20 in the frozen baseline,
  merging into one `SELL MELON 40` order that matches the opponent's own
  simultaneous 40-unit sale at the same market-list index. Delaying either
  hand past hour 20 shrinks our side of that pairing to 20, letting the
  opponent's matching 40-unit sale land in a lighter glut than a mirrored
  pairing would give it -- a fixed gift to the opponent independent of what
  the delayed hand does with its recovered time. Do not retry watering any of
  the three Melon-owning hands without first addressing this hour-20
  synchronization constraint. See the experiment log for the full trace.

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

## Prior next action (superseded)

Move to **P4 -- strategy-family branching**. Design one branch-selection test
using the early shop prefix to choose among the existing Cow-heavy, Sheep-heavy,
Goose, and crop-default plans. Change the decision policy only; retain the
accepted timing, hand ownership, and service routes. Start with a targeted
trace, then a five-seed mirrored screen against Early NE livestock v1.

## Next action

A roadmap detour (Melon same-day sale, see below) is now the frozen baseline;
resume from there rather than Early NE single-Milk v1.

Continue **P4 -- strategy-family branching**. The NE single-Milk Cow routing
change closed one gap in the early-NE trigger; audit the remaining seed
prefixes where the compact NE block still defers to crops (no Yarn, no Milk,
no Egg signal in the first two shops) and decide whether a crop-heavy default
is already correct there or whether another existing plan (Sheep, Goose,
mixed) deserves a similarly targeted trigger. Change one decision-policy
variable at a time, preserve the accepted timing/ownership/suppression rules,
and gate any new branch the same way: a targeted trace, a twenty-seed direct
gate against Melon early return v1, and a five-seed multi-opponent regression.
