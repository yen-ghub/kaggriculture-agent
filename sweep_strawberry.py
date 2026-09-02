import main

from evaluate import evaluate_opponent
from baselines.third_quadrant_v1 import agent as third_quadrant_agent

STRAWBERRY_TARGET_BONUSES = [0, 3, 6, 9]
SEEDS = list(range(1, 21))
STRAWBERRY_LAST_PLANTING_DAY = 18
# SEEDS = list(range(1, 6))


for strawberry_bonus in STRAWBERRY_TARGET_BONUSES:
    main.STRAWBERRY_PLANT_TARGET = 33 + strawberry_bonus
    main.HIGH_STRAWBERRY_PLANT_TARGET = 39 + strawberry_bonus
    main.PREMIUM_CROP_PLANT_TARGET = 39 + strawberry_bonus
    main.CROP_CONFIGS["STRAWBERRY"]["last_production_day"] = (
        main.FINAL_DAY - STRAWBERRY_LAST_PLANTING_DAY
    )
    
    summary = evaluate_opponent(
        f"third quadrant strawberry bonus {strawberry_bonus}",
        third_quadrant_agent,
        SEEDS,
    )

    crop_results = summary["crops"]["STRAWBERRY"]

    average_leftover = sum(
        crop["carried"] + crop["shed"]
        for crop in summary["crops"].values()
    )

    print(
        f"strawberry_bonus={strawberry_bonus:2}, "
        f"targets={main.STRAWBERRY_PLANT_TARGET:2}/"
        f"{main.HIGH_STRAWBERRY_PLANT_TARGET:2}, "
        f"score={100 * summary['match_score']:5.1f}%, "
        f"money={summary['average_ours']:8.1f}, "
        f"opponent={summary['average_opponent']:8.1f}, "
        f"harvests={summary['average_harvests']:5.1f}, "
        f"strawberry_sold={crop_results['sold']:4.1f}, "
        f"leftover={average_leftover:4.1f}, "
        f"errors={summary['results']['ERROR']}"
    )
