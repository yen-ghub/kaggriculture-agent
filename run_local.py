from kaggle_environments import make
from main import agent, TILES_MANAGED, COW_TILES
from baselines.one_tomato_v1 import agent as baseline_agent

env = make(
    "kaggriculture",
    configuration={
        "episodeSteps": 720,
        "seed": 1,
    },
    debug=True,
)

env.run([agent, baseline_agent])

#final_step = env.steps[-1]

max_market_order_count = 0

###########################################################################
# Helper functions:
def describe_tile(tile):
    if tile is None:
        return "empty"

    if isinstance(tile, dict):
        name = tile.get("animal", tile.get("crop", tile.get("kind")))
        watered = tile.get("watered_today")
        crop_yield = tile.get("yield_units")

        if tile.get("animal"):
            return (
                f"{name}(fed={tile.get('fed_today')}, "
                f"unfed={tile.get('consecutive_unfed')}, "
                f"cared={tile.get('cared_today')}, "
                f"yield={crop_yield})"
            )

        return f"{name}(watered={watered}, yield={crop_yield})"

    return str(tile)

def count_crop_plants(farm, crop):
    crop_count = 0

    for row in farm.tiles:
        for tile in row:
            if (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and tile.get("crop") == crop
            ):
                crop_count += 1

    return crop_count


#############################################################
# Start trace

