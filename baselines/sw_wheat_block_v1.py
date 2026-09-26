# Define tiles to manage in (x,y)
# Define tiles to manage in (x, y)
FIRST_QUADRANT_ROUTE = [
    (4,4), (3,4), (2,4), (1,4), (0,4),
    (0,3), (1,3), (2,3), (3,3), (4,3),
    (4,2), (3,2), (2,2), (1,2), (0,2),
    (0,1), (1,1), (2,1), (3,1), (4,1),
    (4,0), (3,0), (2,0), (1,0), (0,0),
]

SECOND_QUADRANT_ROUTE = [
    (5,4), (6,4), (7,4), (8,4), (9,4),
    (9,3), (8,3), (7,3), (6,3), (5,3),
    (5,2), (6,2), (7,2), (8,2), (9,2),
    (9,1), (8,1), (7,1), (6,1), (5,1),
    (5,0), (6,0), (7,0), (8,0), (9,0),
]

THIRD_QUADRANT_ROUTE = [
    (4, 5), (3, 5), (2, 5), (1, 5), (0, 5),
    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6),
    (4, 7), (3, 7),
    (2, 7), (1, 7), (0, 7),
    (0, 8), (1, 8), (2, 8),
]

SECOND_QUADRANT_TILE_COUNT  = 25
SECOND_QUADRANT_NAME        = "NE"
SECOND_QUADRANT_LAND_COST   = 1000
SECOND_QUADRANT_PURCHASE_DAY = 6        # Earlier NE expansion after opening livestock
LAND_WORKING_CAPITAL_RESERVE = 1000

THIRD_QUADRANT_TILE_COUNT   = len(THIRD_QUADRANT_ROUTE)
THIRD_QUADRANT_NAME         = "SW"
THIRD_QUADRANT_LAND_COST    = 2000
THIRD_QUADRANT_PURCHASE_START_DAY = 11
THIRD_QUADRANT_PURCHASE_LAST_DAY = 18

# Combine the two quadrants
TILE_ROUTE = (
    FIRST_QUADRANT_ROUTE
    + SECOND_QUADRANT_ROUTE
    + THIRD_QUADRANT_ROUTE
)

TILE_COUNT = (
    len(FIRST_QUADRANT_ROUTE)
    + SECOND_QUADRANT_TILE_COUNT
    + THIRD_QUADRANT_TILE_COUNT
)

TILES_MANAGED = TILE_ROUTE[:TILE_COUNT]
    
# Define constants and crop configs (a dict)
CROP_CONFIGS = {
    "TOMATO": {
        "seed_cost": 50,
        "harvest_day": 8,
        "harvest_yield": 4,
        "ongoing": True,
        "last_production_day": 11,
    },
    "STRAWBERRY": {
        "seed_cost": 100,
        "harvest_day": 10,
        "harvest_yield": 4,
        "ongoing": True,
        "last_production_day": 16,
    },
    "WHEAT": {
        "seed_cost": 10,
        "harvest_day": 4,
        "harvest_yield": 4,
        "ongoing": False,
        "last_production_day": 4,
    },
    "CARROT": {
        "seed_cost": 20,
        "harvest_day": 3,
        "harvest_yield": 3,
        "ongoing": False,
        "last_production_day": 3
    },
    "MELON": {
        "seed_cost": 80,
        "harvest_day": 10,
        "harvest_yield": 6,
        "ongoing": False,
        "last_production_day": 10,
    },
}
 
STAPLE_CROPS    = ("CARROT", "WHEAT")
CROPS_MANAGED   = ("WHEAT", "CARROT", "MELON", "STRAWBERRY", "TOMATO") # Affects market sale order
# Sell the highest base-price crops first: 250/120/60/35/25 respectively.
# Generalizes the proven Melon-first mechanism (see mechanics.md's lockstep
# documentation) to the rest of CROPS_MANAGED, so Strawberry -- the next most
# valuable crop -- is no longer sold behind cheap Wheat and Carrot purely by
# tuple-definition order. Scoped to crops only: Wool and Milk are left in
# their existing order pending their own evaluation (a related experiment
# found Wool's realized price actually improved from a later list position
# in one case, so animal-product order is not assumed to follow the same
# rule without its own test).
CROP_SALE_PRIORITY = ("MELON", "STRAWBERRY", "TOMATO", "CARROT", "WHEAT")

# Shift five Carrot plantings away from the day-10 shed transition. The
# override is limited to this planting window so earlier Carrot income and
# later adaptive crop allocation remain unchanged.
OVERFLOW_BUFFER_WHEAT_TILES = (
    (8, 0),
    (9, 0),
    (8, 1),
    (9, 1),
    (5, 2),
)
OVERFLOW_BUFFER_WHEAT_START_DAY = 7
OVERFLOW_BUFFER_WHEAT_LAST_DAY = 9

# NW tiles must be free for the day-10 Strawberry wave. A staple planted in NW
# after day STRAWBERRY_START_DAY - 4 is Wheat that cannot be ready by then: the
# day-0 Wheat cycles d0 -> d4 -> d8 -> ready d12, so on seed 9 two NW tiles
# were still growing Wheat when the wave came and missed it for good (13 NW
# Strawberry against the baseline's 15, -2,273). In that window NW plants
# Carrot only while it can still be ready by day 10, and otherwise leaves the
# tile empty until the wave.
NW_PRE_STRAWBERRY_TILES = frozenset(FIRST_QUADRANT_ROUTE)

# Pair each tile with one type of plant (a dict)
def make_fixed_crop_plan(melon_tile_count):
    if not 0 <= melon_tile_count <= len(TILES_MANAGED):
        raise ValueError(
            "melon_tile_count must be between 0 "
            f"and {len(TILES_MANAGED)}"
        )

    crop_plan = {}

    for index, position in enumerate(TILES_MANAGED):
        if index < melon_tile_count:
            crop_plan[position] = "MELON"
        else:
            crop_plan[position] = "CARROT"

    return crop_plan

# Crop related
MELON_LAST_PLANTING_DAY = 0
MELON_REPLANT_PRICE_THRESHOLD = 220
POST_GLUT_MELON_TARGET = 4
HEAVY_OPPONENT_MELON_TARGET = 13
# The single opening Melon wave (planted day 0 only) always matures on this
# day. Hands carrying Melon on this day make an early return trip once their
# other work is done, instead of waiting for the automatic overnight deposit,
# so the sale can beat the opponent to the shared market by a full day.
MELON_HARVEST_DAY = CROP_CONFIGS["MELON"]["harvest_day"]
DEFAULT_SEED_TARGETS = {
    "WHEAT": 1,
    "CARROT": 1,
    "STRAWBERRY": 0,
    "MELON": 0,
    "TOMATO":0
}
SELECTED_CROP_SEED_TARGET = 3
NE_SELECTED_CROP_SEED_TARGET = 8
# No limit (was 18, from the starter agents). Wheat never gluts: both sides
# buy feed Wheat daily and its price climbs 28 -> 50 over the game even with
# ~630 units sold (replays/sw_full_1.json, sw_full_2.json). The cap sent the
# day 24-25 staple plantings to Carrot, 3 x ~41 - 20 against 4 x ~48 - 10.
WHEAT_PLANT_TARGET      = 75

#
# STRAWBERRY related
STRAWBERRY_PLANT_TARGET     = 33        # Fine-tuned: 39; -6 on trial (sweep_strawberry.py)
HIGH_STRAWBERRY_PLANT_TARGET = 39        # 45; -6 on trial
STRAWBERRY_START_DAY        = 10
EARLY_NE_STRAWBERRY_START_DAY = SECOND_QUADRANT_PURCHASE_DAY
# All twelve early Strawberry go into NE on its unlock day, instead of six in
# NE and six more converted from NW Wheat on day 9 (EARLY_NW_STRAWBERRY_TARGET
# below, now 0). Same twelve seeds, two days earlier, and all of them in the
# first NE wave that the off-day Fertilizer rule boosts.
# Superseded by early_ne_strawberry_target in agent(): the early NE wave now
# fills every NE crop tile not reserved for animals (17 on seeds 1 and 15),
# since this is our earliest Strawberry and sells before the opponents' own
# day-10/11 wave starts to glut the market.
EARLY_NE_STRAWBERRY_TARGET = 12
# A real opponent replay (docs/opponent_replay_trace.md, day 5) showed a
# winning agent recycling early-filler staple tiles into Strawberry well
# before our day-10 default. Gated on NE already being unlocked so it never
# competes with the NE land/animal purchase's own cash reservation.
EARLY_NW_STRAWBERRY_TARGET = 0
# Day-5 NW Strawberry (replays/scaling1.json, scaling2.json: the ladder
# leaders plant 4 on harvested day-0 Wheat on day 5). Four day-0 Wheat tiles
# harvested on day 4 stay empty that day instead of taking Carrot, and get
# Strawberry on days 5-6 once the day's sales pay for the seed (day 5 starts
# on ~11-33 coins and ends on ~840-900). Their harvests fall on days 15-21,
# before the glut, instead of 20-26 in the day-10 wave: the live Strawberry
# cap is binding, so these are four plants moved earlier, not four added.
# From day 7 an unplanted tile goes back to the normal crop.
NW_DAY5_STRAWBERRY_TILES = (
    (1, 1), (0, 1), (0, 2), (2, 0),
)
NW_DAY5_STRAWBERRY_HOLD_DAY = 4
NW_DAY5_STRAWBERRY_START_DAY = 5
NW_DAY5_STRAWBERRY_LAST_DAY = 6
STRAWBERRY_DAILY_SELL_CAP   = 8
STRAWBERRY_FORCE_SELL_DAY   = 29
STRAWBERRY_SELL_PRICE_THRESHOLD = 250
HEAVY_OPPONENT_STRAWBERRY_THRESHOLD = 10
HIGH_STRAWBERRY_SHOP_THRESHOLD = 2
STRAWBERRY_LAST_PLANTING_DAY = 18 
THIRD_QUADRANT_STRAWBERRY_BONUS = 3
SW_STRAWBERRY_SHOP_THRESHOLD = 3

# TOMATO related
TOMATO_DEMAND_SHOPS = {
    "PIZZA_SHOP",
    "FARMERS_MARKET",
}

PREMIUM_CROP_PLANT_TARGET = 39        # 45; -6 on trial, clamps the Strawberry target too
TOMATO_PLANTS_PER_DEMAND_SHOP = 3
MAX_TOMATO_PLANT_TARGET = 6
TOMATO_START_DAY = 13
TOMATO_FORCE_SELL_DAY = 29
   
LAST_HOUR_TODAY     = 23
FINAL_DAY           = 29


# Animal related (generalised from COW)
INITIAL_COW_TILES = (
    (4, 4),
    (4, 3),
)
EXPANSION_COW_TILES = (
    (5, 4),
    (5, 3),
)
EXPANSION_COW_COUNT = 2
EXPANSION_COW_START_DAY = SECOND_QUADRANT_PURCHASE_DAY
# Every position permanently reserved for a cow.
COW_TILES = (
    INITIAL_COW_TILES
    + EXPANSION_COW_TILES[:EXPANSION_COW_COUNT]
)

# First stage of the shop-aware livestock ladder.  This western tile sits on
# Hand 0's existing Sheep route, so the extra Cow does not extend the farmer's
# daily circuit. The tile stays in normal crop production until qualifying
# demand is visible; its current crop is harvested before pasture conversion.
STAGED_COW_TILES = (
    (1, 4),
)
STAGED_COW_START_DAY = 8
STAGED_COW_LAST_START_DAY = 10
STAGED_COW_MILK_SHOP_THRESHOLD = 2


EARLY_SHEEP_TILES = (
    (3, 3),
)
DELAYED_SHEEP_TILES = (
    (3, 4),
)
INITIAL_SHEEP_TILES = (
    EARLY_SHEEP_TILES
    + DELAYED_SHEEP_TILES
)
DAY4_ADDITIONAL_SHEEP_TILES = (
    (2, 4),
)
DAY11_ADDITIONAL_SHEEP_TILES = (
    (2, 3),
)
ADDITIONAL_SHEEP_TILES = (
    DAY4_ADDITIONAL_SHEEP_TILES
    + DAY11_ADDITIONAL_SHEEP_TILES
)

SHEEP_TILES = (
    INITIAL_SHEEP_TILES
    + ADDITIONAL_SHEEP_TILES
)

EARLY_SHEEP_START_DAY       = 0
DELAYED_SHEEP_START_DAY     = 0
DAY4_ADDITIONAL_SHEEP_START_DAY = 4
DAY11_ADDITIONAL_SHEEP_START_DAY = 11
EARLY_SHEEP_TILE_REPLANT_CUTOFF_DAY         = 0
DELAYED_SHEEP_TILE_REPLANT_CUTOFF_DAY       = 0
DAY4_ADDITIONAL_SHEEP_REPLANT_CUTOFF_DAY    = 0
DAY11_ADDITIONAL_SHEEP_REPLANT_CUTOFF_DAY   = 10
INITIAL_SHEEP_CASHOUT_HAND_INDEX    = 0                # Early cashout to buy the delayed sheep
# Day 0 buys only that day's feed, so the opening can afford 7 Wheat seeds on
# top of 12 Melons and 4 animals (a real opponent's day 0 in
# replays/day0_setup.json). Day 1's feed is paid for on day 1 by selling the
# Fertilizer the animals produce overnight, the same day, at the opening
# price of ~100, instead of carrying it to the overnight deposit.
FERTILIZER_CASHOUT_DAY = 1
# Day 0's Melon target, whatever the opponent shows. The regular target reads
# 15 at day 0 (the opponent has planted nothing yet), so Melons simply bought
# until the money ran out and the Wheat seeds never got a turn.
DAY0_MELON_TARGET = 12
# Where the day-0 Melons go: the twelve NW crop tiles nearest the shed that are
# free on day 0 and stay with the Melon hands 1-3. Only Melons have to be
# walked back for a same-day sale on day 10 (Wheat reaches the shed overnight
# from a hand's pack), and the walk sets the sale hour: from (1,0), seven
# steps out, no hand sold before ~h18. (1,0) -> (1,3) and (2,0) -> (1,2) take
# the total from 52 steps to 48 and the furthest from 7 to 6. Excluded: the
# animal tiles, (2,4) (day-4 Sheep), (1,4) (staged Cow, may clear on day 8-10)
# and hand 0's tiles (hand 0 runs the Sheep and is not a Melon worker).
# (1,1) -> (0,4) as well (melon_layout_v2): total 48 -> 46, furthest 6 -> 5.
# (0,4) is hand 0's tile; hand 0 is not a Melon worker, so on Melon day the
# crop routine leaves Melon tiles to the crew (see choose_hand_action).
DAY0_MELON_TILES = frozenset((
    (4, 2), (3, 2), (2, 2), (2, 3),
    (4, 1), (3, 1), (2, 1),
    (4, 0), (3, 0),
    (1, 3), (1, 2),
    (0, 4),
))
INITIAL_SHEEP_CASH_RESERVE_START_DAY = 1
INITIAL_SHEEP_CASH_RESERVE_END_DAY  = 3
INITIAL_SHEEP_CASH_RESERVE          = 1000

ADAPTIVE_GOOSE_TILES = (
    (6, 4),
    (6, 3),
)
GOOSE_HAND_INDEX = 4
# Owner of the second Goose while the compact NE block runs alongside the
# Goose branch. Hand 4 keeps (6,4) but must not take (6,3) as well: it is the
# most saturated hand on the farm (1.7% idle on seed 6) and its crop route
# spans the whole quadrant, so a second Goose collapsed its Wheat output
# (233 -> 135 sold on seed 10). Hand 6 has 10.2% idle and its route starts at
# (6,2), one tile from (6,3).
# Hand 4 keeps (6,4): its own crop route already contains the adjacent shed
# access tile (5,4), so that Goose costs it almost no travel -- carrying BOTH
# was what collapsed its Wheat output, not carrying one. The second Goose at
# (6,3) goes to hand 7, the only NE hand with slack on both qualifying seeds
# (17.1% and 18.5% idle), two rows from its route tile (6,1).
# Roles swap in the coexistence branch. Hand 4 becomes the pure livestock hand
# for the four NE animals; hand 5 keeps the NE crop route it would otherwise
# have given up and takes both Geese. Every previous split put a Goose on a
# hand that also owned crops, so the cost always surfaced as lost Wheat; this
# concentrates all six animals' service into two hands instead of spreading
# Goose detours across three crop routes.
# With the animal block relocated to (7,4)/(8,4)/(7,3)/(8,3), the crop hand's
# default slice still reaches (9,4)/(9,3) -- a long detour past the pastures
# from its otherwise western column. Trade those two to hand 6 for the
# adjacent (8,2)/(9,2), which sit on hand 6's own row.
# Explicit NE crop-tile owners while the Geese coexist, overriding the default
# route slices. Hand 4 takes the eastern end of row 2 plus (9,3), so her Goose
# at (6,4) and her crops sit in one block; (5,2) goes to hand 7, whose own
# (5,1) is directly above it.
# Explicit NE crop-tile owners while the Geese coexist, overriding the route
# slices the NE block phase would otherwise compute. That reslicing put both
# Goose hands on the east of the quadrant, so every Goose visit crossed it and
# the far ends of their routes went to weed (seed 15: (7,1), (9,3), (8,1);
# Strawberry 45 vs 48). Each hand now works the row its Goose sits on:
#   hand 6: row 1 from its Goose at (5,1), plus (9,2)
#   hand 5: row 2 from its Goose at (5,2), plus (8,3), (9,3)
#   hand 4: the four NE animals, plus (8,4), (9,4) beside them
# Hand 7 keeps row 0.
# Revised: hand 4 serves the four NE animals only; hand 5 takes row 2 plus the
# east end of rows 3-4; hand 6 takes row 1 plus (9,2)/(9,3); hand 7 keeps row
# 0 and takes the (5,1) Goose directly above it.
NE_COEXIST_CROP_TILE_OWNERS = {
    (6, 2): 5,
    (7, 2): 5,
    (8, 2): 5,
    (8, 3): 5,
    (8, 4): 5,
    (9, 4): 5,
    (6, 1): 6,
    (7, 1): 6,
    (8, 1): 6,
    (9, 1): 6,
    (9, 2): 6,
    (9, 3): 6,
    (5, 0): 7,
    (6, 0): 7,
    (7, 0): 7,
    (8, 0): 7,
    (9, 0): 7,
}
# Left unworked on purpose while the Geese coexist, to measure what these two
# far tiles are actually worth. They sit behind the relocated animal block:
# on hand 4 they scattered her route, and handing them to hand 6 only moved
# the saturation (hand 6 PASS 10.2% -> 3.5%, sum -994 -> -4376 on seeds 6/10).
# The farmer must skip them too, or its crop fallback scan simply claims any
# tile no hand owns and the test measures nothing.
# Nothing is deliberately left idle: leaving (9,4)/(9,3) unworked cost ~2741
# across seeds 6/10, so both went back to hand 4.
NE_COEXIST_UNMANAGED_TILES = ()

# Which hand serves the four NE animals while the Geese coexist. The other of
# hands 4/5 keeps the NE crop slice.
NE_COEXIST_LIVESTOCK_HAND_INDEX = 4
# Where the Geese live when the compact NE block also runs. Keeping them on
# (6,4)/(6,3) pushed the four NE animals one column east, which cost a crop
# tile and made the livestock hand's round finish after the h23 sale, so its
# Milk sold the next morning behind the opponent's (seed 15: -1,296 at
# identical volume). The animals go back on the default block beside the shed
# and the Geese move to the west column of the quadrant, onto the path of the
# hands that serve them.
NE_COEXIST_GOOSE_TILES = (
    (5, 1),
    (5, 2),
)
# Goose tile ownership in the coexistence branch: hand index -> its tiles.
NE_COEXIST_GOOSE_OWNERSHIP = {
    7: (NE_COEXIST_GOOSE_TILES[0],),
    5: (NE_COEXIST_GOOSE_TILES[1],),
}
GOOSE_HAND_TILE = ADAPTIVE_GOOSE_TILES[0]
# Compatibility alias for local trace scripts created before this split.
ADAPTIVE_ANIMAL_TILES = ADAPTIVE_GOOSE_TILES

