from kaggle_environments import make
from main import agent

env = make(
    "kaggriculture",
    configuration={
        "episodeSteps": 4,
        "seed": 1,
    },
    debug=True,
)

env.run([agent, "pass"])

#final_step = env.steps[-1]

for step_number, step in enumerate(env.steps):
    player_state = step[0]
    obs = player_state.observation
    
    print(
            f"step={step_number}, "
            f"action={player_state.action}, "
            f"money={obs.farms[0].money}, "
            f"carrot_seeds={obs.private.seeds['CARROT']}"
    )