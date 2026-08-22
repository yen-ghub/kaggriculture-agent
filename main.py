# Define tiles to manage in (x,y)
TILE_ROUTE = [
    (4,4), (3,4), (2,4), (1,4), (0,4),
    (0,3), (1,3), (2,3), (3,3), (4,3),
    (4,2), (3,2), (2,2), (1,2), (0,2),
    (0,1), (1,1), (2,1), (3,1), (4,1),
    (4,0), (3,0), (2,0), (1,0), (0,0)]

TILE_COUNT = 15
TILES_MANAGED = TILE_ROUTE[:TILE_COUNT]

# Fixed crop allocation used while building multi-crop support.
MELON_TILE_COUNT = 10
    
# Define constants and crop configs (a dict)
CROP_CONFIGS = {
    "CARROT": {
        "seed_cost": 20,
        "harvest_day": 3
    },
    "MELON": {
        "seed_cost": 80,
        "harvest_day": 10,
    },
}
 

CROPS_MANAGED = tuple(CROP_CONFIGS)
CROP_BY_TILE = {}

# Pair each tile with one type of plant (a dict)
for index, position in enumerate(TILES_MANAGED):
    if index < MELON_TILE_COUNT:
        CROP_BY_TILE[position] = "MELON"
    else:
        CROP_BY_TILE[position] = "CARROT"
   
LAST_HOUR_TODAY     = 23
FINAL_DAY           = 29
SHED_ACCESS_TILE    = (4,4) 


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
    ## Moving logic
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
        
    # Convert position (x,y) to tile [y][x]
    def tile_at(farm,pos):
        x,y = pos
        tile = farm["tiles"][y][x] 
        
        return tile 
    
    # Distance calculator
    def distance_between(coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2

        dist_manhattan = abs(x1 - x2) + abs(y1 - y2)
        
        return dist_manhattan
    
    # Find closest actionable tile to current position
    def nearest_position(current, positions):
        pos_nearest = None
        nearest_distance = None

        for position in positions:
            distance = distance_between(current, position)

            if pos_nearest is None or distance < nearest_distance:
                pos_nearest = position
                nearest_distance = distance

        return pos_nearest
    
    
    ####
    # 3. Market orders
    
    ## Buy crop seed if zero in inventory (i.e. maintain one available seed for each crop)
    for crop in CROPS_MANAGED:
        last_planting_day = FINAL_DAY - CROP_CONFIGS[crop]["harvest_day"]
        money_available = farm["money"]
        
        if  (seed_counts[crop] == 0 
                and money_available >= CROP_CONFIGS[crop]["seed_cost"]
                and obs["day"] <= last_planting_day):
            market_orders.append(["BUY_SEED", crop, 1])
            
    ## Sell crop of there is any in the shed (loop for each crop)
    for crop in CROPS_MANAGED:
        if shed_counts[crop] > 0:
            market_orders.append(["SELL", crop, shed_counts[crop]])
        
    
    ####
    # 4. Logic block to decide what to do. First, find a tile for action.
    ## Initiate empty target lists
    
    water_targets   = []
    harvest_targets = []
    plant_targets   = []
    mature_targets  = []        # Ready to harvest, regardless whether it is watered or not (for endgame)
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
    ## First check if the current tile is ready to harvest (mature + watered)        
    if not tile_current_harvestable:      
        for pos in TILES_MANAGED:
            tile = tile_at(farm, pos)
            assigned_crop = CROP_BY_TILE[pos]
            assigned_harvest_day = CROP_CONFIGS[assigned_crop]["harvest_day"]
            last_planting_day = FINAL_DAY - assigned_harvest_day
            
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
                if not tile["watered_today"]:
                    # Only water plants that can be harvested
                    if obs["day"] < FINAL_DAY or crop_age >= harvest_day:
                        water_targets.append(pos)
                elif crop_age >= harvest_day:
                    harvest_targets.append(pos)
            
            # Before planting, check if there is any weed tile to clear
            # (only clear if there is enough time to re-plant and harvest)
            elif (isinstance(tile, dict)
                    and tile["kind"] == "WEED"
                    and obs["day"] <= last_planting_day):
                weed_targets.append(pos)
            
            # If there is enough time, find an empty tile to plant (and water).
            elif (tile is None
                and seed_counts[assigned_crop] > 0
                and obs["hour"] < LAST_HOUR_TODAY
                and obs["day"] <= last_planting_day):
                plant_targets.append(pos)
            
    
    ## First priority, keep plants watered. Find an unwatered tile w/ plant.      
    ## Second priority, harvest. If there is no tile to water, go to a tile ready to harvest.
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
            if tile_target is None:
                farmer_action = ["PLANT", CROP_BY_TILE[pos_current]]    # Plant according to the assigned crop
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
    
    if (obs["day"] == FINAL_DAY
            and backpack_total > 0
            and not tile_current_harvestable
            and not mature_targets):    
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
    
    return {
        "farmer": farmer_action,
        "hands": [],
        "market": market_orders,
    }