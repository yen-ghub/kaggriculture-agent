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
DEFAULT_SEED_TARGETS = {
    "WHEAT": 1,
    "CARROT": 1,
    "STRAWBERRY": 0,
    "MELON": 0,
    "TOMATO":0
}
SELECTED_CROP_SEED_TARGET = 3
NE_SELECTED_CROP_SEED_TARGET = 8
WHEAT_PLANT_TARGET      = 18        # Currently no limit, to flood the carrot market and bring price down for the oponent

#
# STRAWBERRY related
STRAWBERRY_PLANT_TARGET     = 39        # Fine-tuned: 39
HIGH_STRAWBERRY_PLANT_TARGET = 45
STRAWBERRY_START_DAY        = 10
EARLY_NE_STRAWBERRY_START_DAY = SECOND_QUADRANT_PURCHASE_DAY
EARLY_NE_STRAWBERRY_TARGET = 6
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

PREMIUM_CROP_PLANT_TARGET = 45
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
DAY4_ADDITIONAL_SHEEP_REPLANT_CUTOFF_DAY    = 1
DAY11_ADDITIONAL_SHEEP_REPLANT_CUTOFF_DAY   = 10
INITIAL_SHEEP_CASHOUT_HAND_INDEX    = 0                # Early cashout to buy the delayed sheep
INITIAL_SHEEP_CASH_RESERVE_START_DAY = 1
INITIAL_SHEEP_CASH_RESERVE_END_DAY  = 3
INITIAL_SHEEP_CASH_RESERVE          = 1000

