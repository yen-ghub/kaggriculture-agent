import main

from evaluate import evaluate_opponent
from baselines.full_quadrant_strawberry_v1 import agent as strawberry_agent


TILE_COUNTS = [25]
STRAWBERRY_TARGETS = [16, 20, 23,25]
SEEDS = list(range(1, 6))


for tile_count in TILE_COUNTS:
    main.TILE_COUNT = tile_count
    main.TILES_MANAGED = main.TILE_ROUTE[:tile_count]
    main.HANDS_TO_HIRE = 3
    main.DAILY_HAND_HIRE_COST = 4

    main.HAND_WORK_TILES_EACH = [
        main.TILE_ROUTE[:6],
        main.TILE_ROUTE[6:11],
        main.TILE_ROUTE[18:tile_count],
    ]
    
    hand_tile_count = sum(
        len(zone)
        for zone in main.HAND_WORK_TILES_EACH
    )

    for strawberry_target in STRAWBERRY_TARGETS:
        main.STRAWBERRY_PLANT_TARGET = strawberry_target

        summary = evaluate_opponent(
            (
                f"{tile_count} tiles, "
                f"{strawberry_target} strawberries"
            ),
            strawberry_agent,
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
            f"tiles={tile_count:2}, "
            f"hand_tiles={hand_tile_count:2}, "
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
    
    