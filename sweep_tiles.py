import main

from evaluate import evaluate_opponent
from baselines.hand_planting_v1 import agent as hand_planting_agent


TILE_COUNTS = [17, 18, 19]
WHEAT_TARGETS = [16, 20]
SEEDS = list(range(1, 11))

    
for tile_count in TILE_COUNTS:
    main.TILE_COUNT = tile_count
    main.TILES_MANAGED = main.TILE_ROUTE[:tile_count]
    main.HAND_WORK_TILES_EACH = main.make_hand_work_zones(
        main.TILES_MANAGED
    )

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
            hand_planting_agent,
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
    
    
    