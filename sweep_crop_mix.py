from kaggle_environments import make

import main
from baselines.mixed_v1 import agent as baseline_agent

# MELON_COUNTS = range(0, len(main.TILES_MANAGED) + 1)
MELON_COUNTS = [8,10,12,13]
# MELON_COUNTS = range(7, 13)
SEEDS = range(1, 21)
# SEEDS = [16]

def collect_diagnostics(env, our_position):
    harvests = 0

    sold = {
        crop: 0
        for crop in main.CROPS_MANAGED
    }

    for step in env.steps:
        action = step[our_position].action

        if not action:
            continue

        farmer_action = action.get("farmer", [])

        if farmer_action and farmer_action[0] == "HARVEST":
            harvests += 1

        for order in action.get("market", []):
            if (
                len(order) >= 3
                and order[0] == "SELL"
                and order[1] in main.CROPS_MANAGED
            ):
                crop = order[1]
                sold[crop] += order[2]

    final_private = env.steps[-1][our_position].observation.private

    leftover = 0

    for crop in main.CROPS_MANAGED:
        leftover += final_private.shed.get(crop, 0)

        for inventory in final_private.inventories:
            leftover += inventory.get(crop, 0)

    return {
        "harvests": harvests,
        "sold": sold,
        "leftover": leftover,
    }

# Loop for each melon count in the list
for melon_count in MELON_COUNTS:
    carrot_count = len(main.TILES_MANAGED) - melon_count

    # This changes only the running Python process.
    main.CROP_BY_TILE = main.make_fixed_crop_plan(melon_count)

    wins = 0
    losses = 0
    ties = 0
    errors = 0

    our_scores = []
    opponent_scores = []
    harvest_counts = []
    carrot_sold_counts = []
    melon_sold_counts = []
    leftover_counts = []

    for seed in SEEDS:
        for our_position in (0, 1):
            if our_position == 0:
                agents = [main.agent, baseline_agent]
            else:
                agents = [baseline_agent, main.agent]

            env = make(
                "kaggriculture",
                configuration={
                    "episodeSteps": 720,
                    "seed": seed,
                },
                debug=False,
            )

            env.run(agents)

            final_step = env.steps[-1]
            ours = final_step[our_position]
            opponent = final_step[1 - our_position]

            if ours.status != "DONE":
                errors += 1
            elif opponent.status != "DONE":
                wins += 1
            elif ours.reward > opponent.reward:
                wins += 1
            elif ours.reward < opponent.reward:
                losses += 1
            else:
                ties += 1

            if ours.reward is not None:
                our_scores.append(ours.reward)

            if opponent.reward is not None:
                opponent_scores.append(opponent.reward)

            diagnostics = collect_diagnostics(env, our_position)
            if diagnostics["leftover"] > 0:
                final_private = env.steps[-1][our_position].observation.private

                carried_by_crop = {}
                shed_by_crop = {}

                for crop in main.CROPS_MANAGED:
                    carried_by_crop[crop] = sum(
                        inventory.get(crop, 0)
                        for inventory in final_private.inventories
                    )
                    shed_by_crop[crop] = final_private.shed.get(crop, 0)

                print(
                    f"LEFTOVER: seed={seed}, "
                    f"position={our_position}, "
                    f"carried={carried_by_crop}, "
                    f"shed={shed_by_crop}")
                
            harvest_counts.append(diagnostics["harvests"])
            carrot_sold_counts.append(diagnostics["sold"]["CARROT"])
            melon_sold_counts.append(diagnostics["sold"]["MELON"])
            leftover_counts.append(diagnostics["leftover"])

    
    # Compute the performance metrics for this melon count
    completed_matches = wins + losses + ties

    match_score = (
        100 * (wins + 0.5 * ties) / completed_matches
        if completed_matches > 0
        else 0
    )

    average_ours = sum(our_scores) / len(our_scores)
    average_opponent = sum(opponent_scores) / len(opponent_scores)
    average_harvests = sum(harvest_counts) / len(harvest_counts)
    average_carrots = sum(carrot_sold_counts) / len(carrot_sold_counts)
    average_melons = sum(melon_sold_counts) / len(melon_sold_counts)
    average_leftover = sum(leftover_counts) / len(leftover_counts)

    print(
        f"melons={melon_count:2}, "
        f"carrots={carrot_count:2}, "
        f"score={match_score:5.1f}%, "
        f"ours={average_ours:8.1f}, "
        f"opponent={average_opponent:8.1f}, "
        f"harvests={average_harvests:5.1f}, "
        f"carrot_sold={average_carrots:5.1f}, "
        f"melon_sold={average_melons:5.1f}, "
        f"leftover={average_leftover:4.1f}, "
        f"errors={errors}"
    )