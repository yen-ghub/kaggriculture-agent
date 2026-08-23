from kaggle_environments import make
from main import agent, CROPS_MANAGED
from baselines.mixed_v1 import agent as baseline_agent

# Define variables
SEEDS = list(range(1,21))
# SEEDS = [1]
OPPONENT = baseline_agent

# Accumulation count for each plant (dictionaries, one entry for each crop)
harvest_counts = []

sold_counts = {
    crop: []
    for crop in CROPS_MANAGED
}

final_carried_counts = {
    crop: []
    for crop in CROPS_MANAGED
}

final_shed_counts = {
    crop: []
    for crop in CROPS_MANAGED
}


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
    #Initiate vars
    harvest_count = 0
    crops_sold = {
        crop: 0
        for crop in CROPS_MANAGED
    }

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
                and market_order[1] in CROPS_MANAGED
            ):
                crop = market_order[1]
                crops_sold[crop] += market_order[2]

    final_observation = env.steps[-1][our_position].observation
    private = final_observation.private

    crops_carried = {
        crop: sum(
            inventory.get(crop, 0)
            for inventory in private.inventories
        )
        for crop in CROPS_MANAGED
    }

    crops_in_shed = {
        crop: private.shed.get(crop, 0)
        for crop in CROPS_MANAGED
    }

    return {
        "harvests": harvest_count,
        "sold": crops_sold,
        "carried": crops_carried,
        "shed": crops_in_shed,
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

        for crop in CROPS_MANAGED:
            sold_counts[crop].append(diagnostics["sold"][crop])
            final_carried_counts[crop].append(diagnostics["carried"][crop])
            final_shed_counts[crop].append(diagnostics["shed"][crop])
                
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
for crop in CROPS_MANAGED:
    average_sold = sum(sold_counts[crop]) / len(sold_counts[crop])
    average_carried = (
        sum(final_carried_counts[crop])
        / len(final_carried_counts[crop])
    )
    average_shed = (
        sum(final_shed_counts[crop])
        / len(final_shed_counts[crop])
    )

    print(f"Average {crop} sold:    {average_sold:.1f}")
    print(f"Average {crop} carried: {average_carried:.1f}")
    print(f"Average {crop} in shed: {average_shed:.1f}")