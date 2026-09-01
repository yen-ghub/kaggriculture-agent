from kaggle_environments import make

from main import agent
from baselines.full_second_quadrant_v1 import agent as baseline_agent


TOMATO_DEMAND_SHOPS = {
    "PIZZA_SHOP",
    "FARMERS_MARKET",
}

SEEDS = range(1, 21)


seed_groups = {
    "zero": [],
    "one": [],
    "two_or_more": [],
}


for seed in SEEDS:
    env = make(
        "kaggriculture",
        configuration={
            "episodeSteps": 720,
            "seed": seed,
        },
        debug=False,
    )
    env.run([agent, baseline_agent])

    final_observation = env.steps[-1][0].observation
    shops = list(final_observation.town.unlocked_shops)
    tomato_shop_count = sum(
        shop in TOMATO_DEMAND_SHOPS
        for shop in shops
    )

    if tomato_shop_count == 0:
        group = "zero"
    elif tomato_shop_count == 1:
        group = "one"
    else:
        group = "two_or_more"

    seed_groups[group].append(seed)

    print(
        f"seed={seed:2}, "
        f"tomato_shops={tomato_shop_count}, "
        f"shops={shops}"
    )


print()
print("Seed groups for this matchup:")
for group, seeds in seed_groups.items():
    print(f"{group:11}: {seeds}")
