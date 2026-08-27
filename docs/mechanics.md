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

Harvests the crop on the current tile and places the produce in the farmer's
carried inventory.

The harvested tile becomes empty.

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

Local traces confirmed that submitting two `HIRE` orders produces two hands
and sets `hires_today` to `2`. Hands disappear at the next day boundary and
must be hired again. Any carried inventory is deposited into the shed during
the ordinary end-of-day transition.

Each active hand requires a corresponding entry in the returned `hands`
action list. When multiple hands use the same target-selection logic and work
area, they can move onto the same positions and submit duplicate actions.
Assigning non-overlapping work zones prevents this wasted work.

## Action processing order

Farmer actions are processed before market actions during a step.

This has two important consequences:

1. A seed bought during a step cannot be planted by the farmer during that same
   step if no seed was already available.
2. Produce placed into the shed by the farmer can be sold by a market order
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

This was confirmed during the two-hand experiment. Placing both `HIRE` orders
before sales reduced the candidate's match score against Wheat v1 from the
neutral expectation to `0%`. Moving the second `HIRE` after all sales restored
the score to `50%`, with otherwise unchanged crop quantities.

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

## Weeds

A weed tile is represented as:

```python
{"kind": "WEED"}
```

Plants can turn into weeds after missed watering.

A newly planted crop must be watered on its planting day. Existing crops must
also be watered regularly; consecutive missed watering can turn them into
weeds.

Weeds are removed with:

```python
["DIG"]
```

The agent should scan managed tiles for weeds rather than assuming every
managed tile is either empty or planted.

## Crop values used by the agent

The current project has tested wheat, carrots, and melons.

| Crop | Seed cost | Agent harvest age | Observed unfertilized yield |
|---|---:|---:|---:|
| `WHEAT` | 10 | 4 days | 4 |
| `CARROT` | 20 | 3 days | 3 |
| `MELON` | 80 | 10 days | 6 |

These harvest ages are strategy settings chosen from observed crop behavior.
They are not a rule that every crop must be harvested at that age.

The latest planting day is calculated as:

```python
LAST_PLANTING_DAY = FINAL_DAY - CROP_HARVEST_DAY
```

This prevents the agent from buying and planting crops that cannot mature
before the game ends.

## Shared market

The market is shared by both players.

Market prices and inventory can change during the match, so the value of a
crop depends partly on both agents' behavior.

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
