# Kaggriculture Mechanics

Note: AI-generated, to summarise and keep track of the learnings from the incremental improvements.

This document records game mechanics verified through local traces, the
competition environment, or direct experiments.

Strategy choices and unverified assumptions should be recorded separately.

## Game timeline

- A match lasts 720 steps.
- There are 30 in-game days, numbered `0` through `29`.
- Each day has 24 hours, numbered `0` through `23`.
- The final step is day `29`, hour `23`.
- Each player submits one action dictionary per step.
- The player with the most money at the end wins.

Local evaluation shows that the observation at day `29`, hour `23` must be
treated as the terminal state. An action submitted from that observation
should not be relied upon to produce another observable state change. Final
movement, depositing, and selling must therefore be completed before it.

A useful relationship is:

```python
step = day * 24 + hour
```

## Agent interface

The submission entry point is:

```python
def agent(obs):
    ...
```

The agent returns a dictionary containing farmer, hand, and market actions:

```python
return {
    "farmer": ["PASS"],
    "hands": [],
    "market": [],
}
```

The `hands` list contains one action for each currently active farm hand, in
the same order as `farm["hands"]`. It is empty before the day's hires have
spawned and after hands disappear at the day boundary.

Farm hands can perform the same movement and crop actions as the farmer,
including `PLANT`, `WATER`, and `HARVEST`. Seeds are shared across the farmer
and all hands; they are not carried in an individual unit's inventory.

## Observation structure

Important fields include:

```python
obs["player"]
obs["day"]
obs["hour"]
obs["step"]
obs["farms"]
obs["market"]
obs["private"]
```

`obs["player"]` identifies which farm and private state belong to the agent:

```python
player_id = obs["player"]
farm = obs["farms"][player_id]
private = obs["private"]
```

Both farms are publicly visible, but each player's inventory, seeds, and shed
are private.

## Coordinates and tiles

Farmer positions are supplied as:

```python
[x, y]
```

The project converts them to tuples for convenient comparisons:

```python
position = tuple(farm["farmer"])
```

Internally, this project represents positions as:

```python
(x, y)
```

However, the tile grid is indexed in row-major order:

```python
tile = farm["tiles"][y][x]
```

This difference is important:

```text
position:     (x, y)
tile lookup:  tiles[y][x]
```

The northwest `5 × 5` section of the farm is initially available to the agent.

## Farmer actions

### Pass

```python
["PASS"]
```

Take no farmer action.

### Movement

```python
["NORTH"]
["SOUTH"]
["EAST"]
["WEST"]
```

Movement changes the farmer's position by one tile:

| Action | Coordinate change |
|---|---|
| `NORTH` | `y - 1` |
| `SOUTH` | `y + 1` |
| `WEST` | `x - 1` |
| `EAST` | `x + 1` |

### Plant

```python
["PLANT", "MELON"]
```

Planting requires:

- The current tile to be empty
- An available seed of the requested crop
- The tile to be usable by the player

A newly planted crop should be watered during the same day.

The farmer and farm hands all plant from the same seed inventory. If several
units are scheduled to plant during one step, the agent must reserve enough
seeds for all of those planned actions rather than letting every unit assume
the same seed is available. Plant validation is atomic per crop: if the number
of `PLANT` requests for one crop exceeds its available seeds, all planting
requests for that crop become no-ops during that step.

### Water

```python
["WATER"]
```

Waters the plant on the current tile.

A tile's `watered_today` value becomes `True` after successful watering and
resets to `False` at the start of the next day.

### Harvest

```python
["HARVEST"]
```

Harvests the crop on the current tile and places the produce in that unit's
carried inventory.

Harvesting a one-time crop makes the tile empty. Harvesting an ongoing crop,
such as Strawberry, resets its `yield_units` to zero but leaves the plant on
the tile for later scheduled production.

### Dig

```python
["DIG"]
```

Clears a weed from the current tile.

After digging, the tile becomes empty and may be replanted later.

### Place

```python
["PLACE"]
```

At the shed-access tile, this transfers carried produce from the farmer's
backpack into the shed.

The current agent uses `(4, 4)` as its shed-access tile.

### Drop (observed in opponent replay, not used by our own agent)

```python
["DROP"]
```

Not currently emitted by `main.py` -- observed in a real opponent replay
(`docs/opponent_replay_trace.md`, days 4 and 5). Behaves inconsistently by
carried item type at a shed-access tile:

- Carrying only Wheat: the Wheat is deposited into the shed (shed count
  increases by the carried amount), same effective result as `PLACE`.
