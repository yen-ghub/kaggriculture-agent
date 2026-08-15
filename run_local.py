from kaggle_environments import make
from main import agent

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

for step_number, step in enumerate(env.steps):
    player_state = step[0]
    obs = player_state.observation
    tile = obs.farms[0].tiles[4][4]
    farmer_action = player_state.action["farmer"]
    market_action = player_state.action["market"]
    
    # Show the opening turns and the day boundary.
    if (step_number <= 4 
            or obs.hour in (0, 23)
            or farmer_action != ["PASS"]
            or market_action):        
        print(
            f"record={step_number:2}, "
            f"game_step={obs.step:2}, "
            f"day={obs.day}, "
            f"hour={obs.hour:2}, "
            f"action={player_state.action['farmer']}, "
            f"seeds={obs.private.seeds['CARROT']}, "
            f"carried={obs.private.inventories[0].get('CARROT', 0)}, "
            f"shed={obs.private.shed.get('CARROT', 0)}, "
            f"money={obs.farms[0].money}, "
            f"market={player_state.action['market']}, "
            f"tile={tile}"
        )