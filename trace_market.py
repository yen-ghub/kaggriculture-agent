from kaggle_environments import make

from main import agent
from baselines.adaptive_v1 import agent as baseline_agent


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
    observation = step[0].observation

    if observation.hour != 0:
        continue

    prices = observation.market.prices
    inventory = observation.market.inventory

    our_farm = observation.farms[0]
    opponent_farm = observation.farms[1]

    print(
        f"day={observation.day:2}, "
        f"our_money={our_farm['money']:8.1f}, "
        f"opp_money={opponent_farm['money']:8.1f}, "    
        f"carrot_price={prices['CARROT']:3}, "
        f"melon_price={prices['MELON']:3}, "
        f"carrot_inventory={inventory['CARROT']:5}, "
        f"melon_inventory={inventory['MELON']:5}, "
        f"our_plants=(C:{count_plants(our_farm, 'CARROT'):2}, "
        f"M:{count_plants(our_farm, 'MELON'):2}), "
        f"opp_plants=(C:{count_plants(opponent_farm, 'CARROT'):2}, "
        f"M:{count_plants(opponent_farm, 'MELON'):2})"
    )