- Carrying Fertilizer (alone or mixed with another product): the Fertilizer
  is destroyed -- the unit's inventory empties but the shed's Fertilizer
  count does not increase. A `SELL FERTILIZER` order submitted the same
  step then has nothing to sell.

Confirmed directly from replay data (before/after inventory and shed
counts at a shed-access tile, three independent instances). Treat this as a
genuine game mechanic, not certainly a bug -- but Fertilizer specifically
needs `PLACE FERTILIZER` to actually reach the shed; `DROP` loses it.

## Market actions

Market orders are lists inside the `market` action list.

### Buy a seed

```python
["BUY_SEED", "MELON", 1]
```

Example:

```python
"market": [["BUY_SEED", "MELON", 1]]
```

### Sell produce

```python
["SELL", "MELON", 6]
```

Example:

```python
"market": [["SELL", "MELON", 6]]
```

Produce must be in the shed before it can be sold.

### Hire farm hands

```python
["HIRE"]
```

Hiring is submitted as a market order. Hire costs follow the Fibonacci-like
daily sequence:

```text
1, 1, 2, 3, 5, 8, 13, ...
```

The sequence resets each day. Therefore, the first two hands cost one coin
each, for a combined daily cost of two coins.

Because the roster is cleared and re-hired every night, an extra hand is a
**recurring daily cost, not a one-off**, and the marginal cost is the cost of
its own slot in the sequence -- not the cheap early slots. Running twelve hands
costs `1+1+2+3+5+8+13+21+34+55+89+144 = 376` per day, of which the twelfth
slot alone is 144/day (~2,700 across a season). A "hire one extra hand just for
setup" plan is therefore genuinely cheap (one or two days), while a permanent
extra hand must repay 144 every single day.

Local traces confirmed that submitting two `HIRE` orders produces two hands
and sets `hires_today` to `2`. Hands disappear at the next day boundary and
must be hired again. Any carried inventory is deposited into the shed during
the ordinary end-of-day transition.

Each active hand requires a corresponding entry in the returned `hands`
action list. When multiple hands use the same target-selection logic and work
area, they can move onto the same positions and submit duplicate actions.
Assigning non-overlapping work zones prevents this wasted work.

## Observation/action pairing in `env.steps` and replay files

`env.steps[i][player]["observation"]` is the state that resulted from
`env.steps[i][player]["action"]` -- that is, `action` at index `i` was chosen
using `observation` at index `i - 1`, and its effect is what `observation` at
index `i` shows. It is not an action about to be taken from the observation
shown at the same index.

