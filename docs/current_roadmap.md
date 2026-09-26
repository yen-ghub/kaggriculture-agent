# Competitive Agent Roadmap

Read this document before selecting or implementing the next performance
experiment. Detailed completed and rejected results belong in
`docs/experiment-log.md`; confirmed game rules belong in `docs/mechanics.md`.

## Current frozen baseline

`baselines/nw_day5_strawberry_v1.py`

The active strategy in `main.py` should be compared against this baseline until
a newer candidate passes the evaluation gates below. It is `melon_layout_v2`
with four NW Strawberry planted on day 5: the day-0 Wheat tiles (1,1), (0,1),
(0,2), (2,0) stay empty after their day-4 harvest and take Strawberry on days
5-6 as the day's cash allows, and they get off-day Fertilizer from day 13.
Twenty-seed gate **38W--2L--0T, 95.0%, +2,552.6 per game**; the only loss is
seed 20 by 17. Without the Fertilizer the same change gated 35W--5L,
+1,259.9.

Known leak, in the baseline too: on seeds 3, 4, 8 and 13 both sides sell 71
Melons, not 72 -- one tile a unit short (not traced).

`baselines/melon_layout_v2.py` is its direct predecessor: `melon_layout_v1`
with one more Melon moved nearer the shed, (1,1) -> (0,4) (total distance
48 -> 46, furthest 6 -> 5), and a guard so that on Melon day the ordinary crop
routine leaves Melon tiles to the Melon workers (hand 0 owns (0,4) and is not
one). Twenty-seed gate **38W--2L--0T, 95.0%, +743.7 per game**; the only loss
is seed 9 by 92 in both positions.

`baselines/melon_layout_v1.py` is its direct predecessor: `melon_crew_v1`
with the day-0 Melons on a fixed set of twelve NW tiles nearer the shed
(`DAY0_MELON_TILES`): (1,0) -> (1,3) and (2,0) -> (1,2), total distance to the
shed 52 -> 48, furthest 7 -> 6; every other NW crop tile gets Wheat on day 0.
Twenty-seed gate **40W--0L--0T, 100.0%, +1,888.5 per game**.

**Closed: selling Strawberry ahead of the opponent** (evening sale, watering
slack, first-harvest crew; see the experiment log). The edge only exists in
glut, when our hands have no spare hours.

**Next, in order:**

- **A fixed day-10 pairing plan** (expected near break-even now that the
  furthest Melon is 5 steps out). The tiles are fixed now, so the per-turn
  nearest-first matching can be replaced by six pairs of neighbouring tiles,
  one per Melon worker, each worker returning with 12. On seed 1 the matching
  still sent hands back with a single tile and left (2,1) and (3,0) to one
  late hand, which could not reach the shed by h23 (12 Melons overnight).
- From the same replays: NE on day 6. **Early Cows
  on days 2-3 were tried and rejected (4W--36L, -3,693.7)**: the extra Milk
  sells for nothing in our Milk-saturated self-play market, and the 800 they
  tie up delays the Geese and part of the NE Strawberry. The same-day
  Fertilizer sale on days 2-3 that funded them has not been tested on its own.

`baselines/melon_crew_v1.py` is its direct predecessor: `strawberry_ceiling_m6_v1`
with a day-10 Melon crew: all eleven hands hired (8-10 are the SW hands a day
early, Melon only), every Melon watered to 6 before harvest, tiles matched
nearest-first each turn with a detour limit for loaded hands, and each batch
placed and sold on arrival at the shed. Twenty-seed gate **40W--0L--0T,
100.0%, +2,662.8 per game**; Melon sold 72.0 (from 60). Learned from ladder
replays `replays/scaling1.json` and `scaling2.json`.

`baselines/strawberry_ceiling_m6_v1.py` is its direct predecessor:
`ne_strawberry_fill_v1` with the Strawberry acreage ceiling cut by 6 on all
three constants (`STRAWBERRY_PLANT_TARGET` 39 -> 33,
`HIGH_STRAWBERRY_PLANT_TARGET` 45 -> 39, `PREMIUM_CROP_PLANT_TARGET` 45 -> 39).
Twenty-seed gate **32W--8L--0T, 80.0%, +2,058.8 per game**; our own money rose
too (85,724.6 against 83,665.8). At ~268 Strawberry a player the late dumps
sold mostly at the 1-coin floor, so the old 45/48 "denial" optimum no longer
held. A shop-count-gated version (cut only when fewer than two Strawberry
shops are open) was worse: most strong towns gain from the cut as well. Seed 9
(seven Strawberry shops of eight) is the exception, and its late shops are not
visible when the day-10 wave is planted. Public-submission result pending.

`baselines/ne_strawberry_fill_v1.py` is its direct predecessor. It is `day0_opening_v1`
with every free NE crop tile planted with Strawberry on the unlock day (17 on
seeds 1 and 15, up from 12, including the four overflow-buffer Wheat tiles),
and the day-8 Geese yielding their cash to the day-9 NE block. Twenty-seed
gate **40W--0L--0T, 100.0%, +3,081.2 per game**.

