from kaggle_environments import make
from main import agent, TILES_MANAGED, CROP_BY_TILE

env = make(
    "kaggriculture",
    configuration={
        "episodeSteps": 120,
        "seed": 1,
    },
    debug=True,
)

env.run([agent, "pass"])

#final_step = env.steps[-1]

def describe_tile(tile):
    if tile is None:
        return "empty"

    if isinstance(tile, dict):
        name = tile.get("crop", tile.get("kind"))
        watered = tile.get("watered_today")
        crop_yield = tile.get("yield_units")

        return f"{name}(watered={watered}, yield={crop_yield})"

    return str(tile)

for step_number, step in enumerate(env.steps):
    player_state = step[0]
    obs = player_state.observation
    # tile = obs.farms[0].tiles[4][4]
    farmer_action = player_state.action["farmer"]
    market_action = player_state.action["market"]
    position = tuple(obs.farms[0].farmer)
    home_tile = obs.farms[0].tiles[4][4]
    second_tile = obs.farms[0].tiles[4][3]
    
    # Show the opening turns and the day boundary.
    if (step_number <= 6 
            or obs.hour in (0, 23)
            or farmer_action != ["PASS"]
            or market_action):        
        print(
            #f"record={step_number:2}, "
            f"game_step={obs.step:2}, "
            f"day={obs.day}, "
            f"hour={obs.hour:2}, "
            f"action={player_state.action['farmer']}, "
            f"position={position}, "
            # f"seeds={obs.private.seeds['CARROT']}, "
            # f"carried={obs.private.inventories[0].get('CARROT', 0)}, "
            # f"shed={obs.private.shed.get('CARROT', 0)}, "
            f"money={obs.farms[0].money}, "
            # f"market={player_state.action['market']}, "
            # f"tile={tile}"
            # f"home={describe_tile(home_tile)}, "
            # f"second={describe_tile(second_tile)}"
        )
        
final_observation = env.steps[-1][0].observation
final_farm = final_observation.farms[0]

print("\nFinal managed tiles:")

for index, position in enumerate(TILES_MANAGED):
    x, y = position
    tile = final_farm.tiles[y][x]
    assigned_crop = CROP_BY_TILE[position]

    print(
        f"{index:2}: "
        f"position={position}, "
        f"assigned={assigned_crop}, "
        f"actual={describe_tile(tile)}"
    )