def agent(obs):
    
    market_orders = []
    
    if obs["step"] == 0:
        market_orders.append(["BUY_SEED", "CARROT", 1])
    
    return {
        "farmer": ["PASS"],
        "hands": [],
        "market": market_orders,
    }