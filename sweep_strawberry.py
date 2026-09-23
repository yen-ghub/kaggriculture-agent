"""Sweep the Strawberry acreage ceiling against the current frozen baseline.

Raising the ceiling means raising THREE constants together, not one. The
effective limit is

    strawberry_plant_target = min(
        requested_strawberry_target,                     # 39 or 45, + SW bonus
        premium_crop_plant_target - tomato_plant_target, # 45 + SW bonus
    )

so PREMIUM_CROP_PLANT_TARGET clamps the result at 48 no matter how high the
Strawberry targets themselves are set. Moving only STRAWBERRY_PLANT_TARGET or
HIGH_STRAWBERRY_PLANT_TARGET produces a byte-identical agent and a sweep that
reads as "no effect".

What the extra tiles cost: the farm is already saturated. Measured at day 12
on seeds 1, 8 and 19, all 68 managed tiles are in use -- 48 Strawberry, 8-13
Wheat, the rest livestock, with zero empty tiles. Every Strawberry tile this
sweep adds is taken from Wheat, and Wheat is the animal feed supply. Watch
WHEAT leftover and the harvest count, not just the match score: the failure
mode is unfed livestock, which will not show up as a Strawberry number.
"""

import main

from evaluate import evaluate_opponent
from baselines.immediate_milk_deposit_v1 import agent as baseline_agent

# Offsets applied to all three ceilings at once. 0 reproduces the baseline and
# is the control -- it scores 50.0% with both sides on identical money.
#
# Upward was measured and rejected: +3 and +6 raised Strawberry volume to
# 216.3 and 226.4 but cost 38.6 and 56.9 Wheat, and dropped OUR OWN money from
# 97,849 to 92,579 and 91,886 -- the opponent's fell too, so the extra units
# were glutting the shared market rather than earning. Going down is the
# untested direction: the log only ever raised this ceiling (33 -> 39 -> 45,
# plus the SW bonus of 3), so the optimum below 48 has never been looked at.
CEILING_OFFSETS = [-6, -3, 0]
SEEDS = [1, 2, 3, 4, 5, 8, 19]

BASE_STRAWBERRY_TARGET = main.STRAWBERRY_PLANT_TARGET
BASE_HIGH_STRAWBERRY_TARGET = main.HIGH_STRAWBERRY_PLANT_TARGET
BASE_PREMIUM_TARGET = main.PREMIUM_CROP_PLANT_TARGET


for offset in CEILING_OFFSETS:
    main.STRAWBERRY_PLANT_TARGET = BASE_STRAWBERRY_TARGET + offset
    main.HIGH_STRAWBERRY_PLANT_TARGET = BASE_HIGH_STRAWBERRY_TARGET + offset
    main.PREMIUM_CROP_PLANT_TARGET = BASE_PREMIUM_TARGET + offset

    summary = evaluate_opponent(
        f"Strawberry ceiling +{offset}",
        baseline_agent,
        SEEDS,
    )

    strawberry = summary["crops"]["STRAWBERRY"]
    wheat = summary["crops"]["WHEAT"]

    print(
        f"offset=+{offset}, "
        f"targets={main.STRAWBERRY_PLANT_TARGET}/"
        f"{main.HIGH_STRAWBERRY_PLANT_TARGET}, "
        f"premium={main.PREMIUM_CROP_PLANT_TARGET}, "
        f"score={100 * summary['match_score']:5.1f}%, "
        f"money={summary['average_ours']:8.1f}, "
        f"opponent={summary['average_opponent']:8.1f}, "
        f"harvests={summary['average_harvests']:5.1f}, "
        f"sberry_sold={strawberry['sold']:5.1f}, "
        f"wheat_sold={wheat['sold']:5.1f}, "
        f"wheat_left={wheat['carried'] + wheat['shed']:4.1f}, "
        f"errors={summary['results']['ERROR']}"
    )

main.STRAWBERRY_PLANT_TARGET = BASE_STRAWBERRY_TARGET
main.HIGH_STRAWBERRY_PLANT_TARGET = BASE_HIGH_STRAWBERRY_TARGET
main.PREMIUM_CROP_PLANT_TARGET = BASE_PREMIUM_TARGET
