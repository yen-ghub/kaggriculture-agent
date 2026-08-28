import main

from evaluate import evaluate_opponent
from baselines.expanded_wheat_v1 import agent as expanded_wheat_agent

STRAWBERRY_START_DAYS = [10, 11, 12]
STRAWBERRY_TARGETS = [3]
SEEDS = list(range(1, 21))


for strawberry_start_day in STRAWBERRY_START_DAYS:
    main.STRAWBERRY_START_DAY = strawberry_start_day

    summary = evaluate_opponent(
        f"strawberry start day {strawberry_start_day}",
        expanded_wheat_agent,
        SEEDS,
    )

    crop_results = summary["crops"]["STRAWBERRY"]

    average_leftover = sum(
        crop["carried"] + crop["shed"]
        for crop in summary["crops"].values()
    )

    print(
        f"strawberries start day={strawberry_start_day:2}, "
        f"score={100 * summary['match_score']:5.1f}%, "
        f"money={summary['average_ours']:8.1f}, "
        f"opponent={summary['average_opponent']:8.1f}, "
        f"harvests={summary['average_harvests']:5.1f}, "
        f"strawberry_sold={crop_results['sold']:4.1f}, "
        f"leftover={average_leftover:4.1f}, "
        f"errors={summary['results']['ERROR']}"
    )