for step_number, step in enumerate(env.steps):
    player_state = step[0]
    obs = player_state.observation
    farm = obs.farms[0]
    farmer_action = player_state.action["farmer"]
    market_action = player_state.action["market"]
    market_order_count = len(market_action)
    shops = list(obs.town.unlocked_shops)
    strawberry_shop_count = sum(
        shop in {
            "BRUNCH_SPOT",
            "ICE_CREAM_SHOP",
            "SMOOTHIE_SHOP",
            "FARMERS_MARKET",
        }
        for shop in shops
    )

    tomato_shop_count = sum(
        shop in {"PIZZA_SHOP", "FARMERS_MARKET"}
        for shop in shops
    )

    expected_tomato_target = (
        1
        if tomato_shop_count > 0
        else 0
    )

    requested_strawberry_target = (
        39
        if strawberry_shop_count >= 2
        else 33
    )

    expected_strawberry_target = min(requested_strawberry_target, (39 - expected_tomato_target))
   
    if market_order_count > 10:
        print(
            f"OVER_LIMIT step={obs.step}, day={obs.day}, "
            f"hour={obs.hour}, orders={market_action}"
        )

    tomato_plant_count = count_crop_plants(farm, "TOMATO")
    opponent_tomato_plant_count = count_crop_plants(
        obs.farms[1],
        "TOMATO",
    )

    strawberry_plant_count = count_crop_plants(farm, "STRAWBERRY")

    tomato_yield_available = sum(
        tile.get("yield_units", 0)
        for row in farm.tiles
        for tile in row
        if (
            isinstance(tile, dict)
            and tile.get("kind") == "PLANT"
            and tile.get("crop") == "TOMATO"
        )
    )
    max_market_order_count = max(max_market_order_count, market_order_count)
    position = tuple(obs.farms[0].farmer)
    hands = [
        tuple(hand_position)
        for hand_position in obs.farms[0].hands
    ]
    hand_actions = player_state.action["hands"]
    hires_today = obs.farms[0].hires_today
    home_tile = obs.farms[0].tiles[4][4]
    second_tile = obs.farms[0].tiles[4][3]
    first_cow_tile = obs.farms[0].tiles[4][4]
    second_cow_tile = obs.farms[0].tiles[3][4]
    cow_3_tile = obs.farms[0].tiles[4][5]  # (5,4)
    cow_4_tile = obs.farms[0].tiles[3][5]  # (5,3)
    sheep_1_tile = obs.farms[0].tiles[3][3]  # (3,3)
    sheep_2_tile = obs.farms[0].tiles[4][3]  # (3,4)
    sheep_3_tile = obs.farms[0].tiles[3][2]  # (2, 3)
    sheep_4_tile = obs.farms[0].tiles[4][2]  # (2, 4)
    tomato_actions = [
        action
        for action in [farmer_action, *hand_actions]
        if action == ["PLANT", "TOMATO"]
    ]

    tomato_market_orders = [
        order
        for order in market_action
        if len(order) >= 2 and order[1] == "TOMATO"
    ]

    
    seventh_hand_action = (
                            hand_actions[6]
                            if len(hand_actions) >= 7
                            else None
                        )
    
    products_to_trace = (
        "WHEAT",
        "CARROT",
        "MELON",
        "STRAWBERRY",
        "MILK",
        "WOOL",
    )

    inventories = [
        {
            product: inventory.get(product, 0)
            for product in products_to_trace
            if inventory.get(product, 0) > 0
        }
        for inventory in obs.private.inventories
    ]

    shed = {
        product: obs.private.shed.get(product, 0)
        for product in products_to_trace
        if obs.private.shed.get(product, 0) > 0
    }
    
    # Show the opening turns and the day boundary.
    # if (step_number <= 20 
    #         or obs.hour in (0, 23)
    #         or farmer_action != ["PASS"]
    #         or market_action):
    # if (
    #     # 18 >= obs.day >= 10
    #     obs.day >= 29
    #     and (
    #         obs.hour in (0, 1, 23)
    #         or farmer_action[0] in (
    #             "PICKUP",
    #             "FEED",
    #             "CARE",
    #             "HARVEST",
    #             "PLACE",
    #         )
    #         or market_action
    #     )
    # ):
    if (
        9 <= obs.day <= 29
        and (
            obs.hour in (0, 1, 23)
            or tomato_actions
            or tomato_market_orders
        )
    ):
        print(
            # f"record={step_number:2}, "
            # f"step={obs.step:2}, "
            f"day={obs.day}, "
            f"hr={obs.hour:2}, "
            f"tomato_shops={tomato_shop_count}, "
            f"targets=(tomato={expected_tomato_target}, "
            f"strawberry={expected_strawberry_target}), "
            f"plants=(tomato={tomato_plant_count}, "
            f"strawberry={strawberry_plant_count}), "
            f"opponent_tomatoes={opponent_tomato_plant_count}, "
            f"tomato_yield={tomato_yield_available}, "
            f"tomato_seeds={obs.private.seeds.get('TOMATO', 0)}, "
            f"tomato_shed={obs.private.shed.get('TOMATO', 0)}, "
            f"tomato_price={obs.market.prices['TOMATO']}, "
            f"tomato_inventory={obs.market.inventory['TOMATO']}, "
            f"tomato_actions={tomato_actions}, "
            f"tomato_market={tomato_market_orders}, "
            f"shops={shops}"
            # f"act={player_state.action['farmer']}, "
            # f"position={position}, "
            # f"hands={hands}, "
            # f"hand_act={hand_actions}, "
            # f"cow_1={describe_tile(first_cow_tile)}, "
            # f"cow_2={describe_tile(second_cow_tile)}, "
            # f"cow_3={describe_tile(cow_3_tile)}, "
            # f"cow_4={describe_tile(cow_4_tile)}, "
            # f"sheep_1={describe_tile(sheep_1_tile)}, "
            # f"sheep_2={describe_tile(sheep_2_tile)}, "
            # f"sheep_3={describe_tile(sheep_3_tile)}, "
            # f"sheep_4={describe_tile(sheep_4_tile)}, "
            # f"money={obs.farms[0].money}, "
            # f"inventories={inventories}, "
            # f"shed={shed}, "
            # f"farmer_wheat={obs.private.inventories[0].get('WHEAT', 0)}, "
            # f"shed_wheat={obs.private.shed.get('WHEAT', 0)}, "
            # f"unlocked={obs.farms[0].unlocked_quadrants}, "
            # f"hires_today={hires_today}, "
            # f"seventh_action={seventh_hand_action}, "
            # f"shops={shops}, "
            # f"strawberry_shops={strawberry_shop_count}, "
            # f"expected_sberry_target={expected_strawberry_target}, "
            # f"hires_today={hires_today}, "
            # f"carrot_seeds={obs.private.seeds.get('CARROT', 0)}, "
            # f"melon_seeds={obs.private.seeds.get('MELON', 0)}, "
            # f"wheat_seeds={obs.private.seeds.get('WHEAT', 0)}, "
            # f"wheat_price={obs.market.prices['WHEAT']}, "
            # f"carrot_price={obs.market.prices['CARROT']}, "
            # f"carried={obs.private.inventories[0].get('CARROT', 0)}, "
            # f"shed={obs.private.shed.get('CARROT', 0)}, "
            # f"money={obs.farms[0].money}, "
            # f"market={player_state.action['market']}, "
            # f"tile={tile}"
            # f"home={describe_tile(home_tile)}, "
            # f"second={describe_tile(second_tile)}"
        )

print(
    f"\nMaximum submitted market orders: "
    f"{max_market_order_count}"
)
        
final_observation = env.steps[-1][0].observation
final_farm = final_observation.farms[0]

print("\nFinal managed tiles:")

for index, position in enumerate(TILES_MANAGED):
    x, y = position
    tile = final_farm.tiles[y][x]

    print(
        f"{index:2}: "
        f"position={position}, "
        f"actual={describe_tile(tile)}"
    )
