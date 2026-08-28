import main

from evaluate import evaluate_opponent
from baselines.strawberry_v1 import agent as strawberry_agent


TILE_COUNTS = [21, 22]
WHEAT_TARGETS = [18]
SEEDS = list(range(1, 21))


for tile_count in TILE_COUNTS:
    main.TILE_COUNT = tile_count
    main.TILES_MANAGED = main.TILE_ROUTE[:tile_count]
    main.HANDS_TO_HIRE = 3
    main.DAILY_HAND_HIRE_COST = 4

    main.HAND_WORK_TILES_EACH = [
        main.TILE_ROUTE[:5],
        main.TILE_ROUTE[5:9],
        main.TILE_ROUTE[18:tile_count],
    ]
    
    hand_tile_count = sum(
        len(zone)
        for zone in main.HAND_WORK_TILES_EACH
    )

    for wheat_target in WHEAT_TARGETS:
        main.WHEAT_PLANT_TARGET = wheat_target

        summary = evaluate_opponent(
            (
                f"{tile_count} tiles, "
                f"wheat target {wheat_target}"
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

        print(
            f"tiles={tile_count:2}, "
            f"hand_tiles={hand_tile_count:2}, "
            f"wheat_target={wheat_target:2}, "
            f"score={100 * summary['match_score']:5.1f}%, "
            f"money={summary['average_ours']:8.1f}, "
            f"opponent={summary['average_opponent']:8.1f}, "
            f"harvests={summary['average_harvests']:5.1f}, "
            f"sold={average_sold:5.1f}, "
            f"leftover={average_leftover:4.1f}, "
            f"errors={summary['results']['ERROR']}"
        )
    
    
    