`baselines/day0_opening_v1.py` is its direct predecessor:
`offday_fertilize_ne12_v1` plus the day-0 opening package: 12 Melons + 7 Wheat
+ 4 animals on day 0 with day-1 Fertilizer paying for day-1 feed; a fix for a
staged Cow stranded in the shed; and Carrot-or-empty on NW days 7-9 so every
NW tile joins the day-10 Strawberry wave. Twenty-seed gate **25W--15L, 62.5%,
+754.2 per game**. It changes the empty-tile count from day 0, so it re-rolls
most towns and flips individual seeds; judge it by the margin over many games
(public submission) rather than by win count.

`baselines/offday_fertilize_ne12_v1.py` is its direct predecessor:
`offday_fertilize_ne_early_v1` with all twelve early Strawberry seeds planted
in NE on its unlock day (day 7), instead of six there and six converted from NW
Wheat on day 9. Twenty-seed gate **40W--0L--0T, 100.0%, +2,888.2 per game**,
and it held up in public submission. On seed 15 (like-for-like town) the split
split across the four like-for-like seeds was own +1,699 / taken +1,829 --
the first NE Strawberry change with a substantial own-money share. The other
16 seeds re-rolled their towns, but the head-to-head delta is positive on all
20.

`baselines/offday_fertilize_ne_early_v1.py` is its direct predecessor:
off-day Fertilizer extended to NE's first Strawberry wave (planted before day
10). Twenty-seed gate 36W--4L--0T, 90.0%, +1,882.1 per game against the SW-only
baseline.

**That win is mostly taken from the opponent, not earned.** On seed 1 our own
money was level with the baseline mirror (+6) while the opponent lost 2,042:
the SW-only baseline already saturates the shared Strawberry market. Before
building more Strawberry volume on top of this, run
`python tools/trace.py mirror --seeds 1-20 --opponent offday_fertilize_sw_v1`
to see the twenty-seed split.

Next, in order:

- **The twenty-seed own/taken split** above -- one command, two games per seed.
- **NW is not worth extending into** on the seed-1 evidence: the market is
  already saturated, so more units only take the opponent's price. Revisit
  only if the split shows we still earn from extra Strawberry on most seeds.
- **The Strawberry sell side on glut seeds.** When the opponent is
  Strawberry-heavy, the daily cap lifts and the whole shed sells at h01: on
  seed 6 a 49-unit order took the price from 144 to 7. That loses money with or
  without the Fertilizer, and it is the likeliest common factor in the four
  remaining losses (only seed 6 has been traced). Unlike more volume, this
  lever should add our own money rather than only take the opponent's.

`baselines/offday_fertilize_sw_v1.py` is its direct predecessor: off-day
Fertilizer on SW Strawberry only (34W--6L, 85.0%, +3,945.1 per game against
`day10_relief_hand_v1`, and on seed 1 a genuine +7,569 of our own money).

`baselines/day10_relief_hand_v1.py` (commit `2444200`) came before that: `permanent_ne_geese_v1` plus two safety changes, frozen without a
gate:

- **Seed purchases keep tomorrow's hire cost in reserve.** A day 0 that ended
  on zero money hired nobody on day 1 and never recovered
  (`replays/zero_money.json`). Forced locally with `startingMoney` 2989: 0
  final before, 125,969 after.
- **A one-day relief hand on Melon day** when at least three Wheat stand
  ready on the western route (`replays/leftover_wheat.json`). It never fires
  on seeds 1-20 against our own baselines -- the early NW Strawberry
  conversion has already cleared that Wheat by day 9 -- so it cannot be
  measured locally; it only fires when the day-6 Wheat wave slips a day.

The previous baseline, `baselines/permanent_ne_geese_v1.py`, is
`immediate_milk_deposit_v1` plus the permanent NE Geese package: the two NE
Geese run on every seed, not only on Egg-demand prefixes; when the compact NE
block also runs, the Geese sit at (5,1)/(5,2) with the four animals on the
default block beside the shed; and the flat early-NE livestock cash reserve is
removed. Twenty-seed gate 18W--6L--16T, +234.2 per game. The five-seed
regressions have **not** been run yet -- see the experiment log.
`baselines/immediate_milk_deposit_v1.py` is its direct predecessor.

Open items on this baseline, in order:

- Seeds 6 and 10 (Egg + Yarn) moved off the previously accepted coexistence
  layout onto the new one, and seed 6 lost 971 for it. Restricting the new
  layout to the seeds where the Geese exist only because they are permanent
  would return both to byte-identical.
- The animal purchase is still all-or-nothing. Removing the reserve fixed the
  Cow delay on seeds 15 and 19; a seed with even weaker day-8 cash could still
  delay the block behind the Wheat feed floor.
- On seeds with no Egg demand, the Geese carry ~50 bought feed Wheat and two
  lost crop tiles against ~75 Eggs at ~46. Seed 15 says that nets slightly
  positive, seed 19 says slightly negative.

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
- The farmer drops carried Milk into the shed the moment his round is standing
  on a shed-access tile, and leaves it there rather than selling it on the
  spot. Section 3.4's shed seller moves it on the following turn, one to
  several hours earlier than the fused place-and-sell the round used to end
  on. Wool, Egg, and the final day keep the fused place-and-sell.
- Idle hands and the farmer collect Fertilizer; selected premium crops use it
  when the projected return clears the value margin.
