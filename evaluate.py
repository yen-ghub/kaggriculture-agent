from kaggle_environments import make
from main import agent
from baselines.carrot_v1 import agent as baseline_agent

# Define variables
SEEDS = list(range(1,6))
OPPONENT = baseline_agent

harvest_counts = []
sold_counts = []
final_carried_counts = []
final_shed_counts = []


# Define helper functions
def play_match(seed, our_position):
    if our_position == 0:
        agents = [agent, OPPONENT]
    else:
        agents = [OPPONENT, agent]
    
    env = make(
        "kaggriculture",
        configuration={
            "episodeSteps": 720,
            "seed": seed,
        },
        debug=True,
    )

    env.run(agents)

    final_step = env.steps[-1]
    our_state = final_step[our_position]
    opponent_state = final_step[1 - our_position]
    
    return env, our_state, opponent_state

def collect_diagnostics(env, our_position):
    harvest_count = 0
    carrots_sold = 0

    for step in env.steps:
        action = step[our_position].action

        if not action:
            continue

        farmer_action = action.get("farmer", [])

        if farmer_action and farmer_action[0] == "HARVEST":
            harvest_count += 1

        for market_order in action.get("market", []):
            if (
                len(market_order) >= 3
                and market_order[0] == "SELL"
                and market_order[1] == "CARROT"
            ):
                carrots_sold += market_order[2]

    final_observation = env.steps[-1][our_position].observation
    private = final_observation.private

    carrots_carried = sum(
        inventory.get("CARROT", 0)
        for inventory in private.inventories
    )

    carrots_in_shed = private.shed.get("CARROT", 0)

    return {
        "harvests": harvest_count,
        "sold": carrots_sold,
        "carried": carrots_carried,
        "shed": carrots_in_shed,
    }

results = {
    "WIN": 0,
    "LOSS": 0,
    "TIE": 0,
    "ERROR": 0,
}

our_scores = []
opponent_scores = []

for seed in SEEDS:
    for our_position in (0, 1):
        env, our_state, opponent_state = play_match(seed, our_position)
        
        our_score = our_state.reward
        opponent_score = opponent_state.reward

        if our_state.status != "DONE":
            result = "ERROR"
        elif opponent_state.status != "DONE":
            result = "WIN"
        elif our_state.reward > opponent_state.reward:
            result = "WIN"
        elif our_state.reward < opponent_state.reward:
            result = "LOSS"
        else:
            result = "TIE"
            
        results[result] += 1
        
        if our_state.reward is not None:
            our_scores.append(our_state.reward)

        if opponent_state.reward is not None:
            opponent_scores.append(opponent_state.reward)

        # Diagnostics of harvest count
        diagnostics = collect_diagnostics(env, our_position)

        harvest_counts.append(diagnostics["harvests"])
        sold_counts.append(diagnostics["sold"])
        final_carried_counts.append(diagnostics["carried"])
        final_shed_counts.append(diagnostics["shed"])
                
        print(
            f"seed={seed}, "
            f"position={our_position}, "
            f"ours={our_state.reward}, "
            f"opponent={opponent_state.reward}, "
            f"result={result},"
            f"harvests={diagnostics['harvests']}, "
            f"sold={diagnostics['sold']}, "
            f"final_carried={diagnostics['carried']}, "
            f"final_shed={diagnostics['shed']}"
        )

total_matches = (
    results["WIN"]
    + results["LOSS"]
    + results["TIE"]
)        
match_score = (
    results["WIN"]
    + 0.5 * results["TIE"]
) / total_matches
# win_rate = 100 * results["WIN"] / completed_matches

print("\nSummary")
print(f"Wins:         {results['WIN']}")
print(f"Losses:       {results['LOSS']}")
print(f"Ties:         {results['TIE']}")
print(f"Errors:       {results['ERROR']}")
print(f"Match score:  {100 * match_score:.1f}%")
print(f"Average ours: {sum(our_scores) / len(our_scores):.1f}")
print(f"Average opp:  {sum(opponent_scores) / len(opponent_scores):.1f}")
print(f"Average harvests:      {sum(harvest_counts) / len(harvest_counts):.1f}")
print(f"Average carrots sold:  {sum(sold_counts) / len(sold_counts):.1f}")
print(f"Average final carried: {sum(final_carried_counts) / len(final_carried_counts):.1f}")
print(f"Average final shed:    {sum(final_shed_counts) / len(final_shed_counts):.1f}")