ADAPTIVE_GOOSE_TILES = (
    (6, 4),
    (6, 3),
)
GOOSE_HAND_INDEX = 4
GOOSE_HAND_TILE = ADAPTIVE_GOOSE_TILES[0]
# Compatibility alias for local trace scripts created before this split.
ADAPTIVE_ANIMAL_TILES = ADAPTIVE_GOOSE_TILES

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
)
MARKET_SLOTS_RESERVED_AFTER_HIRING = 3

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

    existing_adaptive_geese = []
    adaptive_goose_setup_started = False

    for position in ADAPTIVE_GOOSE_TILES:
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
        bool(existing_adaptive_geese)
        or first_two_shops_demand_eggs
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

    # When second and third quadrants are unlocked, add more animal tiles
    if (SECOND_QUADRANT_NAME in farm["unlocked_quadrants"]
            and obs["day"] >= EXPANSION_COW_START_DAY):
        active_animal_plan.update({
            position: "COW"
            for position in EXPANSION_COW_TILES[:EXPANSION_COW_COUNT]
        })
    
    def animal_is_placed(position, expected_animal):
        x, y = position
        tile = farm["tiles"][y][x]

        return (
            isinstance(tile, dict)
            and tile.get("kind") == ANIMAL_STRUCTURES[expected_animal]
            and tile.get("animal") == expected_animal
        )
        
    base_animal_setup_complete = (
        all(
            animal_is_placed(position, "COW")
            for position in COW_TILES
        )
        and all(
            animal_is_placed(position, "SHEEP")
            for position in SHEEP_TILES
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
    adaptive_mammal_tiles_reserved = (
        THIRD_QUADRANT_NAME in farm["unlocked_quadrants"]
        and adaptive_mammal_type is not None
        and not sw_livestock_selected
        and obs["day"] >= ADAPTIVE_ANIMAL_START_DAY
    )
    sw_livestock_tiles_reserved = sw_livestock_selected

    reserved_adaptive_animal_tiles = set()
    if adaptive_goose_tiles_reserved:
        reserved_adaptive_animal_tiles.update(ADAPTIVE_GOOSE_TILES)
    if sw_livestock_tiles_reserved:
        reserved_adaptive_animal_tiles.update(SW_LIVESTOCK_TILES)
    elif adaptive_mammal_tiles_reserved:
        reserved_adaptive_animal_tiles.update(ADAPTIVE_MAMMAL_TILES)

    if adaptive_goose_phase_active:
        active_animal_plan.update({
            position: "GOOSE"
            for position in ADAPTIVE_GOOSE_TILES
        })

    active_adaptive_mammal_plan = {}
    if adaptive_mammal_phase_active:
        active_adaptive_mammal_plan = {
            position: adaptive_mammal_type
            for position in ADAPTIVE_MAMMAL_TILES
        }
        active_animal_plan.update(active_adaptive_mammal_plan)

    active_sw_service_plan = active_adaptive_mammal_plan
    if sw_livestock_phase_active:
        active_animal_plan.update(active_sw_livestock_plan)
        active_sw_service_plan = active_sw_livestock_plan

    sw_hand_livestock_phase_active = bool(active_sw_service_plan)
    active_sw_livestock_hand_index = (
        SW_LIVESTOCK_HAND_INDEX
        if sw_livestock_phase_active
        else ADAPTIVE_MAMMAL_HAND_INDEX
    )
    
    active_animal_tiles = list(active_animal_plan)
    animal_count_target = len(active_animal_tiles)
    animal_feed_reserve = 2 * animal_count_target
    
    # Reassign the SW hands once the compact livestock block activates.
    current_hand_work_tiles_each = [
        list(positions)
        for positions in HAND_WORK_TILES_EACH
    ]

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
    early_ne_strawberry_phase_active = (
        SECOND_QUADRANT_NAME in farm["unlocked_quadrants"]
        and EARLY_NE_STRAWBERRY_START_DAY
            <= obs["day"]
            < STRAWBERRY_START_DAY
        and count_crop_plants(farm, "STRAWBERRY")
            < EARLY_NE_STRAWBERRY_TARGET
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

        return "CARROT"
    
    
    # 2.8 Farm hand logic
    def choose_hand_action(
        hand_position, 
        assigned_tiles, 
        crop_to_plant,
        available_seed_counts,
        last_planting_day):
        
        hand_harvest_targets = []
        hand_water_targets = []
        hand_plant_targets = []
        hand_weed_targets = []
        
        # First, scan the farm-hand-assigned tiles
        for position in assigned_tiles:
            # Animal tiles are reserved for the farmer, skip this tile
            if position in active_animal_tiles:
                continue

            tile = tile_at(farm, position)

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
                elif position in DAY4_ADDITIONAL_SHEEP_TILES:
                    position_crop_to_plant = "CARROT"
                    position_last_planting_day = (
                        DAY4_ADDITIONAL_SHEEP_REPLANT_CUTOFF_DAY
                    )
                elif (
                    position in OVERFLOW_BUFFER_WHEAT_TILES
                    and OVERFLOW_BUFFER_WHEAT_START_DAY
                        <= obs["day"]
                        <= OVERFLOW_BUFFER_WHEAT_LAST_DAY
                ):
                    position_crop_to_plant = "WHEAT"

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
        
        if hand_position in hand_plant_targets:
            plant_crop = crop_to_plant

            if hand_position in INITIAL_SHEEP_TILES:
                plant_crop = "CARROT"
            elif hand_position in DAY4_ADDITIONAL_SHEEP_TILES:
                plant_crop = "CARROT"
            elif (
                hand_position in OVERFLOW_BUFFER_WHEAT_TILES
                and OVERFLOW_BUFFER_WHEAT_START_DAY
                    <= obs["day"]
                    <= OVERFLOW_BUFFER_WHEAT_LAST_DAY
            ):
                plant_crop = "WHEAT"

            available_seed_counts[plant_crop] -= 1
            return ["PLANT", plant_crop]

        # Third, travel to harvest ready produce first, then handle remaining watering.
        if hand_harvest_targets:
            target = nearest_position(hand_position, hand_harvest_targets)
        elif hand_water_targets:
            target = nearest_position(hand_position, hand_water_targets)
        elif hand_weed_targets:
            target = nearest_position(hand_position, hand_weed_targets)
        elif hand_plant_targets:
            target = nearest_position(hand_position, hand_plant_targets)
        else:
            return ["PASS"]

        return move_to(hand_position, target)

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

    # 2.9 To get a HAND to help the FARMER to care for sheep
    def choose_sheep_hand_action(hand_position, hand_inventory):
        sheep_positions = [
            position
            for position in animal_positions
            if active_animal_plan[position] == "SHEEP"
                and position in SHEEP_TILES  # SW sheep belong to Hand 10.
        ]

        if not sheep_positions:
            return None

        current_sheep = animal_tiles.get(hand_position)
        wheat_carried = hand_inventory.get("WHEAT", 0)

        if (isinstance(current_sheep, dict)
                and hand_position in sheep_positions):
            if not current_sheep.get("fed_today", False):
                if wheat_carried > 0:
                    return ["FEED"]

            elif not current_sheep.get("cared_today", False):
                return ["CARE"]

            elif (current_sheep.get("yield_units", 0)
                    >= ANIMAL_HARVEST_THRESHOLD):
                return ["HARVEST"]

        sheep_attention_targets = [
            position
            for position in sheep_positions
            if (
                not animal_tiles[position].get("fed_today", False)
                or not animal_tiles[position].get("cared_today", False)
                or animal_tiles[position].get("yield_units", 0)
                    >= ANIMAL_HARVEST_THRESHOLD
            )
        ]

        unfed_sheep_count = sum(
            not animal_tiles[position].get("fed_today", False)
            for position in sheep_positions
        )

        if unfed_sheep_count > wheat_carried:
            if hand_position not in SHED_ACCESS_TILES:
                target = nearest_position(
                    hand_position,
                    SHED_ACCESS_TILES,
                )
                return move_to(hand_position, target)

            quantity_to_pickup = min(shed_counts["WHEAT"], (unfed_sheep_count - wheat_carried))
            if quantity_to_pickup > 0:
                return ["PICKUP", "WHEAT", quantity_to_pickup]

        if sheep_attention_targets:
            target = nearest_position(hand_position, sheep_attention_targets)
            return move_to(hand_position, target)

        return None

    # The hand owning the compact SW block handles its setup and daily care.
    def choose_sw_livestock_hand_action(hand_position, hand_inventory):
        if not sw_hand_livestock_phase_active:
            return None

        sw_service_positions = list(active_sw_service_plan)
        sw_animal_positions = [
            position
            for position in animal_positions
            if position in active_sw_service_plan
        ]

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
        wheat_carried = hand_inventory.get("WHEAT", 0)

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
    def choose_goose_hand_action(hand_position, hand_inventory):
        if not adaptive_goose_phase_active:
            return None

        target = GOOSE_HAND_TILE
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
                    return ["PICKUP", "WHEAT", 1]

            goose_needs_attention = (
                not target_tile.get("fed_today", False)
                or not target_tile.get("cared_today", False)
                or target_tile.get("yield_units", 0)
                    >= ANIMAL_HARVEST_THRESHOLD
            )
            if goose_needs_attention:
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

            if target_tile.get("fertilizer_available", False):
                if hand_position == target:
                    return ["COLLECT_FERTILIZER"]
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
    
    
    
    
    #########################################################
    # 3. Opening market orders
    
    ## 3.1 Get animal and animal product count before buying
    animal_tiles = {
        position: tile_at(farm, position)
        for position in active_animal_tiles
    }
    animal_positions = [
        position
        for position, tile in animal_tiles.items()
        if (
            isinstance(tile, dict)
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
            and position != GOOSE_HAND_TILE
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
        wheat_shed_reserve = animal_feed_reserve
        wheat_stock_target = animal_feed_reserve
    
    for crop in CROPS_MANAGED:
        quantity_to_sell = shed_counts[crop]

        # For wheat, reserve some wheat for livestock feed.
        if crop == "WHEAT":
            quantity_to_sell = max(0, quantity_to_sell - wheat_shed_reserve,)

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
    
    # 3.5 Buy each missing animal type
    animal_purchase_planned = False
    # Loop for each animal (currently cows and sheep)
    for animal in ANIMAL_PRODUCTS:
        quantity_to_buy = max(0, animal_target_counts[animal] - animals_owned[animal])
        purchase_cost = quantity_to_buy * ANIMAL_COSTS[animal]

        if (
            quantity_to_buy > 0
            and money_available >= purchase_cost
        ):
            market_orders.append([
                "BUY_ANIMAL",
                animal,
                quantity_to_buy,
            ])
            money_available -= purchase_cost
            animal_purchase_planned = True

    # 3.6 Buy enough wheat to maintain the livestock feed reserve.
    if sum(animals_owned.values()) > 0 or animal_purchase_planned:
        wheat_feed_stock    = (shed_counts["WHEAT"] + wheat_in_farmer_inventory)
        if obs["day"] == FINAL_DAY:
            wheat_feed_stock = (shed_counts["WHEAT"] + wheat_in_all_inventories)

        wheat_to_buy = max(0, wheat_stock_target - wheat_feed_stock)
        
        wheat_price         = obs["market"]["prices"]["WHEAT"]
        wheat_purchase_cost = wheat_to_buy * wheat_price

        cash_reserve_after_wheat_purchase = (
            INITIAL_SHEEP_CASH_RESERVE
            if (
                initial_sheep_cash_reserve_active
                and obs["day"] == DELAYED_SHEEP_START_DAY
            )
            else 0
        )

        if (
            wheat_to_buy > 0
            and money_available - wheat_purchase_cost
                >= cash_reserve_after_wheat_purchase
        ):
            market_orders.append(
                ["BUY_PRODUCT", "WHEAT", wheat_to_buy]
            )
            money_available -= wheat_purchase_cost
    
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
                and position not in ADAPTIVE_GOOSE_TILES
                and position not in SW_LIVESTOCK_TILES
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
                for position in reversed(ADAPTIVE_GOOSE_TILES)
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
                
        # Service the animal at the current position first.
        current_animal = animal_tiles.get(pos_current)

        # Action logic block: FEED, CARE or HARVEST
        if (isinstance(current_animal, dict)
                and current_animal.get("kind")
                    == ANIMAL_STRUCTURES[active_animal_plan[pos_current]]
                and current_animal.get("animal") == active_animal_plan.get(pos_current)
                and pos_current in farmer_animal_positions
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
            for position in ADAPTIVE_GOOSE_TILES
            if (
                position in active_animal_tiles
                and position not in animal_positions
                and position != GOOSE_HAND_TILE
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


    animal_action = choose_animal_action()

    if animal_action is not None:
        farmer_action = animal_action

        if (farmer_action[0] == "PLACE" and farmer_action[1] in ANIMAL_PRODUCT_ORDER):
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
    
    # Loop for each HAND    
    for hand_index, hand_position in enumerate(farm["hands"]):
        if hand_index < len(current_hand_work_tiles_each):
            assigned_tiles = current_hand_work_tiles_each[hand_index]
        else:
            assigned_tiles = []

        hand_inventory = private["inventories"][hand_index + 1]
        
        hand_action = None

        # Choose action according to priority: liquidate -> sheep care for the designated HAND -> other actions
        hand_action = choose_hand_liquidation_action(tuple(hand_position), hand_inventory)

        if hand_action is None:
            hand_action = choose_initial_sheep_cashout_action(
                hand_index,
                tuple(hand_position),
                hand_inventory,
            )

        if (hand_action is None and (hand_index == SHEEP_HAND_INDEX)):
            hand_action = choose_sheep_hand_action(tuple(hand_position), hand_inventory)

        if (
            hand_action is None
            and hand_index == GOOSE_HAND_INDEX
        ):
            hand_action = choose_goose_hand_action(
                tuple(hand_position),
                hand_inventory,
            )

        if (
            hand_action is None
            and hand_index == active_sw_livestock_hand_index
        ):
            hand_action = choose_sw_livestock_hand_action(
                tuple(hand_position),
                hand_inventory,
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

            hand_action = choose_hand_action(
                tuple(hand_position),
                assigned_tiles,
                hand_crop_to_plant,
                available_seed_counts,
                hand_last_planting_day)
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
        if (
            crop == "STRAWBERRY"
            and early_ne_strawberry_phase_active
        ):
            target_seed_count = max(
                0,
                EARLY_NE_STRAWBERRY_TARGET
                    - planned_strawberry_count,
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
        
        quantity_to_buy = (target_seed_count - available_seed_counts[crop])

        total_seed_cost = (quantity_to_buy * seed_cost)
        
        cash_reserve_after_seed_purchase = (
            INITIAL_SHEEP_CASH_RESERVE
            if initial_sheep_cash_reserve_active
            else 0
        )

        if (
            quantity_to_buy > 0
            and money_available - total_seed_cost
                >= cash_reserve_after_seed_purchase
            and obs["day"] <= last_planting_day
        ):
            market_orders.append(["BUY_SEED", crop, quantity_to_buy])          
            money_available -= total_seed_cost
    
    # Always give the Melon sale first market priority.
    for order_index, order in enumerate(market_orders):
        if order[0] == "SELL" and order[1] == "MELON":
            melon_sell_order = market_orders.pop(order_index)
            market_orders.insert(0, melon_sell_order)
            break
        
    # Unlock the second quadrant.
    if (SECOND_QUADRANT_NAME not in farm["unlocked_quadrants"]
            and obs["day"] >= SECOND_QUADRANT_PURCHASE_DAY
            # and obs["day"] % 2 == 1                             # To stagger COW production
            and money_available >= (SECOND_QUADRANT_LAND_COST + LAND_WORKING_CAPITAL_RESERVE)
            and len(market_orders) < 10):
        market_orders.append(["BUY_LAND"])
        money_available -= SECOND_QUADRANT_LAND_COST
    
    base_animal_setup_complete = all(
        position in animal_positions
        for position in COW_TILES + SHEEP_TILES
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

    fertilizer_in_shed = shed.get("FERTILIZER", 0)

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
