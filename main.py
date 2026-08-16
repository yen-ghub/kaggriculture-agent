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

    # Define constants
    CARROT_SEED_COST    = 20
    LAST_HOUR_TODAY     = 23
    MAX_YIELD_DAY_CARROT = 3
    
    # Define tiles to manage in (x,y)
    TILES_MANAGED = [(4,4),(3,4)]
    
    # Get observations
    player_id   = obs["player"]
    farm        = obs["farms"][player_id]
    private     = obs["private"]
    shed        = private["shed"]
    farmer_inventory = private["inventories"][0]
    
    pos_current = tuple(farm["farmer"])
    
    # Inventory count
    seed_carrot = private["seeds"].get("CARROT", 0)
    shed_carrot = shed.get("CARROT", 0)
    
    # Initialise
    market_orders = []
    farmer_action = ["PASS"]
    
    # Define moving function
    def move_to(current,target):
        x_curr,y_curr = current
        x_targ,y_targ = target
        
        if x_curr > x_targ:
           return ["WEST"]
        if x_curr < x_targ:
            return ["EAST"]
        if y_curr > x_targ:
            return ["SOUTH"]
        if y_curr < y_targ:
            return ["NORTH"]
        
        return ["PASS"]
        
    # Convert position (x,y) to tile [y][x]
    def tile_at(farm,pos):
        x,y = pos
        tile = farm["tiles"][y][x] 
        
        return tile 
    
    # Market orders
    # Buy carrot seed if zero in inventory
    if  seed_carrot == 0 and farm["money"] >= CARROT_SEED_COST:
        market_orders.append(["BUY_SEED", "CARROT", 1])
    # Sell carrot of there is any in the shed
    if shed_carrot > 0:
        market_orders.append(["SELL", "CARROT", shed_carrot])
    
    ## Logic block to decide what to do. First, find a tile for action.
    # Initiate empty target position
    pos_target = None
    
    # First priority, keep plants watered. Find an unwatered tile w/ plant.
    for pos in TILES_MANAGED:
        tile = tile_at(farm, pos)
        if (tile is not None
                and tile["kind"] == "PLANT"
                and not tile["watered_today"]):  
            pos_target = pos
        
            break
            
    # Second priority, harvest. Find a plant ready to harvest.
    # Only check if there is no unwatered tile w/ plant.
    if pos_target is None:
         for pos in TILES_MANAGED:
             tile = tile_at(farm,pos) 
             
             if (tile is not None and tile["kind"] == "PLANT"):
                 crop_age = obs["day"] - tile["planted_day"]
                 
                 if crop_age >= MAX_YIELD_DAY_CARROT:
                     pos_target = pos
                     break
    
    # Third priority, plant. If there is enough time, find an empty tile to plant.
    if (pos_target is None
            and seed_carrot > 0
            and obs["hour"] < LAST_HOUR_TODAY):
        for pos in TILES_MANAGED:
            tile =  tile_at(farm,pos)
            
            if tile is None:
                pos_target = pos
                break
    
    # If there is a target position, move. If already at target position, load tile info.
    if pos_target is not None:
        if pos_target != pos_current:
            farmer_action = move_to(pos_current,pos_target)
        else:
            tile_target = tile_at(farm,pos_current)
            
            # Choose action depending on the tile info
            if tile_target is None:
                farmer_action = ["PLANT", "CARROT"]
            elif tile_target["watered_today"] is False:
                farmer_action = ["WATER"]
            else:
                farmer_action = ["HARVEST"]    
            
    
    return {
        "farmer": farmer_action,
        "hands": [],
        "market": market_orders,
    }