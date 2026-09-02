from kaggle_environments import make
from main import (
    agent,
    TILES_MANAGED,
    COW_TILES,
    ADAPTIVE_ANIMAL_TILES,
    MILK_DEMAND_SHOPS,
    WOOL_DEMAND_SHOPS,
)
from baselines.hand_weed_clearing_v1 import agent as baseline_agent

env = make(
    "kaggriculture",
    configuration={
        "episodeSteps": 720,
        "seed": 2,
    },
    debug=True,
)

env.run([agent, baseline_agent])

#final_step = env.steps[-1]

max_market_order_count = 0
previous_new_sw_state = None
previous_hires_today = None

NEW_SW_TILES = (
    (2, 7),
    (1, 7),
    (0, 7),
    (0, 8),
    (1, 8),
    (2, 8),
)

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

    milk_shop_count = sum(
        shop in MILK_DEMAND_SHOPS
        for shop in shops
    )

    wool_shop_count = sum(
        shop in WOOL_DEMAND_SHOPS
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
    new_sw_state = tuple(
        describe_tile(farm.tiles[y][x])
        for x, y in NEW_SW_TILES
    )
    new_sw_weeds = tuple(
        position
        for position in NEW_SW_TILES
        if (
            isinstance(farm.tiles[position[1]][position[0]], dict)
            and farm.tiles[position[1]][position[0]].get("kind") == "WEED"
        )
    )
    new_sw_hand_action = (
        hand_actions[10]
        if len(hand_actions) > 10
        else None
    )
    new_sw_hand_position = (
        hands[10]
        if len(hands) > 10
        else None
    )
    hire_order_count = sum(
        order[0] == "HIRE"
        for order in market_action
    )
    hires_today = obs.farms[0].hires_today
    adaptive_tiles = [
        describe_tile(farm.tiles[y][x])
        for x, y in ADAPTIVE_ANIMAL_TILES
    ]
    adaptive_market_orders = [
        order
        for order in market_action
        if order[0] in ("BUY_LAND", "BUY_ANIMAL")
    ]
    farmer_on_adaptive_tile = position in ADAPTIVE_ANIMAL_TILES
    placed_animal_counts = {
        animal: sum(
            isinstance(tile, dict)
            and tile.get("kind") == "PASTURE"
            and tile.get("animal") == animal
            for row in farm.tiles
            for tile in row
        )
        for animal in ("COW", "SHEEP")
    }
    loose_animal_counts = {
        animal: (
            obs.private.shed.get(animal, 0)
            + sum(
                inventory.get(animal, 0)
                for inventory in obs.private.inventories
            )
        )
        for animal in ("COW", "SHEEP")
    }
    farmer_animal_products = {
        product: obs.private.inventories[0].get(product, 0)
        for product in ("MILK", "WOOL")
    }
    shed_animal_products = {
        product: obs.private.shed.get(product, 0)
        for product in ("MILK", "WOOL")
    }
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
        15 <= obs.day <= 20
        and (
            new_sw_state != previous_new_sw_state
            or hires_today != previous_hires_today
            or hire_order_count > 0
            or new_sw_hand_action not in (None, ["PASS"])
            or obs.hour in (0, 23)
        )
    ):
        print(
            f"day={obs.day:2}, "
            f"hr={obs.hour:2}, "
            f"hires={hires_today}, "
            f"hire_orders={hire_order_count}, "
            f"market_orders={market_order_count}, "
            f"hand_10={new_sw_hand_action}@{new_sw_hand_position}, "
            f"weeds={new_sw_weeds}, "
            f"new_sw={new_sw_state}"
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

    previous_new_sw_state = new_sw_state
    previous_hires_today = hires_today

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