Confirmed directly from a real match replay (`replays/110311259.json`,
local only) by checking farmer movement across consecutive hours: at hour
`h`, the farmer's recorded position already reflects the direction submitted
in `action[h]` (e.g. `action[h] == ["EAST"]` moves the position shown at
`observation[h]` one tile east of `observation[h-1]`'s position), not the
position the farmer was at when that action was chosen. The same pairing
was independently confirmed against a locally-run `main.py` trace via
`kaggle_environments`.

This matters for any tool or analysis that walks `env.steps` (a replay file,
a local `env.run()` trace, or the evaluation script's diagnostics) and wants
to say "the unit was at position P when it took action A" -- P is the
*previous* step's observation, not the current one's.

## Action processing order

Farmer and farm-hand actions are processed before market actions during a
step.

This has two important consequences:

1. A seed bought during a step cannot be planted by the farmer or a hand during
   that same step if no seed was already available.
2. Produce placed into the shed by a unit can be sold by a market order
   submitted during the same step.

For example:

```python
return {
    "farmer": ["PLACE"],
    "hands": [],
    "market": [["SELL", "MELON", backpack_melon]],
}
```

This can deposit and sell carried melons during the same step when the farmer
is at the shed-access tile.

### Order position within the market list

The position of an order inside the `market` list matters. The environment
processes the two players' market queues by list index. Orders at index zero
are considered before orders at index one, and so on.

Compatible buy and sell orders at the same index are processed in lockstep,
using the same pre-commit market inventory for the next unit. An extra order
near the start of only one player's list can therefore push that player's
sale to a later index. The opponent may then sell first, change the shared
inventory, and reduce the price received by the delayed seller.

Confirmed directly against the environment source: lockstep pairing at a
shared index continues one unit at a time only while both players still have
units remaining in their order at that index. Once the smaller order is
exhausted, the larger order's remaining units continue alone, still within
the same index, using whatever inventory state resulted from the earlier
paired units. A same-index sale of a much larger quantity than the opponent's
therefore only gets the shared, more favorable pre-commit pricing for the
portion matching the opponent's own quantity; the rest is no worse off than
selling alone at that point in the sequence. Conversely, a player whose
same-index order is markedly *smaller* than the opponent's effectively
shrinks the combined quantity absorbed by the shared market that step,
leaving the opponent's larger order to finish with less accumulated glut than
a matched (same-size) pairing would have caused. This was confirmed during a
Melon same-day-sale follow-up: delaying one of three Melon-selling hands past
the hour when two of them previously sold together broke a `40`-vs-`40`
same-index pairing into a `20`-vs-`40` pairing, and the opponent's matching
40-unit order gained a fixed, seed-independent amount from the lighter
shared glut, independent of what the delayed hand did with its own sale.

This was confirmed during the two-hand experiment. Placing both `HIRE` orders
before sales reduced the candidate's match score against Wheat v1 from the
neutral expectation to `0%`. Moving the second `HIRE` after all sales restored
the score to `50%`, with otherwise unchanged crop quantities.

It was confirmed again while adding Strawberry. Deriving the sale order from
the insertion order of `CROP_CONFIGS` placed the new Strawberry sale before
the established Wheat, Carrot, and Melon sales. This shifted the legacy sales
to later market indices and caused a large regression despite producing
similar quantities. Restoring an explicit, stable sale order fixed it:

```python
CROPS_MANAGED = (
    "WHEAT",
    "CARROT",
    "MELON",
    "STRAWBERRY",
)
```

Dictionary insertion order should therefore not implicitly determine market
priority. Adding a new crop must not silently reorder existing sales.

Time-sensitive sales should therefore remain early and aligned where
possible. Non-price-sensitive orders, such as an additional `HIRE`, can be
placed after sales because every order in the accepted market list is still
processed during the same game step.

## Inventory flow

Harvested produce moves through these locations:

```text
plant → backpack → shed → market sale → money
```

The farmer's carried inventory is stored in:

```python
private["inventories"][0]
```

The shed inventory is stored in:

```python
private["shed"]
```

For example:

```python
backpack_melon = private["inventories"][0].get("MELON", 0)
shed_melon = private["shed"].get("MELON", 0)
```

## End-of-day deposit

At an ordinary day boundary, carried produce is automatically transferred to
the shed.

For example:

```text
day 3, hour 23: backpack=3, shed=0
day 4, hour 0:  backpack=0, shed=3
```

It can then be sold through a market order.

The game ends immediately after the final step, so the normal next-day
automatic deposit does not occur after day `29`, hour `23`.

Therefore, produce remaining in the backpack or shed at the end of the match
does not contribute to final money. The agent must liquidate it before the
game ends.

On the final day, the number of usable actions remaining for liquidation is:

```python
usable_actions_remaining = 23 - obs["hour"]
```

The terminal observation at hour `23` therefore has zero usable actions
remaining. For example, at hour `19` there are four usable actions in which to
move, deposit, and sell.

Returning carried produce requires one movement action per tile of Manhattan
distance to the shed-access tile. It also requires one `PLACE` action for each
distinct crop type being carried.

## Cows and Milk

A cow occupies a pasture tile. Establishing one requires two actions on that
tile:

```python
["BUILD_PASTURE"]
["PLACE", "COW", 1]
```

The purchased cow first enters the shed and must be collected by the farmer:

```python
["PICKUP", "COW", quantity]
```

Multiple cows can be picked up together and then placed one at a time in their
pastures. A farmhand can likewise carry multiple animals and Wheat in the same
inventory, so a compact livestock route can prebuild pastures one day and batch
pickup, placement, and initial feeding on the following day.

An established cow requires two ordered care actions every day:

```text
FEED -> CARE
```

`FEED` consumes one Wheat carried by the farmer. Wheat can be collected from
the shed in a batch, so one `PICKUP` action can supply several cows. The farmer
must submit `FEED` before `CARE` for each cow. When Milk is available, collecting
it requires a third action on that pasture:

```python
["HARVEST"]
```

Consequently, each cow needs at least two on-pasture actions on an ordinary
day and three on a Milk-harvest day. Movement between pastures, collecting
Wheat, returning to the shed, and placing Milk are additional actions. Four
cows therefore need eight on-pasture actions every day before counting any
harvests or travel. Staggering cow start dates spreads their harvest actions
across different days.

Milk is carried in the farmer's inventory after harvest. The farmer must return
to the shed-access tile and deposit it explicitly:

```python
["PLACE", "MILK", quantity]
```

Because farmer actions are processed before market actions, a matching
`SELL MILK` order can sell that deposited Milk during the same step.

Local traces established the following unfertilized production schedule for a
cow started on day 0:

- The first harvest is six Milk on day 8.
- Later harvests produce three Milk every two days through day 28.
- The complete schedule produces 36 Milk.

Cows started on day 9 first produce six Milk on day 17, followed by three Milk
every two days through day 29, for 24 Milk each. The current staggered setup of
two day-0 cows and two day-9 cows can therefore produce:

```text
2 * 36 + 2 * 24 = 120 Milk
```

Cow actions must retain priority during final-day liquidation. A trace showed
that allowing crop liquidation to overwrite a pending `FEED` or `CARE` action
created a loop in which Wheat was repeatedly picked up, placed, and sold. The
two expansion cows then missed their last harvests, losing six Milk. The safe
priority rule is:

```python
if (
    cow_action is None
    and obs["day"] == FINAL_DAY
    and backpack_total > 0
    and (liquidation_is_urgent or harvest_is_done)
):
    ...
```

With this guard, all four cows completed their final care and harvest actions,
and evaluation returned to the expected 120 Milk sold with zero Milk leftover.

## Plants and watering

A plant tile is represented by a dictionary similar to:

```python
{
    "kind": "PLANT",
    "crop": "MELON",
    "planted_day": 0,
    "watered_today": True,
    "consecutive_unwatered": 0,
    "yield_units": 6,
    "max_lifespan_step": 264,
    "fertilized_until_day": -1,
}
```

Important fields:

| Field | Meaning |
|---|---|
| `kind` | Type of object occupying the tile |
| `crop` | Crop planted on the tile |
| `planted_day` | Day on which the crop was planted |
| `watered_today` | Whether it has been watered during the current day |
| `consecutive_unwatered` | Consecutive watering failures |
| `yield_units` | Produce currently available at harvest |
| `max_lifespan_step` | Step associated with crop lifespan |
| `fertilized_until_day` | Final day of any active fertilizer effect |

Crop age is calculated as:

```python
crop_age = obs["day"] - tile["planted_day"]
```

Regular watering increases or preserves the crop's useful harvest yield.

### One-time and ongoing crops

Wheat, Carrot, and Melon are one-time crops. Their harvest readiness can be
determined from crop age, and a successful harvest removes the plant.

Strawberry is an ongoing crop. Its scheduled production occurs at plant ages
`10`, `12`, `14`, and `16`. Each scheduled event produces one unit without
fertilizer, up to four units over the plant's productive life. Unharvested
units can accumulate on the tile.

For an ongoing crop, age alone does not prove that produce is currently
available: the plant may already have been harvested and be waiting for its
next scheduled production. Readiness should therefore use:

```python
tile.get("yield_units", 0) > 0
```

A successful Strawberry harvest collects the available units, resets
`yield_units` to zero, and leaves the plant in place. The plant must still be
watered regularly and eventually decays after its final production cycle.

## Weeds

A weed tile is represented as:

```python
{"kind": "WEED"}
```

Plants can turn into weeds after missed watering.

A newly planted crop must be watered on its planting day. Existing crops must
also be watered regularly; consecutive missed watering can turn them into
weeds.

Confirmed threshold: at each day boundary, a tile's `consecutive_unwatered`
counter increments if it was not watered that day, or resets to zero if it
was. The tile converts to `WEED` once that counter reaches 2 -- i.e. missing
watering on two consecutive days destroys the plant. A single missed day is
not fatal by itself. This is separate from a one-time crop's own lifespan
decay (see `max_lifespan_step` above), which destroys an unharvested crop that
overstays its harvest window regardless of watering.

Weeds are removed with:

```python
["DIG"]
```

The agent should scan managed tiles for weeds rather than assuming every
managed tile is either empty or planted.

## Crop values used by the agent

The current project has tested Wheat, Carrot, Melon, and Strawberry.

| Crop | Yield type | Seed cost | Agent harvest rule | Observed unfertilized yield |
|---|---|---:|---|---:|
| `WHEAT` | One-time | 10 | Age 4 days | 4 |
| `CARROT` | One-time | 20 | Age 3 days | 3 |
| `MELON` | One-time | 80 | Age 10 days | 6 |
| `STRAWBERRY` | Ongoing | 100 | `yield_units > 0` | 1 at ages 10, 12, 14, and 16 |

These harvest rules are strategy settings chosen from observed crop behavior.
They are not a rule that every crop must be harvested at one fixed age.

### Confirmed: one-time crops reach their configured `harvest_yield` one day
### after their configured `harvest_day`

Verified with isolated single-tile traces (one farmer, one tile, watered every
day, no other hands or opponent activity to confound the result) for Wheat,
Carrot, and Melon: a one-time crop's `yield_units` does not jump straight to
`harvest_yield` at `harvest_day`. It grows on a fixed per-crop curve and only
reaches the table's yield value the day *after* the table's harvest-day
value -- i.e. harvesting at the currently configured `harvest_day` delivers
exactly one unit less than `CROP_CONFIGS` assumes, for every one-time crop:

| Crop | Age at harvest via current `harvest_day` | Actual `yield_units` delivered | Assumed `harvest_yield` | Age `yield_units` actually reaches the assumed value |
|---|---:|---:|---:|---:|
| `WHEAT` | 4 | 3 | 4 | 5 |
| `CARROT` | 3 | 2 | 3 | 4 |
| `MELON` | 10 | 5 | 6 | 11 |

Observed Wheat growth curve (age -> `yield_units`, watered every day):
`1, 1, 2, 3, 4` for ages 1-5. Carrot: `1, 1, 2, 3` for ages 1-4. Melon holds
at `1` through age 6, then ramps `2, 3, 4, 5, 6` for ages 7-11. In all three
cases `yield_units` plateaus at the assumed `harvest_yield` once reached (it
does not keep growing), and an unharvested tile still decays once it passes
its `max_lifespan_step`, separately from this yield curve.

This means `crop_profit_per_day()` currently overstates every one-time
crop's profitability (it divides `harvest_yield` by `harvest_day`, but the
agent's own `crop_is_harvestable()` gate lets hands harvest at `harvest_day`,
one day before that yield is actually available), and every one-time-crop
harvest across a full game is one unit short of what the formula assumes.
Not yet investigated: whether Strawberry's periodic `yield_units > 0` harvest
timing (ages 10, 12, 14, 16) has an equivalent one-day discrepancy, and
whether fertilizer changes the growth curve's shape rather than just its
final value.

Despite being a confirmed, verified mechanic, three attempts to act on it
were all tried and rejected -- see `docs/experiment-log.md`. Waiting the
extra day for the full assumed yield is not free: for Wheat and Carrot it
narrows the profit-per-day gap between them enough to destabilize which one
`choose_crop_for_planting()` treats as the default staple, and for Melon it
delays the harvest day past the point where the existing early-return-trip
mechanism (`MELON_HARVEST_DAY`) can still beat the opponent to market with
the first sale, losing more to a lower realized price than the extra unit
is worth. This mechanic is real but is not, by itself, an actionable fix.

For a one-time crop, the latest planting day is calculated as:

```python
LAST_PLANTING_DAY = FINAL_DAY - CROP_HARVEST_DAY
```

This prevents the agent from buying and planting crops that cannot mature
before the game ends.

For Strawberry, the current strategy requires enough time for its complete
four-production cycle:

```python
STRAWBERRY_LAST_FULL_CYCLE_DAY = FINAL_DAY - 16
```

With `FINAL_DAY = 29`, this permits new Strawberry plants only through day
`13`. This is a strategy choice rather than a legality rule: a later planting
could produce some fruit, but not all four scheduled yields.

## Shops and demand signals

Unlocked shops are available through:

```python
obs["town"]["unlocked_shops"]
```

The list can contain the same shop type more than once. Each entry represents
a separate unlocked shop, so demand-sensitive logic must count matching list
entries rather than converting the list to a set or checking only whether a
name is present. For example:

```python
yarn_store_count = sum(
    shop == "YARN_STORE"
    for shop in obs["town"]["unlocked_shops"]
)
```

Local traces include seeds with two Yarn Stores and seeds with multiple
Milk-demand shops of the same type.

## Shared market

The market is shared by both players.

Market prices and inventory can change during the match, so the value of a
crop depends partly on both agents' behavior.

Strawberry has a base sale price of `120`, but its glut side is highly price
sensitive: the environment uses a threshold of only `100` units and a linear
price curve. As with Melon, producing more Strawberry units does not guarantee
more money if both players saturate the shared market.

Experiments confirmed that when both players sell melons, average melon-agent
earnings are substantially lower than when the melon agent plays against a
carrot agent.

This makes opponent behavior and crop competition strategically important.

## Illegal actions

Some invalid farmer actions behave like silent no-ops instead of raising an
obvious Python error.

Examples include attempting to:

- Plant without a seed
- Plant on an occupied tile
- Water an empty tile
- Harvest an immature or invalid tile
- Move outside an allowed area

A match completing without an exception does not prove every submitted action
was legal. Local traces should confirm that the intended state change occurred.

## Verified endgame requirements

Before the final step, the agent should:

- Stop buying seeds that cannot produce a mature crop
- Stop planting crops that cannot mature
- Harvest remaining mature crops
- Return carried produce to the shed-access tile
- Use `PLACE` to deposit carried produce
- Sell all produce remaining in the shed
- Finish with zero carried produce and zero shed produce

The agent should compare its remaining action budget with the work needed to
liquidate:

```python
actions_needed_to_liquidate = (
    distance_to_shed
    + number_of_carried_crop_types
)
```

When the remaining usable actions are less than or equal to this requirement,
liquidation must take priority over watering or harvesting additional crops.

The evaluation script records final carried and shed quantities to detect
failed liquidation.

## Confirmed: neglected livestock are unplaced overnight

Verified while root-causing a "tiles get destroyed" bug reported during an
early-Cow-expansion experiment (see `docs/experiment-log.md`). An animal
tile has `fed_today`/`cared_today` booleans that reset to `False` at the
start of each day, same as a crop tile's `watered_today`. If an animal goes
the entire day with `fed_today == False` (i.e. it is never fed even once
that day), the game engine appears to unplace it overnight: the tile keeps
its `PASTURE`/`COOP` `kind`, but `animal` reverts to `None`. This applies to
every animal on the farm simultaneously if none of them got fed that day --
not a per-animal independent check tied to some other condition.

Confirmed with a real trace (docs/experiment-log.md's "Early NW Cow
expansion" iteration 3/6): on a day where an agent variant's Wheat-feed
purchase failed for the entire day (see below), every tracked animal --
2 original Cows, 3 Sheep, 2 newly added Cows, 7 in total -- showed
`fed_today=False, cared_today=False` at hour 23, and several of them (not
all -- the exact selection was not further isolated) showed `animal: None`
at hour 0 the next day.

This means the actual failure mode in that experiment was not a bug in the
shared `active_animal_plan`/`choose_setup_action` tracking logic (as
originally suspected) -- it was starving Wheat feed for an entire day by
overspending on new Cow purchases the same day, given `BUY_ANIMAL` runs
before the Wheat-feed-reserve calculation in section "3.6" and both draw
from the same day's `money_available`. Adding more animals at once (a large
combined purchase cost) can crowd out that same day's Wheat purchase for
*every* animal already on the farm, not just the new ones, triggering this
neglect mechanic across the board.

## Confirmed: the servicing unit determines when produce reaches the market

An animal's product is sold from the shed, so whoever services the animal sets
the hour its output becomes sellable. Adding one extra animal to the *farmer's*
daily round pushed its Cow-milk collection and shed deposit from hour ~15 to
hour ~21 on every single day of the game -- the same days, the same quantities,
six to seven hours later.

That is not a rounding detail. Prices move with shared market inventory during
the day, so on a glutted product the later fill is materially worse:

```text
MILK sale prices, same days, same quantities, identical volume (126 each):
  farmer carrying an extra animal:  129, 108,  99, 103, 68, 57, 47, 36, 26, 15,  5, 1 ...
  farmer round left untouched:      154, 120, 108, 112, 89, 66, 55, 45, 34, 24, 13, 3 ...
```

Cost: -2,554 on Milk+Wool on one seed, at equal or greater volume. Moving the
extra animal to a hand restored the baseline hours and made Milk revenue match
exactly.

Rule of thumb: treat the farmer's animal round as a latency-critical path.
Prefer giving a new animal to a hand, and when measuring any change that could
shift service order, compare sale *hours*, not just totals.

## Confirmed: hand inventories are banked free at every day boundary

`_drop_inventories_to_shed` empties every hand inventory into the shed at each
day boundary (overflow beyond `shedCapacity`, default 100, is discarded), and
`_inv_add` imposes no per-hand carry limit. Carrying produce costs nothing and
risks nothing as long as the day's accumulation stays under the shed cap.

Walking to the shed to deposit therefore buys only one thing: selling a day
earlier. That is worth doing for a steeply glutted product such as Milk, and
not worth doing for a flat one such as Egg. Holding Eggs until the overnight
drop -- placing them only when the round already ends at the shed -- cost zero
Eggs sold and freed enough actions to be worth +1,588 across two seeds.

Corollary for multi-animal hands: fetch feed in one batch sized to the number
of unfed animals the hand owns. A hardcoded single-unit `PICKUP` forces one
shed round-trip per animal; a hand with two Geese made 88 shed arrivals against
a four-Sheep hand's 22.

## Confirmed: the intraday Milk curve peaks at midday and collapses on the day's supply

Milk's price climbs through the morning, peaks around hour 13--14, and falls in
the hour the day's supply reaches the market. Seed 1, day 10, one round:

| h00 | h06 | h12 | h13 | h14 | h15 | h18 | h23 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 187 | 191 | 193 | 194 | 194 | 175 | 177 | 179 |

The hour-15 fall is the sale itself: neither agent had sold Milk earlier that
day. The size of the fall tracks the volume dumped -- 12 units cost about 19,
while a 24-unit dump at hour 23 cost about 59. This extends "the servicing unit
determines when produce reaches the market" from a between-days effect to a
within-day one.

Corollary: the farmer's round already crosses shed access on most production
days -- on day 10 he harvests at `(4,4)`, itself a shed-access tile, at hour 04
and reaches `(5,4)` at hour 12 -- so an opportunistic early deposit costs one
`PLACE` action and no travel. Depositing and selling can be split without
costing an extra turn, because section 3.4's shed seller moves whatever the
shed holds on the following turn.

When the split is evaluated matters. Firing the deposit *before* servicing an
animal that is standing on a shed-access tile is what captures the h13--h14
peak; on day 15 the second Milk deposit lands at `(5,4)` at h13--h14, so a
deposit evaluated after servicing still sells into the h15 collapse.

## Confirmed: an ongoing crop's yield count is fixed by `last_production_day`, not by how early it is planted

Ongoing crops (TOMATO, STRAWBERRY) produce on a schedule measured in *growth
days*: the first yield lands at `harvest_day`, then every `interval` days, and
production stops after `last_production_day`. The number of cycles a plant
delivers is therefore a property of the crop, not of its planting date.

    STRAWBERRY  harvest_day 10  interval 2  last_production_day 16
                -> growth days 10, 12, 14, 16 = four yields

    planted day 10 -> yields on days 20, 22, 24, 26
    planted day 11 -> yields on days 21, 23, 25, 27

Four either way. **Pulling an ongoing-crop planting forward by one day buys no
extra yield cycle.** It only moves each sale one day earlier, which is worth
something against a declining price curve and nothing else.

The practical rule: before spending actions, hands or coins to plant an
ongoing crop earlier, divide the days remaining before `FINAL_DAY` by
`interval` and compare against `last_production_day`. If the plant already
reaches its last production day inside the season, an earlier planting adds
no production.

Two experiments have now been built and rejected against this arithmetic: the
permanent goose at `(4,2)` and the melon-harvest-day relief hire. Both were
answerable from the crop table before any code was written.

One-shot crops (WHEAT, CARROT, MELON) behave differently -- see the
`harvest_yield` section above -- because each watered day inside their window
converts to yield, so for them the planting date does move the total.

## Confirmed: which shop unlocks depends on how many tiles are empty on BOTH farms

The shop sequence is not fixed per seed. At each day boundary the engine does,
in order (`kaggriculture.py`, day-end block):

    rng = random.Random((seed * 1_000_003) ^ day)
    for each farm (player 0, then player 1):
        _daily_refresh_plants(...)
        _spawn_weeds(farm, ..., rng)     # one rng.random() per EMPTY tile
        ...
    if (day + 1) % townShopUnlockInterval == 0:        # every 3rd day
        town["unlocked_shops"].append(rng.choice(sorted(SHOPS)))

Weed spawning and the shop draw share one RNG, and weed spawning consumes one
draw per empty tile on each farm. So the shop that unlocks on days 3, 6, 9,
12, ... is a function of the total number of empty tiles on both farms at the
end of the previous day. Change that count by one and a different shop can
unlock -- for both players.

Evidence, seed 15, NE Goose layout experiment vs the baseline mirror:

| unlock | empty tiles (ours+opp) | shop, candidate | shop, baseline mirror |
|---|---|---|---|
| after d17 | 8+7 vs 7+7 | BAKERY | FARMERS_MARKET |

and the sequence diverged from day 12 on (candidate: PET_CAFE, BAKERY,
SMOOTHIE_SHOP; baseline: SMOOTHIE_SHOP, FARMERS_MARKET, ICE_CREAM_SHOP). Losing
three Milk/Strawberry demand shops took BOTH players from ~118,000 to
80,000-83,000, with Milk selling at 70-80 by day 22.

What this means in practice:

- **Single-seed deltas after about day 11 carry a town-lottery term.** Any
  change that alters the empty-tile count at an unlock boundary can re-roll
  the rest of the shop sequence. A seed that swings by thousands on a small
  change may be measuring the town, not the change. Check the unlock sequence
  (`town.unlocked_shops` over time) before attributing a large single-seed
  swing to the strategy.
- The first two shops (days 3 and 6) are usually stable, because both farms
  are nearly identical that early. `tools/trace.py shops` only reports those
  two, so it will not show a divergence that starts later.
- It is potentially steerable. Both farms' tiles are visible, so at hour 23 on
  an unlock day an agent could evaluate which shop each achievable empty count
  would produce. Untested: a naive replay from the hour-23 observation
  mispredicted 3 of 7 unlocks on seed 15, because the plant refresh and the
  final hour's actions change the count after that observation.

## Confirmed: an ongoing crop's Fertilizer bonus is decided on the production night, and needs that day watered

From `_daily_refresh_plants`, on the night of each production day only:

    fertilized = was_watered and tile["fertilized_until_day"] >= current_day
    tile["yield_units"] += (2 if fertilized else 1)

and from the FERTILIZE action:

    tile["fertilized_until_day"] = max(..., day + 2)   # active day, day+1, day+2

So, for Strawberry (production nights at plant ages 9, 11, 13 and 15; the
units appear the next morning at ages 10, 12, 14 and 16):

- **The production day must be watered** or the bonus is lost -- Fertilizer
  applied to a dry production day is simply wasted, and the night yields the
  normal +1.
- **Fertilizer applied on the off day before a production day** covers that
  production night (`day + 1 <= day + 2`), and can replace that off day's
  watering: a plant watered the day before survives one dry day. This is free
  in actions and costs one Fertilizer per bonus unit.
- **Fertilizer applied on a production day** (with its watering) covers that
  night and the next production night two days later -- two bonus units per
  Fertilizer, but one extra action. This is what the older
  `fertilizer_bonus_units` pass does at ages 9 and 13.
- Watering an ongoing crop on an off day has no effect on yield. It only
  resets the dry-day counter.
- The yield itself does not depend on watering at all. A dry production day
  still yields +1; only the bonus needs the water.
- HARVEST does not require the tile to be watered that day.

## Confirmed: player position is not always symmetric

Two identical agents do not always score identically. Seed 16, the frozen
baseline `offday_fertilize_ne12_v1` playing itself: **122,522 in position 0,
122,596 in position 1**, reproducibly. Mirrored gate lines have also started
to disagree across positions (seed 11: 78,875 vs 78,817 for the same pairing).
Seed 9, `ne_strawberry_fill_v1` playing itself: **132,407 vs 131,727**, the
two players' actions first diverging at d11 h03 (hand 3, WEST vs EAST).
`tools/trace.py isolation` now compares against this self-play result rather
than against the other player in the same game.

Earlier entries (experiment log, "the environment carries no first-mover
asymmetry"; roadmap line on 40 games being 20 independent seeds) generalised
from seeds where the two positions happened to tie. They are not a rule. The
likely source is order of resolution when both players act on the shared
market or town in the same turn, which only matters once the two agents'
orders overlap.

In practice:

- `tools/trace.py isolation` will flag seed 16 as changed even for a candidate
  identical to the baseline. Check a flagged seed against the baseline's own
  self-play before blaming the change.
- The two positions of a mirrored gate are usually, but not always, the same
  sample. The difference is small next to a strategy's effect (74 here).

## Confirmed: how the market drains, and the $1 floor

From `kaggriculture.py` (`_town_consume` and the SELL branch):

- Every 4 steps (6 times a day), each unlocked shop instance removes 1 unit
  of every product it lists, or 2 if it lists only one product (Pet Cafe,
  Yarn Store). A shop drawn twice consumes twice.
- Once a day, the town centre removes 1 unit of every product except
  Fertilizer.
- A sale at price 1 does **not** add to market inventory.

| Shop | Products |
|---|---|
| BAKERY | Egg, Wheat |
| PIZZA_SHOP | Milk, Tomato, Wheat |
| BRUNCH_SPOT | Egg, Wheat, Strawberry |
| YARN_STORE | Wool (x2) |
| ICE_CREAM_SHOP | Strawberry, Milk, Wheat |
| PET_CAFE | Carrot (x2) |
| SMOOTHIE_SHOP | Strawberry, Milk |
| FARMERS_MARKET | Wheat, Carrot, Tomato, Strawberry |

So Strawberry absorbs `1 + 6 x (Strawberry shops)` units a day and nothing
else drains it. Seed 1 (`ne_strawberry_fill_v1` self-play) opens its first
Strawberry shop on day 15 and absorbs ~180 units over the season against 416
sold by the two players; Strawberry averaged 25.6.

The floor matters for any argument that our volume "denies" the opponent a
price. Seed 1, day 22: both players sold 55 at h00, market inventory rose
only 31 (10,028 -> 10,059), so ~79 of the 110 units sold for 1 coin. A unit
sold at the floor earns nothing and moves the opponent's price not at all.

An undersupplied market pays little more for the staples. At a shortfall of
`T` units (the curve's scale) the price is `base x (1 + below_target)`:
Carrot 42, Wheat 45, Tomato 84, Strawberry 204. Carrot (log) and Wheat (sqrt)
climb very slowly past that -- Carrot is still only ~45 at a 10,000-unit
shortfall -- so a Pet-Cafe-heavy town absorbing hundreds of Carrots does not
make Carrot a premium crop.
