from kaggle_environments import make
from main import agent

env = make(
    "kaggriculture",
    configuration={
        "episodeSteps": 48,
        "seed": 1,
    },
    debug=True,
)

env.run([agent, "pass"])

final_step = env.steps[-1]

for player_id, state in enumerate(final_step):
    print(
        f"Player {player_id}: "
        f"reward={state.reward}, "
        f"status={state.status}"
    )