- Market sell orders are sorted by a `CROP_SALE_PRIORITY` tuple (`MELON,
  STRAWBERRY, TOMATO, CARROT, WHEAT`, descending base price) via a stable
  sort, generalizing the earlier Melon-only priority special case. Every
  other order (seed buys, hires, land, Fertilizer, animal products) keeps
  its existing relative order; Fertilizer is still explicitly forced last.
  Scoped to crops only -- Wool/Milk order is untouched pending its own test.
- Endgame liquidation and the NE Wheat overflow buffer are active.
- Once NE is unlocked and before day 10, the original NW hands (index
  0-3) get their own early Strawberry wave (`early_nw_strawberry_phase_active`),
  recycling mature staple-crop tiles into Strawberry instead of always
  replanting the same staple, up to 6 plants counted on NW's own tiles.
  Mirrors the existing NE early-Strawberry mechanism but counts separately
  so the two waves cannot starve each other's target through a shared
  counter; the combined seed-purchase target covers both. See "Opponent-
  replay-informed staged packages" below.
- The Wheat feed-reserve purchase (livestock feed) is now computed before
  any new animal purchase, and that cost is a cash floor the animal
  purchase must clear -- protects against a confirmed engine mechanic
  where a full day of zero feed unplaces every animal on the farm
  overnight, not just new ones. See "Early NW Cow expansion" below for how
  this was found and `docs/mechanics.md` for the confirmed mechanic.

Latest frozen validation (Wheat-feed cash-reserve fix) against Early NW
Strawberry v1:

- Five-seed mirrored screen: 5W-5L, 50.0% match score, 95510.5 vs 95323.4
  (+187.1 average), zero errors -- neutral, as expected for a correctness
  fix carrying no strategic change.
- Twenty-seed direct gate: 19W-21L, 47.5% match score, 95239.0 vs 95182.6
  (+56.4 average), zero errors -- confirms the five-seed result was not
  hiding a regression at scale.
- Five-seed regressions won 10W--0L against both Locked SW livestock v1
  (85586.8 vs 75230.6) and Day-0 livestock v1 (96242.0 vs 84929.2), both
  zero-error -- matching the predecessor's own acceptance numbers against
  these same two baselines.

Prior validation (Early NW Strawberry v1, superseded above) against Crop
sale priority v1: 36W-4L-0T over 20 mirrored seeds, 90.0% match score,
94,896.2 vs 93,034.9 (+1,861.3 average), 369.0 average harvests, zero
errors; five-seed regressions won 10W-0L against both standard baselines.

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

Replay-informed livestock-scale finding:

- A real ranked-match replay (`replays/110311259.json`, local only, not
  tracked in git) showed our agent losing 90,253 to 140,537, with the money
  gap widening almost linearly from day 10 onward -- a sustained per-day
  production deficit, not a one-time opening loss. Ground truth at days
  15--19 showed 9 Cows + 4 Sheep (13 animals) for us against 9 Cows + 5
  Sheep + 3 Geese (17 animals) for the opponent, on a shop prefix (two
  Smoothie Shops, no Yarn, no explicit multi-Milk shop) that activated our
  early-NE all-Cow branch.
- The early-NE compact block, the adaptive Goose branch, and the SW
  four-animal branch were mutually exclusive by construction, not just
  policy: the Goose tiles are two of the early-NE block's four tiles (a hard
  tile conflict), and the SW/early-NE branches share one hand-index variable
  and one hand-action function.
- **The Goose/early-NE half of this is now resolved.** When both branches
  qualify (first two shops demand Eggs *and* signal Yarn or double Milk) the
  livestock block shifts one column east to `(7,4)`, `(8,4)`, `(7,3)`, `(8,3)`,
  the Geese keep `(6,4)`/`(6,3)`, and six animals run where four did. Hand 5
  serves the animals, hands 4 and 6 own one Goose each, and the farmer is kept
  off both. Twenty-seed gate: 5W-1L-34T, 55.0%, +198.3, zero errors; the one
  loss is -76 on 114,115. Regressions against the two standard baselines were
  not run, so this is not frozen -- `wheat_feed_cash_reserve_v1` is still the
  reference baseline. See the experiment log for the full breakdown.
- The lesson generalises beyond the tiles: the relocation alone scored
  -2,947/-1,829 on the traced seeds. All of the gain came from *service*
  fixes -- keeping the farmer's round untouched, holding flat-priced produce
  until the overnight drop, batching feed pickups, and giving each hand a
  contiguous route. Any future attempt to run two animal branches at once
  should budget most of its effort there, not on tile choice.
- The SW/early-NE shared-dispatch conflict is still unresolved and still needs
  its own experiment.
- A narrower candidate -- widening the early-NE block itself from 4 to 6
  tiles (adding `(8,4)` and `(8,3)`, same hand, same days) -- was tried and
  rejected. It bought 2 more Cows cleanly (zero errors, unlock timing
  unchanged) but lost a consistent 3589--6763 coins on every one of the five
  mirrored seeds where it activated (average deficit 4736.4; the fifth seed
  tied because the branch never triggered). The extra tiles came entirely
  from Hand 7's zone, and Milk's tight glut threshold likely meant the
  10th-Cow Milk output could not repay its own cost. Do not retry a wider
  early-NE block without freeing tiles from a less-loaded hand or addressing
  Milk oversupply directly.