# Move the existing four-animal SW branch into a compact NE block when the
# first two shops already give a strong livestock signal.  The decision is
# known before NE planting begins, so qualifying seeds can reserve these tiles
# without destroying an established Strawberry crop.
EARLY_NE_LIVESTOCK_TILES = (
    (6, 4),
    (7, 4),
    (6, 3),
    (7, 3),
)
# When the first two shops demand Eggs AND also signal Yarn or Milk, both the
# Goose branch and the compact NE block qualify.
#
# In practice this is SHEEP-ONLY, and unreachable for Cows. Cow coexistence
# would need eggs AND first_two_shops_both_demand_milk AND no yarn; but
# `both_demand_milk` requires BOTH of the two shops to be Milk shops, and
# EGG_DEMAND_SHOPS (BAKERY, BRUNCH_SPOT) is disjoint from MILK_DEMAND_SHOPS
# (ICE_CREAM_SHOP, PIZZA_SHOP, SMOOTHIE_SHOP), so an all-Milk prefix can never
# also demand Eggs. The third NE trigger, first_two_shops_milk_only, excludes
# Egg demand explicitly. So early_ne_all_cow_plan is never built under
# coexistence, and every measurement behind this feature is the Sheep case.
#
# That matters if the trigger is ever widened. Wool held at 208 in every
# allocation tested, which is why the animal side never regressed; Milk is the
# deeply glutted product where a six-hour deposit delay cost -2554. Admitting
# Cows here needs fresh measurement, not an extension of these results. They used to suppress each
# other because (6,4)/(6,3) are shared by both layouts -- a hard tile conflict,
# not a policy choice (see docs/current_roadmap.md, P1). Shifting the livestock
# block one column east frees the Geese's own tiles so the two can run at once.
# Now identical to the default block: the Geese moved to (5,1)/(5,2) instead.
EARLY_NE_GOOSE_COEXIST_LIVESTOCK_TILES = EARLY_NE_LIVESTOCK_TILES
# Tiles unique to each layout. With both layouts on the same tiles there is
# nothing left to tell apart; the latch below resolves to the default block.
EARLY_NE_DEFAULT_ONLY_TILES = ((6, 4), (6, 3))
EARLY_NE_COEXIST_ONLY_TILES = ()

EARLY_NE_LIVESTOCK_HAND_INDEX = 5
# Weakest shop prefix that still routes the NE block to the existing all-Cow
# plan.  Applied only when the prefix carries no Yarn and no Egg signal, so the
# accepted Sheep, double-Milk and Goose branches keep their current triggers.
EARLY_NE_SINGLE_MILK_SHOP_THRESHOLD = 1
EARLY_NE_LIVESTOCK_PASTURE_START_DAY = 8
EARLY_NE_LIVESTOCK_START_DAY = 9
EARLY_NE_LIVESTOCK_CASH_RESERVE = 0

SW_LIVESTOCK_PLAN = {
    (4, 5): "COW",
    (3, 5): "SHEEP",
    (3, 6): "SHEEP",
    (4, 6): "COW",
}
SW_LIVESTOCK_TILES = tuple(SW_LIVESTOCK_PLAN)
ADAPTIVE_MAMMAL_TILES = SW_LIVESTOCK_TILES[:2]
SW_LIVESTOCK_OUTER_TILES = SW_LIVESTOCK_TILES[2:]
SW_ALL_SHEEP_PLAN = {
    position: "SHEEP"
    for position in SW_LIVESTOCK_TILES
}
SW_ALL_COW_PLAN = {
    position: "COW"
    for position in SW_LIVESTOCK_TILES
}

ADAPTIVE_ANIMAL_START_DAY = 12
ADAPTIVE_ANIMAL_LAST_START_DAY = 15
ADAPTIVE_GOOSE_START_DAY = SECOND_QUADRANT_PURCHASE_DAY + 2
# Run the two NE Geese on every seed, not only when the first two shops
# demand Eggs. Egg prices barely respond to demand (51 -> 50 over a season
# without it, 54 -> 52 with it), so the shop gate was protecting a ~6% price
# premium while leaving the birds off half the seeds. Wherever the compact NE
# block also runs, it takes the coexistence layout the Egg seeds already use.
PERMANENT_NE_GEESE = True
# ADAPTIVE_GOOSE_CASH_RESERVE = 800
SW_LIVESTOCK_START_DAY = 12
SW_LIVESTOCK_LAST_START_DAY = 15
SW_LIVESTOCK_HAND_INDEX = 9
ADAPTIVE_MAMMAL_HAND_INDEX = 8
MILK_DEMAND_SHOP_THRESHOLD = 2
WOOL_DEMAND_SHOP_THRESHOLD = 1
SW_MILK_DEMAND_SHOP_THRESHOLD = 1
SW_WOOL_DEMAND_SHOP_THRESHOLD = 1
SW_ALL_SHEEP_SHOP_THRESHOLD = 2
SW_ALL_COW_SHOP_THRESHOLD = 3
SW_LIVESTOCK_MIN_MILK_PRICE = 150
SW_LIVESTOCK_PRODUCT_RETURN_THRESHOLD = 8

# Every position permanently reserved for livestock.
ANIMAL_TILES = COW_TILES + SHEEP_TILES

ANIMAL_PRODUCTS = {
    "COW": "MILK",
    "SHEEP": "WOOL",
    "GOOSE": "EGG",
}

ANIMAL_STRUCTURES = {
    "COW": "PASTURE",
    "SHEEP": "PASTURE",
    "GOOSE": "COOP",
}

ANIMAL_COSTS = {
    "COW": 400,
    "SHEEP": 500,
    "GOOSE": 300,
}

ANIMAL_PRODUCT_ORDER = ("MILK", "WOOL", "EGG")

ANIMAL_HARVEST_THRESHOLD = 1
FERTILIZER_USE_VALUE_MARGIN = 1.20

# Off-day Fertilizer for SW Strawberry. An ongoing crop's yield is computed on
# the night of each production day, and the +1 Fertilizer bonus needs THAT day
# watered. FERTILIZE lasts three days (day .. day+2), so applying it on the off
# day before a production day boosts that night and replaces the off day's
# watering: a plant watered yesterday survives one dry day. Same action count,
# one Fertilizer (sold at ~46-50) per extra Strawberry. SW first
# (offday_fertilize_sw_v1: 34W-6L, +3,945 per game), now NE as well. NE's
# earliest Strawberry is planted on day 7, so its first off day is day 15.
OFFDAY_FERTILIZE_START_DAY = 15
# Plus the four day-5 NW Strawberry: they replace four of the last day-10/11
# plantings (many of them SW, which is boosted), and without the boost they
# gave 4 units a plant instead of up to 8 (seed 14: 9 fewer Strawberry,
# -1,146). They produce on nights 14-20, before the glut, and take their first
# off-day Fertilizer on day 13, ahead of OFFDAY_FERTILIZE_START_DAY.
OFFDAY_FERTILIZE_TILES = frozenset(
    SECOND_QUADRANT_ROUTE
    + THIRD_QUADRANT_ROUTE
    + list(NW_DAY5_STRAWBERRY_TILES)
)
# NE only for its early wave (planted before STRAWBERRY_START_DAY, i.e. the
# day-7 planting), which produces on days 16-22 while Strawberry still sells
# at 220-240. Boosting NE's day-11 wave as well added 37 units on seed 1 but
# earned us nothing (-276 against the baseline mirror): it produces on days
# 20-26, when the shared market is already saturated, so it only took the
# opponent's price (-3,041).
OFFDAY_FERTILIZE_NE_TILES = frozenset(SECOND_QUADRANT_ROUTE)
STRAWBERRY_PRODUCTION_INTERVAL = 2

# All four centre-adjacent positions can access the shed.
SHED_ACCESS_TILES = (
    (4, 4),
    (5, 4),
    (4, 5),
    # (5, 5),
)


# Farm hands
MAX_MARKET_ORDERS_PER_TURN  = 10
NW_HAND_COUNT               = 4           # First quadrant
SECOND_QUADRANT_HAND_COUNT  = 8
THIRD_QUADRANT_HAND_COUNT   = 11
SHEEP_HAND_INDEX            = 0        # The chosen HAND to help with SHEEP
HAND_HIRE_COSTS = (
    1,   # First hand hired today
    1,
    2,
    3,
    5,
    8,
    13,  # Seventh hand
    21,
    34,
    55,
    89,
    144, # Twelfth hand: the SW Wheat block only
)
MARKET_SLOTS_RESERVED_AFTER_HIRING = 3

# SW Wheat block (replays/sw_full_1.json, sw_full_2.json: the ladder opponents
# crop all 25 SW tiles). The seven SW tiles outside THIRD_QUADRANT_ROUTE get
# Wheat, worked by a twelfth hand that does nothing else. Wheat never gluts
# (~48 late in the game), so seven tiles make ~270/day against its 144/day
# hire. The hand never walks to the shed: its harvest goes in with the
# overnight deposit and sells the next morning (on the final day the normal
# liquidation carries it). It is hired from SW unlock while Wheat can still
# be planted (day 25) and after that while any Wheat stands on the block.
SW_WHEAT_BLOCK_ACTIVE = True
SW_WHEAT_BLOCK_TILES = (
    (3, 8), (4, 8),
    (4, 9), (3, 9), (2, 9), (1, 9), (0, 9),
)
SW_WHEAT_BLOCK_HAND_INDEX = THIRD_QUADRANT_HAND_COUNT
SW_WHEAT_BLOCK_LAST_PLANTING_DAY = FINAL_DAY - CROP_CONFIGS["WHEAT"]["harvest_day"]
# Wheat starts at 1 unit and each watering at ages 2-4 adds one, reaching 4 on
# day 4. The hand waters only for yield or survival: not at age 1 (it adds
# nothing, and a plant watered the day before survives a dry day), and not a
# full plant before harvesting it. A cycle is then 4 waterings, a harvest and
# a replant; the generic crop routine spent 6 waterings and lost the far
# tiles to drought (seed 1: the hand is hired at h2 and walks to h6).
SW_WHEAT_BLOCK_MAX_YIELD = 4

# Melon harvest day saturates the NW hands: they clear the opening Melon wave
# and make an extra return trip to bank it, and the western Wheat planted on
# day 6 is left unwatered on the last day of its yield window. Harvested a day
# late it keeps yield 3 instead of 4 (replays/leftover_wheat.json: four tiles).
# One extra hand is hired for that single day, on a fixed route:
#   (4,2), (3,2), (2,2), the freed Melon tiles: plant and water Strawberry;
#   then (1,2), (0,2), (0,1), (0,0): water and harvest Wheat only.
# Planting the western tiles as well does not fit in one day's actions; their
# owners replant them on day 11 as usual.
# Slot nine costs 34 and the roster is re-hired nightly, so it is a one-off.
MELON_RELIEF_HAND_INDEX = SECOND_QUADRANT_HAND_COUNT
MELON_RELIEF_ROW_TILES = (
    (4, 2), (3, 2), (2, 2),
)
MELON_RELIEF_HARVEST_ONLY_TILES = (
    (1, 2), (0, 2), (0, 1), (0, 0),
)
MELON_RELIEF_TILES = MELON_RELIEF_ROW_TILES + MELON_RELIEF_HARVEST_ONLY_TILES
# The route trails the Melon owners through (4,2)-(2,2). Waiting on an
# uncleared Melon tile is abandoned after this hour so the western half of the
# route still gets done.
MELON_RELIEF_WAIT_LAST_HOUR = 12
# Only hire when the day starts with at least this many harvest-ready Wheat on
# the route. The Wheat is the hire's only real payoff: Strawberry planted on
# day 10 still gets four cycles, the same as day 11.
MELON_RELIEF_MIN_READY_WHEAT = 3

# Melon day crew (replays/scaling1.json, scaling2.json). The ladder leaders
# hire all eleven hands on day 10, WATER each Melon before harvesting it (a
# watering inside a one-time crop's window adds a unit on the spot, so a
# 5-unit Melon becomes 6), and sell each hand's batch as it reaches the shed
# from h09. We harvested at 5 with three hands and sold at h14 and h19, after
# them: 60 Melons for 11,261 against their 72 for 16,087.
# On day 10 the three SW hands (indices 8-10) are hired a day early as a
# one-day crew. Crew and Melon owners share the ripe Melon tiles, matched
# nearest-first every turn; each waters to full yield, harvests, and returns
# to sell once carrying a trip's load or when no Melon is left unclaimed.
# Replaces the day-10 relief hand, which needs index 8.
MELON_CREW_ACTIVE = True
MELON_CREW_FIRST_HAND_INDEX = SECOND_QUADRANT_HAND_COUNT
MELON_CREW_HAND_COUNT = THIRD_QUADRANT_HAND_COUNT - SECOND_QUADRANT_HAND_COUNT
# Hand 0 runs the NW Sheep; hands 1-3 own the Melon tiles.
MELON_OWNER_HAND_INDICES = tuple(range(1, NW_HAND_COUNT))
# Two tiles at full yield per trip.
MELON_TRIP_LOAD = 12
# A worker already carrying Melon only takes another tile if the detour
# costs at most this many extra steps on its way back to the shed; otherwise
# it sells what it has. Unrestricted nearest-first pairing sent loaded hands
# from (2,3) to (1,1) and left them seven steps out at h14.
MELON_DETOUR_SLACK = 2
MELON_MAX_YIELD = 6

# List tiles for crops (not reserved for animal)
FIRST_QUADRANT_CROP_TILES = [
    position
    for position in FIRST_QUADRANT_ROUTE
    if position not in COW_TILES
]

SECOND_QUADRANT_CROP_TILES = [
    position
    for position in SECOND_QUADRANT_ROUTE[:SECOND_QUADRANT_TILE_COUNT]
    if position not in COW_TILES
]

THIRD_QUADRANT_CROP_TILES = [
    position
    for position in THIRD_QUADRANT_ROUTE[:THIRD_QUADRANT_TILE_COUNT]
]

# Divide managed tiles amongst farm hands
HAND_WORK_TILES_EACH = [
    FIRST_QUADRANT_CROP_TILES[:5],
    FIRST_QUADRANT_CROP_TILES[5:12],
    FIRST_QUADRANT_CROP_TILES[12:18],
    FIRST_QUADRANT_CROP_TILES[18:],

    SECOND_QUADRANT_CROP_TILES[:6],
    SECOND_QUADRANT_CROP_TILES[6:12],
    SECOND_QUADRANT_CROP_TILES[12:18],
    SECOND_QUADRANT_CROP_TILES[18:],
    
    THIRD_QUADRANT_CROP_TILES[:6],
    THIRD_QUADRANT_CROP_TILES[6:12],
    THIRD_QUADRANT_CROP_TILES[12:18],
]


STRAWBERRY_DEMAND_SHOPS = {
    "BRUNCH_SPOT",
    "ICE_CREAM_SHOP",
    "SMOOTHIE_SHOP",
    "FARMERS_MARKET",
}

MILK_DEMAND_SHOPS = {
    "PIZZA_SHOP",
    "ICE_CREAM_SHOP",
    "SMOOTHIE_SHOP",
}

WOOL_DEMAND_SHOPS = {
    "YARN_STORE",
}

EGG_DEMAND_SHOPS = {
    "BAKERY",
    "BRUNCH_SPOT",
}

#######################################################################################################

