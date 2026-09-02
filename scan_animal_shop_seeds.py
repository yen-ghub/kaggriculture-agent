from kaggle_environments import make

from main import agent
from baselines.adaptive_tomato_v1 import agent as baseline_agent


MILK_DEMAND_SHOPS = {
    "PIZZA_SHOP",
    "ICE_CREAM_SHOP",
    "SMOOTHIE_SHOP",
}

SEEDS = range(1, 21)
LAST_DECISION_DAY = 15


for seed in SEEDS:
    env = make(
        "kaggriculture",
        configuration={
            "episodeSteps": (LAST_DECISION_DAY + 1) * 24,
            "seed": seed,
        },
        debug=False,
    )

    env.run([agent, baseline_agent])

    shops_by_day = {}

    for step in env.steps:
        obs = step[0].observation

        if obs.day in (12, 15):
            shops_by_day[obs.day] = list(obs.town.unlocked_shops)

    shops_on_day_12 = shops_by_day.get(12, [])
    shops_on_day_15 = shops_by_day.get(15, [])

    if "YARN_STORE" in shops_on_day_12:
        yarn_day = 12
        decision_shops = shops_on_day_12
    elif "YARN_STORE" in shops_on_day_15:
        yarn_day = 15
        decision_shops = shops_on_day_15
    else:
        continue

    milk_shop_count = sum(
        shop in MILK_DEMAND_SHOPS
        for shop in decision_shops
    )

    print(
        f"seed={seed:2}, "
        f"yarn_day={yarn_day}, "
        f"milk_shops={milk_shop_count}, "
        f"shops={decision_shops}"
    )
