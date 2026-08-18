from kaggle_environments import make
from main import agent

SEEDS = [1, 2, 3, 4, 5]
OPPONENT = "starter"

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
    
    return our_state, opponent_state

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
        our_state, opponent_state = play_match(seed, our_position)
        
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

        print(
            f"seed={seed}, "
            f"position={our_position}, "
            f"ours={our_state.reward}, "
            f"opponent={opponent_state.reward}, "
            f"result={result}"
        )
        
completed_matches = results["WIN"] + results["LOSS"] + results["TIE"]
win_rate = 100 * results["WIN"] / completed_matches

print("\nSummary")
print(f"Wins:         {results['WIN']}")
print(f"Losses:       {results['LOSS']}")
print(f"Ties:         {results['TIE']}")
print(f"Errors:       {results['ERROR']}")
print(f"Win rate:     {win_rate:.1f}%")
print(f"Average ours: {sum(our_scores) / len(our_scores):.1f}")
print(f"Average opp:  {sum(opponent_scores) / len(opponent_scores):.1f}")