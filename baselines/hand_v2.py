# Define tiles to manage in (x,y)
TILE_ROUTE = [
    (4,4), (3,4), (2,4), (1,4), (0,4),
    (0,3), (1,3), (2,3), (3,3), (4,3),
    (4,2), (3,2), (2,2), (1,2), (0,2),
    (0,1), (1,1), (2,1), (3,1), (4,1),
    (4,0), (3,0), (2,0), (1,0), (0,0)]

TILE_COUNT = 17
TILES_MANAGED = TILE_ROUTE[:TILE_COUNT]

# Fixed crop allocation used while building multi-crop support.
MELON_TILE_COUNT = 10
    
# Define constants and crop configs (a dict)
CROP_CONFIGS = {
    "CARROT": {
        "seed_cost": 20,
        "harvest_day": 3,
        "harvest_yield": 3
    },
    "MELON": {
        "seed_cost": 80,
        "harvest_day": 10,
        "harvest_yield": 6
    },
}
 

CROPS_MANAGED = tuple(CROP_CONFIGS)

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

CROP_BY_TILE = make_fixed_crop_plan(MELON_TILE_COUNT)
MELON_REPLANT_PRICE_THRESHOLD = 220
POST_GLUT_MELON_TARGET = 4
HEAVY_OPPONENT_MELON_TARGET = 13
   