- Any future attempt to close this 13-vs-17 animal gap must treat the
  tile/hand-index restructuring as its own experiment, gated the same way as
  any other candidate, rather than folding it into a threshold tweak.

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
- A follow-up twelfth-hand experiment (Carrot on the seven unmanaged SW
  tiles) was also tried and rejected; see P0 above and the experiment log
  for the full breakdown.

## Crop sale priority order -- accepted (roadmap detour)

Requested outside the P0--P4 sequence: audit `market_orders` construction and
confirm premium crops sell first. Only Melon had ever been explicitly
prioritized; everything else sold in raw `CROPS_MANAGED` /
`ANIMAL_PRODUCT_ORDER` tuple-definition order, not by value -- Strawberry
(base price 120) sold behind Wheat (25) and Carrot (35) purely by definition
order.

- Generalized the Melon-only pop/insert special case into a
  `CROP_SALE_PRIORITY` tuple (`MELON, STRAWBERRY, TOMATO, CARROT, WHEAT`,
  descending base price) and one stable sort. Every other order (seed buys,
  hires, land, Fertilizer, animal products) keeps its existing relative
  order untouched; Fertilizer is still explicitly forced last. Scoped to
  crops only -- Wool/Milk order was deliberately left alone, since the
  twelfth-hand experiment immediately above found Wool's realized price
  actually *improving* from a later list position in that case.
- Twenty-seed mirrored gate against Melon early return v1: 25W--15L--0T
  (62.5%), zero errors, 92,970.3 versus 92,814.5 (+155.8). All three sampled
  losses were thin (31, 47, 91 coins), consistent with isolated per-seed
  deltas of -27 to +270 measured directly -- much smaller than the
  large-quantity Melon and SW-hand cases, since these crops co-occur in the
  same step far less often and in smaller quantities.
- The five-seed multi-opponent regression was explicitly skipped at the
  user's request; accepted on the twenty-seed direct-gate evidence alone.
- Accepted and frozen as `baselines/crop_sale_priority_v1.py`, now the
  current frozen baseline.

## Deprioritized directions

- Fourth-quadrant expansion: none of the five replay agents used it, while all
  fully exploited the first three quadrants.
- Unconditional extra SW livestock: earlier results were highly seed-sensitive
  and sometimes displaced more valuable crops.
- Adding livestock tiles beyond the current plan, generally: eight separate
  attempts (seven early-NW-Cow variants plus one wider-NE-pasture variant,
  see "Early NW Cow expansion" and "Wider NE pasture staging" above) all lost
  once properly evaluated, despite each being inspired by a real opponent
  replay pattern. The tile's lost crop income plus ongoing feed cost
  consistently outweighs the extra animal's Milk/Wool/Egg revenue under this
  economy. Do not retry this shape (one or two extra tiles bolted onto an
  existing livestock group) without a fundamentally different angle; a full
  branch/composition change (see "Next action") is a different kind of bet.
- Earlier Geese without workload sharing: day-7/day-8 farmer-only versions lost
  crop output and liquidity. The Hand 5 split is the retained solution.
- Broad early liquidation to avoid shed overflow: it diverted hands from more
  valuable field work. Prefer harvest staggering and targeted product returns.
- Large multi-variable changes: they make failures impossible to attribute.
- Raising the Strawberry acreage ceiling: swept in both directions and
  rejected both ways; 45/48 is confirmed optimal against the frozen baseline.
  Upward gluts the shared market and drops our own money from 97,849 to
  91,886; downward costs us almost nothing but raises the *opponent's* money
  to 98,670, because a large part of what this acreage buys is denying them a
  Strawberry price. Moving it requires `PREMIUM_CROP_PLANT_TARGET` as well --
  the other two constants alone are clamped and produce an identical agent.
  See the experiment log for the full curve and one unexplained non-monotonic
  row at offset -3.
- Planting an ongoing crop earlier to gain a day: rejected twice, as the
  permanent goose at `(4,2)` and as the melon-harvest-day relief hire
  (26W--14L, 65.0%). Strawberry delivers four yield cycles whether it is
  planted on day 10 or day 11, because `last_production_day` caps growth-day
  production at 16 -- see `docs/mechanics.md`. Before proposing this shape
  again, do the cycle arithmetic from the crop table first; both attempts were
  answerable on paper before any code was written. Acreage is capped by live
  plant count too, so earlier planting displaces other crops rather than
  adding tiles.

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

## Prior next action (superseded)

Two roadmap detours (Melon same-day sale, then Crop sale priority order; see
below) are now the frozen baseline; resume from there rather than Early NE
single-Milk v1.

Continue **P4 -- strategy-family branching**. The NE single-Milk Cow routing
change closed one gap in the early-NE trigger; audit the remaining seed
prefixes where the compact NE block still defers to crops (no Yarn, no Milk,
no Egg signal in the first two shops) and decide whether a crop-heavy default
is already correct there or whether another existing plan (Sheep, Goose,
mixed) deserves a similarly targeted trigger. Change one decision-policy
variable at a time, preserve the accepted timing/ownership/suppression rules,
and gate any new branch the same way: a targeted trace, a twenty-seed direct
gate against Crop sale priority v1, and a five-seed multi-opponent regression.

## Prior next action (superseded)

