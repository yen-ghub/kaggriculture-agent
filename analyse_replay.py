import json
from collections import Counter, defaultdict
from pathlib import Path


path = Path("replays/106651909.json")
data = json.loads(path.read_text(encoding="utf-8"))
steps = data["steps"]

print("agents", [a["Name"] for a in data["info"]["Agents"]])
print("seed", data["info"]["seed"], "rewards", data["rewards"], "steps", len(steps))


def tile_counts(tiles):
    counts = Counter()
    crop_yield = Counter()
    animal_state = Counter()
    for row in tiles:
        for tile in row:
            if tile is None:
                counts["EMPTY"] += 1
            elif tile == "LOCKED":
                counts["LOCKED"] += 1
            elif isinstance(tile, dict):
                kind = tile.get("kind", "?")
                if kind == "PLANT":
                    crop = tile.get("crop", "?")
                    counts[f"PLANT:{crop}"] += 1
                    crop_yield[crop] += tile.get("yield_units", 0)
                elif kind in ("PASTURE", "COOP"):
                    animal = tile.get("animal", "?")
                    counts[f"ANIMAL:{animal}"] += 1
                    animal_state[(animal, "fed")] += int(bool(tile.get("fed_today")))
                    animal_state[(animal, "cared")] += int(bool(tile.get("cared_today")))
                    animal_state[(animal, "yield")] += tile.get("yield_units", 0)
                else:
                    counts[kind] += 1
    return counts, crop_yield, animal_state


for player in (0, 1):
    farmer_ops = Counter()
    hand_ops = Counter()
    market_ops = Counter()
    sales = Counter()
    buys = Counter()
    daily_sales = defaultdict(Counter)
    daily_farmer = defaultdict(Counter)
    daily_hands = defaultdict(Counter)
    daily_market = defaultdict(list)

    for records in steps:
        rec = records[player]
        obs = rec.get("observation") or {}
        day = obs.get("day", -1)
        action = rec.get("action") or {}
        farmer = action.get("farmer") or ["PASS"]
        farmer_ops[farmer[0]] += 1
        daily_farmer[day][farmer[0]] += 1
        for h in action.get("hands") or []:
            hand_ops[h[0]] += 1
            daily_hands[day][h[0]] += 1
        for order in action.get("market") or []:
            market_ops[order[0]] += 1
            daily_market[day].append(order)
            if order[0] == "SELL":
                sales[order[1]] += order[2]
                daily_sales[day][order[1]] += order[2]
            elif order[0].startswith("BUY"):
                item = order[1] if len(order) > 1 else order[0]
                qty = order[2] if len(order) > 2 else 1
                buys[(order[0], item)] += qty

    print("\nPLAYER", player)
    print("farmer_ops", dict(farmer_ops))
    print("hand_ops", dict(hand_ops))
    print("market_ops", dict(market_ops))
    print("sales", dict(sales))
    print("buys", dict(buys))

    for day in range(30):
        day_records = [r[player] for r in steps if (r[player].get("observation") or {}).get("day") == day]
        if not day_records:
            continue
        rec = day_records[-1]
        obs = rec["observation"]
        farm = obs["farms"][player]
        counts, crop_yield, animal_state = tile_counts(farm["tiles"])
        private = obs.get("private", {})
        crops = {k.split(":", 1)[1]: v for k, v in counts.items() if k.startswith("PLANT:")}
        animals = {k.split(":", 1)[1]: v for k, v in counts.items() if k.startswith("ANIMAL:")}
        if day in (0, 2, 3, 4, 5, 6, 8, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 29):
            print(
                f"D{day:02d} money={farm['money']:8.0f} hands={len(farm['hands']):2d} "
                f"lands={','.join(farm['unlocked_quadrants'])} weeds={counts['WEED']:2d} "
                f"crops={crops} animals={animals} shed={private.get('shed', {})} "
                f"sales={dict(daily_sales[day])}"
            )

    print("daily action summary days 10+")
    for day in range(10, 30):
        print(
            f"D{day:02d} farmer={dict(daily_farmer[day])} "
            f"hands={dict(daily_hands[day])} sales={dict(daily_sales[day])}"
        )


print("\nDAILY MONEY AND SHOPS")
for day in range(30):
    matching = [records for records in steps if records[0]["observation"]["day"] == day]
    records = matching[-1]
    obs = records[0]["observation"]
    farms = obs["farms"]
    print(
        f"D{day:02d} p0={farms[0]['money']:8.0f} p1={farms[1]['money']:8.0f} "
        f"gap={farms[0]['money'] - farms[1]['money']:8.0f} shops={obs['town']['unlocked_shops']}"
    )


