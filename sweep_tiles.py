import main

from evaluate import evaluate_opponent
from baselines.four_cows_v1 import agent as agent


TILE_COUNTS = [25]
STRAWBERRY_TARGETS = [35]
SEEDS = list(range(1, 6))


hand_tile_count = sum(
    len(zone)
    for zone in main.HAND_WORK_TILES_EACH
)

for tile_count in TILE_COUNTS:
    
    for strawberry_target in STRAWBERRY_TARGETS:
        main.STRAWBERRY_PLANT_TARGET = strawberry_target

        summary = evaluate_opponent(
            (
                # f"{tile_count} tiles, "
                f"{strawberry_target} strawberries"
            ),
            agent,
            SEEDS,
        )

        average_sold = sum(
                    summary["crops"][crop]["sold"]
                    for crop in main.CROPS_MANAGED
                )
            
        average_leftover = sum(
            summary["crops"][crop]["carried"]
            + summary["crops"][crop]["shed"]
            for crop in main.CROPS_MANAGED
                )
        strawberry_results = summary["crops"]["STRAWBERRY"]
        print(
            f"crop_tiles={hand_tile_count:2}, "
            f"sberry_target={strawberry_target:2}, "
            f"score={100 * summary['match_score']:5.1f}%, "
            f"money={summary['average_ours']:8.1f}, "
            f"opponent={summary['average_opponent']:8.1f}, "
            f"harvests={summary['average_harvests']:5.1f}, "
            f"sberry_sold={strawberry_results['sold']:5.1f}, "
            f"sold={average_sold:5.1f}, "
            f"leftover={average_leftover:4.1f}, "
            f"errors={summary['results']['ERROR']}"
        )
    
    