A replay-informed detour (see "Replay-informed livestock-scale finding"
above) tested widening the early-NE block to close the 13-vs-17 animal gap
seen in a real lost match; it was rejected on the five-seed screen. The
replay study also surfaced a real architectural constraint -- the early-NE,
Goose, and SW livestock branches share tiles and a hand-index dispatch, so
none of them can simply be "turned on" alongside another. That restructuring
is its own future experiment, not a quick follow-up.

Resume the still-open **P4** audit from the prior next action above: the
remaining seed prefixes where the compact NE block defers to crops (no Yarn,
no Milk, no Egg signal). If more replays land in `replays/`, prefer
ground-truth-state comparisons (animal counts, hand counts, land-unlock day,
shop prefix) over action-log tallies -- submitted market orders include
no-ops and cannot be trusted as executed quantities. Any candidate that would
add a livestock branch on top of an already-active one must budget for the
tile/hand-index restructuring above as part of its own scope, not as a
one-line threshold change.

## Opponent-replay-informed staged packages

`docs/opponent_replay_trace.md` reconstructs a real winning opponent's
actions day-by-day (currently days 0-6). Rather than replaying it verbatim
(only our own agent's days 0-1 are verified deterministic across seeds; the
opponent's days 2+ come from one seed and may not generalize), insights are
being translated into `main.py` as small, independently-gated dynamic-rule
packages. See `docs/experiment-log.md` ("Opponent-replay-informed staged
packages") for full evidence.

- **Package 1 -- accepted**: early NW Strawberry conversion. Frozen as
  `baselines/early_nw_strawberry_v1.py` (superseded as the current frozen
  baseline by `baselines/wheat_feed_cash_reserve_v1.py`, see top of this
  document -- Package 1's own characteristics are unchanged and carried
  forward).
- **A 5th day-0 hand -- investigated, not implemented**: our own agent's 21
  real NW crop tiles are already fully divided across the existing 4 hands
  and fill in completely by day 4 using only those 4 -- the fill rate is
  cash-gated, not hand-time-gated (day 0 ends at 11 coins, day 1 at 4, no
  idle cash sitting unused). A 5th hand would only redistribute the same 21
  tiles, adding a recurring hire cost with no new capacity to spend it on.
  Do not retry this without first finding an actual cash-efficiency lever
  (see below) that would let a 5th hand's hire cost be recovered.
- **Package 2 -- rejected**: Wheat-vs-Carrot early staple preference. Our
  fixed per-turn seed-purchase target (not "spend all available cash")
  means Wheat's cheaper seed does not fill tiles any faster than Carrot
  once there is enough cash to clear that target, so forcing Wheat just
  locks in a lower profit-per-day for the same tiles -- a controlled
  isolated-trace (idle opponent, 3 seeds) showed a consistent net loss with
  no evaluate.py run needed. See `docs/experiment-log.md` for the full
  writeup. This investigation surfaced a bigger finding below.

## Harvest-timing finding -- confirmed mechanic, three fix attempts rejected

`docs/mechanics.md` confirms one-time crops (Wheat, Carrot, Melon) do not
reach their configured `harvest_yield` until one day *after* their
configured `harvest_day` -- the agent harvests every one-time crop one day
too early, all game, for one fewer unit than `crop_profit_per_day()`
assumes. The mechanic is real, but three direct ways to act on it were all
tried (single-seed each) and rejected -- see `docs/experiment-log.md` for
the full writeup:

1. Wheat + Carrot `harvest_day` +1 together: narrowed their profit-per-day
   gap enough to flip-flop which one `choose_crop_for_planting()` treats as
   the default staple day to day, dropped average harvests from 369 to
   284.5, and lost.
2. Wheat + Carrot `harvest_yield` -1 only (timing unchanged): same
   direction, smaller deficit, still lost.
3. Melon `harvest_day` +1 alone (no staple-selection interaction): still
   lost, consistently across 3 seeds but by a much smaller ~2% margin --
   the extra unit did not make up for losing `MELON_HARVEST_DAY`'s
   first-mover market-timing advantage over the opponent's unmodified
   schedule.

Not recommended to revisit without a genuinely new angle (e.g. a
Melon-specific approach that keeps the early sale timing but still captures
the extra unit some other way) rather than a direct `CROP_CONFIGS` edit.

## Early NW Cow expansion -- rejected after six iterations; root cause fixed

Investigated whether our Carrot-based cash flow could support the
opponent's 3rd/4th Cow before day 4 (our own baseline stays at 2 Cows until
day 6-8). Six iterations, each a different failure mode until the last --
see `docs/experiment-log.md` for the full writeup:

1. Reused an existing Carrot tile: mixed, net-negative 1W-2L result.
2. Reserved two tiles unconditionally from day 0: outbid the entire Melon
   wave for day-0 cash (permanent, whole-game loss), plus a tile collision
   with `DAY4_ADDITIONAL_SHEEP_TILES` silently produced a Sheep instead of
   a Cow.
3. Fixed both of those: hit a real, uninvestigated bug instead -- Sheep and
   Cow tiles were destroyed (reverted to empty) partway through the game on
   every seed.
4. Sidestepped the shared system with an independent construction routine
   that only hands a tile to the shared logic once already placed: no more
   destruction, but it turned out to be grabbing *every* Cow the shared
   purchase loop bought for itself -- `(4,4)`/`(4,3)` (the original 2 Cows)
   sat completely unplaced through day 7 on every seed, while the two new
   tiles filled by day 1.
5. Fixed the misallocation (self-gated on the original 2 Cows being placed
   first): correctly restored `(4,4)`/`(4,3)` filling by day 1, but this
   made things worse, not better -- the destructive-tile bug from
   iteration 3 reappeared (seed-dependent now, not universal: one of three
   seeds traced showed Sheep and Cows both briefly drop to 0 around day
   8-9), and final scores were worse than iteration 4's own numbers on
   every seed.

`main.py` reverted to the frozen baseline.

**Root cause found, and it corrects the diagnosis above.** The
"destructive-tile" failures in iterations 3 and 5 were re-investigated
(rather than left as "hand-index dispatch fragility") and turned out to be
a specific, narrower bug: `docs/mechanics.md` now confirms an animal left
unfed for a full day gets unplaced overnight. On the failing days, *every*
animal on the farm (not just the new ones) showed zero feeding all day,
because Wheat shed stock was 0 -- the `BUY_ANIMAL` purchase (section "3.5")
runs before the Wheat feed reserve purchase ("3.6") each turn and both draw
from the same cash, so buying two new Cows at once left nothing for that
day's Wheat. `active_animal_plan`/`choose_setup_action` were never actually
corrupted. See `docs/experiment-log.md`'s "Root cause found" writeup.

**Fixed and validated.** `wheat_to_buy`/`wheat_purchase_cost` are now
computed once, before the animal-purchase section, and used as a cash
floor any new animal purchase must respect -- the same pattern
`EARLY_NE_LIVESTOCK_CASH_RESERVE` already used for a different reserve.
Five-seed mirrored screen with no livestock experiment layered on top:
5W-5L, 50.0% match score, +187.1 average, zero errors -- neutral, as
expected for a pure correctness fix. See `docs/experiment-log.md`'s
"Accepted: Wheat-feed cash-reserve fix" for the twenty-seed gate result.

Confirmed the fix actually resolves the target bug: re-added early NW Cow
expansion (iteration 5's design) on top of it and re-traced the same seeds
that previously showed destruction -- zero drops, Cows/Sheep progress
strictly monotonically the whole game, `(4,4)`/`(4,3)` correctly fill by
day 1 every time.

6. **With the bug now actually fixed**, early NW Cow expansion's own
   five-seed mirrored result was clean but decisive: 0W-10L, 0.0% match
   score, -6227.4 average, zero errors. Rejected on economics, not on a
   lingering bug -- converting 2 tiles' crop income plus the new Cows'
   ongoing feed cost does not pay for itself against our Carrot-based
   economy. `main.py` reverted to the frozen baseline plus the reorder fix
   only (no livestock experiment). Do not retry this specific idea without
   a fundamentally different angle on that trade-off.
7. **Scoped down to just the single 3rd Cow at `(4,2)`**, day-2-gated to
   match the opponent's own timing, using the shared construction path
   instead of the six-iteration saga's bespoke routine (safe to do now:
   only one tile changes hands at a time, and the cash-reserve fix already
   covers the Wheat-starvation failure mode). Construction itself came out
   clean after fixing one new bug (the farmer's own crop-fallback scan,
   separate from the hand-route logic, had no idea the tile was reserved --
   see `docs/experiment-log.md`'s "Rejected: single-tile 3rd Cow" for the
   fix). Cash-gated to day 5 rather than day 2 under our own Carrot economy
   (expected, not a bug). Five-seed mirrored screen: 3W-7L, 30.0% match
   score, -2732.8 average, zero errors -- still a clean loss, smaller than
   the two-tile version but not close to neutral. `main.py` reverted to the
   frozen baseline. Seven iterations of this tile-count/timing family now,
   all net negative; not recommended to retry without a fundamentally
   different angle (a cheaper tile, or a cash source that doesn't compete
   with Melon/Carrot spending), same conclusion as iteration 6.
8. **Paired with an early-Wheat staple preference** (forcing Wheat over the
   normal profit-per-day comparison during the pre-NE opening), at the
   user's request -- on the hypothesis that Wheat's half-price seed might
   free enough cash to move the Cow's placement closer to the opponent's
   day-2 timing even though the staple-preference idea already lost on its
   own (see "Rejected: Wheat-vs-Carrot early staple preference" above).
   Mechanically the hypothesis held (Cow placement moved from day 5 to day
   4), but final scores were worse, not better: five-seed mirrored screen
   0W-10L, 0.0% match score, -4546.2 average, zero errors -- a bigger loss
   than the Cow alone. Wheat's lower whole-game profit-per-day dominates any
   cash-timing benefit elsewhere. `main.py` reverted to the frozen baseline.
   Do not pair Wheat-as-opening-staple with other early-cash-timing ideas
   again; the revenue cost has now failed to be offset twice.

## Wider NE pasture staging -- both halves rejected

Part (a), pre-building pasture ahead of affording the animal: measured our
own frozen baseline's construction timing directly (not the opponent's)
before writing any code. `EXPANSION_COW_TILES` builds pasture and places the
animal the *same day* on every seed traced; `EARLY_NE_LIVESTOCK_TILES` (when
it activates at all) shows only a 1-day gap. Unlike the opponent, our cash
rhythm means these tiles already enter the plan around when we can afford
them -- there was no gap to close, so this half was rejected on the
measurement alone, no code written.