# Start the main agent function
def agent(obs):
    '''
    The content of `obs`:
    {
    "player": int,           # 0 or 1
    "day":    int,           # 0-indexed in-game day
    "hour":   int,           # 0-indexed turn within the day
    "farms":  [farm, farm],  # public per-player state, indexed by player id (shared)
    "market": {              # shared
        "inventory": { "WHEAT": int, "CARROT": int, ... },
        "prices":    { "WHEAT": int, "CARROT": int, ... },
    },
    "town": {                # shared
        "unlocked_shops": ["BAKERY", "BAKERY", ...],   # may repeat; each entry consumes independently
    },
    "private": {             # this player only; opponent's private state is not visible
        "shed":        { "WHEAT": int, "GOOSE": int, "FERTILIZER": int, ... },
        "seeds":       { "WHEAT": int, "CARROT": int, ... },
        "inventories": [farmer_inv, hand_inv, ...],  # [0] is the main farmer
    },
    }
    
    The content of tile dict:
    {
        "kind":                 "PLANT",
        "crop":                 "WHEAT" | "CARROT" | "TOMATO" | "STRAWBERRY" | "MELON",
        "planted_day":          int,
        "watered_today":        bool,   # reset to False each end-of-day
        "consecutive_unwatered": int,   # 2+ → tile turns to a weed
        "yield_units":          int,    # units currently harvestable
        "max_lifespan_step":    int,    # step at which decay begins; -1 for ongoing crops
        "fertilized_until_day": int,    # last day fertilizer bonus applies; -1 if none
    }
    
    
    '''
    
    # 1. Get observations and setup
    player_id       = obs["player"]
    farm            = obs["farms"][player_id]
    private         = obs["private"]
    shed            = private["shed"]
    unlocked_shops  = obs["town"]["unlocked_shops"]
    farmer_inventory = private["inventories"][0]
    
    pos_current = tuple(farm["farmer"])
    
    # 1.1 Check shop count to decide which additional animals
    milk_demand_shop_count = sum(
        shop in MILK_DEMAND_SHOPS
        for shop in unlocked_shops
    )

    wool_demand_shop_count = sum(
        shop in WOOL_DEMAND_SHOPS
        for shop in unlocked_shops
    )

    first_two_shops = unlocked_shops[:2]
    first_two_shops_demand_eggs = any(
        shop in EGG_DEMAND_SHOPS
        for shop in first_two_shops
    )
    first_two_shops_include_yarn = any(
        shop in WOOL_DEMAND_SHOPS
        for shop in first_two_shops
    )
    first_two_shops_both_demand_milk = (
        len(first_two_shops) == 2
        and all(
            shop in MILK_DEMAND_SHOPS
            for shop in first_two_shops
        )
    )
    first_two_shops_milk_shop_count = sum(
        shop in MILK_DEMAND_SHOPS
        for shop in first_two_shops
    )
    # Openings whose prefix shows Milk demand but no Yarn or Egg demand leave
    # the compact NE block in crops and defer every extra animal to the day-12
    # SW decision.  Route them to the existing all-Cow NE plan instead; timing,
    # hand ownership and service routes are unchanged.
    first_two_shops_milk_only = (
        first_two_shops_milk_shop_count
            >= EARLY_NE_SINGLE_MILK_SHOP_THRESHOLD
        and not first_two_shops_include_yarn
        and not first_two_shops_demand_eggs
    )

    # The Goose branch is decided first: the compact NE block's tile layout
    # depends on whether the Geese are also running, so this can no longer be
    # resolved after the NE block the way it used to be.
    existing_adaptive_geese = []
    adaptive_goose_setup_started = False

    for position in ADAPTIVE_GOOSE_TILES + NE_COEXIST_GOOSE_TILES:
        x, y = position
        tile = farm["tiles"][y][x]

        if (
            isinstance(tile, dict)
            and tile.get("kind") in ANIMAL_STRUCTURES.values()
        ):
            adaptive_goose_setup_started = True

            if tile.get("animal") == "GOOSE":
                existing_adaptive_geese.append("GOOSE")
            elif tile.get("kind") == "COOP":
                # Keep the Goose branch after setup even if a Goose escapes.
                existing_adaptive_geese.append("GOOSE")

    adaptive_goose_selected = (
        PERMANENT_NE_GEESE
        or bool(existing_adaptive_geese)
        or first_two_shops_demand_eggs
    )

    # Latch onto whichever block is already on the ground; only the tiles
    # unique to each layout can distinguish them.
    def ne_block_pasture_exists(positions):
        for x, y in positions:
            tile = farm["tiles"][y][x]
            if isinstance(tile, dict) and tile.get("kind") == "PASTURE":
                return True
        return False

    if ne_block_pasture_exists(EARLY_NE_DEFAULT_ONLY_TILES):
        active_early_ne_livestock_tiles = EARLY_NE_LIVESTOCK_TILES
    elif ne_block_pasture_exists(EARLY_NE_COEXIST_ONLY_TILES):
        active_early_ne_livestock_tiles = (
            EARLY_NE_GOOSE_COEXIST_LIVESTOCK_TILES
        )
    elif adaptive_goose_selected:
        active_early_ne_livestock_tiles = (
            EARLY_NE_GOOSE_COEXIST_LIVESTOCK_TILES
        )
    else:
        active_early_ne_livestock_tiles = EARLY_NE_LIVESTOCK_TILES

    early_ne_all_sheep_plan = {
        position: "SHEEP"
        for position in active_early_ne_livestock_tiles
    }
    early_ne_all_cow_plan = {
        position: "COW"
        for position in active_early_ne_livestock_tiles
    }

    existing_early_ne_animals_by_position = {}
    early_ne_livestock_setup_started = False

    for position in active_early_ne_livestock_tiles:
        x, y = position
        tile = farm["tiles"][y][x]

        if (
            isinstance(tile, dict)
            and tile.get("kind") == "PASTURE"
        ):
            early_ne_livestock_setup_started = True
            if tile.get("animal") in ("COW", "SHEEP"):
                existing_early_ne_animals_by_position[position] = (
                    tile["animal"]
                )

    early_ne_livestock_selected = (
        early_ne_livestock_setup_started
        or (
            len(first_two_shops) == 2
            and (
                first_two_shops_include_yarn
                or first_two_shops_both_demand_milk
                or first_two_shops_milk_only
            )
        )
    )

    # With the NE block running, the Geese take the west-column tiles so the
    # block keeps its tiles beside the shed. Decided from the shop prefix
    # alone, so the reservation is stable from the NE unlock onwards.
    active_goose_tiles = (
        NE_COEXIST_GOOSE_TILES
        if adaptive_goose_selected and early_ne_livestock_selected
        else ADAPTIVE_GOOSE_TILES
    )

    if existing_early_ne_animals_by_position:
        existing_early_ne_animal_types = set(
            existing_early_ne_animals_by_position.values()
        )
        if existing_early_ne_animal_types == {"SHEEP"}:
            active_early_ne_livestock_plan = early_ne_all_sheep_plan
        elif existing_early_ne_animal_types == {"COW"}:
            active_early_ne_livestock_plan = early_ne_all_cow_plan
        elif first_two_shops_include_yarn:
            active_early_ne_livestock_plan = early_ne_all_sheep_plan
        else:
            active_early_ne_livestock_plan = early_ne_all_cow_plan
    elif first_two_shops_include_yarn:
        active_early_ne_livestock_plan = early_ne_all_sheep_plan
    else:
        active_early_ne_livestock_plan = early_ne_all_cow_plan

    first_four_shops = unlocked_shops[:4]

    first_shop_yarn_sheep_condition = (
        len(first_four_shops) == 4
        and first_four_shops[0] == "YARN_STORE"
        and sum(
            shop in MILK_DEMAND_SHOPS
            for shop in first_four_shops
        ) < SW_ALL_COW_SHOP_THRESHOLD
    )

    sw_all_cow_condition = (
        milk_demand_shop_count >= SW_ALL_COW_SHOP_THRESHOLD
    )

    sw_all_sheep_condition = (
        first_shop_yarn_sheep_condition
        or wool_demand_shop_count >= SW_ALL_SHEEP_SHOP_THRESHOLD
    )

    existing_adaptive_mammals = []
    adaptive_mammal_setup_started = False

    for position in ADAPTIVE_MAMMAL_TILES:
        x, y = position
        tile = farm["tiles"][y][x]

        if (
            isinstance(tile, dict)
            and tile.get("kind") == "PASTURE"
        ):
            adaptive_mammal_setup_started = True

            if tile.get("animal") in ("COW", "SHEEP"):
                existing_adaptive_mammals.append(tile["animal"])

    sw_livestock_setup_started = False
    sw_pasture_count = 0
    existing_sw_animals_by_position = {}

    for position in SW_LIVESTOCK_TILES:
        x, y = position
        tile = farm["tiles"][y][x]
        if (
            isinstance(tile, dict)
            and tile.get("kind") == "PASTURE"
        ):
            sw_pasture_count += 1
            if position in SW_LIVESTOCK_OUTER_TILES:
                sw_livestock_setup_started = True
            if tile.get("animal") in ("COW", "SHEEP"):
                existing_sw_animals_by_position[position] = tile["animal"]

    locked_sw_livestock_plan = None
    if sw_pasture_count == len(SW_LIVESTOCK_TILES):
        # Once all four SW pastures exist, preserve the established animal
        # allocation. Later shop unlocks must not turn escaped Sheep into Cows
        # (or vice versa).
        if len(existing_sw_animals_by_position) == len(SW_LIVESTOCK_TILES):
            for candidate_plan in (
                SW_ALL_SHEEP_PLAN,
                SW_ALL_COW_PLAN,
                SW_LIVESTOCK_PLAN,
            ):
                if existing_sw_animals_by_position == candidate_plan:
                    locked_sw_livestock_plan = candidate_plan
                    break

        if locked_sw_livestock_plan is None:
            # Empty pastures can remain after an animal escapes. Reconstruct
            # the plan from the earliest shop prefix that could have activated
            # the branch, rather than from later shops.
            for shop_count in range(4, len(unlocked_shops) + 1):
                shop_prefix = unlocked_shops[:shop_count]
                prefix_milk_count = sum(
                    shop in MILK_DEMAND_SHOPS
                    for shop in shop_prefix
                )
                prefix_wool_count = sum(
                    shop in WOOL_DEMAND_SHOPS
                    for shop in shop_prefix
                )
                prefix_yarn_first = (
                    shop_prefix[0] == "YARN_STORE"
                    and sum(
                        shop in MILK_DEMAND_SHOPS
                        for shop in shop_prefix[:4]
                    ) < SW_ALL_COW_SHOP_THRESHOLD
                )

                if prefix_yarn_first:
                    locked_sw_livestock_plan = SW_ALL_SHEEP_PLAN
                elif prefix_milk_count >= SW_ALL_COW_SHOP_THRESHOLD:
                    locked_sw_livestock_plan = SW_ALL_COW_PLAN
                elif prefix_wool_count >= SW_ALL_SHEEP_SHOP_THRESHOLD:
                    locked_sw_livestock_plan = SW_ALL_SHEEP_PLAN
                elif (
                    prefix_milk_count >= SW_MILK_DEMAND_SHOP_THRESHOLD
                    and prefix_wool_count >= SW_WOOL_DEMAND_SHOP_THRESHOLD
                ):
                    locked_sw_livestock_plan = SW_LIVESTOCK_PLAN

                if locked_sw_livestock_plan is not None:
                    break

    if locked_sw_livestock_plan is not None:
        active_sw_livestock_plan = locked_sw_livestock_plan
    elif first_shop_yarn_sheep_condition:
        active_sw_livestock_plan = SW_ALL_SHEEP_PLAN
    elif sw_all_cow_condition:
        active_sw_livestock_plan = SW_ALL_COW_PLAN
    elif wool_demand_shop_count >= SW_ALL_SHEEP_SHOP_THRESHOLD:
        active_sw_livestock_plan = SW_ALL_SHEEP_PLAN
    else:
        active_sw_livestock_plan = SW_LIVESTOCK_PLAN

    sw_mixed_livestock_condition = (
        milk_demand_shop_count >= SW_MILK_DEMAND_SHOP_THRESHOLD
        and wool_demand_shop_count >= SW_WOOL_DEMAND_SHOP_THRESHOLD
        and obs["market"]["prices"]["MILK"] >= SW_LIVESTOCK_MIN_MILK_PRICE
    )

    # The full four-animal SW branch excludes only the smaller SW mammal pair.
    # NE Geese are independent and can run alongside either SW plan. The full
    # branch builds an outer tile first, which permanently marks its selection.
    sw_livestock_selected = (
        sw_livestock_setup_started
        or (
            THIRD_QUADRANT_NAME in farm["unlocked_quadrants"]
            and (
                sw_all_cow_condition
                or sw_all_sheep_condition
                or sw_mixed_livestock_condition
            )
            and not adaptive_mammal_setup_started
            and not early_ne_livestock_selected
            and obs["day"] <= SW_LIVESTOCK_LAST_START_DAY
        )
    )

    if existing_adaptive_mammals:
        adaptive_mammal_type = existing_adaptive_mammals[0]
    elif wool_demand_shop_count >= WOOL_DEMAND_SHOP_THRESHOLD:
        adaptive_mammal_type = "SHEEP"
    elif milk_demand_shop_count >= MILK_DEMAND_SHOP_THRESHOLD:
        adaptive_mammal_type = "COW"
    else:
        adaptive_mammal_type = None

    # Sheep tiles remain crop tiles until their opening crops have been cleared.
    def sheep_group_is_active(positions, start_day):
        target_tiles = [
            farm["tiles"][y][x]
            for x, y in positions
        ]

        is_setup_started = any(
            isinstance(tile, dict)
            and tile.get("kind") == "PASTURE"
            for tile in target_tiles
        )

        is_tiles_ready = all(
            tile is None
            or (
                isinstance(tile, dict)
                and tile.get("kind") == "WEED"
            )
            for tile in target_tiles
        )

        return (
            is_setup_started
            or (obs["day"] >= start_day and is_tiles_ready)
        )


    early_sheep_phase_active = sheep_group_is_active(
        EARLY_SHEEP_TILES,
        EARLY_SHEEP_START_DAY,
    )
    delayed_sheep_phase_active = sheep_group_is_active(
        DELAYED_SHEEP_TILES,
        DELAYED_SHEEP_START_DAY,
    )
    day4_additional_sheep_phase_active = sheep_group_is_active(
        DAY4_ADDITIONAL_SHEEP_TILES,
        DAY4_ADDITIONAL_SHEEP_START_DAY,
    )
    day11_additional_sheep_phase_active = sheep_group_is_active(
        DAY11_ADDITIONAL_SHEEP_TILES,
        DAY11_ADDITIONAL_SHEEP_START_DAY,
    )

    def animal_is_placed(position, expected_animal):
        x, y = position
        tile = farm["tiles"][y][x]

        return (
            isinstance(tile, dict)
            and tile.get("kind") == ANIMAL_STRUCTURES[expected_animal]
            and tile.get("animal") == expected_animal
        )

    staged_cow_setup_started = any(
        isinstance(farm["tiles"][y][x], dict)
        and farm["tiles"][y][x].get("kind") == "PASTURE"
        for x, y in STAGED_COW_TILES
    )
    expansion_cow_setup_complete = all(
        animal_is_placed(position, "COW")
        for position in EXPANSION_COW_TILES[:EXPANSION_COW_COUNT]
    )
    staged_cow_selected = (
        milk_demand_shop_count >= STAGED_COW_MILK_SHOP_THRESHOLD
    )
    staged_cow_tile_is_ready = all(
        farm["tiles"][y][x] is None
        or (
            isinstance(farm["tiles"][y][x], dict)
            and farm["tiles"][y][x].get("kind") in {"WEED", "PASTURE"}
        )
        for x, y in STAGED_COW_TILES
    )
    # A staged Cow bought late on the last start day can reach midnight with
    # its Pasture unbuilt; the phase then lapses and the Cow sits in the shed
    # for the rest of the game (seed 11: bought d10 h18, never placed). The
    # Pasture is what normally latches the phase, so latch it here as well,
    # on the next day only, for a Cow already bought. Nothing else buys Cows
    # on day 11 -- SW and adaptive livestock start on day 12, the expansion and
    # NE-block Cows are placed by day 9 -- so an unplaced Cow then, with every
    # other Cow plan complete, is the stranded staged one. Seeds whose Pasture
    # went up in time latch through the existing path and are unchanged.
    unplaced_cows = (
        shed.get("COW", 0)
        + sum(
            inventory.get("COW", 0)
            for inventory in private["inventories"]
        )
    )
    early_ne_cows_complete = (
        not early_ne_livestock_selected
        or all(
            isinstance(farm["tiles"][y][x], dict)
            and farm["tiles"][y][x].get("animal")
            for x, y in active_early_ne_livestock_tiles
        )
    )
    stranded_staged_cow = (
        obs["day"] == STAGED_COW_LAST_START_DAY + 1
        and staged_cow_selected
        and staged_cow_tile_is_ready
        and expansion_cow_setup_complete
        and early_ne_cows_complete
        and unplaced_cows > 0
    )
    staged_cow_phase_active = (
        staged_cow_setup_started
        or stranded_staged_cow
        or (
            staged_cow_selected
            and SECOND_QUADRANT_NAME in farm["unlocked_quadrants"]
            and STAGED_COW_START_DAY
                <= obs["day"]
                <= STAGED_COW_LAST_START_DAY
            and expansion_cow_setup_complete
            and staged_cow_tile_is_ready
        )
    )
    staged_cow_tile_is_reserved = (
        staged_cow_setup_started
        or stranded_staged_cow
        or (
            staged_cow_selected
            and SECOND_QUADRANT_NAME in farm["unlocked_quadrants"]
            and STAGED_COW_START_DAY
                <= obs["day"]
                <= STAGED_COW_LAST_START_DAY
        )
    )

    # Initial COWs are active from the opening.
    active_animal_plan = {
        position: "COW"
        for position in INITIAL_COW_TILES
    }

    # SHEEP activate only after their former crop tiles are available.
    if early_sheep_phase_active:
        active_animal_plan.update({
            position: "SHEEP"
            for position in EARLY_SHEEP_TILES
        })

    if delayed_sheep_phase_active:
        active_animal_plan.update({
            position: "SHEEP"
            for position in DELAYED_SHEEP_TILES
        })

    if day4_additional_sheep_phase_active:
        active_animal_plan.update({
            position: "SHEEP"
            for position in DAY4_ADDITIONAL_SHEEP_TILES
        })

    if day11_additional_sheep_phase_active:
        active_animal_plan.update({
            position: "SHEEP"
            for position in DAY11_ADDITIONAL_SHEEP_TILES
        })

    if staged_cow_phase_active:
        active_animal_plan.update({
            position: "COW"
            for position in STAGED_COW_TILES
        })

    # When second and third quadrants are unlocked, add more animal tiles
    if (SECOND_QUADRANT_NAME in farm["unlocked_quadrants"]
            and obs["day"] >= EXPANSION_COW_START_DAY):
        active_animal_plan.update({
            position: "COW"
            for position in EXPANSION_COW_TILES[:EXPANSION_COW_COUNT]
        })
    
    base_animal_setup_complete = (
        all(
            animal_is_placed(position, "COW")
            for position in COW_TILES
        )
        and all(
            animal_is_placed(position, "SHEEP")
            for position in SHEEP_TILES
        )
        and (
            not staged_cow_phase_active
            or all(
                animal_is_placed(position, "COW")
                for position in STAGED_COW_TILES
            )
        )
    )

    sw_livestock_phase_active = (
        sw_livestock_selected
        and base_animal_setup_complete
        and (
            sw_livestock_setup_started
            or obs["day"] >= SW_LIVESTOCK_START_DAY
        )
    )

    adaptive_goose_phase_active = (
        SECOND_QUADRANT_NAME in farm["unlocked_quadrants"]
        and adaptive_goose_selected
        and obs["day"] >= ADAPTIVE_GOOSE_START_DAY
    )
    adaptive_mammal_phase_active = (
        THIRD_QUADRANT_NAME in farm["unlocked_quadrants"]
        and adaptive_mammal_type is not None
        and not sw_livestock_selected
        and not early_ne_livestock_selected
        and base_animal_setup_complete
        and (
            adaptive_mammal_setup_started
            or (
                ADAPTIVE_ANIMAL_START_DAY
                <= obs["day"]
                <= ADAPTIVE_ANIMAL_LAST_START_DAY
            )
        )
    )
    adaptive_goose_tiles_reserved = (
        SECOND_QUADRANT_NAME in farm["unlocked_quadrants"]
        and adaptive_goose_selected
    )
    early_ne_livestock_tiles_reserved = (
        SECOND_QUADRANT_NAME in farm["unlocked_quadrants"]
        and early_ne_livestock_selected
    )
    early_ne_livestock_construction_phase_active = (
        early_ne_livestock_tiles_reserved
        and obs["day"] >= EARLY_NE_LIVESTOCK_PASTURE_START_DAY
    )
    early_ne_livestock_phase_active = (
        early_ne_livestock_tiles_reserved
        and obs["day"] >= EARLY_NE_LIVESTOCK_START_DAY
        and (
            early_ne_livestock_setup_started
            or expansion_cow_setup_complete
        )
    )
    # With the compact NE block running alongside the Geese, the farmer must
    # keep its baseline animal round. Handing it the second Goose at (6,3)
    # pushed its Cow-milk collection and shed deposit from hour ~15 to hour
    # ~21 every day; on Milk's glutted price curve that six-hour slip cost
    # more (-2554 on Milk+Wool, seed 6) than the Eggs earned. Give both Goose
    # tiles to the Goose hand instead and leave the farmer untouched.
    early_ne_goose_coexist_active = (
        adaptive_goose_phase_active
        and early_ne_livestock_tiles_reserved
    )
    if early_ne_goose_coexist_active:
        goose_hand_tile_by_index = dict(NE_COEXIST_GOOSE_OWNERSHIP)
    else:
        goose_hand_tile_by_index = {GOOSE_HAND_INDEX: (GOOSE_HAND_TILE,)}

    # Every tile a hand owns is a tile the farmer must leave alone.
    goose_hand_tiles = tuple(
        tile
        for hand_tiles in goose_hand_tile_by_index.values()
        for tile in hand_tiles
    )

    adaptive_mammal_tiles_reserved = (
        THIRD_QUADRANT_NAME in farm["unlocked_quadrants"]
        and adaptive_mammal_type is not None
        and not sw_livestock_selected
        and not early_ne_livestock_selected
        and obs["day"] >= ADAPTIVE_ANIMAL_START_DAY
    )
    sw_livestock_tiles_reserved = sw_livestock_selected

    reserved_adaptive_animal_tiles = set()
    if staged_cow_tile_is_reserved:
        reserved_adaptive_animal_tiles.update(STAGED_COW_TILES)
    if adaptive_goose_tiles_reserved:
        reserved_adaptive_animal_tiles.update(active_goose_tiles)
    if early_ne_livestock_tiles_reserved:
        reserved_adaptive_animal_tiles.update(
            active_early_ne_livestock_tiles
        )
    if sw_livestock_tiles_reserved:
        reserved_adaptive_animal_tiles.update(SW_LIVESTOCK_TILES)
    elif adaptive_mammal_tiles_reserved:
        reserved_adaptive_animal_tiles.update(ADAPTIVE_MAMMAL_TILES)

    if adaptive_goose_phase_active:
        active_animal_plan.update({
            position: "GOOSE"
            for position in active_goose_tiles
        })

    active_adaptive_mammal_plan = {}
    if adaptive_mammal_phase_active:
        active_adaptive_mammal_plan = {
            position: adaptive_mammal_type
            for position in ADAPTIVE_MAMMAL_TILES
        }
        active_animal_plan.update(active_adaptive_mammal_plan)

    active_sw_service_plan = {}
    if early_ne_livestock_construction_phase_active:
        active_sw_service_plan = active_early_ne_livestock_plan

    if early_ne_livestock_phase_active:
        active_animal_plan.update(active_early_ne_livestock_plan)
    elif active_adaptive_mammal_plan:
        active_sw_service_plan = active_adaptive_mammal_plan

    if sw_livestock_phase_active:
        active_animal_plan.update(active_sw_livestock_plan)
        active_sw_service_plan = active_sw_livestock_plan

    sw_hand_livestock_phase_active = bool(active_sw_service_plan)
    if sw_livestock_phase_active:
        active_sw_livestock_hand_index = SW_LIVESTOCK_HAND_INDEX
    elif early_ne_livestock_construction_phase_active:
        active_sw_livestock_hand_index = (
            NE_COEXIST_LIVESTOCK_HAND_INDEX
            if early_ne_goose_coexist_active
            else EARLY_NE_LIVESTOCK_HAND_INDEX
        )
    else:
        active_sw_livestock_hand_index = ADAPTIVE_MAMMAL_HAND_INDEX
    
    active_animal_tiles = list(active_animal_plan)
    animal_count_target = len(active_animal_tiles)
    
    # Reassign the SW hands once the compact livestock block activates.
    current_hand_work_tiles_each = [
        list(positions)
        for positions in HAND_WORK_TILES_EACH
    ]

    if early_ne_livestock_construction_phase_active:
        remaining_ne_crop_tiles = [
            position
            for position in SECOND_QUADRANT_CROP_TILES
            if position not in reserved_adaptive_animal_tiles
        ]
        first_ne_route_size = 5 if adaptive_goose_phase_active else 6

        if early_ne_goose_coexist_active:
            ne_livestock_index = NE_COEXIST_LIVESTOCK_HAND_INDEX
            ne_crop_index = (
                GOOSE_HAND_INDEX
                if NE_COEXIST_LIVESTOCK_HAND_INDEX != GOOSE_HAND_INDEX
                else EARLY_NE_LIVESTOCK_HAND_INDEX
            )
        else:
            ne_livestock_index = EARLY_NE_LIVESTOCK_HAND_INDEX
            ne_crop_index = GOOSE_HAND_INDEX

        current_hand_work_tiles_each[ne_crop_index] = (
            remaining_ne_crop_tiles[:first_ne_route_size]
        )
        current_hand_work_tiles_each[ne_livestock_index] = []
        current_hand_work_tiles_each[6] = (
            remaining_ne_crop_tiles[
                first_ne_route_size:first_ne_route_size + 6
            ]
        )
        current_hand_work_tiles_each[7] = (
            remaining_ne_crop_tiles[first_ne_route_size + 6:]
        )

        if early_ne_goose_coexist_active:
            reassigned_tiles = (
                set(NE_COEXIST_CROP_TILE_OWNERS)
                | set(NE_COEXIST_UNMANAGED_TILES)
            )

            for hand_tiles in current_hand_work_tiles_each:
                for position in reassigned_tiles:
                    if position in hand_tiles:
                        hand_tiles.remove(position)

            for position, owner_index in NE_COEXIST_CROP_TILE_OWNERS.items():
                owner_tiles = current_hand_work_tiles_each[owner_index]

                if position not in owner_tiles:
                    owner_tiles.append(position)

    if sw_livestock_phase_active:
        remaining_sw_crop_tiles = [
            position
            for position in THIRD_QUADRANT_CROP_TILES
            if position not in active_sw_service_plan
        ]

        current_hand_work_tiles_each[8] = remaining_sw_crop_tiles[:6]
        current_hand_work_tiles_each[9] = []
        current_hand_work_tiles_each[10] = remaining_sw_crop_tiles[6:]
    elif active_adaptive_mammal_plan:
        current_hand_work_tiles_each[8] = [
            (2, 5), (2, 6),
            (3, 6), (4, 6),
        ]
        current_hand_work_tiles_each[9] = [
            (1, 5), (0, 5),
            (0, 6), (1, 6),
            (0, 7), (1, 7),
        ]
        current_hand_work_tiles_each[10] = [
            (2, 7), (3, 7), (4, 7),
            (0, 8), (1, 8), (2, 8),
        ]


    # Melon harvest day only (NE unlocked, SW not, so index 8 is unused).
    # The tiles stay with their usual owners as well: the relief hand works
    # them on its own fixed route and never takes over the Melon round-trip.
    melon_relief_ready_wheat = 0
    for x, y in MELON_RELIEF_TILES:
        relief_tile = farm["tiles"][y][x]
        if (
            isinstance(relief_tile, dict)
            and relief_tile.get("kind") == "PLANT"
            and relief_tile.get("crop") == "WHEAT"
            and obs["day"] - relief_tile["planted_day"]
                >= CROP_CONFIGS["WHEAT"]["harvest_day"]
        ):
            melon_relief_ready_wheat += 1

    # Decided once, when the day's roster is hired: the roster resets every
    # night, so a hand at this index means the hire already happened today.
    # Without that latch the count falls as the relief hand harvests, and the
    # gate would switch off with the route half done.
    melon_relief_already_hired = (
        len(farm["hands"]) > MELON_RELIEF_HAND_INDEX
    )
    melon_crew_active = (
        MELON_CREW_ACTIVE
        and obs["day"] == MELON_HARVEST_DAY
        and SECOND_QUADRANT_NAME in farm["unlocked_quadrants"]
        and THIRD_QUADRANT_NAME not in farm["unlocked_quadrants"]
    )
    melon_relief_hand_active = (
        not MELON_CREW_ACTIVE
        and obs["day"] == MELON_HARVEST_DAY
        and SECOND_QUADRANT_NAME in farm["unlocked_quadrants"]
        and THIRD_QUADRANT_NAME not in farm["unlocked_quadrants"]
        and (
            melon_relief_already_hired
            or melon_relief_ready_wheat >= MELON_RELIEF_MIN_READY_WHEAT
        )
    )

    if melon_relief_hand_active:
        current_hand_work_tiles_each[MELON_RELIEF_HAND_INDEX] = list(
            MELON_RELIEF_TILES
        )

    # Create a list of work tiles of the farm hands
    active_hand_work_tiles = []
    for hand_index in range(
            min(len(farm["hands"]), len(current_hand_work_tiles_each))
    ):
        active_hand_work_tiles.extend(
            current_hand_work_tiles_each[hand_index]
        )
    
       
    # 1.2 Count number of HANDs
    if THIRD_QUADRANT_NAME in farm["unlocked_quadrants"]:
        hands_to_hire_today = THIRD_QUADRANT_HAND_COUNT
    elif SECOND_QUADRANT_NAME in farm["unlocked_quadrants"]:
        hands_to_hire_today = SECOND_QUADRANT_HAND_COUNT
    else:
        hands_to_hire_today = NW_HAND_COUNT

    if melon_relief_hand_active:
        hands_to_hire_today = MELON_RELIEF_HAND_INDEX + 1

    if melon_crew_active:
        hands_to_hire_today = (
            MELON_CREW_FIRST_HAND_INDEX + MELON_CREW_HAND_COUNT
        )

    sw_wheat_block_plants = sum(
        1
        for x, y in SW_WHEAT_BLOCK_TILES
        if (
            isinstance(farm["tiles"][y][x], dict)
            and farm["tiles"][y][x].get("kind") == "PLANT"
        )
    )
    sw_wheat_block_active = (
        SW_WHEAT_BLOCK_ACTIVE
        and THIRD_QUADRANT_NAME in farm["unlocked_quadrants"]
        and (
            obs["day"] <= SW_WHEAT_BLOCK_LAST_PLANTING_DAY
            or sw_wheat_block_plants > 0
        )
    )
    # Tiles still waiting for a Wheat seed (empty or weeded).
    sw_wheat_block_pending = (
        len(SW_WHEAT_BLOCK_TILES) - sw_wheat_block_plants
        if (
            sw_wheat_block_active
            and obs["day"] <= SW_WHEAT_BLOCK_LAST_PLANTING_DAY
        )
        else 0
    )

    if sw_wheat_block_active:
        hands_to_hire_today = max(
            hands_to_hire_today,
            SW_WHEAT_BLOCK_HAND_INDEX + 1,
        )
            
    # Inventory count in the shed and in the backpack (dictionaries, one entry for each crop)
    seed_counts     = {
        crop: private["seeds"].get(crop, 0)
        for crop in CROPS_MANAGED
    }
    
    shed_counts     = {
        crop: shed.get(crop, 0)
        for crop in CROPS_MANAGED
    }

    backpack_counts = {
        crop: farmer_inventory.get(crop, 0)
        for crop in CROPS_MANAGED
    }
    
    # Check shop counts to decide crops to plant
    strawberry_shop_count = sum(
        shop in STRAWBERRY_DEMAND_SHOPS
        for shop in obs["town"]["unlocked_shops"]
    )

    tomato_shop_count = sum(
        shop in TOMATO_DEMAND_SHOPS
        for shop in obs["town"]["unlocked_shops"]
    )

    tomato_plant_target = (
            tomato_shop_count
            if tomato_shop_count > 1
    else 0)

    third_quadrant_strawberry_bonus = 0

    sw_bonus_tile_is_empty = any(
        farm["tiles"][y][x] is None
        for x, y in THIRD_QUADRANT_CROP_TILES[12:18]
    )
    
    if (THIRD_QUADRANT_NAME in farm["unlocked_quadrants"]
            and strawberry_shop_count >= SW_STRAWBERRY_SHOP_THRESHOLD
            and sw_bonus_tile_is_empty
            and obs["day"] <= STRAWBERRY_LAST_PLANTING_DAY ):
        third_quadrant_strawberry_bonus = THIRD_QUADRANT_STRAWBERRY_BONUS

    requested_strawberry_target = (
        HIGH_STRAWBERRY_PLANT_TARGET
        if strawberry_shop_count >= HIGH_STRAWBERRY_SHOP_THRESHOLD
        else STRAWBERRY_PLANT_TARGET
    )

    requested_strawberry_target += third_quadrant_strawberry_bonus

    premium_crop_plant_target = (
        PREMIUM_CROP_PLANT_TARGET
        + third_quadrant_strawberry_bonus
    )

    strawberry_plant_target = min(
        requested_strawberry_target,
        premium_crop_plant_target - tomato_plant_target,
    )
    
    
    # Initialise important variables
    market_orders = []
    farmer_action = ["PASS"]
    
    ####
    # 2. Define helper functions
    
    ## 2.1 Moving logic
    def move_to(current,target):
        x_curr,y_curr = current
        x_targ,y_targ = target
        
        if x_curr > x_targ:
           return ["WEST"]
        if x_curr < x_targ:
            return ["EAST"]
        if y_curr > y_targ:
            return ["NORTH"]
        if y_curr < y_targ:
            return ["SOUTH"]
        
        return ["PASS"]
        
    ## 2.2 Convert position (x,y) to tile [y][x]
    def tile_at(farm,pos):
        x,y = pos
        tile = farm["tiles"][y][x] 
        
        return tile 
    
    ## 2.3 Distance calculator between two tiles
    def distance_between(coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2

        dist_manhattan = abs(x1 - x2) + abs(y1 - y2)
        
        return dist_manhattan
    
    ## 2.4 Find closest actionable tile to current position
    def nearest_position(current, positions):
        pos_nearest = None
        nearest_distance = None

        for position in positions:
            distance = distance_between(current, position)

            if pos_nearest is None or distance < nearest_distance:
                pos_nearest = position
                nearest_distance = distance

        return pos_nearest
    
    ## 2.5 Count a specific crop type in a farm (primarily to inspect opponent's crop)
    def count_crop_plants(farm_to_check, crop):
        plant_count = 0
        
        # Loope through every tile in the chosen farm
        for row in farm_to_check["tiles"]:
            for tile in row:
                if (isinstance(tile, dict)
                        and tile.get("kind") == "PLANT"
                        and tile.get("crop") == crop):
                    
                    plant_count += 1
                    
        return plant_count

    # Give only the newly hired northeast hands an early Strawberry wave.
    # The normal farm-wide Strawberry allocation still begins on day 10.
    # Counted on NE's own tiles, like the NW wave below: with a farm-wide
    # count, Strawberry already growing in NW would use up NE's target.
    our_ne_strawberries = sum(
        1
        for position in SECOND_QUADRANT_CROP_TILES
        if (
            isinstance(tile_at(farm, position), dict)
            and tile_at(farm, position).get("crop") == "STRAWBERRY"
        )
    )
    # Every NE crop tile the animals do not need. The live Strawberry cap
    # (strawberry_plant_target) still bounds the season's total, so this moves
    # Strawberry earlier rather than adding more: each extra NE tile today is
    # one fewer NW/SW planting on day 10-11.
    early_ne_strawberry_target = sum(
        1
        for position in SECOND_QUADRANT_CROP_TILES
        if position not in reserved_adaptive_animal_tiles
    )
    early_ne_strawberry_phase_active = (
        SECOND_QUADRANT_NAME in farm["unlocked_quadrants"]
        and EARLY_NE_STRAWBERRY_START_DAY
            <= obs["day"]
            < STRAWBERRY_START_DAY
        and our_ne_strawberries < early_ne_strawberry_target
    )

    # Give the original northwest hands their own early Strawberry wave once
    # NE is unlocked, recycling mature staple-crop tiles instead of always
    # replanting the same staple. Gated on NE already being unlocked so this
    # never competes with the NE land/animal purchase's own cash reserve.
    # Counted on NW's own tiles specifically (not the farm-wide total used by
    # early_ne_strawberry_phase_active above) so the two early waves cannot
    # starve each other's target through a shared counter.
    our_nw_strawberries = sum(
        1
        for position in FIRST_QUADRANT_CROP_TILES
        if (
            isinstance(tile_at(farm, position), dict)
            and tile_at(farm, position).get("crop") == "STRAWBERRY"
        )
    )
    nw_day5_strawberry_pending = sum(
        1
        for x, y in NW_DAY5_STRAWBERRY_TILES
        if (
            farm["tiles"][y][x] is None
            or (
                isinstance(farm["tiles"][y][x], dict)
                and farm["tiles"][y][x].get("kind") == "WEED"
            )
        )
    )
    nw_day5_strawberry_phase_active = (
        NW_DAY5_STRAWBERRY_START_DAY
            <= obs["day"]
            <= NW_DAY5_STRAWBERRY_LAST_DAY
        and nw_day5_strawberry_pending > 0
    )

    early_nw_strawberry_phase_active = (
        SECOND_QUADRANT_NAME in farm["unlocked_quadrants"]
        and obs["day"] < STRAWBERRY_START_DAY
        and our_nw_strawberries < EARLY_NW_STRAWBERRY_TARGET
    )

    ## 2.6 Detect if crop is harvestable, incorporating yield_units to support multi-harvest crops
    def crop_is_harvestable(tile):
        if (not isinstance(tile, dict)
                or tile.get("kind") != "PLANT"
                or tile.get("crop") not in CROPS_MANAGED):
            return False

        crop = tile["crop"]
        crop_config = CROP_CONFIGS[crop]

        if crop_config["ongoing"]:
            return tile.get("yield_units", 0) > 0

        crop_age = obs["day"] - tile["planted_day"]

        return crop_age >= crop_config["harvest_day"]
    
    ## 2.6
    def crop_profit_per_day(crop):
        crop_config     = CROP_CONFIGS[crop]
        current_price   = obs["market"]["prices"][crop]

        expected_revenue    = (crop_config["harvest_yield"] * current_price)
        expected_profit     = (expected_revenue - crop_config["seed_cost"])

        return expected_profit / crop_config["harvest_day"]
    
    
    def choose_melon_plant_target():
        opponent_id = 1 - player_id
        opponent_farm = obs["farms"][opponent_id]
        opponent_melons = count_crop_plants(opponent_farm, "MELON")
        opponent_carrots = count_crop_plants(opponent_farm, "CARROT")
        current_melon_price = obs["market"]["prices"]["MELON"]

        if current_melon_price < MELON_REPLANT_PRICE_THRESHOLD:
            target_melons = POST_GLUT_MELON_TARGET
        elif opponent_melons == 0:
            target_melons = 15
        elif opponent_carrots > 0 and opponent_melons <= 10:
            target_melons = 13
        else:
            target_melons = HEAVY_OPPONENT_MELON_TARGET

        if obs["day"] == 0:
            target_melons = min(target_melons, DAY0_MELON_TARGET)

        return min(target_melons, len(TILES_MANAGED))

    ## 2.7 Adaptive crop selection, considering market price and opponent's crop selection
    def choose_crop_for_planting():
        # Strawberry as priority
        our_strawberries = count_crop_plants(farm,"STRAWBERRY")

        if (our_strawberries < strawberry_plant_target
                and obs["day"] >= STRAWBERRY_START_DAY
                and obs["day"] <= STRAWBERRY_LAST_PLANTING_DAY):
            return "STRAWBERRY"
        
        # Tomato test
        our_tomatoes = count_crop_plants(farm, "TOMATO")
        tomato_last_full_cycle_day = (FINAL_DAY - CROP_CONFIGS["TOMATO"]["last_production_day"])

        if (our_tomatoes < tomato_plant_target
                and obs["day"] >= TOMATO_START_DAY
                and obs["day"] <= tomato_last_full_cycle_day):
            return "TOMATO"

        # First decision layer, filter based on number of days left, no point planting if can't harvest
        
        # Find staple crops that can still mature this season.
        eligible_staples = []

        our_wheat = count_crop_plants(farm, "WHEAT")
        
        for crop in STAPLE_CROPS:
            last_planting_day = (FINAL_DAY- CROP_CONFIGS[crop]["harvest_day"])
            
            wheat_target_reached = (crop == "WHEAT" and our_wheat >= WHEAT_PLANT_TARGET)
            
            # If enough time and wheat target is not reached, add to the eligible list
            if obs["day"] <= last_planting_day and not wheat_target_reached:
                eligible_staples.append(crop)
        
        # Melons are limited to the opening wave. Their planting-day price
        # does not account for the first large sale depressing the market.
        melon_can_mature = obs["day"] <= MELON_LAST_PLANTING_DAY

        # If there is no eligible staple crop, but melon is eligible, choose melon. Otherwise, return None.
        # Currently melon takes the longest to mature
        # Howevver, this is to cover future changes introduce staple crops that takes longer than melon to mature
        if not eligible_staples:
            if melon_can_mature:
                return "MELON"

            return None
        
        # Find the currently most profitable eligible staple
        best_staple = eligible_staples[0]
        best_staple_profit = crop_profit_per_day(best_staple)

        for crop in eligible_staples[1:]:
            crop_profit = crop_profit_per_day(crop)

            if crop_profit > best_staple_profit:
                best_staple = crop
                best_staple_profit = crop_profit

        # When melons cannot mature, use the best eligible staple.
        if not melon_can_mature:
            return best_staple

        # Second decision layer, based on expected profit per day (based on the current market price)
        melon_profit = crop_profit_per_day("MELON")

        # Prefer staple when current melon economics are worse
        if melon_profit <= best_staple_profit:
            return best_staple


        # Third decision layer, based on opponent's crop
        our_melons          = count_crop_plants(farm, "MELON")
        target_melons = choose_melon_plant_target()

        if our_melons < target_melons:
            return "MELON"

        # Carrot seeds are not bought on day 0, so fill the rest of day 0
        # with Wheat, as a real opponent does (replays/day0_setup.json).
        if obs["day"] == 0:
            return "WHEAT"

        return "CARROT"
    
    
    # 2.8 Farm hand logic
    # Plant ages whose night is a Strawberry production night: 9, 11, 13, 15.
    strawberry_production_ages = tuple(range(
        CROP_CONFIGS["STRAWBERRY"]["harvest_day"] - 1,
        CROP_CONFIGS["STRAWBERRY"]["last_production_day"],
        STRAWBERRY_PRODUCTION_INTERVAL,
    ))

    def offday_fertilize_applies(position, tile, day_offset=0):
        # True on the off day before a production night, for SW Strawberry
        # that tomorrow's Fertilizer bonus does not already cover.
        day = obs["day"] + day_offset

        if (
            (
                day < OFFDAY_FERTILIZE_START_DAY
                and position not in NW_DAY5_STRAWBERRY_TILES
            )
            or position not in OFFDAY_FERTILIZE_TILES
            or not isinstance(tile, dict)
            or tile.get("kind") != "PLANT"
            or tile.get("crop") != "STRAWBERRY"
        ):
            return False

        # Only worth a Fertilizer when the extra Strawberry outsells it -- the
        # same test the production-day pass uses. On a Strawberry-glut seed
        # (seed 6: no Strawberry shop until day 18, sold at ~19) the extra
        # units are worth less than the Fertilizer, and pushing them into the
        # glut lowers the price of every Strawberry sold.
        if (
            obs["market"]["prices"]["STRAWBERRY"]
            < obs["market"]["prices"]["FERTILIZER"]
                * FERTILIZER_USE_VALUE_MARGIN
        ):
            return False

        if (
            position in OFFDAY_FERTILIZE_NE_TILES
            and tile["planted_day"] >= STRAWBERRY_START_DAY
        ):
            return False

        return (day - tile["planted_day"]) + 1 in strawberry_production_ages

    def offday_fertilizer_needed(position, tile):
        # Today's plants that still need their off-day Fertilizer. Only a plant
        # watered yesterday may go dry today.
        return (
            offday_fertilize_applies(position, tile)
            and not tile["watered_today"]
            and tile.get("consecutive_unwatered", 0) == 0
            and tile.get("fertilized_until_day", -1) < obs["day"] + 1
        )

    def nw_day5_strawberry_crop(position, crop):
        # Day 4: leave the tile empty (its day-0 Wheat was just harvested).
        # Days 5-6: Strawberry. Otherwise unchanged.
        if position not in NW_DAY5_STRAWBERRY_TILES:
            return crop

        if obs["day"] == NW_DAY5_STRAWBERRY_HOLD_DAY:
            return None

        if (
            NW_DAY5_STRAWBERRY_START_DAY
                <= obs["day"]
                <= NW_DAY5_STRAWBERRY_LAST_DAY
        ):
            return "STRAWBERRY"

        return crop

    def day0_layout_crop(position, crop):
        # Day 0 only: Melon on DAY0_MELON_TILES, Wheat on every other NW crop
        # tile, whichever of the two the day's crop selection asks for.
        if (
            obs["day"] != 0
            or crop not in ("MELON", "WHEAT")
            or position not in NW_PRE_STRAWBERRY_TILES
        ):
            return crop

        return "MELON" if position in DAY0_MELON_TILES else "WHEAT"

    def nw_pre_strawberry_crop(position, crop):
        # The crop to plant on an empty NW tile in the days just before the
        # Strawberry wave: unchanged outside that window or for non-staples,
        # Carrot while it can still be ready by the wave, otherwise None
        # (leave the tile empty).
        day = obs["day"]

        if (
            position not in NW_PRE_STRAWBERRY_TILES
            or crop not in STAPLE_CROPS
            or not (
                STRAWBERRY_START_DAY - CROP_CONFIGS["WHEAT"]["harvest_day"]
                < day
                < STRAWBERRY_START_DAY
            )
        ):
            return crop

        if day + CROP_CONFIGS["CARROT"]["harvest_day"] <= STRAWBERRY_START_DAY:
            return "CARROT"

        return None

    def choose_hand_action(
        hand_position,
        assigned_tiles,
        crop_to_plant,
        available_seed_counts,
        last_planting_day,
        fertilizer_carried=0):
        
        hand_harvest_targets = []
        hand_water_targets = []
        hand_fertilize_targets = []
        hand_plant_targets = []
        hand_weed_targets = []
        
        # First, scan the farm-hand-assigned tiles
        for position in assigned_tiles:
            # Animal tiles are reserved for the farmer, skip this tile
            if position in active_animal_tiles:
                continue

            tile = tile_at(farm, position)

            # On Melon crew day the workers' matching owns every Melon tile.
            # Hand 0 owns (0,4) but is not a worker; left to its crop routine
            # it would harvest a Melon the crew had just watered, or one at 5.
            if (
                melon_crew_active
                and isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and tile.get("crop") == "MELON"
            ):
                continue

            if isinstance(tile, dict) and tile.get("kind") == "WEED":
                    animal_tile_is_reserved = (
                        position in reserved_adaptive_animal_tiles
                    )
            
                    can_dig = (
                        not animal_tile_is_reserved
                        and crop_to_plant is not None
                        and obs["day"] <= last_planting_day
                    )
            
                    if can_dig:
                        hand_weed_targets.append(position)
            
                    continue
                
            # If tile is empty, plant
            if tile is None:
                # Keep tile free if it is designated for SHEEP
                position_crop_to_plant = crop_to_plant
                position_last_planting_day = last_planting_day

                if position in EARLY_SHEEP_TILES:
                    position_crop_to_plant = "CARROT"
                    position_last_planting_day = (
                        EARLY_SHEEP_TILE_REPLANT_CUTOFF_DAY
                    )
                elif position in DELAYED_SHEEP_TILES:
                    position_crop_to_plant = "CARROT"
                    position_last_planting_day = (
                        DELAYED_SHEEP_TILE_REPLANT_CUTOFF_DAY
                    )
                elif (
                    position in OVERFLOW_BUFFER_WHEAT_TILES
                    and OVERFLOW_BUFFER_WHEAT_START_DAY
                        <= obs["day"]
                        <= OVERFLOW_BUFFER_WHEAT_LAST_DAY
                    and position_crop_to_plant != "STRAWBERRY"
                ):
                    position_crop_to_plant = "WHEAT"
                else:
                    position_crop_to_plant = nw_day5_strawberry_crop(
                        position,
                        nw_pre_strawberry_crop(
                            position,
                            day0_layout_crop(position, position_crop_to_plant),
                        ),
                    )

                    if position_crop_to_plant is None:
                        continue

                initial_sheep_tile_is_reserved = (
                    position in EARLY_SHEEP_TILES
                    and obs["day"]
                        >= EARLY_SHEEP_TILE_REPLANT_CUTOFF_DAY
                )

                if (position in DELAYED_SHEEP_TILES
                        and obs["day"] >= DELAYED_SHEEP_TILE_REPLANT_CUTOFF_DAY ):
                    initial_sheep_tile_is_reserved = True

                additional_sheep_tile_is_reserved = (
                    (
                        position in DAY4_ADDITIONAL_SHEEP_TILES
                        and obs["day"]
                            >= DAY4_ADDITIONAL_SHEEP_REPLANT_CUTOFF_DAY
                    )
                    or (
                        position in DAY11_ADDITIONAL_SHEEP_TILES
                        and obs["day"]
                            >= DAY11_ADDITIONAL_SHEEP_REPLANT_CUTOFF_DAY
                    )
                )

                if (
                    initial_sheep_tile_is_reserved
                    or additional_sheep_tile_is_reserved
                ):
                    continue

                animal_tile_is_reserved = (
                    position in reserved_adaptive_animal_tiles
                )
                
                can_plant = (
                    not animal_tile_is_reserved
                    and position_crop_to_plant is not None
                    and available_seed_counts[position_crop_to_plant] > 0
                    and obs["hour"] < LAST_HOUR_TODAY
                    and obs["day"] <= position_last_planting_day
                )

                if can_plant:
                    hand_plant_targets.append(position)

                continue
            
            # If not planting, harvest or water
            # Validate the tile before reading plant-specific fields.
            if (not isinstance(tile, dict)
                    or tile.get("kind") != "PLANT"
                    or tile.get("crop") not in CROPS_MANAGED):
                continue
            
            ready_to_harvest = crop_is_harvestable(tile)

            # Off day before a production night: Fertilizer replaces the
            # watering, or the watering is skipped outright when tomorrow is
            # already boosted. Harvesting needs no water, so it goes ahead.
            if (
                not tile["watered_today"]
                and tile.get("consecutive_unwatered", 0) == 0
                and offday_fertilize_applies(position, tile)
            ):
                if ready_to_harvest:
                    hand_harvest_targets.append(position)

                if tile.get("fertilized_until_day", -1) >= obs["day"] + 1:
                    continue

                if fertilizer_carried > 0:
                    hand_fertilize_targets.append(position)
                else:
                    hand_water_targets.append(position)
                continue

            if tile["watered_today"] and ready_to_harvest:
                hand_harvest_targets.append(position)
            elif not tile["watered_today"]:
                hand_water_targets.append(position)

        # Second, check if already on actionable tile before travelling elsewhere
        # If actionable, then enact
        if hand_position in hand_weed_targets:
            return ["DIG"]
        
        if hand_position in hand_harvest_targets:
            return ["HARVEST"]

        if hand_position in hand_water_targets:
            return ["WATER"]

        if hand_position in hand_fertilize_targets:
            return ["FERTILIZE"]

        if hand_position in hand_plant_targets:
            plant_crop = crop_to_plant

            if hand_position in INITIAL_SHEEP_TILES:
                plant_crop = "CARROT"
            elif (
                hand_position in OVERFLOW_BUFFER_WHEAT_TILES
                and OVERFLOW_BUFFER_WHEAT_START_DAY
                    <= obs["day"]
                    <= OVERFLOW_BUFFER_WHEAT_LAST_DAY
                and plant_crop != "STRAWBERRY"
            ):
                plant_crop = "WHEAT"
            else:
                plant_crop = nw_day5_strawberry_crop(
                    hand_position,
                    nw_pre_strawberry_crop(
                        hand_position,
                        day0_layout_crop(hand_position, plant_crop),
                    ),
                )

            available_seed_counts[plant_crop] -= 1
            return ["PLANT", plant_crop]

        # Third, travel to harvest ready produce first, then handle remaining watering.
        if hand_harvest_targets:
            target = nearest_position(hand_position, hand_harvest_targets)
        elif hand_water_targets or hand_fertilize_targets:
            target = nearest_position(
                hand_position,
                hand_water_targets + hand_fertilize_targets,
            )
        elif hand_weed_targets:
            target = nearest_position(hand_position, hand_weed_targets)
        elif hand_plant_targets:
            target = nearest_position(hand_position, hand_plant_targets)
        else:
            return ["PASS"]

        return move_to(hand_position, target)

    # 2.8b Melon-harvest-day relief hand: a fixed route, not the generic
    # nearest-tile routine, which would send it to whichever tile is closest
    # and let it pick up Melon work.
    def choose_melon_relief_hand_action(hand_position, available_seed_counts):
        def go(position, action):
            if hand_position == position:
                return action
            return move_to(hand_position, position)

        for position in MELON_RELIEF_TILES:
            if position in active_animal_tiles:
                continue

            plant_after_harvest = position in MELON_RELIEF_ROW_TILES
            tile = tile_at(farm, position)

            if (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and tile.get("crop") == "MELON"
            ):
                # Its owner clears it and banks the Melon a day early. Hold
                # station rather than walking west past it, but not all day.
                if obs["hour"] >= MELON_RELIEF_WAIT_LAST_HOUR:
                    continue
                return go(position, ["PASS"])

            if (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and tile.get("crop") == "WHEAT"
            ):
                # Water first: day 10 is the last day of the yield window.
                if not tile["watered_today"]:
                    return go(position, ["WATER"])
                if crop_is_harvestable(tile):
                    return go(position, ["HARVEST"])
                continue

            if not plant_after_harvest:
                continue

            # A new plant starts one dry day down, so an unwatered planting
            # day kills it overnight: water every Strawberry planted today.
            if (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and tile.get("crop") == "STRAWBERRY"
                and tile.get("planted_day") == obs["day"]
                and not tile["watered_today"]
            ):
                return go(position, ["WATER"])

            if isinstance(tile, dict) and tile.get("kind") == "WEED":
                return go(position, ["DIG"])

            if (
                tile is None
                and available_seed_counts.get("STRAWBERRY", 0) > 0
                and obs["hour"] < LAST_HOUR_TODAY
            ):
                if hand_position == position:
                    available_seed_counts["STRAWBERRY"] -= 1
                    return ["PLANT", "STRAWBERRY"]
                return move_to(hand_position, position)

        # Route finished: stay put rather than fall back to the generic
        # routine, which would plant the harvest-only tiles too.
        return ["PASS"]

    def fertilizer_bonus_units(tile):
        crop = tile["crop"]
        crop_age = obs["day"] - tile["planted_day"]

        # Production is applied during the nightly refresh, so these are the
        # action days immediately before the relevant yield becomes visible.
        if crop == "TOMATO" and crop_age == 7:
            return 3

        if crop == "STRAWBERRY" and crop_age in (9, 13):
            return 2

        return 0

    # 2.9 Hand 0 owns the NW Sheep circuit and the staged western Cow.
    def choose_staged_cow_setup_action(hand_position, hand_inventory):
        staged_setup_targets = [
            position
            for position in STAGED_COW_TILES
            if (
                staged_cow_phase_active
                and position not in animal_positions
            )
        ]

        if not staged_setup_targets:
            return None

        if hand_inventory.get("COW", 0) > 0:
            target = nearest_position(
                hand_position,
                staged_setup_targets,
            )

            if hand_position != target:
                return move_to(hand_position, target)

            target_tile = animal_tiles[target]

            if target_tile is None:
                return ["BUILD_PASTURE"]

            if target_tile.get("kind") != "PASTURE":
                return ["DIG"]

            if target_tile.get("animal") is None:
                return ["PLACE", "COW", 1]

            return None

        if animals_in_shed["COW"] <= 0:
            return None

        if hand_position not in SHED_ACCESS_TILES:
            target = nearest_position(
                hand_position,
                SHED_ACCESS_TILES,
            )
            return move_to(hand_position, target)

        return ["PICKUP", "COW", 1]

    def choose_sheep_hand_action(hand_position, hand_inventory):
        nw_livestock_positions = [
            position
            for position in animal_positions
            if (
                (
                    active_animal_plan[position] == "SHEEP"
                    and position in SHEEP_TILES
                )
                or position in STAGED_COW_TILES
            )
        ]

        if not nw_livestock_positions:
            return None

        current_animal = animal_tiles.get(hand_position)
        wheat_carried = hand_inventory.get("WHEAT", 0)

        if (isinstance(current_animal, dict)
                and hand_position in nw_livestock_positions):
            if not current_animal.get("fed_today", False):
                if wheat_carried > 0:
                    return ["FEED"]

            elif not current_animal.get("cared_today", False):
                return ["CARE"]

            elif (current_animal.get("yield_units", 0)
                    >= ANIMAL_HARVEST_THRESHOLD):
                return ["HARVEST"]

        attention_targets = [
            position
            for position in nw_livestock_positions
            if (
                not animal_tiles[position].get("fed_today", False)
                or not animal_tiles[position].get("cared_today", False)
                or animal_tiles[position].get("yield_units", 0)
                    >= ANIMAL_HARVEST_THRESHOLD
            )
        ]

        unfed_animal_count = sum(
            not animal_tiles[position].get("fed_today", False)
            for position in nw_livestock_positions
        )

        if unfed_animal_count > wheat_carried:
            if hand_position not in SHED_ACCESS_TILES:
                target = nearest_position(
                    hand_position,
                    SHED_ACCESS_TILES,
                )
                return move_to(hand_position, target)

            quantity_to_pickup = min(
                shed_counts["WHEAT"],
                unfed_animal_count - wheat_carried,
            )
            if quantity_to_pickup > 0:
                return ["PICKUP", "WHEAT", quantity_to_pickup]

        if attention_targets:
            target = nearest_position(hand_position, attention_targets)
            return move_to(hand_position, target)

        return choose_staged_cow_setup_action(hand_position, hand_inventory)

    # The hand owning a compact mammal block handles its setup and daily care.
    # This supports the ordinary SW block and its early-NE relocation branch.
    def choose_sw_livestock_hand_action(hand_position, hand_inventory):
        if not sw_hand_livestock_phase_active:
            return None

        sw_service_positions = list(active_sw_service_plan)
        sw_animal_positions = [
            position
            for position in animal_positions
            if position in active_sw_service_plan
        ]
        wheat_carried = hand_inventory.get("WHEAT", 0)

        # For the early NE relocation, build the whole compact pasture block
        # before collecting animals. This replaces four shed-to-pasture setup
        # loops with one construction circuit and one placement circuit.
        if (
            early_ne_livestock_construction_phase_active
            and not sw_animal_positions
            and not any(
                hand_inventory.get(animal, 0) > 0
                for animal in ("COW", "SHEEP")
            )
        ):
            unbuilt_pasture_targets = [
                position
                for position in sw_service_positions
                if (
                    not isinstance(animal_tiles[position], dict)
                    or animal_tiles[position].get("kind") != "PASTURE"
                )
            ]

            if unbuilt_pasture_targets:
                target = nearest_position(
                    hand_position,
                    unbuilt_pasture_targets,
                )

                if hand_position != target:
                    return move_to(hand_position, target)

                target_tile = animal_tiles[target]
                if target_tile is None:
                    return ["BUILD_PASTURE"]

                return ["DIG"]

        if (
            early_ne_livestock_construction_phase_active
            and not early_ne_livestock_phase_active
        ):
            return None

        # Animals can be carried in a batch. Collect the matching feed batch
        # before leaving the shed so each placement does not trigger another
        # round trip for one Wheat.
        carried_setup_animal_count = sum(
            hand_inventory.get(animal, 0)
            for animal in ("COW", "SHEEP")
        )
        if (
            early_ne_livestock_phase_active
            and carried_setup_animal_count > wheat_carried
        ):
            if hand_position not in SHED_ACCESS_TILES:
                shed_target = nearest_position(
                    hand_position,
                    SHED_ACCESS_TILES,
                )
                return move_to(hand_position, shed_target)

            wheat_to_pickup = min(
                shed_counts["WHEAT"],
                carried_setup_animal_count - wheat_carried,
            )
            if wheat_to_pickup > 0:
                return ["PICKUP", "WHEAT", wheat_to_pickup]

        def animal_needs_attention(position):
            animal_tile = animal_tiles[position]
            yield_is_ready = (
                animal_tile.get("yield_units", 0)
                >= ANIMAL_HARVEST_THRESHOLD
            )

            if obs["day"] == FINAL_DAY:
                return yield_is_ready

            return (
                not animal_tile.get("fed_today", False)
                or not animal_tile.get("cared_today", False)
                or yield_is_ready
            )

        current_animal = animal_tiles.get(hand_position)
        if (
            isinstance(current_animal, dict)
            and hand_position in sw_animal_positions
            and animal_needs_attention(hand_position)
        ):
            if obs["day"] != FINAL_DAY:
                if not current_animal.get("fed_today", False):
                    if wheat_carried > 0:
                        return ["FEED"]
                elif not current_animal.get("cared_today", False):
                    return ["CARE"]

            if (
                current_animal.get("yield_units", 0)
                >= ANIMAL_HARVEST_THRESHOLD
            ):
                return ["HARVEST"]

        attention_targets = [
            position
            for position in sw_animal_positions
            if animal_needs_attention(position)
        ]

        if obs["day"] == FINAL_DAY:
            unfed_animal_count = 0
        else:
            unfed_animal_count = sum(
                not animal_tiles[position].get("fed_today", False)
                for position in sw_animal_positions
            )

        if unfed_animal_count > wheat_carried:
            if hand_position not in SHED_ACCESS_TILES:
                shed_target = nearest_position(
                    hand_position,
                    SHED_ACCESS_TILES,
                )
                return move_to(hand_position, shed_target)

            quantity_to_pickup = min(
                shed_counts["WHEAT"],
                unfed_animal_count - wheat_carried,
            )
            if quantity_to_pickup > 0:
                return ["PICKUP", "WHEAT", quantity_to_pickup]

        if attention_targets:
            target = nearest_position(hand_position, attention_targets)
            return move_to(hand_position, target)

        sw_setup_complete = (
            len(sw_animal_positions) == len(active_sw_service_plan)
        )
        
        # This block is to protect shed overload
        carried_products = [
            product
            for product in ANIMAL_PRODUCT_ORDER
            if hand_inventory.get(product, 0) > 0
        ]
        carried_product_count = sum(
            hand_inventory[product]
            for product in carried_products
        )

        if (carried_products
                and carried_product_count >= SW_LIVESTOCK_PRODUCT_RETURN_THRESHOLD):
            if hand_position not in SHED_ACCESS_TILES:
                shed_target = nearest_position(
                    hand_position,
                    SHED_ACCESS_TILES,
                )
                return move_to(hand_position, shed_target)

            product = carried_products[0]
            return ["PLACE",  product, hand_inventory[product]]
            
        if sw_setup_complete:
            fertilizer_targets = [
                position
                for position in sw_animal_positions
                if animal_tiles[position].get(
                    "fertilizer_available",
                    False,
                )
            ]

            if hand_position in fertilizer_targets:
                return ["COLLECT_FERTILIZER"]

            if fertilizer_targets:
                target = nearest_position(
                    hand_position,
                    fertilizer_targets,
                )
                return move_to(hand_position, target)

        carried_products = [
            product
            for product in ANIMAL_PRODUCT_ORDER
            if hand_inventory.get(product, 0) > 0
        ]

        if carried_products:
            if hand_position not in SHED_ACCESS_TILES:
                shed_target = nearest_position(
                    hand_position,
                    SHED_ACCESS_TILES,
                )
                return move_to(hand_position, shed_target)

            product = carried_products[0]
            return ["PLACE", product, hand_inventory[product]]

        setup_target_order = sw_service_positions
        if (
            sw_livestock_phase_active
            and not sw_livestock_setup_started
        ):
            # Establish an outer pasture before touching the shared near pair.
            # That pasture permanently identifies this as the four-animal branch.
            setup_target_order = [
                position
                for position in sw_service_positions
                if position in SW_LIVESTOCK_OUTER_TILES
            ]

        setup_targets = [
            position
            for position in setup_target_order
            if position not in sw_animal_positions
        ]

        if not setup_targets:
            return None

        carried_setup_targets = [
            position
            for position in setup_targets
            if hand_inventory.get(active_sw_service_plan[position], 0) > 0
        ]

        if carried_setup_targets:
            target = nearest_position(
                hand_position,
                carried_setup_targets,
            )

            if hand_position != target:
                return move_to(hand_position, target)

            target_tile = animal_tiles[target]
            target_animal = active_sw_service_plan[target]

            if target_tile is None:
                return ["BUILD_PASTURE"]

            if target_tile.get("kind") != "PASTURE":
                return ["DIG"]

            if target_tile.get("animal") is None:
                return ["PLACE", target_animal, 1]

            return None

        animal_to_pickup = None
        for animal in ANIMAL_PRODUCTS:
            if (
                any(
                    active_sw_service_plan[position] == animal
                    for position in setup_targets
                )
                and animals_in_shed[animal] > 0
            ):
                animal_to_pickup = animal
                break

        if animal_to_pickup is None:
            return None

        if hand_position not in SHED_ACCESS_TILES:
            shed_target = nearest_position(
                hand_position,
                SHED_ACCESS_TILES,
            )
            return move_to(hand_position, shed_target)

        matching_targets = sum(
            active_sw_service_plan[position] == animal_to_pickup
            for position in setup_targets
        )

        return [
            "PICKUP",
            animal_to_pickup,
            min(animals_in_shed[animal_to_pickup], matching_targets),
        ]

    # Hand 5 owns the nearest NE Goose tile, so let it establish and service
    # that Goose without pulling the farmer away from the main livestock loop.
    def choose_goose_hand_action(hand_position, hand_inventory, hand_index):
        if not adaptive_goose_phase_active:
            return None

        hand_targets = goose_hand_tile_by_index.get(hand_index, ())

        if not hand_targets:
            return None

        # Carry one Wheat per Goose still waiting to be fed. Fetching a single
        # unit per trip forced a separate shed round-trip for every bird: a
        # hand with two Geese made 88 shed arrivals against the four-Sheep
        # hand's 22, for half the animals.
        wheat_pickup_count = max(
            1,
            sum(
                1
                for target in hand_targets
                if (
                    target in animal_positions
                    and not animal_tiles[target].get("fed_today", False)
                )
            ),
        )

        # Unbuilt coops first, so a half-finished pair never stalls behind an
        # already-serviced Goose.
        ordered_targets = (
            [
                target
                for target in hand_targets
                if target not in animal_positions
            ]
            + [
                target
                for target in hand_targets
                if target in animal_positions
            ]
        )

        for target in ordered_targets:
            goose_action = choose_goose_tile_action(
                hand_position,
                hand_inventory,
                target,
                wheat_pickup_count,
            )

            if goose_action is not None:
                return goose_action

        # Every owned Goose is serviced, so bank the whole round's produce in
        # one trip instead of walking back after each bird.
        def goose_deposit_action():
            carried_products = [
                product
                for product in ANIMAL_PRODUCT_ORDER
                if hand_inventory.get(product, 0) > 0
            ]

            if not carried_products:
                return None

            hand_is_at_shed = hand_position in SHED_ACCESS_TILES

            # Egg prices are flat next to Milk's and Wool's, and the engine
            # empties every hand inventory into the shed at each day boundary.
            # So never spend a walk banking Eggs: place them when the round
            # already finishes at the shed, and otherwise let the overnight
            # drop do it for free. A hand accrues at most 2 Eggs per Goose per
            # day, far under the shed cap, so nothing overflows.
            if (
                early_ne_goose_coexist_active
                and not hand_is_at_shed
                and all(
                    product == "EGG"
                    for product in carried_products
                )
            ):
                return None

            if not hand_is_at_shed:
                return move_to(
                    hand_position,
                    nearest_position(hand_position, SHED_ACCESS_TILES),
                )

            product = carried_products[0]
            return ["PLACE", product, hand_inventory[product]]

        def goose_fertilizer_action():
            for target in ordered_targets:
                if target not in animal_positions:
                    continue

                target_tile = animal_tiles[target]

                if (
                    isinstance(target_tile, dict)
                    and target_tile.get("fertilizer_available", False)
                ):
                    if hand_position == target:
                        return ["COLLECT_FERTILIZER"]

                    return move_to(hand_position, target)

            return None

        # Collecting Fertilizer before banking folds both errands into one shed
        # trip. Applied only while the Geese coexist with the NE block, so
        # every non-qualifying seed keeps the frozen baseline's
        # deposit-then-fertilizer order exactly.
        round_closing_steps = (
            (goose_fertilizer_action, goose_deposit_action)
            if early_ne_goose_coexist_active
            else (goose_deposit_action, goose_fertilizer_action)
        )

        for closing_step in round_closing_steps:
            closing_action = closing_step()

            if closing_action is not None:
                return closing_action

        return None

    def choose_goose_tile_action(
            hand_position,
            hand_inventory,
            target,
            wheat_pickup_count=1,
    ):
        target_tile = animal_tiles[target]
        goose_is_present = target in animal_positions
        wheat_carried = hand_inventory.get("WHEAT", 0)

        if goose_is_present:
            if hand_position == target:
                if not target_tile.get("fed_today", False):
                    if wheat_carried > 0:
                        return ["FEED"]
                elif not target_tile.get("cared_today", False):
                    return ["CARE"]
                elif (
                    target_tile.get("yield_units", 0)
                    >= ANIMAL_HARVEST_THRESHOLD
                ):
                    return ["HARVEST"]

            if (
                not target_tile.get("fed_today", False)
                and wheat_carried == 0
            ):
                if hand_position not in SHED_ACCESS_TILES:
                    shed_target = nearest_position(
                        hand_position,
                        SHED_ACCESS_TILES,
                    )
                    return move_to(hand_position, shed_target)

                if shed_counts["WHEAT"] > 0:
                    return [
                        "PICKUP",
                        "WHEAT",
                        min(shed_counts["WHEAT"], wheat_pickup_count),
                    ]

            goose_needs_attention = (
                not target_tile.get("fed_today", False)
                or not target_tile.get("cared_today", False)
                or target_tile.get("yield_units", 0)
                    >= ANIMAL_HARVEST_THRESHOLD
            )
            if goose_needs_attention:
                return move_to(hand_position, target)

            return None

        if hand_inventory.get("GOOSE", 0) > 0:
            if hand_position != target:
                return move_to(hand_position, target)

            if target_tile is None:
                return ["BUILD_COOP"]

            if target_tile.get("kind") != "COOP":
                return ["DIG"]

            if target_tile.get("animal") is None:
                return ["PLACE", "GOOSE", 1]

            return None

        if animals_in_shed["GOOSE"] > 0:
            if hand_position not in SHED_ACCESS_TILES:
                shed_target = nearest_position(
                    hand_position,
                    SHED_ACCESS_TILES,
                )
                return move_to(hand_position, shed_target)

            return ["PICKUP", "GOOSE", 1]

        return None
    
    # 2.10
    def choose_hand_liquidation_action(
            hand_position,
            hand_inventory,
    ):
        if obs["day"] != FINAL_DAY:
            return None

        product_order = (
            CROPS_MANAGED
            + ANIMAL_PRODUCT_ORDER
            + ("FERTILIZER",)
        )

        carried_products = [
            product
            for product in product_order
            if hand_inventory.get(product, 0) > 0
        ]

        if not carried_products:
            return None

        shed_target = nearest_position(hand_position, SHED_ACCESS_TILES)

        actions_to_liquidate = (distance_between(hand_position, shed_target) + len(carried_products))
        actions_remaining = LAST_HOUR_TODAY - obs["hour"]

        if actions_remaining > (actions_to_liquidate + 1):
            return None

        if hand_position not in SHED_ACCESS_TILES:
            return move_to(hand_position, shed_target)

        product = carried_products[0]

        return [
            "PLACE",
            product,
            hand_inventory[product],
        ]

    # Day 1: bank carried Fertilizer at once so it sells the same day and pays
    # for that day's feed. Only shed stock can be sold, and a unit that DROPs
    # Fertilizer loses it (docs/mechanics.md), so it must be PLACEd.
    def choose_fertilizer_cashout_action(hand_position, hand_inventory):
        fertilizer_quantity = hand_inventory.get("FERTILIZER", 0)

        if obs["day"] != FERTILIZER_CASHOUT_DAY or fertilizer_quantity == 0:
            return None

        if hand_position not in SHED_ACCESS_TILES:
            return move_to(
                hand_position,
                nearest_position(hand_position, SHED_ACCESS_TILES),
            )

        return ["PLACE", "FERTILIZER", fertilizer_quantity]

    # Cash out the first reserved Sheep-tile Carrots as soon as they are
    # harvested, so their proceeds can fund both opening Sheep on day 3.
    def choose_initial_sheep_cashout_action(
            hand_index,
            hand_position,
            hand_inventory,
    ):
        carrot_quantity = hand_inventory.get("CARROT", 0)

        if (
            obs["day"] != DELAYED_SHEEP_START_DAY
            or hand_index != INITIAL_SHEEP_CASHOUT_HAND_INDEX
            or carrot_quantity == 0
            or animals_owned["SHEEP"] >= len(INITIAL_SHEEP_TILES)
        ):
            return None

        if hand_position not in SHED_ACCESS_TILES:
            shed_target = nearest_position(
                hand_position,
                SHED_ACCESS_TILES,
            )
            return move_to(hand_position, shed_target)

        return ["PLACE", "CARROT", carrot_quantity]

    # On melon harvest day, a hand keeps replanting each Melon tile the moment
    # it empties (normal crop-hand behavior), so it never reaches an idle PASS
    # turn on its own. Detect completion explicitly instead: once none of a
    # hand's assigned tiles still holds an unharvested Melon plant, any Melon
    # it is carrying is done growing for the day. Send it straight to the shed
    # to sell before it touches replanting or its other tiles, so the sale
    # beats the automatic overnight deposit by a full day and gets ahead of
    # the opponent's own Melon sale in the shared market.
    def hand_has_pending_melon_work(assigned_tiles):
        for x, y in assigned_tiles:
            tile = farm["tiles"][y][x]

            if (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and tile.get("crop") == "MELON"
            ):
                return True

        return False

    # Every other crop is watered once more before harvest to claim its extra
    # yield point, at the cost of a second action per tile. Twelve tiles' worth
    # of that costs more of the day's 24-action budget than most hands have to
    # spare, so on melon harvest day a Melon tile is harvested the moment it is
    # mature, forfeiting that single bonus unit in exchange for reliably
    # finishing the block and making the same-day return trip.
    def choose_melon_priority_harvest_action(hand_position, assigned_tiles):
        if obs["day"] != MELON_HARVEST_DAY:
            return None

        melon_harvest_targets = []

        for position in assigned_tiles:
            x, y = position
            tile = farm["tiles"][y][x]

            if (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and tile.get("crop") == "MELON"
                and crop_is_harvestable(tile)
            ):
                melon_harvest_targets.append(position)

        if not melon_harvest_targets:
            return None

        if hand_position in melon_harvest_targets:
            return ["HARVEST"]

        target = nearest_position(hand_position, melon_harvest_targets)

        return move_to(hand_position, target)

    # Melon day crew: match the ripe Melon tiles to the Melon workers once per
    # turn. A worker already standing on a Melon keeps it (it may need two
    # turns there, WATER then HARVEST); the rest are paired nearest-first. A
    # worker carrying a trip's load takes no tile and goes to sell.
    melon_worker_indices = []
    melon_crew_targets = {}

    if melon_crew_active:
        melon_worker_indices = [
            hand_index
            for hand_index in (
                list(MELON_OWNER_HAND_INDICES)
                + list(range(
                    MELON_CREW_FIRST_HAND_INDEX,
                    MELON_CREW_FIRST_HAND_INDEX + MELON_CREW_HAND_COUNT,
                ))
            )
            if hand_index < len(farm["hands"])
        ]
        unclaimed_melon_tiles = set(
            (x, y)
            for x, y in FIRST_QUADRANT_ROUTE
            if (
                isinstance(farm["tiles"][y][x], dict)
                and farm["tiles"][y][x].get("kind") == "PLANT"
                and farm["tiles"][y][x].get("crop") == "MELON"
                and crop_is_harvestable(farm["tiles"][y][x])
            )
        )
        free_melon_workers = [
            hand_index
            for hand_index in melon_worker_indices
            if private["inventories"][hand_index + 1].get("MELON", 0)
                < MELON_TRIP_LOAD
        ]

        for hand_index in free_melon_workers:
            worker_position = tuple(farm["hands"][hand_index])

            if worker_position in unclaimed_melon_tiles:
                melon_crew_targets[hand_index] = worker_position
                unclaimed_melon_tiles.discard(worker_position)

        unmatched_melon_workers = [
            hand_index
            for hand_index in free_melon_workers
            if hand_index not in melon_crew_targets
        ]

        def distance_to_shed(position):
            return min(
                distance_between(position, shed_tile)
                for shed_tile in SHED_ACCESS_TILES
            )

        def melon_tile_is_eligible(hand_index, melon_tile):
            worker_position = tuple(farm["hands"][hand_index])

            if private["inventories"][hand_index + 1].get("MELON", 0) <= 0:
                return True

            return (
                distance_between(worker_position, melon_tile)
                + distance_to_shed(melon_tile)
                <= distance_to_shed(worker_position) + MELON_DETOUR_SLACK
            )

        while unmatched_melon_workers and unclaimed_melon_tiles:
            melon_candidates = [
                (
                    distance_between(
                        tuple(farm["hands"][hand_index]),
                        melon_tile,
                    ),
                    hand_index,
                    melon_tile,
                )
                for hand_index in unmatched_melon_workers
                for melon_tile in unclaimed_melon_tiles
                if melon_tile_is_eligible(hand_index, melon_tile)
            ]

            if not melon_candidates:
                break

            _, hand_index, melon_tile = min(melon_candidates)
            melon_crew_targets[hand_index] = melon_tile
            unmatched_melon_workers.remove(hand_index)
            unclaimed_melon_tiles.discard(melon_tile)

    def choose_sw_wheat_block_action(hand_position):
        dig_targets = []
        water_targets = []
        harvest_targets = []
        plant_targets = []
        can_still_plant = obs["day"] <= SW_WHEAT_BLOCK_LAST_PLANTING_DAY

        for position in SW_WHEAT_BLOCK_TILES:
            tile = tile_at(farm, position)

            if tile is None:
                if (
                    can_still_plant
                    and available_seed_counts["WHEAT"] > 0
                    and obs["hour"] < LAST_HOUR_TODAY
                ):
                    plant_targets.append(position)
                continue

            if not isinstance(tile, dict):
                continue

            if tile.get("kind") == "WEED":
                if can_still_plant:
                    dig_targets.append(position)
                continue

            if tile.get("kind") != "PLANT":
                continue

            below_max = tile.get("yield_units", 0) < SW_WHEAT_BLOCK_MAX_YIELD
            crop_age = obs["day"] - tile["planted_day"]
            water_adds_yield = (
                below_max
                and 2 <= crop_age <= CROP_CONFIGS["WHEAT"]["harvest_day"]
            )
            water_keeps_alive = tile.get("consecutive_unwatered", 0) >= 1

            if tile["watered_today"]:
                if crop_is_harvestable(tile):
                    harvest_targets.append(position)
            elif water_adds_yield:
                water_targets.append(position)
            elif crop_is_harvestable(tile):
                harvest_targets.append(position)
            elif water_keeps_alive:
                water_targets.append(position)

        if hand_position in dig_targets:
            return ["DIG"]

        if hand_position in water_targets:
            return ["WATER"]

        if hand_position in harvest_targets:
            return ["HARVEST"]

        if hand_position in plant_targets:
            available_seed_counts["WHEAT"] -= 1
            return ["PLANT", "WHEAT"]

        # A plant dry since yesterday dies tonight: reach those first. A ripe
        # Wheat keeps its 4 units, so its harvest can wait a day.
        urgent_targets = [
            position
            for position in water_targets
            if tile_at(farm, position).get("consecutive_unwatered", 0) >= 1
        ]

        if urgent_targets:
            return move_to(
                hand_position,
                nearest_position(hand_position, urgent_targets),
            )

        targets = dig_targets + water_targets + harvest_targets + plant_targets

        if not targets:
            return ["PASS"]

        return move_to(hand_position, nearest_position(hand_position, targets))

    def choose_melon_crew_action(hand_index, hand_position, hand_inventory):
        melon_target = melon_crew_targets.get(hand_index)

        if melon_target is not None:
            if hand_position != melon_target:
                return move_to(hand_position, melon_target)

            x, y = melon_target
            melon_tile = farm["tiles"][y][x]

            if (
                not melon_tile.get("watered_today", False)
                and melon_tile.get("yield_units", 0) < MELON_MAX_YIELD
            ):
                return ["WATER"]

            return ["HARVEST"]

        melon_carried = hand_inventory.get("MELON", 0)

        if melon_carried <= 0:
            return None

        if hand_position not in SHED_ACCESS_TILES:
            return move_to(
                hand_position,
                nearest_position(hand_position, SHED_ACCESS_TILES),
            )

        return ["PLACE", "MELON", melon_carried]

    def choose_melon_return_action(hand_position, hand_inventory, assigned_tiles):
        if obs["day"] != MELON_HARVEST_DAY:
            return None

        melon_carried = hand_inventory.get("MELON", 0)

        if melon_carried <= 0:
            return None

        if hand_has_pending_melon_work(assigned_tiles):
            return None

        if hand_position not in SHED_ACCESS_TILES:
            shed_target = nearest_position(
                hand_position,
                SHED_ACCESS_TILES,
            )
            return move_to(hand_position, shed_target)

        return ["PLACE", "MELON", melon_carried]


    
    
    #########################################################
    # 3. Opening market orders
    
    ## 3.1 Get animal and animal product count before buying
    animal_tracking_tiles = list(active_animal_tiles)
    for position in active_sw_service_plan:
        if position not in animal_tracking_tiles:
            animal_tracking_tiles.append(position)
    animal_tiles = {
        position: tile_at(farm, position)
        for position in animal_tracking_tiles
    }
    animal_positions = [
        position
        for position, tile in animal_tiles.items()
        if (
            position in active_animal_plan
            and isinstance(tile, dict)
            and tile.get("kind")
                == ANIMAL_STRUCTURES[active_animal_plan[position]]
            and tile.get("animal") == active_animal_plan[position]
        )
    ]
    farmer_animal_positions = [
        position
        for position in animal_positions
        if (
            active_animal_plan[position] != "SHEEP"
            and position not in active_sw_service_plan
            and position not in goose_hand_tiles
            and position not in STAGED_COW_TILES
        )
    ]

    # Get animal count depending on their exact location
    animal_target_counts = {
        animal: sum(
            planned_animal == animal
            for planned_animal in active_animal_plan.values()
        )
        for animal in ANIMAL_PRODUCTS
    }
    animals_in_shed = {
        animal: shed.get(animal, 0)
        for animal in ANIMAL_PRODUCTS
    }
    animals_in_farmer_inventory = {
        animal: farmer_inventory.get(animal, 0)
        for animal in ANIMAL_PRODUCTS
    }
    animals_in_any_inventory = {
        animal: sum(
            inventory.get(animal, 0)
            for inventory in private["inventories"]
        )
        for animal in ANIMAL_PRODUCTS
    }
    animals_owned = {
        animal: (
            sum(
                active_animal_plan[position] == animal
                for position in animal_positions
            )
            + animals_in_shed[animal]
            + animals_in_any_inventory[animal]
        )
        for animal in ANIMAL_PRODUCTS
    }

    initial_sheep_purchase_pending = (
        animals_owned["SHEEP"] < len(INITIAL_SHEEP_TILES)
    )
    initial_sheep_cash_reserve_active = (
        initial_sheep_purchase_pending
        and INITIAL_SHEEP_CASH_RESERVE_START_DAY
            <= obs["day"]
            <= INITIAL_SHEEP_CASH_RESERVE_END_DAY
    )

    wheat_in_farmer_inventory = farmer_inventory.get("WHEAT", 0)
    animal_products_in_farmer_inventory = {
        product: farmer_inventory.get(product, 0)
        for product in ANIMAL_PRODUCT_ORDER
    }
    animal_products_in_shed = {
        product: shed.get(product, 0)
        for product in ANIMAL_PRODUCT_ORDER
    }
    
    
    ## 3.2 Pick a crop based on the current strategy (market price + opponent's crops)
    crop_selected_for_planting = choose_crop_for_planting()       
    if crop_selected_for_planting is not None:
        if crop_selected_for_planting == "MELON":
            selected_last_planting_day = MELON_LAST_PLANTING_DAY
        else:
            selected_harvest_day = CROP_CONFIGS[
                crop_selected_for_planting
            ]["harvest_day"]
            selected_last_planting_day = (
                FINAL_DAY - selected_harvest_day
            )
    else:
        selected_last_planting_day = -1
    
    money_available = farm["money"]
    
    ## 3.3 Sell crop of there is any in the shed (loop for each crop)
    
    # Test strawberry sale timing
    opponent_id = 1 - player_id
    opponent_farm = obs["farms"][opponent_id]

    opponent_strawberries = count_crop_plants(opponent_farm, "STRAWBERRY")

    opponent_is_strawberry_heavy = (
        opponent_strawberries
        >= HEAVY_OPPONENT_STRAWBERRY_THRESHOLD
    )
    STRAWBERRY_SALE_HOUR = 0
    
    opponent_tomatoes = count_crop_plants(
        opponent_farm,
        "TOMATO",
    )       
    
    remaining_animal_feeds = sum(
        not animal_tiles[position].get("fed_today", False)
        for position in animal_positions
    )

    # Sell all wheat on the last day
    wheat_in_all_inventories = sum(
        inventory.get("WHEAT", 0)
        for inventory in private["inventories"]
    )

    if obs["day"] == FINAL_DAY:
        wheat_shed_reserve = max(
            0,
            remaining_animal_feeds - wheat_in_all_inventories,
        )
        wheat_stock_target = remaining_animal_feeds
    else:
        pending_animal_setups = max(
            0,
            animal_count_target - len(animal_positions),
        )
        # The first term is tomorrow's feed, bought a day ahead. Day 0 skips
        # it: day 1's feed is bought on day 1 from same-day Fertilizer sales.
        wheat_stock_target = (
            (animal_count_target if obs["day"] > 0 else 0)
            + remaining_animal_feeds
            + pending_animal_setups
        )
        wheat_shed_reserve = max(
            0,
            wheat_stock_target - wheat_in_all_inventories,
        )
    
    for crop in CROPS_MANAGED:
        quantity_to_sell = shed_counts[crop]

        # For wheat, reserve some wheat for livestock feed.
        if crop == "WHEAT":
            quantity_to_sell = max(0, quantity_to_sell - wheat_shed_reserve,)

            # Hold it while the roster is still being hired. A morning Wheat
            # order takes one of the 10 market slots from the hires: on seeds
            # 8 and 15 the NE Cow hand (5th hire) came in an hour late, ran
            # its round two hours behind, and sold its 24 Milk after the
            # opponent's (-1.2k). Wheat's price is flat, so waiting is free.
            if (
                len(farm["hands"]) < hands_to_hire_today
                and obs["day"] < FINAL_DAY
            ):
                quantity_to_sell = 0

        # For strawberry, cap sale if below certain price
        if (crop == "STRAWBERRY"):
            if obs["hour"] != STRAWBERRY_SALE_HOUR:
                quantity_to_sell = 0
                
            elif (STRAWBERRY_DAILY_SELL_CAP is not None
                    and not opponent_is_strawberry_heavy
                    and obs["market"]["prices"]["STRAWBERRY"] < STRAWBERRY_SELL_PRICE_THRESHOLD
                    and obs["day"] < STRAWBERRY_FORCE_SELL_DAY):
                quantity_to_sell = min(quantity_to_sell, STRAWBERRY_DAILY_SELL_CAP)
        
        # Hold Tomatoes when the opponent has no active Tomato production.
        if crop == "TOMATO":
            if (
                opponent_tomatoes == 0
                and obs["day"] < TOMATO_FORCE_SELL_DAY
            ):
                quantity_to_sell = 0
        
        if quantity_to_sell > 0:
            market_orders.append(["SELL", crop, quantity_to_sell])
    
    # 3.4 Sell animal products in a particular order (does not matter now, may be useful later)
    for product in ANIMAL_PRODUCT_ORDER:
        quantity_to_sell = animal_products_in_shed[product]
        if quantity_to_sell > 0:
            market_orders.append(["SELL", product, quantity_to_sell])
    
    # 3.4 Hire HANDs
    missing_hand_count = max(0, (hands_to_hire_today - len(farm["hands"])))

    market_slots_remaining = max(0, (MAX_MARKET_ORDERS_PER_TURN - len(market_orders)) - MARKET_SLOTS_RESERVED_AFTER_HIRING)

    next_hire_index = farm["hires_today"]

    for _ in range(min(missing_hand_count, market_slots_remaining)):
        hire_cost = HAND_HIRE_COSTS[next_hire_index]

        if money_available < hire_cost:
            break

        market_orders.append(["HIRE"])
        money_available -= hire_cost
        next_hire_index += 1
    
    # Cash floor for section "3.5" below: this day's Wheat feed need,
    # computed before any new animal purchase can spend the money that
    # feed requires. wheat_stock_target already includes animals not yet
    # owned (pending_animal_setups above), so this reserve covers a
    # pending purchase's own future feed need too, not just existing
    # animals'. Without this, buying multiple animals in one turn could
    # leave nothing for Wheat that day, starving every animal already on
    # the farm (not just the new ones) into the engine's own neglect
    # mechanic -- see docs/mechanics.md ("Confirmed: neglected livestock
    # are unplaced overnight") and docs/experiment-log.md's "Early NW Cow
    # expansion" root-cause writeup.
    #
    # Wheat carried by a hand is still committed feed stock. Ignoring it
    # causes the market logic to rebuy the same units after pickup.
    wheat_feed_stock = (
        shed_counts["WHEAT"]
        + wheat_in_all_inventories
    )
    wheat_to_buy = max(0, wheat_stock_target - wheat_feed_stock)
    wheat_price = obs["market"]["prices"]["WHEAT"]
    wheat_purchase_cost = wheat_to_buy * wheat_price

    # The Geese yield their cash to the NE block. A Goose a day late costs
    # about one Egg; the NE block a day late cost the synchronized day-17 Milk
    # batch (seed 15: -5,730 in one day). So while any block animal is still
    # to be bought, a Goose purchase must leave its price in hand. Animals
    # already bought and waiting in the shed or an inventory count as bought.
    pending_ne_block_cost = 0

    if early_ne_livestock_selected:
        pending_ne_block_animals = {}

        for x, y in active_early_ne_livestock_tiles:
            tile = farm["tiles"][y][x]

            if not (isinstance(tile, dict) and tile.get("animal")):
                block_animal = active_early_ne_livestock_plan[(x, y)]
                pending_ne_block_animals[block_animal] = (
                    pending_ne_block_animals.get(block_animal, 0) + 1
                )

        for block_animal, count in pending_ne_block_animals.items():
            still_to_buy = max(
                0,
                count
                - animals_in_shed[block_animal]
                - animals_in_any_inventory[block_animal],
            )
            pending_ne_block_cost += still_to_buy * ANIMAL_COSTS[block_animal]

    # 3.5 Buy each missing animal type
    animal_purchase_planned = False
    # Loop for each animal (currently cows and sheep)
    for animal in ANIMAL_PRODUCTS:
        quantity_to_buy = max(0, animal_target_counts[animal] - animals_owned[animal])
        purchase_cost = quantity_to_buy * ANIMAL_COSTS[animal]
        livestock_purchase_cash_reserve = (
            EARLY_NE_LIVESTOCK_CASH_RESERVE
            if (
                early_ne_livestock_phase_active
                and THIRD_QUADRANT_NAME
                    not in farm["unlocked_quadrants"]
            )
            else 0
        ) + wheat_purchase_cost

        if animal == "GOOSE":
            livestock_purchase_cash_reserve += pending_ne_block_cost

        if (
            quantity_to_buy > 0
            and money_available - purchase_cost
                >= livestock_purchase_cash_reserve
        ):
            market_orders.append([
                "BUY_ANIMAL",
                animal,
                quantity_to_buy,
            ])
            money_available -= purchase_cost
            animal_purchase_planned = True

    # 3.6 Buy enough wheat to maintain the livestock feed reserve.
    # wheat_to_buy/wheat_purchase_cost are computed above, before 3.5, so
    # they can act as its cash floor; section 3.5's own spending is
    # guaranteed not to have touched this reserve, by construction.
    if sum(animals_owned.values()) > 0 or animal_purchase_planned:
        cash_reserve_after_wheat_purchase = (
            INITIAL_SHEEP_CASH_RESERVE
            if (
                initial_sheep_cash_reserve_active
                and obs["day"] == DELAYED_SHEEP_START_DAY
            )
            else 0
        )

        # Buy what the cash allows rather than all or nothing: short of the
        # full amount, some feed still beats none. On day 1 this is what turns
        # each Fertilizer sale into feed as soon as the money lands.
        affordable_wheat = (
            int(
                max(0, money_available - cash_reserve_after_wheat_purchase)
                // wheat_price
            )
            if wheat_price > 0
            else wheat_to_buy
        )
        wheat_quantity_to_buy = min(wheat_to_buy, affordable_wheat)

        if wheat_quantity_to_buy > 0:
            market_orders.append(
                ["BUY_PRODUCT", "WHEAT", wheat_quantity_to_buy]
            )
            money_available -= wheat_quantity_to_buy * wheat_price
    
    #####################################
    # 4. Logic block to decide what to do. First, find a tile for action.
    
    ## Initiate empty target lists
    water_targets   = []
    harvest_targets = []        # Fully ready to harvest (mature + watered)
    plant_targets   = []
    mature_targets  = []        # Partially ready to harvest, regardless whether it is watered or not (for endgame)
    weed_targets    = []
    
    ## To check if current tile is ready to harvest
    tile_current = tile_at(farm, pos_current)
    tile_current_harvestable = False
    
    ## 4.1 First check if current tile is harvestable (i.e. mature + watered, for efficiency)
    if (isinstance(tile_current, dict)
                and pos_current not in active_hand_work_tiles       # i.e. not a hand's tile
                and (
                    not sw_hand_livestock_phase_active
                    or pos_current not in active_sw_service_plan
                )
                and tile_current["kind"] == "PLANT"
                and tile_current["crop"] in CROPS_MANAGED
                and tile_current["watered_today"] == True
                and crop_is_harvestable(tile_current)):

            tile_current_harvestable = True
            
    ## 4.2 If not harvestable, scan MANAGED_TILES for actionable tiles
    if not tile_current_harvestable:      
        for pos in TILES_MANAGED:
            if (
                sw_hand_livestock_phase_active
                and pos in active_sw_service_plan
            ):
                continue

            if (
                early_ne_goose_coexist_active
                and pos in NE_COEXIST_UNMANAGED_TILES
            ):
                continue

            tile = tile_at(farm, pos)
            
            if (isinstance(tile, dict)
                    and tile["kind"] == "PLANT"
                    and tile["crop"] in CROPS_MANAGED):
                # List mature plants (regardless watered or not, useful for the final liquidation)
                ready_to_harvest = crop_is_harvestable(tile)
                
                if ready_to_harvest:
                    mature_targets.append(pos)
                
                # Check if there is any tile to water, else, find a plant ready to harvest.
                # Check who is the tile assigned to a hand
                hand_is_responsible = pos in active_hand_work_tiles       # Binary flag
                if not tile["watered_today"]:
                    # Only water plants that can be harvested.
                    if (not hand_is_responsible 
                            and (obs["day"] < FINAL_DAY or ready_to_harvest)):
                        water_targets.append(pos)
                        
                elif ready_to_harvest:
                    if not hand_is_responsible:
                        harvest_targets.append(pos)
            
            # Before planting, check if there is any weed tile to clear
            # (only clear if there is enough time to re-plant and harvest)
            elif (isinstance(tile, dict)
                    and tile["kind"] == "WEED"
                    and pos not in active_hand_work_tiles
                    and crop_selected_for_planting is not None
                    and obs["day"] <= selected_last_planting_day):
                weed_targets.append(pos)
            
            # If there is enough time, find an empty tile to plant crop_selected_for_planting
            elif (tile is None
                    and pos not in active_hand_work_tiles               # not a hand's tile
                    and crop_selected_for_planting is not None
                    and seed_counts[crop_selected_for_planting] > 0     # we have seeds available
                    and obs["hour"] < LAST_HOUR_TODAY
                    and obs["day"] <= selected_last_planting_day):
                plant_targets.append(pos)
            
    ## 4.3 After actionable tiles are found, find a tile to move to
    ## First, harvest mature crops that are already watered.   
    ## Second, water crops that still need care.
    ## Third priority, plant. If no tile to water and no plant ready to harvest, plant.
    if tile_current_harvestable:
        pos_target = pos_current            # If current tile is harvestable, this is where we want to be
    elif water_targets:
        pos_target = nearest_position(pos_current, water_targets)
    elif harvest_targets:
        pos_target = nearest_position(pos_current, harvest_targets)
    elif weed_targets:
        pos_target = nearest_position(pos_current, weed_targets)    
    elif plant_targets:
        pos_target = nearest_position(pos_current, plant_targets)
    else:
        pos_target = None
  
    # If there is a target position, move. If already at target position, load tile info.
    if pos_target is not None:
        if pos_target != pos_current:
            farmer_action = move_to(pos_current,pos_target)
        else:
            tile_target = tile_at(farm,pos_current)
            
            # Choose action depending on the tile info
            # If tile is empty, PLANT
            if tile_target is None:
                farmer_action = ["PLANT", crop_selected_for_planting]    # Plant according to the assigned crop
            # If there is weed, DIG
            elif tile_target.get("kind") == "WEED":
                farmer_action = ["DIG"]
            # If a plant exist, either harvest or water
            elif tile_target.get("kind") == "PLANT":
                if not tile_target["watered_today"]:
                    farmer_action = ["WATER"]
                else:
                    farmer_action = ["HARVEST"]    
    
    # Livestock is a large investment, so its setup and daily care take priority.
    def move_to_shed_access():
        target = nearest_position(pos_current, SHED_ACCESS_TILES)
        return move_to(pos_current, target)

    def get_wheat_action():
        if pos_current not in SHED_ACCESS_TILES:
            return move_to_shed_access()

        unfed_animal_count = sum(
            not animal_tiles[position].get("fed_today", False)
            for position in farmer_animal_positions
        )

        quantity_to_pickup = min(
            shed_counts["WHEAT"],
            max(1, unfed_animal_count),
        )

        if quantity_to_pickup > 0:
            return ["PICKUP", "WHEAT", quantity_to_pickup]

        return ["PASS"]
    
    # Choose what to do with animals (very large block!)
    def choose_animal_action():
        
        def animal_needs_attention(position):
            animal_tile = animal_tiles[position]

            yield_is_ready = (
                animal_tile.get("yield_units", 0)
                >= ANIMAL_HARVEST_THRESHOLD
            )

            if obs["day"] == FINAL_DAY:
                return yield_is_ready

            return (
                not animal_tile.get("fed_today", False)
                or not animal_tile.get("cared_today", False)
                or yield_is_ready
            )

        def choose_setup_action(setup_targets):
            if not setup_targets:
                return None

            carried_setup_targets = [
                position
                for position in setup_targets
                if animals_in_farmer_inventory[
                    active_animal_plan[position]
                ] > 0
            ]

            if carried_setup_targets:
                target = nearest_position(
                    pos_current,
                    carried_setup_targets,
                )
            else:
                animal_to_pickup = None

                setup_animal_order = list(ANIMAL_PRODUCTS)

                # During the opening, place the Sheep first. Their dedicated
                # hand can begin servicing them while the farmer returns to
                # establish and service the Cows beside the shed.
                opening_sheep_missing = any(
                    position in INITIAL_SHEEP_TILES
                    for position in setup_targets
                )
                opening_cow_missing = any(
                    position in INITIAL_COW_TILES
                    for position in setup_targets
                )

                if opening_sheep_missing and opening_cow_missing:
                    setup_animal_order.remove("SHEEP")
                    setup_animal_order.insert(0, "SHEEP")

                for animal in setup_animal_order:
                    needs_animal = any(
                        active_animal_plan[position] == animal
                        for position in setup_targets
                    )

                    if needs_animal and animals_in_shed[animal] > 0:
                        animal_to_pickup = animal
                        break

                if animal_to_pickup is not None:
                    if pos_current not in SHED_ACCESS_TILES:
                        return move_to_shed_access()

                    matching_targets = sum(
                        active_animal_plan[position] == animal_to_pickup
                        for position in setup_targets
                    )

                    return [
                        "PICKUP",
                        animal_to_pickup,
                        min(animals_in_shed[animal_to_pickup], matching_targets)
                    ]

                return None

            if pos_current != target:
                return move_to(pos_current, target)

            target_tile = animal_tiles[target]
            target_animal = active_animal_plan[target]
            target_structure = ANIMAL_STRUCTURES[target_animal]

            if target_tile is None:
                if target_structure == "COOP":
                    return ["BUILD_COOP"]

                return ["BUILD_PASTURE"]

            if target_tile.get("kind") != target_structure:
                return ["DIG"]

            if target_tile.get("animal") is None:
                if animals_in_farmer_inventory[target_animal] > 0:
                    return ["PLACE", target_animal, 1]

                return None

            return None         # End of choose_setup_action()

        base_setup_targets = [
            position
            for position in active_animal_tiles
            if (
                position not in animal_positions
                and position not in active_goose_tiles
                and position not in active_sw_service_plan
                and position not in STAGED_COW_TILES
            )
        ]

        base_setup_action = choose_setup_action(
            base_setup_targets
        )

        if base_setup_action is not None:
            return base_setup_action
        
        
        # On the final day, service the outer animals first and work
        # inward toward the shed.
        if obs["day"] == FINAL_DAY:
            outer_attention_targets = [
                position
                for position in reversed(active_goose_tiles)
                if (
                    position in farmer_animal_positions
                    and animal_needs_attention(position)
                )
            ]

            if outer_attention_targets:
                target = outer_attention_targets[0]
                target_animal = animal_tiles[target]

                if (not target_animal.get("fed_today", False) and wheat_in_farmer_inventory == 0):
                    return get_wheat_action()

                if pos_current != target:
                    return move_to(pos_current, target)
                
        # Milk is the steepest-glutted product we sell: its intraday price
        # climbs to a midday peak and then falls the hour the day's milk
        # reaches the market (see docs/mechanics.md, "the servicing unit
        # determines when produce reaches the market").  The farmer's round
        # already crosses shed-access tiles, so dropping carried Milk the
        # moment he is standing on one costs a single action and moves the
        # sale into the better hour.  Section 3.4's shed seller picks it up
        # on the following turn.
        #
        # Deliberately disabled on the final day: there is no next turn after
        # hour 23, so the endgame keeps the fused place-and-sell behaviour.
        milk_carried = animal_products_in_farmer_inventory["MILK"]

        if (
            milk_carried > 0
            and obs["day"] < FINAL_DAY
            and pos_current in SHED_ACCESS_TILES
        ):
            return ["PLACE", "MILK", milk_carried]

        # Service the animal at the current position first.
        current_animal = animal_tiles.get(pos_current)

        # Action logic block: FEED, CARE or HARVEST
        if (isinstance(current_animal, dict)
                and pos_current in farmer_animal_positions
                and current_animal.get("kind")
                    == ANIMAL_STRUCTURES[active_animal_plan[pos_current]]
                and current_animal.get("animal") == active_animal_plan.get(pos_current)
                and animal_needs_attention(pos_current)):
            if not current_animal.get("fed_today", False):
                if wheat_in_farmer_inventory > 0:
                    return ["FEED"]

                return get_wheat_action()

            if not current_animal.get("cared_today", False):
                return ["CARE"]

            if (current_animal.get("yield_units", 0) >= ANIMAL_HARVEST_THRESHOLD):
                return ["HARVEST"]

        # Finish the compact NE Goose setup before travelling to other
        # livestock. The block above still services an animal already under
        # the farmer before continuing setup.
        adaptive_setup_targets = [
            position
            for position in active_goose_tiles
            if (
                position in active_animal_tiles
                and position not in animal_positions
                and position not in goose_hand_tiles
            )
        ]

        goose_setup_feed_shortfall = max(
            0,
            len(adaptive_setup_targets) - wheat_in_farmer_inventory,
        )

        if goose_setup_feed_shortfall > 0:
            if pos_current not in SHED_ACCESS_TILES:
                return move_to_shed_access()

            wheat_to_pickup = min(
                shed_counts["WHEAT"],
                goose_setup_feed_shortfall,
            )

            if wheat_to_pickup > 0:
                return ["PICKUP", "WHEAT", wheat_to_pickup]

        adaptive_setup_action = choose_setup_action(
            adaptive_setup_targets
        )

        if adaptive_setup_action is not None:
            return adaptive_setup_action

        # Travel to another animal that requires attention.
        attention_targets = [
            position
            for position in farmer_animal_positions
            if animal_needs_attention(position)
        ]

        if attention_targets:
            target = nearest_position(pos_current, attention_targets )
            target_animal = animal_tiles[target]

            if (
                not target_animal.get("fed_today", False)
                and wheat_in_farmer_inventory == 0
            ):
                return get_wheat_action()

            return move_to(pos_current, target)

        # Batch all completed Milk and Wool harvests before returning to shed.
        carried_products = [
            product
            for product in ANIMAL_PRODUCT_ORDER
            if animal_products_in_farmer_inventory[product] > 0
        ]

        if carried_products:
            if pos_current not in SHED_ACCESS_TILES:
                return move_to_shed_access()

            product = carried_products[0]
            return [
                "PLACE",
                product,
                animal_products_in_farmer_inventory[product],
            ]
            
        return None


    # Day 1: until the day's feed is covered, the farmer gathers the
    # Fertilizer the animals produced overnight and banks it for sale, instead
    # of waiting at the shed for Wheat nobody can afford yet. Its animals sit
    # next to the shed, so this is a few actions, and the proceeds buy the
    # feed through the partial Wheat purchase below.
    farmer_fertilizer_cashout_action = None
    farmer_fertilizer_carried = private["inventories"][0].get("FERTILIZER", 0)
    day1_feed_is_short = (
        obs["day"] == FERTILIZER_CASHOUT_DAY
        and remaining_animal_feeds
            > shed_counts["WHEAT"] + wheat_in_all_inventories
    )

    if day1_feed_is_short:
        day1_fertilizer_targets = [
            position
            for position in farmer_animal_positions
            if animal_tiles[position].get("fertilizer_available", False)
        ]

        if pos_current in day1_fertilizer_targets:
            farmer_fertilizer_cashout_action = ["COLLECT_FERTILIZER"]
        elif day1_fertilizer_targets:
            farmer_fertilizer_cashout_action = move_to(
                pos_current,
                nearest_position(pos_current, day1_fertilizer_targets),
            )

    if (
        farmer_fertilizer_cashout_action is None
        and obs["day"] == FERTILIZER_CASHOUT_DAY
        and farmer_fertilizer_carried > 0
    ):
        if pos_current in SHED_ACCESS_TILES:
            farmer_fertilizer_cashout_action = [
                "PLACE",
                "FERTILIZER",
                farmer_fertilizer_carried,
            ]
            market_orders.append([
                "SELL",
                "FERTILIZER",
                farmer_fertilizer_carried,
            ])
        else:
            farmer_fertilizer_cashout_action = move_to_shed_access()

    animal_action = (
        farmer_fertilizer_cashout_action
        if farmer_fertilizer_cashout_action is not None
        else choose_animal_action()
    )

    if animal_action is not None:
        farmer_action = animal_action

        if (farmer_action[0] == "PLACE"
                and farmer_action[1] in ANIMAL_PRODUCT_ORDER
                # Milk dropped before the final day is left in the shed on
                # purpose so section 3.4 sells it on the next turn, at the
                # earlier hour.  Wool and Egg keep the fused place-and-sell,
                # and the final day keeps it for Milk too.
                and not (
                    farmer_action[1] == "MILK"
                    and obs["day"] < FINAL_DAY
                )):
            product = farmer_action[1]
            market_orders.append([
                "SELL",
                product,
                animal_products_in_farmer_inventory[product],
            ])
            
    # Collect Fertilizer only when the farmer has no livestock or crop work.
    # Remember the target so an idle hand does not duplicate the same trip.
    farmer_fertilizer_target = None

    if (animal_action is None
            and farmer_action == ["PASS"]
            and obs["day"] < FINAL_DAY):
        fertilizer_targets = [
            position
            for position in farmer_animal_positions
            if animal_tiles[position].get("fertilizer_available", False)
        ]

        if pos_current in fertilizer_targets:
            farmer_fertilizer_target = pos_current
            farmer_action = ["COLLECT_FERTILIZER"]
        elif fertilizer_targets:
            target = nearest_position(pos_current, fertilizer_targets)
            farmer_fertilizer_target = target
            farmer_action = move_to(pos_current, target)
            
            
    ##########################################################            
    # 5. Final liquidation of harvested plants in the backpack
    ## Check if it is the final day and if farmer is still carrying crop
    backpack_total = sum(backpack_counts.values())
    
    ## Check if we need to override the "harvest everything before PLACE-ing in the shed" logic
    ## Calculate the number of actions needed to go back to the shed + to PLACE the crops
    n_crops_carried = 0
    for crop in CROPS_MANAGED:
        if backpack_counts[crop] > 0:
            n_crops_carried += 1
    
    liquidation_shed_target = nearest_position(pos_current, SHED_ACCESS_TILES)
    
    actions_to_liquidate = n_crops_carried + distance_between(pos_current, liquidation_shed_target)
    actions_remaining = (LAST_HOUR_TODAY) - obs["hour"]
    
    # Create flags for liquidation conditions (start liquidation if either is True)
    liquidation_is_urgent = (
        obs["day"] == FINAL_DAY
        and backpack_total > 0
        and  actions_remaining <= actions_to_liquidate
    )
    harvest_is_done = (
        not tile_current_harvestable
        and not mature_targets
    )
    
    if (obs["day"] == FINAL_DAY
            and animal_action is None
            and backpack_total > 0
            and (liquidation_is_urgent or harvest_is_done)):    
        if pos_current not in SHED_ACCESS_TILES:
            farmer_action = move_to(pos_current, liquidation_shed_target)
        else:
            crop_to_place       = None
            for crop in CROPS_MANAGED:
                if backpack_counts[crop] > 0:
                    crop_to_place = crop
                    break
            quantity_to_place   = backpack_counts[crop_to_place]
            
            farmer_action = ["PLACE", crop_to_place, quantity_to_place]
            market_orders.append(["SELL", crop_to_place, quantity_to_place])
    
    # 6. Hand action assignment
    hand_actions = []
    available_seed_counts = seed_counts.copy()

    if farmer_action[0] == "PLANT":
        farmer_crop = farmer_action[1]
        available_seed_counts[farmer_crop] -= 1
    
    # Fertilizer the hands take from the shed this turn, so the market below
    # does not sell the same units.
    offday_fertilizer_shed_available = shed.get("FERTILIZER", 0)
    offday_fertilizer_picked = 0

    # Loop for each HAND
    for hand_index, hand_position in enumerate(farm["hands"]):
        if hand_index < len(current_hand_work_tiles_each):
            assigned_tiles = current_hand_work_tiles_each[hand_index]
        else:
            assigned_tiles = []

        hand_inventory = private["inventories"][hand_index + 1]
        fertilizer_carried = hand_inventory.get("FERTILIZER", 0)

        hand_action = None

        # Choose action according to priority: liquidate -> sheep care for the designated HAND -> other actions
        hand_action = choose_hand_liquidation_action(tuple(hand_position), hand_inventory)

        if (
            hand_action is None
            and hand_index == SW_WHEAT_BLOCK_HAND_INDEX
            and sw_wheat_block_active
        ):
            hand_action = choose_sw_wheat_block_action(tuple(hand_position))

        # The day-10 crew hands are SW hands hired a day early: their SW
        # routes and routines do not exist yet, so they only work Melon.
        if (
            hand_action is None
            and melon_crew_active
            and hand_index >= MELON_CREW_FIRST_HAND_INDEX
        ):
            hand_action = choose_melon_crew_action(
                hand_index,
                tuple(hand_position),
                hand_inventory,
            )

            if hand_action is None:
                hand_action = ["PASS"]

        # Take today's off-day Fertilizer from the shed before leaving it.
        # Hands spawn on shed access, so this costs one action and no walk.
        # It runs ahead of the Goose and livestock routines: those always
        # have a first action at the shed (a Wheat pickup), so a later check
        # never saw the Goose hands there idle and NE boosted only 25 of 51
        # production nights on seed 1 (SW, with no Goose hands: 53 of 54).
        if (
            hand_action is None
            and tuple(hand_position) in SHED_ACCESS_TILES
            and offday_fertilizer_shed_available > 0
        ):
            offday_fertilizer_need = sum(
                1
                for position in assigned_tiles
                if offday_fertilizer_needed(position, tile_at(farm, position))
            )
            quantity_to_pickup = min(
                offday_fertilizer_shed_available,
                offday_fertilizer_need - fertilizer_carried,
            )

            if quantity_to_pickup > 0:
                hand_action = ["PICKUP", "FERTILIZER", quantity_to_pickup]
                offday_fertilizer_shed_available -= quantity_to_pickup
                offday_fertilizer_picked += quantity_to_pickup

        if hand_action is None:
            hand_action = choose_fertilizer_cashout_action(
                tuple(hand_position),
                hand_inventory,
            )

        if hand_action is None:
            hand_action = choose_initial_sheep_cashout_action(
                hand_index,
                tuple(hand_position),
                hand_inventory,
            )

        # A stranded staged Cow goes on its tile before the Sheep round: with
        # four Sheep to feed and care for, the round fills hand 0's day and it
        # only reached the Cow at h23 on both day 10 and day 11 (seed 11), so
        # the Cow went back to the shed overnight each time.
        if (
            hand_action is None
            and hand_index == SHEEP_HAND_INDEX
            and stranded_staged_cow
        ):
            hand_action = choose_staged_cow_setup_action(
                tuple(hand_position),
                hand_inventory,
            )

        if (hand_action is None and (hand_index == SHEEP_HAND_INDEX)):
            hand_action = choose_sheep_hand_action(tuple(hand_position), hand_inventory)

        if (
            hand_action is None
            and hand_index in goose_hand_tile_by_index
        ):
            hand_action = choose_goose_hand_action(
                tuple(hand_position),
                hand_inventory,
                hand_index,
            )

        if (
            hand_action is None
            and hand_index == active_sw_livestock_hand_index
        ):
            hand_action = choose_sw_livestock_hand_action(
                tuple(hand_position),
                hand_inventory,
            )

        hand_is_melon_relief = (
            melon_relief_hand_active
            and hand_index == MELON_RELIEF_HAND_INDEX
        )

        if hand_action is None and hand_is_melon_relief:
            hand_action = choose_melon_relief_hand_action(
                tuple(hand_position),
                available_seed_counts,
            )

        if melon_crew_active:
            if hand_action is None and hand_index in melon_worker_indices:
                hand_action = choose_melon_crew_action(
                    hand_index,
                    tuple(hand_position),
                    hand_inventory,
                )
        else:
            # On melon harvest day, clear any mature Melon tile immediately,
            # then sell once the block is done, ahead of replanting or other
            # tiles.
            if hand_action is None:
                hand_action = choose_melon_priority_harvest_action(
                    tuple(hand_position),
                    assigned_tiles,
                )

            if hand_action is None:
                hand_action = choose_melon_return_action(
                    tuple(hand_position),
                    hand_inventory,
                    assigned_tiles,
                )


        if hand_action is None:
            hand_crop_to_plant = crop_selected_for_planting
            hand_last_planting_day = selected_last_planting_day

            if (
                early_ne_strawberry_phase_active
                and NW_HAND_COUNT
                    <= hand_index
                    < SECOND_QUADRANT_HAND_COUNT
            ):
                hand_crop_to_plant = "STRAWBERRY"
                hand_last_planting_day = STRAWBERRY_LAST_PLANTING_DAY
            elif (
                early_nw_strawberry_phase_active
                and hand_index < NW_HAND_COUNT
            ):
                hand_crop_to_plant = "STRAWBERRY"
                hand_last_planting_day = STRAWBERRY_LAST_PLANTING_DAY

            hand_action = choose_hand_action(
                tuple(hand_position),
                assigned_tiles,
                hand_crop_to_plant,
                available_seed_counts,
                hand_last_planting_day,
                fertilizer_carried)

        hand_actions.append(hand_action)

    # Spend carried Fertilizer on valuable premium-crop production windows.
    # Normal crop and livestock work retains priority.
    for hand_index, hand_action in enumerate(hand_actions):
        if hand_action != ["PASS"]:
            continue

        hand_inventory = private["inventories"][hand_index + 1]

        if hand_inventory.get("FERTILIZER", 0) == 0:
            continue

        if hand_index >= len(current_hand_work_tiles_each):
            continue

        hand_position = tuple(farm["hands"][hand_index])
        fertilization_targets = []

        for position in current_hand_work_tiles_each[hand_index]:
            tile = tile_at(farm, position)

            if (
                not isinstance(tile, dict)
                or tile.get("kind") != "PLANT"
                or tile.get("crop") not in ("TOMATO", "STRAWBERRY")
                or not tile.get("watered_today", False)
                or tile.get("fertilized_until_day", -1) >= obs["day"]
            ):
                continue

            bonus_units = fertilizer_bonus_units(tile)
            crop_price = obs["market"]["prices"][tile["crop"]]
            fertilizer_price = obs["market"]["prices"]["FERTILIZER"]

            if (
                bonus_units > 0
                and bonus_units * crop_price
                    >= fertilizer_price * FERTILIZER_USE_VALUE_MARGIN
            ):
                fertilization_targets.append(position)

        if not fertilization_targets:
            continue

        target = nearest_position(
            hand_position,
            fertilization_targets,
        )

        if hand_position == target:
            hand_actions[hand_index] = ["FERTILIZE"]
        else:
            hand_actions[hand_index] = move_to(
                hand_position,
                target,
            )

    # Once their assigned work is complete, use otherwise-idle hands to
    # collect Fertilizer from animals outside the dedicated SW livestock loop.
    # Allocate targets globally so two hands do not make the same trip.
    if obs["day"] < FINAL_DAY:
        claimed_fertilizer_targets = set()

        if farmer_fertilizer_target is not None:
            claimed_fertilizer_targets.add(farmer_fertilizer_target)

        available_fertilizer_targets = [
            position
            for position in animal_positions
            if (
                animal_tiles[position].get(
                    "fertilizer_available",
                    False,
                )
                and position not in claimed_fertilizer_targets
                and not (
                    sw_hand_livestock_phase_active
                    and position in active_sw_service_plan
                )
            )
        ]
        idle_hand_indices = [
            hand_index
            for hand_index, hand_action in enumerate(hand_actions)
            if hand_action == ["PASS"]
        ]

        while idle_hand_indices and available_fertilizer_targets:
            _, hand_index, target = min(
                (
                    distance_between(
                        tuple(farm["hands"][hand_index]),
                        target,
                    ),
                    hand_index,
                    target,
                )
                for hand_index in idle_hand_indices
                for target in available_fertilizer_targets
            )
            hand_position = tuple(farm["hands"][hand_index])

            if hand_position == target:
                hand_actions[hand_index] = ["COLLECT_FERTILIZER"]
            else:
                hand_actions[hand_index] = move_to(
                    hand_position,
                    target,
                )

            idle_hand_indices.remove(hand_index)
            available_fertilizer_targets.remove(target)

    planned_strawberry_count = count_crop_plants(farm, "STRAWBERRY")
    planned_tomato_count = count_crop_plants(farm, "TOMATO")
    planned_melon_count = count_crop_plants(farm, "MELON")
    if farmer_action == ["PLANT", "STRAWBERRY"]:
        planned_strawberry_count += 1
    elif farmer_action == ["PLANT", "TOMATO"]:
        planned_tomato_count += 1
    elif farmer_action == ["PLANT", "MELON"]:
        planned_melon_count += 1
        
    for hand_action in hand_actions:
        if hand_action == ["PLANT", "STRAWBERRY"]:
            planned_strawberry_count += 1
        elif hand_action == ["PLANT", "TOMATO"]:
            planned_tomato_count += 1
        elif hand_action == ["PLANT", "MELON"]:
            planned_melon_count += 1
        elif hand_action[0] == "PLACE":
            product     = hand_action[1]
            quantity    = hand_action[2]
  
            # Check if a sell order for this product exists
            existing_sell_order = None
            for order in market_orders:
                if order[0] == "SELL" and order[1] == product:
                    existing_sell_order = order
                    break
            # If it exists, then just add to the quantity, otherwise create a new sell order
            if existing_sell_order is not None:
                existing_sell_order[2] += quantity
            else:
                market_orders.append([
                    "SELL",
                    product,
                    quantity,
                ])
    
    
    #######################################################
    # 7. Closing market order (buy seeds and purchase land)
    
    ## Buy crop seed (i.e. maintain a certain number available seed for each crop)
    selected_crop_seed_target = (
        NE_SELECTED_CROP_SEED_TARGET
        if SECOND_QUADRANT_NAME in farm["unlocked_quadrants"]
        else SELECTED_CROP_SEED_TARGET
    )

    for crop in CROPS_MANAGED:
        if crop == "MELON":
            last_planting_day = MELON_LAST_PLANTING_DAY
        else:
            last_planting_day = (
                FINAL_DAY - CROP_CONFIGS[crop]["harvest_day"]
            )
        seed_cost = CROP_CONFIGS[crop]["seed_cost"]
        
        target_seed_count = DEFAULT_SEED_TARGETS[crop]
        if obs["day"] == 0 and crop == "CARROT":
            target_seed_count = 0

        if crop == "STRAWBERRY" and nw_day5_strawberry_phase_active:
            target_seed_count = nw_day5_strawberry_pending
        elif (
            crop == "STRAWBERRY"
            and (early_ne_strawberry_phase_active or early_nw_strawberry_phase_active)
        ):
            # Top each early wave up against its own quadrant's count, the
            # same counters its phase uses.
            target_seed_count = (
                (
                    max(0, early_ne_strawberry_target - our_ne_strawberries)
                    if early_ne_strawberry_phase_active
                    else 0
                )
                + (
                    max(0, EARLY_NW_STRAWBERRY_TARGET - our_nw_strawberries)
                    if early_nw_strawberry_phase_active
                    else 0
                )
            )
        elif crop == crop_selected_for_planting:
            if crop == "MELON":
                target_seed_count = min(
                    selected_crop_seed_target,
                    max(
                        0,
                        choose_melon_plant_target()
                        - planned_melon_count,
                    ),
                )
            elif crop == "STRAWBERRY":
                target_seed_count = max(0, (strawberry_plant_target - planned_strawberry_count))
            elif crop == "TOMATO":
                target_seed_count = max(0, (tomato_plant_target - planned_tomato_count))
            else:
                target_seed_count = selected_crop_seed_target
        
        if crop == "WHEAT":
            target_seed_count += sw_wheat_block_pending

        quantity_to_buy = (target_seed_count - available_seed_counts[crop])

        total_seed_cost = (quantity_to_buy * seed_cost)
        
        # Never let seeds spend the money tomorrow's roster needs. The whole
        # roster is re-hired every morning, and on day 1 the hands' Fertilizer
        # is the farm's first income: a day 0 that ends on zero hires nobody,
        # collects nothing, and never recovers (replays/zero_money.json -- the
        # Melon top-up bought one seed an hour until the last 80 coins went).
        next_day_hire_count = hands_to_hire_today

        if (
            MELON_CREW_ACTIVE
            and obs["day"] == MELON_HARVEST_DAY - 1
            and SECOND_QUADRANT_NAME in farm["unlocked_quadrants"]
        ):
            next_day_hire_count = max(
                next_day_hire_count,
                MELON_CREW_FIRST_HAND_INDEX + MELON_CREW_HAND_COUNT,
            )

        next_day_hire_cost = sum(HAND_HIRE_COSTS[:next_day_hire_count])
        cash_reserve_after_seed_purchase = max(
            INITIAL_SHEEP_CASH_RESERVE
            if initial_sheep_cash_reserve_active
            else 0,
            next_day_hire_cost,
        )

        # The early Strawberry waves buy what the cash allows: filling NE on
        # its unlock day can ask for more seed than one turn affords, and all
        # or nothing would then buy none, not even the first twelve.
        if (
            crop == "STRAWBERRY"
            and (
                early_ne_strawberry_phase_active
                or early_nw_strawberry_phase_active
                or nw_day5_strawberry_phase_active
            )
            and quantity_to_buy > 0
        ):
            quantity_to_buy = min(
                quantity_to_buy,
                max(0, money_available - cash_reserve_after_seed_purchase)
                    // seed_cost,
            )
            total_seed_cost = quantity_to_buy * seed_cost

        if (
            quantity_to_buy > 0
            and money_available - total_seed_cost
                >= cash_reserve_after_seed_purchase
            and obs["day"] <= last_planting_day
        ):
            market_orders.append(["BUY_SEED", crop, quantity_to_buy])          
            money_available -= total_seed_cost
    
    # Sell premium crops first, in descending base-price order. A stable sort
    # only reorders the CROP_SALE_PRIORITY entries to the front; every other
    # order (seed buys, hires, land, Fertilizer, animal products) keeps its
    # existing relative order and simply follows after, unchanged.
    def sale_priority_key(order):
        if order[0] == "SELL" and order[1] in CROP_SALE_PRIORITY:
            return CROP_SALE_PRIORITY.index(order[1])
        return len(CROP_SALE_PRIORITY)

    market_orders.sort(key=sale_priority_key)

    # Unlock the second quadrant.
    if (SECOND_QUADRANT_NAME not in farm["unlocked_quadrants"]
            and obs["day"] >= SECOND_QUADRANT_PURCHASE_DAY
            # and obs["day"] % 2 == 1                             # To stagger COW production
            and money_available >= (SECOND_QUADRANT_LAND_COST + LAND_WORKING_CAPITAL_RESERVE)
            and len(market_orders) < 10):
        market_orders.append(["BUY_LAND"])
        money_available -= SECOND_QUADRANT_LAND_COST
    
    required_base_animal_tiles = COW_TILES + SHEEP_TILES
    if staged_cow_phase_active:
        required_base_animal_tiles += STAGED_COW_TILES

    base_animal_setup_complete = all(
        position in animal_positions
        for position in required_base_animal_tiles
    )
    
    # Unlock the third quadrant.
    if (
        SECOND_QUADRANT_NAME in farm["unlocked_quadrants"]
        and THIRD_QUADRANT_NAME not in farm["unlocked_quadrants"]
        and THIRD_QUADRANT_PURCHASE_START_DAY
            <= obs["day"]
            <= THIRD_QUADRANT_PURCHASE_LAST_DAY
        and money_available
            >= THIRD_QUADRANT_LAND_COST + LAND_WORKING_CAPITAL_RESERVE
        and len(market_orders) < MAX_MARKET_ORDERS_PER_TURN
        and base_animal_setup_complete
    ):
        market_orders.append(["BUY_LAND"])
        money_available -= THIRD_QUADRANT_LAND_COST

    # Fertilizer is optional income, so sell it after every strategic order.
    # If all market slots are occupied, keep it in the shed for a later turn.
    fertilizer_sell_order = None

    for order in market_orders:
        if order[:2] == ["SELL", "FERTILIZER"]:
            fertilizer_sell_order = order
            break

    offday_fertilizer_reserve = 0

    for position in OFFDAY_FERTILIZE_TILES:
        tile = tile_at(farm, position)

        if offday_fertilizer_needed(position, tile):
            offday_fertilizer_reserve += 1
        elif (
            offday_fertilize_applies(position, tile, day_offset=1)
            and tile.get("fertilized_until_day", -1) < obs["day"] + 2
        ):
            offday_fertilizer_reserve += 1

    offday_fertilizer_reserve = max(
        0,
        offday_fertilizer_reserve
        - offday_fertilizer_picked
        - sum(
            inventory.get("FERTILIZER", 0)
            for inventory in private["inventories"][1:]
        ),
    )

    fertilizer_in_shed = max(
        0,
        shed.get("FERTILIZER", 0)
        - offday_fertilizer_picked
        - offday_fertilizer_reserve,
    )

    if fertilizer_sell_order is not None:
        fertilizer_sell_order[2] += fertilizer_in_shed
        market_orders.remove(fertilizer_sell_order)
    elif fertilizer_in_shed > 0:
        fertilizer_sell_order = [
            "SELL",
            "FERTILIZER",
            fertilizer_in_shed,
        ]

    if (
        fertilizer_sell_order is not None
        and len(market_orders) < MAX_MARKET_ORDERS_PER_TURN
    ):
        market_orders.append(fertilizer_sell_order)
        
    return {
        "farmer": farmer_action,
        "hands": hand_actions,
        "market": market_orders,
    }
