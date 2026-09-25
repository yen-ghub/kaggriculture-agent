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
from baselines.ne_strawberry_fill_v1 import agent as baseline_agent

# Offsets applied to all three ceilings at once. 0 reproduces the baseline and
# is the control -- it scores 50.0% with both sides on identical money.
#
# Upward was measured and rejected: +3 and +6 raised Strawberry volume to
# 216.3 and 226.4 but cost 38.6 and 56.9 Wheat, and dropped OUR OWN money from
# 97,849 to 92,579 and 91,886 -- the opponent's fell too, so the extra units
# were glutting the shared market rather than earning. Going down is the
# untested direction: the log only ever raised this ceiling (33 -> 39 -> 45,
# plus the SW bonus of 3), so the optimum below 48 has never been looked at.
# Re-run downward on ne_strawberry_fill_v1 (2026-09-25): the sweep above was
# measured at ~200 Strawberry per player, before off-day Fertilizer and the NE
# fill took it to ~268. At that volume the late dumps sell mostly at the price
# floor (seed 1, d22: 110 units sold, market inventory +31, so ~79 went for 1
# coin), and a unit sold at the floor neither earns nor lowers the opponent's
# price, so the denial argument for 48 may no longer hold.
#
# Seven-seed result (seeds 1-5, 8, 19, both positions), control 85,996.7 each:
#
#   offset  ours      opponent  margin   score  Strawberry  Wheat
#   -12     87,976.9  87,309.7   +667.2  57.1%  201.9       232.0
#    -9     91,053.4  89,279.0  +1774.4  71.4%  224.6       225.0
#    -6     89,002.6  87,091.0  +1911.6  71.4%  233.7       204.6
#    -3     89,804.0  88,847.3   +956.7  85.7%  259.0       191.1
#     0     85,996.7  85,996.7      0.0  50.0%  264.4       178.3
#
# Every cut raised our OWN money, the reverse of the ~200-unit sweep. The
# -6/-9 plateau is the twenty-seed candidate; -3 gains 3,807 for only 5 fewer
# Strawberry, which smells of re-rolled towns on seven seeds.
CEILING_OFFSETS = [-9]  # -6 is main.py now: gate it with evaluate.py
SEEDS = list(range(1, 21))

# Hard-coded to ne_strawberry_fill_v1's values, so the offsets stay relative to
# the baseline while main.py carries a trial value.
BASE_STRAWBERRY_TARGET = 39
BASE_HIGH_STRAWBERRY_TARGET = 45
BASE_PREMIUM_TARGET = 45


for offset in CEILING_OFFSETS:
    main.STRAWBERRY_PLANT_TARGET = BASE_STRAWBERRY_TARGET + offset
    main.HIGH_STRAWBERRY_PLANT_TARGET = BASE_HIGH_STRAWBERRY_TARGET + offset
    main.PREMIUM_CROP_PLANT_TARGET = BASE_PREMIUM_TARGET + offset

    summary = evaluate_opponent(
        f"Strawberry ceiling {offset:+d}",
        baseline_agent,
        SEEDS,
    )

    strawberry = summary["crops"]["STRAWBERRY"]
    wheat = summary["crops"]["WHEAT"]

    print(
        f"offset={offset:+d}, "
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