Part (b), genuinely adding `(5,2)`/`(6,2)` as two more NE pasture Cow tiles
(the only two of the opponent's 7 staged NE positions not already covered by
`EXPANSION_COW_TILES` + `EARLY_NE_LIVESTOCK_TILES`): implemented as the
minimal change (appended to `EXPANSION_COW_TILES`, `EXPANSION_COW_COUNT`
2 -> 4, reusing the existing tested construction/purchase path unchanged).
Clean trace (no drops, all four tiles build together on day 7 once
affordable), but the five-seed mirrored screen was a clean loss: 2W-8L,
20.0% match score, -3208.0 average, zero errors. See
`docs/experiment-log.md` for both writeups.

This is the 8th iteration of "add more livestock tiles" (7 earlier attempts
at an early NW Cow, in every shape; now one NE attempt), and the 8th to
lose. Treat this as a settled dead end for the current economy, not a
candidate to retry in yet another location without a fundamentally
different angle -- the opponent's replay shows the pattern working for
*their* economy, but every attempt to port it into ours has landed net
negative once actually evaluated.

## NE Goose relocation -- rejected; real bug found and fixed, then reverted

At the user's request (in place of pursuing the cattle-heavy branch below,
for which the needed replay file was not available locally -- see
`docs/experiment-log.md`): relocated `ADAPTIVE_GOOSE_TILES` from `(6,4)`/
`(6,3)` to `(5,2)`/`(6,2)` and removed the hard exclusion that prevented
Geese from being selected whenever the compact NE livestock block
(`EARLY_NE_LIVESTOCK_TILES`) was also selected -- the two used to physically
share two tiles, which is the only reason they were ever mutually exclusive.