LAST_HOUR_TODAY     = 23
FINAL_DAY           = 29
SHED_ACCESS_TILE    = (4,4) 
FIRST_HAND_HIRE_COST = 1
HAND_WORK_TILE_COUNT = 8
HAND_WORK_TILES = TILES_MANAGED[:HAND_WORK_TILE_COUNT]


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
    
    # 1. Get observations
    player_id       = obs["player"]
    farm            = obs["farms"][player_id]
    private         = obs["private"]
    shed            = private["shed"]
    farmer_inventory = private["inventories"][0]
    
    pos_current = tuple(farm["farmer"])
    
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
    
    # Initialise
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
    
    ## 2.3 Distance calculator
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
    
    ## 2.6
    def crop_profit_per_day(crop):
        crop_config = CROP_CONFIGS[crop]
        current_price = obs["market"]["prices"][crop]

        expected_revenue = (
            crop_config["harvest_yield"]
            * current_price
        )
        expected_profit = (
            expected_revenue
            - crop_config["seed_cost"]
        )

        return expected_profit / crop_config["harvest_day"]
    
    ## 2.7 Adaptive crop selection, considering market price and opponent's crop selection
    def choose_crop_for_planting():
        # First decision layer, filter based on no of days left, no point planting if can't harvest
        carrot_last_planting_day = (
            FINAL_DAY
            - CROP_CONFIGS["CARROT"]["harvest_day"]
        )
        melon_last_planting_day = (
            FINAL_DAY
            - CROP_CONFIGS["MELON"]["harvest_day"]
        )

        # When there is not enough time for both crops
        if obs["day"] > carrot_last_planting_day:
            return None

        # When there is not enough time for melon, choose carrot
        if obs["day"] > melon_last_planting_day:
            return "CARROT"

        # Second decision layer, based on expected profit per day (based on the current market price)
        carrot_profit = crop_profit_per_day("CARROT")
        melon_profit = crop_profit_per_day("MELON")

        # Prefer carrots when current melon economics are worse
        if melon_profit <= carrot_profit:
            return "CARROT"

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
    def choose_hand_action(hand_position):
        
        hand_harvest_targets = []
        hand_water_targets = []
        
        # Scan the farm-hand-assigned tiles
        for position in HAND_WORK_TILES:
            tile = tile_at(farm, position)

            # Validate the tile before reading plant-specific fields.
            if (not isinstance(tile, dict)
                    or tile.get("kind") != "PLANT"
                    or tile.get("crop") not in CROPS_MANAGED):
                continue
            
            crop = tile["crop"]
            crop_age = obs["day"] - tile["planted_day"]
            harvest_day = CROP_CONFIGS[crop]["harvest_day"]
            
            if (isinstance(tile, dict)
                    and tile.get("kind") == "PLANT"
                    and tile["watered_today"]
                    and crop_age >= harvest_day):
                hand_harvest_targets.append(position)
            elif not tile["watered_today"]:
                hand_water_targets.append(position)

        # Check if already on actionable tile before travelling elsewhere
        if hand_position in hand_harvest_targets:
            return ["HARVEST"]

        if hand_position in hand_water_targets:
            return ["WATER"]

        # Travel to harvest ready produce first, then handle remaining watering.
        if hand_harvest_targets:
            target = nearest_position(hand_position, hand_harvest_targets)
        elif hand_water_targets:
            target = nearest_position(hand_position, hand_water_targets)
        else:
            return ["PASS"]

        return move_to(hand_position, target)
    
    ####
    # 3. Market orders
    money_available = farm["money"]
    
    if (obs["day"] < FINAL_DAY
            and obs["hour"] == 0 
            and money_available >= FIRST_HAND_HIRE_COST):
        market_orders.append(["HIRE"])
        money_available -= FIRST_HAND_HIRE_COST
        
    ## Buy crop seed if zero in inventory (i.e. maintain one available seed for each crop)
    for crop in CROPS_MANAGED:
        last_planting_day = FINAL_DAY - CROP_CONFIGS[crop]["harvest_day"]    
        seed_cost = CROP_CONFIGS[crop]["seed_cost"]
        
        if  (seed_counts[crop] == 0 
                and money_available >= seed_cost
                and obs["day"] <= last_planting_day):
            market_orders.append(["BUY_SEED", crop, 1])          
            money_available -= seed_cost
            
    ## Sell crop of there is any in the shed (loop for each crop)
    for crop in CROPS_MANAGED:
        if shed_counts[crop] > 0:
            market_orders.append(["SELL", crop, shed_counts[crop]])
        
    
    ####
    # 4. Logic block to decide what to do. First, find a tile for action.
    
    ## Initiate empty target lists
    water_targets   = []
    harvest_targets = []        # Fully ready to harvest (mature + watered)
    plant_targets   = []
    mature_targets  = []        # Partially ready to harvest, regardless whether it is watered or not (for endgame)
    weed_targets    = []
    #pos_target = None
    
    ## To check if current tile is ready to harvest
    tile_current = tile_at(farm, pos_current)
    tile_current_harvestable = False
    
    ## First check if current tile is harvestable (i.e. mature + watered, for efficiency)
    if (isinstance(tile_current, dict)
                and tile_current["kind"] == "PLANT"
                and tile_current["crop"] in CROPS_MANAGED
                and tile_current["watered_today"] == True):
        current_crop = tile_current["crop"]
        crop_age = obs["day"] - tile_current["planted_day"]
        
        if crop_age >= CROP_CONFIGS[current_crop]["harvest_day"]:
            tile_current_harvestable = True
            
    ## If not, scan MANAGED_TILES for actionable tiles
    
    ## Pick a crop based on the current strategy (market price + opponent's crops)
    crop_selected_for_planting = choose_crop_for_planting()       
    if crop_selected_for_planting is not None:
        selected_harvest_day = CROP_CONFIGS[crop_selected_for_planting]["harvest_day"]

        selected_last_planting_day = (FINAL_DAY - selected_harvest_day)
    else:
        selected_last_planting_day = -1
                   
    ## First check if the current tile is ready to harvest (mature + watered)        
    if not tile_current_harvestable:      
        for pos in TILES_MANAGED:
            tile = tile_at(farm, pos)
            
            if (isinstance(tile, dict)
                    and tile["kind"] == "PLANT"
                    and tile["crop"] in CROPS_MANAGED):
                crop_age        = obs["day"] - tile["planted_day"]
                planted_crop    = tile["crop"]
                harvest_day     = CROP_CONFIGS[planted_crop]["harvest_day"]
                
                # List mature plants (regardless watered or not, useful for the final liquidation)
                if crop_age >= harvest_day:
                    mature_targets.append(pos)
                
                # Check if there is any tile to water, else, find a plant ready to harvest.
                # First check who is the tile assigned to
                hand_is_responsible = (len(farm["hands"]) > 0 and pos in HAND_WORK_TILES)
                if not tile["watered_today"]:
                    # Only water plants that can be harvested.
                    if (not hand_is_responsible 
                            and (obs["day"] < FINAL_DAY or crop_age >= harvest_day)):
                        water_targets.append(pos)
                        
                elif crop_age >= harvest_day:
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
                    and crop_selected_for_planting is not None
                    and seed_counts[crop_selected_for_planting] > 0
                    and obs["hour"] < LAST_HOUR_TODAY
                    and obs["day"] <= selected_last_planting_day):
                plant_targets.append(pos)
            
    
    ## First, harvest mature crops that are already watered.   
    ## Second, water crops that still need care.
    ## Third priority, plant. If no tile to water and no plant ready to harvest, plant.
    if tile_current_harvestable:
        pos_target = pos_current
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

    for hand_position in farm["hands"]:
        hand_action = choose_hand_action(
            tuple(hand_position)
        )
        hand_actions.append(hand_action)
    
    return {
        "farmer": farmer_action,
        "hands": hand_actions,
        "market": market_orders,
    }