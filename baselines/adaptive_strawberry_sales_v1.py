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

SECOND_QUADRANT_TILE_COUNT = 14
SECOND_QUADRANT_NAME = "NE"
SECOND_QUADRANT_LAND_COST = 1000
SECOND_QUADRANT_PURCHASE_DAY = 9        # To stagger COW production days
LAND_WORKING_CAPITAL_RESERVE = 1000

# Combine the two quadrants
TILE_ROUTE = (
    FIRST_QUADRANT_ROUTE
    + SECOND_QUADRANT_ROUTE
)

TILE_COUNT = (
    len(FIRST_QUADRANT_ROUTE)
    + SECOND_QUADRANT_TILE_COUNT
)

TILES_MANAGED = TILE_ROUTE[:TILE_COUNT]
    
# Define constants and crop configs (a dict)
CROP_CONFIGS = {
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
CROPS_MANAGED   = ("WHEAT", "CARROT", "MELON", "STRAWBERRY") # Affects market sale order

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
MELON_REPLANT_PRICE_THRESHOLD = 220
POST_GLUT_MELON_TARGET = 4
HEAVY_OPPONENT_MELON_TARGET = 13
DEFAULT_SEED_TARGETS = {
    "WHEAT": 1,
    "CARROT": 1,
    "STRAWBERRY": 0,
    "MELON": 1,
}
SELECTED_CROP_SEED_TARGET = 3
WHEAT_PLANT_TARGET      = 18        # Currently no limit, to flood the carrot market and bring price down for the oponent

STRAWBERRY_PLANT_TARGET = 33        # Fine-tuned: 33
STRAWBERRY_START_DAY    = 10
STRAWBERRY_DAILY_SELL_CAP = None
STRAWBERRY_FORCE_SELL_DAY = 29
STRAWBERRY_SELL_PRICE_THRESHOLD = 250
HEAVY_OPPONENT_STRAWBERRY_THRESHOLD = 10
   
LAST_HOUR_TODAY     = 23
FINAL_DAY           = 29
SHED_ACCESS_TILE    = (4,4)

# Animal related (generalised from COW)
INITIAL_COW_TILES = (
    (4, 4),
    (4, 3),
)

INITIAL_SHEEP_TILES = (
    (3, 3),
    (3, 4),
)

EXPANSION_COW_TILES = (
    (5, 4),
    (5, 3),
)

EXPANSION_COW_COUNT = 2

# Every position permanently reserved for a cow.
COW_TILES = (
    INITIAL_COW_TILES
    + EXPANSION_COW_TILES[:EXPANSION_COW_COUNT]
)

SHEEP_TILES = INITIAL_SHEEP_TILES
SHEEP_START_DAY = 11
SHEEP_TILE_REPLANT_CUTOFF_DAY = SHEEP_START_DAY - 1

# Every position permanently reserved for livestock.
ANIMAL_TILES = COW_TILES + SHEEP_TILES

ANIMAL_PRODUCTS = {
    "COW": "MILK",
    "SHEEP": "WOOL",
}

ANIMAL_COSTS = {
    "COW": 400,
    "SHEEP": 500,
}

ANIMAL_PRODUCT_ORDER = ("MILK", "WOOL")

ANIMAL_HARVEST_THRESHOLD = 1

# All four centre-adjacent positions can access the shed.
SHED_ACCESS_TILES = (
    (4, 4),
    (5, 4),
    (4, 5),
    (5, 5),
)

# Farm hands
NW_HAND_COUNT = 4           # First quadrant
EXPANDED_HAND_COUNT = 6
SHEEP_HAND_INDEX = 3        # The chosen HAND to help with SHEEP

HAND_HIRE_COST_BY_COUNT = {
    4: 7,
    6: 20,
}

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

# Divide managed tiles amongst farm hands
HAND_WORK_TILES_EACH = [
    FIRST_QUADRANT_CROP_TILES[:5],
    FIRST_QUADRANT_CROP_TILES[5:12],
    FIRST_QUADRANT_CROP_TILES[12:18],
    FIRST_QUADRANT_CROP_TILES[18:],
    SECOND_QUADRANT_CROP_TILES[:6],
    SECOND_QUADRANT_CROP_TILES[6:],
]

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
    farmer_inventory = private["inventories"][0]
    
    pos_current = tuple(farm["farmer"])
    
    if SECOND_QUADRANT_NAME in farm["unlocked_quadrants"]:
        hands_to_hire_today = EXPANDED_HAND_COUNT
    else:
        hands_to_hire_today = NW_HAND_COUNT

    daily_hand_hire_cost = HAND_HIRE_COST_BY_COUNT[
        hands_to_hire_today
    ]
    
    # Sheep tiles remain crop tiles until their opening crops have been cleared.
    sheep_target_tiles = [
        farm["tiles"][y][x]
        for x, y in INITIAL_SHEEP_TILES
    ]

    sheep_setup_started = (
        shed.get("SHEEP", 0) > 0
        or any(
            inventory.get("SHEEP", 0) > 0
            for inventory in private["inventories"]
        )
        or any(
            isinstance(tile, dict)
            and tile.get("kind") == "PASTURE"
            for tile in sheep_target_tiles
        )
    )

    sheep_tiles_ready = all(
        tile is None
        or (
            isinstance(tile, dict)
            and tile.get("kind") == "WEED"
        )
        for tile in sheep_target_tiles
    )

    sheep_phase_active = (
        sheep_setup_started
        or (
            obs["day"] >= SHEEP_START_DAY
            and sheep_tiles_ready
        )
    )

    # Cows are active from the opening.
    active_animal_plan = {
        position: "COW"
        for position in INITIAL_COW_TILES
    }

    # Sheep activate only after their former crop tiles are available.
    if sheep_phase_active:
        active_animal_plan.update({
            position: "SHEEP"
            for position in INITIAL_SHEEP_TILES
        })

    # When second quadrant is unlocked, add more animal tiles
    if SECOND_QUADRANT_NAME in farm["unlocked_quadrants"]:
        active_animal_plan.update({
            position: "COW"
            for position in EXPANSION_COW_TILES[:EXPANSION_COW_COUNT]
        })

    active_animal_tiles = list(active_animal_plan)
    animal_count_target = len(active_animal_tiles)
    animal_feed_reserve = 2 * animal_count_target
    
    # Create a list of work tiles of the farm hands
    active_hand_work_tiles = []
    for hand_index in range(
            min(len(farm["hands"]), len(HAND_WORK_TILES_EACH))
    ):
        active_hand_work_tiles.extend(
            HAND_WORK_TILES_EACH[hand_index]
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
        crop_config = CROP_CONFIGS[crop]
        current_price = obs["market"]["prices"][crop]

        expected_revenue = (crop_config["harvest_yield"] * current_price)
        expected_profit = (expected_revenue - crop_config["seed_cost"])

        return expected_profit / crop_config["harvest_day"]
    
    
    ## 2.7 Adaptive crop selection, considering market price and opponent's crop selection
    def choose_crop_for_planting():
        
        # Strawberry as priority
        our_strawberries = count_crop_plants(farm,"STRAWBERRY")

        strawberry_last_full_cycle_day = (FINAL_DAY - CROP_CONFIGS["STRAWBERRY"]["last_production_day"])

        if (our_strawberries < STRAWBERRY_PLANT_TARGET
                and obs["day"] >= STRAWBERRY_START_DAY
                and obs["day"] <= strawberry_last_full_cycle_day):
            return "STRAWBERRY"

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
        
        # Check melon too
        melon_last_planting_day = (FINAL_DAY - CROP_CONFIGS["MELON"]["harvest_day"])
        
        melon_can_mature = (obs["day"] <= melon_last_planting_day)

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
        opponent_id         = 1 - player_id
        opponent_farm       = obs["farms"][opponent_id]
        opponent_melons     = count_crop_plants(opponent_farm, "MELON")
        opponent_carrots    = count_crop_plants(opponent_farm, "CARROT")
        our_melons          = count_crop_plants(farm, "MELON")
        current_melon_price = obs["market"]["prices"]["MELON"]
        
        # Optimal number of melon tiles based on experiment
        # Guard against melon price crash 
        if current_melon_price < MELON_REPLANT_PRICE_THRESHOLD:
            target_melons = POST_GLUT_MELON_TARGET
        # If opponent not planting melon, go full melon
        elif opponent_melons == 0:
            target_melons = 15
        elif (opponent_carrots > 0 and opponent_melons <= 10):
            target_melons = 13
        else:
            target_melons = HEAVY_OPPONENT_MELON_TARGET

        target_melons = min(
            target_melons,
            len(TILES_MANAGED),
        )

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
        
        # First, scan the farm-hand-assigned tiles
        for position in assigned_tiles:
            # Animal tiles are reserved for the farmer, skip this tile
            if position in active_animal_tiles:
                continue
            
            tile = tile_at(farm, position)

            # If tile is empty, plant
            if tile is None:
                
                # Keep tile free if it is designated for SHEEP
                if ((position in SHEEP_TILES)
                        and obs["day"] >= SHEEP_TILE_REPLANT_CUTOFF_DAY):
                    continue
                
                can_plant = (
                    crop_to_plant is not None
                    and available_seed_counts[crop_to_plant] > 0
                    and obs["hour"] < LAST_HOUR_TODAY
                    and obs["day"] <= last_planting_day
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
        if hand_position in hand_harvest_targets:
            return ["HARVEST"]

        if hand_position in hand_water_targets:
            return ["WATER"]
        
        if hand_position in hand_plant_targets:
            available_seed_counts[crop_to_plant] -= 1
            return ["PLANT", crop_to_plant]

        # Third, travel to harvest ready produce first, then handle remaining watering.
        if hand_harvest_targets:
            target = nearest_position(hand_position, hand_harvest_targets)
        elif hand_water_targets:
            target = nearest_position(hand_position, hand_water_targets)
        elif hand_plant_targets:
            target = nearest_position(hand_position, hand_plant_targets)
        else:
            return ["PASS"]

        return move_to(hand_position, target)

    # To get a HAND to help the FARMER to care for sheep
    def choose_sheep_hand_action(hand_position, hand_inventory):
        sheep_positions = [
            position
            for position in animal_positions
            if active_animal_plan[position] == "SHEEP"
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

            quantity_to_pickup = min(
                shed_counts["WHEAT"],
                unfed_sheep_count - wheat_carried,
            )
            if quantity_to_pickup > 0:
                return ["PICKUP", "WHEAT", quantity_to_pickup]

        if sheep_attention_targets:
            target = nearest_position(
                hand_position,
                sheep_attention_targets,
            )
            return move_to(hand_position, target)

        return None
    
    
    
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
            and tile.get("kind") == "PASTURE"
            and tile.get("animal") == active_animal_plan[position]
        )
    ]
    farmer_animal_positions = [
        position
        for position in animal_positions
        if active_animal_plan[position] != "SHEEP"
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
        selected_harvest_day = CROP_CONFIGS[crop_selected_for_planting]["harvest_day"]

        selected_last_planting_day = (FINAL_DAY - selected_harvest_day)
    else:
        selected_last_planting_day = -1
    
    money_available = farm["money"]
    
    ## 3.3 Sell crop of there is any in the shed (loop for each crop)
    
    # Test strawberry sale timing
    opponent_id = 1 - player_id
    opponent_farm = obs["farms"][opponent_id]

    opponent_strawberries = count_crop_plants(
        opponent_farm,
        "STRAWBERRY",
    )

    opponent_is_strawberry_heavy = (
        opponent_strawberries
        >= HEAVY_OPPONENT_STRAWBERRY_THRESHOLD
    )
    STRAWBERRY_SALE_HOUR = 0
    for crop in CROPS_MANAGED:
        quantity_to_sell = shed_counts[crop]

        # For wheat, reserve some wheat for livestock feed.
        if crop == "WHEAT":
            quantity_to_sell = max(0, quantity_to_sell - animal_feed_reserve,)

        # For strawberry, cap sale if below certain price
        if (crop == "STRAWBERRY"):
            if obs["hour"] != STRAWBERRY_SALE_HOUR:
                quantity_to_sell = 0
                
            elif (STRAWBERRY_DAILY_SELL_CAP is not None
                    and not opponent_is_strawberry_heavy
                    and obs["market"]["prices"]["STRAWBERRY"] < STRAWBERRY_SELL_PRICE_THRESHOLD
                    and obs["day"] < STRAWBERRY_FORCE_SELL_DAY):
                quantity_to_sell = min(quantity_to_sell, STRAWBERRY_DAILY_SELL_CAP)
        
        if quantity_to_sell > 0:
            market_orders.append(["SELL", crop, quantity_to_sell])
    
    # 3.4 Sell animal products in a particular order (does not matter now, may be useful later)
    for product in ANIMAL_PRODUCT_ORDER:
        quantity_to_sell = animal_products_in_shed[product]
        if quantity_to_sell > 0:
            market_orders.append(["SELL", product, quantity_to_sell])
    
    # 3.4 Hire HANDs
    if (not farm["hands"]
            and money_available >= daily_hand_hire_cost):
        for _ in range(hands_to_hire_today):
            market_orders.append(["HIRE"])

        money_available -= daily_hand_hire_cost
    
    # 3.5 Buy each missing animal type
    animal_purchase_planned = False
    # Loop for each animal (currently cows and sheep)
    for animal in ANIMAL_PRODUCTS:
        quantity_to_buy = max(0, animal_target_counts[animal] - animals_owned[animal])
        purchase_cost = quantity_to_buy * ANIMAL_COSTS[animal]

        if quantity_to_buy > 0 and money_available >= purchase_cost:
            market_orders.append([
                "BUY_ANIMAL",
                animal,
                quantity_to_buy,
            ])
            money_available -= purchase_cost
            animal_purchase_planned = True

    # Buy enough wheat to maintain the livestock feed reserve.
    if sum(animals_owned.values()) > 0 or animal_purchase_planned:
        wheat_feed_stock    = (shed_counts["WHEAT"] + wheat_in_farmer_inventory)
        wheat_to_buy        = max(0, animal_feed_reserve - wheat_feed_stock,)
        wheat_price         = obs["market"]["prices"]["WHEAT"]
        wheat_purchase_cost = wheat_to_buy * wheat_price

        if (wheat_to_buy > 0 and money_available >= wheat_purchase_cost):
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
                and tile_current["kind"] == "PLANT"
                and tile_current["crop"] in CROPS_MANAGED
                and tile_current["watered_today"] == True
                and crop_is_harvestable(tile_current)):

            tile_current_harvestable = True
            
    ## 4.2 If not harvestable, scan MANAGED_TILES for actionable tiles
    if not tile_current_harvestable:      
        for pos in TILES_MANAGED:
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
        # Build pastures and place missing livestock before ordinary care.
        setup_targets = [
            position
            for position in active_animal_tiles
            if position not in animal_positions
        ]

        if setup_targets:
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
                for animal in ANIMAL_PRODUCTS:
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
                        min(
                            animals_in_shed[animal_to_pickup],
                            matching_targets,
                        ),
                    ]

                target = nearest_position(pos_current, setup_targets)

            if pos_current != target:
                return move_to(pos_current, target)

            target_tile = animal_tiles[target]
            target_animal = active_animal_plan[target]

            if target_tile is None:
                return ["BUILD_PASTURE"]

            if target_tile.get("kind") != "PASTURE":
                return ["DIG"]

            if target_tile.get("animal") is None:
                if animals_in_farmer_inventory[target_animal] > 0:
                    return ["PLACE", target_animal, 1]

                return ["PASS"]

        # Service the animal at the current position first.
        current_animal = animal_tiles.get(pos_current)

        # Action logic block: FEED, CARE or HARVEST
        if (isinstance(current_animal, dict)
                and current_animal.get("kind") == "PASTURE"
                and current_animal.get("animal") == active_animal_plan.get(pos_current)
                and pos_current in farmer_animal_positions):
            if not current_animal.get("fed_today", False):
                if wheat_in_farmer_inventory > 0:
                    return ["FEED"]

                return get_wheat_action()

            if not current_animal.get("cared_today", False):
                return ["CARE"]

            if (
                current_animal.get("yield_units", 0)
                >= ANIMAL_HARVEST_THRESHOLD
            ):
                return ["HARVEST"]

        # Travel to another animal that requires attention.
        attention_targets = [
            position
            for position in farmer_animal_positions
            if (
                not animal_tiles[position].get("fed_today", False)
                or not animal_tiles[position].get("cared_today", False)
                or animal_tiles[position].get("yield_units", 0)
                    >= ANIMAL_HARVEST_THRESHOLD
            )
        ]

        if attention_targets:
            target = nearest_position(
                pos_current,
                attention_targets,
            )
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

        if (
            farmer_action[0] == "PLACE"
            and farmer_action[1] in ANIMAL_PRODUCT_ORDER
        ):
            product = farmer_action[1]
            market_orders.append([
                "SELL",
                product,
                animal_products_in_farmer_inventory[product],
            ])
            
            
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
    
    actions_to_liquidate = n_crops_carried + distance_between(pos_current, SHED_ACCESS_TILE)
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
        if pos_current != SHED_ACCESS_TILE:
            farmer_action = move_to(pos_current, SHED_ACCESS_TILE)
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
        if hand_index < len(HAND_WORK_TILES_EACH):
            assigned_tiles = HAND_WORK_TILES_EACH[hand_index]
        else:
            assigned_tiles = []

        hand_action = None

        if hand_index == SHEEP_HAND_INDEX:
            hand_action = choose_sheep_hand_action(
                tuple(hand_position),
                private["inventories"][hand_index + 1],
            )

        if hand_action is None:
            hand_action = choose_hand_action(
                tuple(hand_position),
                assigned_tiles,
                crop_selected_for_planting,
                available_seed_counts,
                selected_last_planting_day)
        hand_actions.append(hand_action)

    planned_strawberry_count = count_crop_plants(
        farm,
        "STRAWBERRY",
    )

    if farmer_action == ["PLANT", "STRAWBERRY"]:
        planned_strawberry_count += 1

    for hand_action in hand_actions:
        if hand_action == ["PLANT", "STRAWBERRY"]:
            planned_strawberry_count += 1
    
    
    ####################################
    # 7. Closing market order (buy seeds and purchase land)
    
    ## Buy crop seed (i.e. maintain a certain number available seed for each crop)
    for crop in CROPS_MANAGED:
        last_planting_day = FINAL_DAY - CROP_CONFIGS[crop]["harvest_day"]    
        seed_cost = CROP_CONFIGS[crop]["seed_cost"]
        
        target_seed_count = DEFAULT_SEED_TARGETS[crop]
        if crop == crop_selected_for_planting:
            if crop == "STRAWBERRY":
                target_seed_count = max(
                    0,
                    STRAWBERRY_PLANT_TARGET
                    - planned_strawberry_count,
                )
            else:
                target_seed_count = SELECTED_CROP_SEED_TARGET
        
        quantity_to_buy = (target_seed_count - available_seed_counts[crop])

        total_seed_cost = (quantity_to_buy * seed_cost)
        
        if  (quantity_to_buy > 0 
                and money_available >= total_seed_cost
                and obs["day"] <= last_planting_day):
            market_orders.append(["BUY_SEED", crop, quantity_to_buy])          
            money_available -= total_seed_cost
    
        
    # Unlock the second quadrant.
    if (SECOND_QUADRANT_NAME not in farm["unlocked_quadrants"]
            and obs["day"] >= SECOND_QUADRANT_PURCHASE_DAY
            and obs["day"] % 2 == 1                             # To stagger COW production
            and money_available >= (SECOND_QUADRANT_LAND_COST + LAND_WORKING_CAPITAL_RESERVE)
            and len(market_orders) < 10):
        market_orders.append(["BUY_LAND"])
        money_available -= SECOND_QUADRANT_LAND_COST
    
    
    return {
        "farmer": farmer_action,
        "hands": hand_actions,
        "market": market_orders,
    }