This surfaced a genuine latent bug in `choose_animal_action`'s farmer
service logic: it indexed `active_animal_plan[pos_current]` before checking
`pos_current` was actually a key, which crashed (`KeyError`) the moment the
farmer's route legitimately crossed a tile mid-construction under a *second*
animal group it didn't own yet -- unreachable before this change because no
two animal groups had ever been allowed to run concurrently with physically
adjacent tiles. Fixed by reordering the condition to check membership first.
See `docs/experiment-log.md`'s "Rejected: NE Goose relocation" for the full
root cause.

**Known codebase constraint** (new, worth remembering for any future
livestock-branch work): any code that indexes `active_animal_plan[position]`
must confirm `position in active_animal_plan` (or draw `position` from an
already-filtered list such as `animal_positions`/`farmer_animal_positions`)
*before* indexing, not after. Every such site except this one already
followed that order; audit it again if a future change lets two animal
groups run concurrently with tiles anywhere near each other. The fix itself
was reverted along with the rest of this experiment (it protects an
otherwise-unreachable path once `ADAPTIVE_GOOSE_TILES` is back at `(6,4)`/
`(6,3)`), so it will need to be reapplied if this ordering is revisited.

With the crash fixed, the mechanism itself worked correctly (no further
errors, no destructive-tile drops, genuine coexistence confirmed on 2 of 20
seeds) but lost decisively on economics: 20-seed direct gate 1W-23L-16T,
22.5% match score, -1204.7 average, zero errors. The 16 ties are exactly the
seeds where Geese were never selected (proving the relocation is inert when
unused); every seed where Geese *were* selected lost, including both
coexistence seeds -- the new tiles sit one row farther from the shed than
the original pair, and that extra daily FEED/CARE travel cost outweighs the
two Geese's Egg income even when coexistence fires as designed.

`main.py` reverted to the frozen baseline at that point. Picked back up
per the closing suggestion above (try a closer tile pair / better hand
ownership before concluding coexistence itself has no value) -- four more
iterations, all reverted, fully closing out this line of work:

1. Made the relocation conditional on `early_ne_livestock_selected` (Geese
   only move to `(5,2)`/`(6,2)` when the compact block is actually
   selected; otherwise byte-for-byte identical to the pre-relocation
   baseline -- verified with an exact-match trace).
2. Root-caused hand 4's travel cost concretely (a real ~5-hour/day detour,
   traced hour by hour) rather than just theorized.
3. Tried hand 6 alone: real improvement (both coexistence seeds' margins
   roughly halved) but neither flipped to a win.
4. Tried splitting the pair between hands 4 and 5: hand 5 is also
   `EARLY_NE_LIVESTOCK_HAND_INDEX`, and adding even one Goose tile to its
   existing 4-animal service duty caused it to periodically miss feeds --
   both coexistence seeds showed a reproducible Sheep-count drop (days 15
   and 17) and margins collapsed to roughly -20000.
5. Tried hand 5 alone (both tiles, no hand 4): identical drop days, same
   magnitude of loss -- isolates the cause as hand 5's own workload, not
   two-hand coordination.

**Settled conclusion**: no hand assignment tried gets both a cost-free
route to the coexistence tiles *and* spare capacity at the same time --
hands with a natural route there (hand 5, under the default tile split)
have no spare capacity once claimed by the compact NE block; hands with
spare capacity (hand 6) have no natural route and pay a travel tax instead.
Not recommended to keep iterating on hand assignment for this specific tile
pair without a structural change (redefining which physical tiles belong to
which hand's default patrol, not just reassigning Goose ownership among the
existing fixed patrols). See `docs/experiment-log.md`'s "Rejected (four more
variants)" for full per-iteration numbers.

