from kaggle_environments import make
import main
from main import agent
# from baselines.delayed_sheep_v1 import agent as baseline_agent
from baselines.low_strawberry_test import agent as baseline_agent


def count_plants(farm, crop):
    count = 0

    for row in farm["tiles"]:
        for tile in row:
            if (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and tile.get("crop") == crop
            ):
                count += 1

    return count

env = make(
    "kaggriculture",
    configuration={
        "episodeSteps": 720,
        "seed": 1,
    },
    debug=False,
)

env.run([agent, baseline_agent])

for step in env.steps:
    our_state = step[0]
    opponent_state = step[1]
    obs = our_state.observation
    
    if (
        our_state.action is None
        or opponent_state.action is None
    ):
        continue
    
    our_strawberry_sales = [
        order
        for order in our_state.action["market"]
        if (
            order[0] == "SELL"
            and order[1] == "STRAWBERRY"
        )
    ]

    opponent_strawberry_sales = [
        order
        for order in opponent_state.action["market"]
        if (
            order[0] == "SELL"
            and order[1] == "STRAWBERRY"
        )
    ]

    if (
        obs.day >= 18
        and (
            obs.hour in (0, 1, 23)
            and (our_strawberry_sales or opponent_strawberry_sales)
        )
    ):
        print(
            f"day={obs.day:2}, "
            f"hour={obs.hour:2}, "
            f"price={obs.market.prices['STRAWBERRY']:3}, "
            f"market_inventory="
            f"{obs.market.inventory['STRAWBERRY']:5}, "
            f"our_shed="
            f"{obs.private.shed.get('STRAWBERRY', 0):3}, "
            f"our_money={obs.farms[0].money:8.1f}, "
            f"our_sales={our_strawberry_sales}, "
            f"opponent_sales={opponent_strawberry_sales}"
        )