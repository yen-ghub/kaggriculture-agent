# Define tiles to manage in (x,y)
TILES_MANAGED = [(4,4),(3,4),(2,4),(1,4),(0,4),
                (1,3),(0,3)]

 # Choose crop to plant
CROP = "MELON"
    
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
   
CROP_SEED_COST      = CROP_CONFIGS[CROP]["seed_cost"]
CROP_HARVEST_DAY = CROP_CONFIGS[CROP]["harvest_day"]
LAST_HOUR_TODAY     = 23
FINAL_DAY           = 29
LAST_PLANTING_DAY   = FINAL_DAY - CROP_HARVEST_DAY
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
    
    # Get observations
    player_id       = obs["player"]
    farm            = obs["farms"][player_id]
    private         = obs["private"]
    shed            = private["shed"]
    farmer_inventory = private["inventories"][0]
    
    pos_current = tuple(farm["farmer"])
    
    # Inventory count in the shed and in the backpack
    seed_crop     = private["seeds"].get(CROP, 0)
    shed_crop     = shed.get(CROP, 0)
    backpack_crop = farmer_inventory.get(CROP, 0)
    
    # Initialise
    market_orders = []
    farmer_action = ["PASS"]
    
    ###
    
    # Define helper functions
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
    # Market orders
    ## Buy crop seed if zero in inventory
    if  (seed_crop == 0 
            and farm["money"] >= CROP_SEED_COST
            and obs["day"] <= LAST_PLANTING_DAY):
        market_orders.append(["BUY_SEED", CROP, 1])
    ## Sell crop of there is any in the shed
    if shed_crop > 0:
        market_orders.append(["SELL", CROP, shed_crop])
    
    
    ####
    # Logic block to decide what to do. First, find a tile for action.
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
    
    ## First check if current tile is harvestable (for efficiency)
    if (isinstance(tile_current, dict)
                and tile_current["kind"] == "PLANT"
                and tile_current["crop"] == CROP
                and tile_current["watered_today"] == True):
        crop_age = obs["day"] - tile_current["planted_day"]
        if crop_age >= CROP_HARVEST_DAY:
            tile_current_harvestable = True
            
    ## If not, scan MANAGED_TILES for actionable tiles
    ## First check if the current tile is ready to harvest (mature + watered)        
    if not tile_current_harvestable:      
        for pos in TILES_MANAGED:
            tile = tile_at(farm, pos)
            if (isinstance(tile, dict)
                    and tile["kind"] == "PLANT"
                    and tile["crop"] == CROP):
                crop_age = obs["day"] - tile["planted_day"]
                
                # List mature plants (regardless watered or not)
                if crop_age >= CROP_HARVEST_DAY:
                    mature_targets.append(pos)
                
                # Check if there is any tile to water, else, find a plant ready to harvest.
                if not tile["watered_today"]:
                    # Only water plants that can be harvested
                    if obs["day"] < FINAL_DAY or crop_age >= CROP_HARVEST_DAY:
                        water_targets.append(pos)
                elif crop_age >= CROP_HARVEST_DAY:
                    harvest_targets.append(pos)
            
            # Before planting, check if there is any weed tile to clear
            elif (isinstance(tile, dict)
                    and tile["kind"] == "WEED"
                    and obs["day"] <= LAST_PLANTING_DAY):
                weed_targets.append(pos)
            
            # If there is enough time, find an empty tile to plant (and water).
            elif (tile is None
                and seed_crop > 0
                and obs["hour"] < LAST_HOUR_TODAY
                and obs["day"] <= LAST_PLANTING_DAY):
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
                farmer_action = ["PLANT", CROP]
            elif tile_target.get("kind") == "WEED":
                farmer_action = ["DIG"]
            # If a plant exist, either harvest or water
            elif tile_target.get("kind") == "PLANT":
                if not tile_target["watered_today"]:
                    farmer_action = ["WATER"]
                else:
                    farmer_action = ["HARVEST"]    
                
    # Final liquidation of harvested plants in the backpack
    ## Check if it is the final day and if farmer is still carrying crop
    if (obs["day"] == FINAL_DAY
            and backpack_crop > 0
            and not tile_current_harvestable
            and not mature_targets):    
        if pos_current != SHED_ACCESS_TILE:
            farmer_action = move_to(pos_current, SHED_ACCESS_TILE)
        else:
            farmer_action = ["PLACE", CROP, backpack_crop]
            market_orders.append(["SELL", CROP, backpack_crop])
    
    return {
        "farmer": farmer_action,
        "hands": [],
        "market": market_orders,
    }