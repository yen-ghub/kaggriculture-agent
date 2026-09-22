"""Diagnostic: when does MILK reach the market, and at what price?

Prints the intraday MILK price curve, every MILK sale (ours and the
opponent's), and how long the farmer actually carries collected milk
before depositing it.  Read-only; changes no agent behaviour.
"""

from kaggle_environments import make

from main import agent
from baselines.locked_sw_livestock_v1 import agent as opponent_agent

SEED = 1
PRICE_SAMPLE_HOURS = tuple(range(24))
ACTION_SAMPLE_DAYS = (10, 15)


def sell_orders(action, product):
    if not action:
        return []

    return [
        order
        for order in action.get("market", [])
        if len(order) >= 3
        and order[0] == "SELL"
        and order[1] == product
    ]


def farmer_placed(action, product):
    if not action:
        return 0

    farmer_action = action.get("farmer", [])

    if farmer_action[:2] == ["PLACE", product]:
        return farmer_action[2]

    return 0


env = make(
    "kaggriculture",
    configuration={
        "episodeSteps": 720,
        "seed": SEED,
    },
    debug=False,
)

env.run([agent, opponent_agent])

price_rows = {}
carry_by_day = {}
deposit_by_day = {}
events = []
action_rows = {}

for step in env.steps:
    our_state = step[0]
    opponent_state = step[1]

    if our_state.action is None or opponent_state.action is None:
        continue

    obs = our_state.observation

    if obs.hour in PRICE_SAMPLE_HOURS:
        price_rows.setdefault(obs.day, {})[obs.hour] = (
            obs.market.prices["MILK"],
            obs.market.inventory["MILK"],
        )

    carried = obs.private.inventories[0].get("MILK", 0)

    if carried > 0:
        carry_by_day.setdefault(obs.day, []).append((obs.hour, carried))

    placed = farmer_placed(our_state.action, "MILK")
    our_sales = sell_orders(our_state.action, "MILK")
    opponent_sales = sell_orders(opponent_state.action, "MILK")

    if placed:
        deposit_by_day.setdefault(obs.day, []).append((obs.hour, placed))

    if obs.day in ACTION_SAMPLE_DAYS:
        action_rows.setdefault(obs.day, []).append((
            obs.hour,
            tuple(obs.farms[0]["farmer"]),
            our_state.action.get("farmer", []),
            carried,
            obs.private.shed.get("MILK", 0),
        ))

    if placed or our_sales or opponent_sales:
        events.append((
            obs.day,
            obs.hour,
            placed,
            carried,
            obs.private.shed.get("MILK", 0),
            our_sales,
            obs.market.prices["MILK"],
            opponent_sales,
        ))

print(f"seed={SEED}, opponent=locked_sw_livestock_v1, position=0")
print(
    f"final rewards: ours={env.steps[-1][0].reward:.1f}, "
    f"opponent={env.steps[-1][1].reward:.1f}"
)
print()

print("=== MILK price by hour (grid; h00..h23) ===")
print("day |" + "".join(f"{hour:6d}" for hour in PRICE_SAMPLE_HOURS))

for day in sorted(price_rows):
    cells = []

    for hour in PRICE_SAMPLE_HOURS:
        entry = price_rows[day].get(hour)
        cells.append("     -" if entry is None else f"{entry[0]:6d}")

    print(f"{day:3d} |" + "".join(cells))

print()
print("=== MILK events (day hour | placed carried shed | our_sell | price | opp_sell) ===")

for event in events:
    day, hour, placed, carried, shed, our_sales, price, opponent_sales = event
    print(
        f"{day:3d} {hour:3d} | "
        f"{placed:6d} {carried:7d} {shed:4d} | "
        f"{str(our_sales):24s} | "
        f"p={price:3d} | "
        f"{opponent_sales}"
    )

print()
print("=== Farmer hourly actions on sample days ===")

for day in sorted(action_rows):
    print(f"-- day {day} (pos / action / carried) --")

    for hour, position, action, carried, shed in action_rows[day]:
        print(
            f"  h{hour:02d} {str(position):8s} "
            f"{str(action):32s} carried={carried:3d} shed={shed:3d}"
        )

print()
print("=== Farmer carry span per day (hours with MILK in backpack) ===")

for day in sorted(set(carry_by_day) | set(deposit_by_day)):
    spans = carry_by_day.get(day, [])

    if spans:
        span_text = (
            f"h{spans[0][0]:02d}-h{spans[-1][0]:02d} "
            f"over {len(spans):2d}h, max {max(c for _, c in spans):3d}"
        )
    else:
        span_text = "none"

    print(
        f"day {day:3d}: {span_text:34s} "
        f"deposits {deposit_by_day.get(day, [])}"
    )
