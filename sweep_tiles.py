from kaggle_environments import make

import main
from baselines.carrot_v1 import agent as baseline_agent


TILE_COUNTS = range(14, 17)
SEEDS = range(1, 21)


def collect_diagnostics(env, our_position):
    harvests = 0
    sold = 0

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
                and order[1] == main.CROP
            ):
                sold += order[2]

    final_private = env.steps[-1][our_position].observation.private

    carried = sum(
        inventory.get(main.CROP, 0)
        for inventory in final_private.inventories
    )
    shed = final_private.shed.get(main.CROP, 0)

    return harvests, sold, carried + shed


for tile_count in TILE_COUNTS:
    # The agent reads this global list each time it is called.
    main.TILES_MANAGED = main.TILE_ROUTE[:tile_count]

    scores = []
    harvest_counts = []
    sold_counts = []
    leftover_counts = []

    wins = 0
    losses = 0
    ties = 0
    errors = 0

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
                debug=True,
            )

            env.run(agents)

            final_step = env.steps[-1]
            ours = final_step[our_position]
            opponent = final_step[1 - our_position]

            if ours.status != "DONE":
                errors += 1
                continue

            scores.append(ours.reward)

            if opponent.status != "DONE" or ours.reward > opponent.reward:
                wins += 1
            elif ours.reward < opponent.reward:
                losses += 1
            else:
                ties += 1

            harvests, sold, leftover = collect_diagnostics(
                env,
                our_position,
            )

            harvest_counts.append(harvests)
            sold_counts.append(sold)
            leftover_counts.append(leftover)

    completed = wins + losses + ties
    match_score = (wins + 0.5 * ties) / completed

    print(
        f"tiles={tile_count:2}, "
        f"match_score={100 * match_score:5.1f}%, "
        f"money={sum(scores) / len(scores):8.1f}, "
        f"harvests={sum(harvest_counts) / len(harvest_counts):5.1f}, "
        f"sold={sum(sold_counts) / len(sold_counts):5.1f}, "
        f"leftover={sum(leftover_counts) / len(leftover_counts):4.1f}, "
        f"errors={errors}"
    )