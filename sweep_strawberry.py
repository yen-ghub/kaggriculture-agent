import main

from evaluate import evaluate_opponent
from baselines.eleven_hand_v1 import agent as eleven_hand_agent

STRAWBERRY_TARGET_BONUSES = [1, 2, 3]
SEEDS = [1, 2, 3, 4, 5, 12]
STRAWBERRY_LAST_PLANTING_DAY = 18
# SEEDS = list(range(1, 6))


for strawberry_bonus in STRAWBERRY_TARGET_BONUSES:
    main.THIRD_QUADRANT_STRAWBERRY_BONUS = strawberry_bonus
    
    summary = evaluate_opponent(
        f"SW strawberry bonus {strawberry_bonus}",
        eleven_hand_agent,
        SEEDS,
    )

    crop_results = summary["crops"]["STRAWBERRY"]

    average_leftover = sum(
        crop["carried"] + crop["shed"]
        for crop in summary["crops"].values()
    )

    print(
        f"strawberry_bonus={strawberry_bonus:2}, "
        f"targets={39 + strawberry_bonus}/"
        f"{45 + strawberry_bonus}, "
        f"score={100 * summary['match_score']:5.1f}%, "
        f"money={summary['average_ours']:8.1f}, "
        f"opponent={summary['average_opponent']:8.1f}, "
        f"harvests={summary['average_harvests']:5.1f}, "
        f"strawberry_sold={crop_results['sold']:4.1f}, "
        f"leftover={average_leftover:4.1f}, "
        f"errors={summary['results']['ERROR']}"
    )
