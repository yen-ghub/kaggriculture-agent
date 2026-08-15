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

    CARROT_SEED_COST    = 20
    LAST_HOUR_TODAY     = 23
    MAX_YIELD_DAY_CARROT = 3
    
    # Get observations
    player_id   = obs["player"]
    farm        = obs["farms"][player_id]
    private     = obs["private"]
    shed        = private["shed"]
    farmer_inventory = private["inventories"][0]
    
    x,y         = farm["farmer"]
    tile_focus  = farm["tiles"][y][x]
    
    # Inventory count
    seed_carrot = private["seeds"].get("CARROT", 0)
    shed_carrot = shed.get("CARROT", 0)
    
    # Initialise
    market_orders = []
    farmer_action = ["PASS"]
    
    # Market orders
    # Buy carrot seed if zero in inventory
    if  seed_carrot == 0 and farm["money"] > CARROT_SEED_COST:
        market_orders.append(["BUY_SEED", "CARROT", 1])
    # Sell carrot of there is any in the shed
    if shed_carrot > 0:
        market_orders.append(["SELL", "CARROT", shed_carrot])
    
    # Plant carrot or water carrot or harvest carrot
    if (tile_focus is None 
            and seed_carrot > 0 
            and obs["hour"] < LAST_HOUR_TODAY):
        farmer_action = ["PLANT", "CARROT"]
    elif (tile_focus is not None
            and tile_focus["kind"] == "PLANT"
            and tile_focus["crop"] == "CARROT"):
        # Check if ready to harvest
        crop_age = obs["day"] - tile_focus["planted_day"]
        if not tile_focus["watered_today"]:
            farmer_action = ["WATER"]
        elif crop_age >= MAX_YIELD_DAY_CARROT:
            farmer_action = ["HARVEST"]
    
    return {
        "farmer": farmer_action,
        "hands": [],
        "market": market_orders,
    }