print("\nMELON TIMELINE DAYS 9-12")
previous_money = [3000.0, 3000.0]
for step_index, records in enumerate(steps):
    obs0 = records[0]["observation"]
    day = obs0["day"]
    for player in (0, 1):
        money = records[player]["observation"]["farms"][player]["money"]
        action = records[player].get("action") or {}
        farmer = action.get("farmer") or ["PASS"]
        hands = action.get("hands") or []
        market = action.get("market") or []
        interesting = (
            9 <= day <= 12
            and (
                any(order[:2] == ["SELL", "MELON"] for order in market)
                or farmer[0] == "HARVEST"
                or any(hand[0] == "HARVEST" for hand in hands)
            )
        )
        if interesting:
            print(
                f"step={step_index:3d} D{day:02d}H{obs0['hour']:02d} p{player} "
                f"money={money:8.0f} dm={money - previous_money[player]:7.0f} "
                f"melon_price={obs0['market']['prices']['MELON']:3d} "
                f"melon_inv={obs0['market']['inventory']['MELON']:5d} "
                f"farmer={farmer} hand_harvests={sum(h[0] == 'HARVEST' for h in hands)} "
                f"market={market}"
            )
        previous_money[player] = money


import math

MARKET_I0 = 10000
MARKET_PARAMS = {
    "WHEAT":      {"base": 25,  "I0": MARKET_I0, "T": 400, "below_func": "sqrt", "below_target": .80, "above_func": "log", "above_target": .20},
    "CARROT":     {"base": 35,  "I0": MARKET_I0, "T": 450, "below_func": "log", "below_target": .20, "above_func": "sqrt", "above_target": .70},
    "TOMATO":     {"base": 60,  "I0": MARKET_I0, "T": 200, "below_func": "linear", "below_target": .40, "above_func": "sqrt", "above_target": .60},
    "STRAWBERRY": {"base": 120, "I0": MARKET_I0, "T": 100, "below_func": "sqrt", "below_target": .70, "above_func": "linear", "above_target": 1.60},
    "MELON":      {"base": 250, "I0": MARKET_I0, "T": 300, "below_func": "log", "below_target": .20, "above_func": "sq", "above_target": 3.60},
    "EGG":        {"base": 50,  "I0": MARKET_I0, "T": 332, "below_func": "linear", "below_target": .40, "above_func": "log", "above_target": .20},
    "MILK":       {"base": 160, "I0": MARKET_I0, "T": 122, "below_func": "sqrt", "below_target": .60, "above_func": "linear", "above_target": 1.60},
    "WOOL":       {"base": 200, "I0": MARKET_I0, "T": 105, "below_func": "log", "below_target": .20, "above_func": "sq", "above_target": 3.20},
    "FERTILIZER": {"base": 100, "I0": MARKET_I0, "T": 200, "below_func": "linear", "below_target": .40, "above_func": "linear", "above_target": .40},
}


def shape(name, value):
    value = max(0.0, value)
    return {
        "linear": lambda x: x,
        "sq": lambda x: x * x,
        "sqrt": math.sqrt,
        "log": lambda x: math.log(1 + x),
    }[name](value)


def market_price(item, inventory):
    p = MARKET_PARAMS[item]
    delta = inventory - p["I0"]
    if delta < 0:
        func, target, sign = p["below_func"], p["below_target"], 1
    else:
        func, target, sign = p["above_func"], p["above_target"], -1
    denominator = shape(func, p["T"])
    amp = target * p["base"] / denominator if denominator else 0
    return max(1, round(p["base"] + sign * amp * shape(func, abs(delta))))


sale_revenue = [Counter(), Counter()]
purchase_cost = [Counter(), Counter()]
for step_index in range(1, len(steps)):
    inventory = dict(steps[step_index - 1][0]["observation"]["market"]["inventory"])
    queues = []
    for player in (0, 1):
        action = steps[step_index][player].get("action") or {}
        queues.append((action.get("market") or [])[:10])
    for order_index in range(max(map(len, queues), default=0)):
        states = []
        for player in (0, 1):
            if order_index >= len(queues[player]):
                states.append(None)
                continue
            order = queues[player][order_index]
            if order and order[0] in ("SELL", "BUY_PRODUCT") and len(order) >= 3:
                states.append([order[0], order[1], int(order[2])])
            else:
                states.append(None)
        while any(state and state[2] > 0 for state in states):
            quoted = []
            for state in states:
                if not state or state[2] <= 0:
                    quoted.append(None)
                elif state[0] == "SELL":
                    quoted.append(market_price(state[1], inventory[state[1]]))
                else:
                    quoted.append(market_price(state[1], inventory[state[1]] - 1))
            for player, state in enumerate(states):
                if not state or state[2] <= 0:
                    continue
                op, item, _ = state
                price = quoted[player]
                if op == "SELL":
                    sale_revenue[player][item] += price
                    if price > 1:
                        inventory[item] += 1
                else:
                    purchase_cost[player][item] += price
                    inventory[item] -= 1
                state[2] -= 1

print("\nAPPROX MARKET REVENUE ATTRIBUTION")
for player in (0, 1):
    print(
        "p", player,
        "sales", dict(sale_revenue[player]),
        "sale_total", sum(sale_revenue[player].values()),
        "product_buys", dict(purchase_cost[player]),
        "buy_total", sum(purchase_cost[player].values()),
    )