## Immediate Milk deposit -- accepted

Requested as an incremental change outside the P0--P4 sequence, not a
continuation of any queued track. The farmer used to carry harvested Milk in
his backpack until his animal round finished, then deposit and sell it in the
same action at whatever hour that round happened to end. The accepted change
drops carried Milk into the shed the moment his round is standing on a
shed-access tile, and suppresses the paired `SELL` so section 3.4's shed
seller moves it on the following turn.

The mechanism is a measured intraday price curve, not an inference. Milk's
price climbs to a midday peak and collapses in the hour the day's supply
lands. On seed 1, day 10 ran 187, 190, 190, 191, 193, 194 across hours 0--14,
then fell to 175 in the hour the h15 sale landed, recovering only to 179 by
hour 23. The farmer was selling into his own collapse. His route already
crosses shed access at `(4,4)` and `(5,4)`, so the earlier drop costs one
action rather than a detour -- no travel is added.

- Twenty-seed mirrored gate against the direct predecessor
  (`baselines/ne_goose_coexist_v1.py`, byte-identical to `main.py` before this
  change): 34W--6L--0T (85.0%), zero errors, 95,400.5 versus 94,892.9
  (+507.6). Zero ties, because unlike the shop-gated coexistence trigger this
  round runs on every seed, so every game is decided by the change.
- The six losses are all thin and arrive in mirrored pairs: seeds 8 (-38),
  11 (-32) and 17 (-84), on scores near 100,000.
- Both mirrored positions return identical scores, so the environment carries
  no first-mover asymmetry and the 40 games are 20 independent seeds.
  (Not always true -- see docs/mechanics.md on position asymmetry.)
- Five-seed regressions, candidate side only: 10W--0L against Day-0 livestock
  v1 (+10,941.0), Early NW Strawberry v1 (+668.3) and the frozen reference
  Wheat-feed cash-reserve v1 (+498.4), all zero errors. These establish that
  no opponent regressed; they do not size the gain, because the predecessor's
  side of the same matchups was not run.
- Accepted and frozen as `baselines/immediate_milk_deposit_v1.py`, now the
  current frozen baseline.

### Open item

Some of the gate win may be positional rather than absolute. Against
`locked_sw_livestock_v1` on seed 1, our own money fell 187 while the
opponent's fell 305 -- the gain came from making the opponent lose more, which
is exactly what a change to *when* produce reaches a shared market can do to a
copy that is about to dump into the same hour. At a +0.53% average margin that
effect alone could account for the result. The predecessor side of the
five-seed regressions is the measurement that would settle it.

Two levers the trace exposed but that this change does not address:

- The **hands** sell their Milk at hour 23, the worst hour of the day. On seed
  1, day 17 they moved 24 units at 122 after the market had already fallen
  from 181 earlier the same day. That is the largest single Milk event in the
  match and it still lands after the crush.
- Only the **first half** of the farmer's daily Milk moves. The second deposit
  lands at `(5,4)` at hours 13--14 and still sells into the h15 collapse. If
  the first-half fix is to be extended, firing the deposit *before* servicing
  an animal on the tile is what would capture the h13--h14 peak instead of
  landing at h15.

## Next action

The opponent-replay-informed package track (`docs/opponent_replay_trace.md`)
is now exhausted: Package 1 accepted, Package 2 rejected, the 5th day-0 hand
investigated and rejected, and now wider NE pasture staging rejected in both
halves. No further packages are queued from that source. Candidates worth
considering next, none yet scoped or traced:

- **Day-0 cash-efficiency lever**: flagged but never directly investigated
  on its own (only as a prerequisite for the already-rejected 5th-hand
  idea). Worth a dedicated look at whether day-0/day-1 spending order has
  any recoverable slack, independent of any specific use for that cash.
- **Xiangyu Liu's cattle-heavy branch** (`docs/current_roadmap.md`'s "Top-
  player replay study"): ~9 Cows, 3 Sheep, 1 Goose, 12 hands, earlier SW
  expansion -- the one static replay tape that beat the current live agent
  on its own recorded seed. Different in kind from the rejected tile-count
  additions above (a full branch/composition change, not one or two extra
  tiles on top of the existing plan), so not automatically subject to the
  same conclusion, but should be sized as a real branch-selection
  experiment (P4-style), not another incremental tile add.
- **QQ Farming's diversified/Goose-heavy branch**: fewer hands, more
  Tomato/Carrot, six Geese in a Pet-Cafe-heavy market -- another full
  alternative composition, same caveat as above.

Change one variable at a time (or one tightly coupled branch, per the
evaluation protocol's definition), gate each the same way as prior work: a
targeted trace, a five-seed screen against the current frozen baseline, and
(if promising) a twenty-seed direct gate plus the standard regression against
the recent frozen baselines. Run the predecessor's side of any regression
whose result you intend to promote -- the immediate-Milk-deposit entry above
shows what is left unmeasured when you do not.

Before reaching for any of them, note the two unclaimed levers recorded in
that entry: the hands' hour-23 Milk sale, and the second half of the farmer's
own Milk round. Both are strictly larger than anything left in the queued
candidates below and neither needs a new strategic branch.
