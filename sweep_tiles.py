import main

from evaluate import evaluate_opponent
from baselines.hand_v1 import agent as hand_agent


TILE_COUNTS = [16,17,18,19]
HAND_TILE_COUNTS = range(7, 10)
SEEDS = list(range(1, 6))

    
for tile_count in TILE_COUNTS:
    main.TILE_COUNT = tile_count
    main.TILES_MANAGED = main.TILE_ROUTE[:tile_count]

    for hand_tile_count in HAND_TILE_COUNTS:
        main.HAND_WORK_TILE_COUNT = hand_tile_count
        main.HAND_WORK_TILES = main.TILES_MANAGED[:hand_tile_count]

        summary = evaluate_opponent(
            f"hand_v1 with {tile_count} tiles",
            hand_agent,
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
            f"score={100 * summary['match_score']:5.1f}%, "
            f"money={summary['average_ours']:8.1f}, "
            f"harvests={summary['average_harvests']:5.1f}, "
            f"sold={average_sold:5.1f}, "
            f"leftover={average_leftover:4.1f}, "
            f"errors={summary['results']['ERROR']}"
        )