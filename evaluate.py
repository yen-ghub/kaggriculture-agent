from kaggle_environments import make
from main import agent, CROPS_MANAGED
# from baselines.carrot_v1 import agent as carrot_agent
# from baselines.melon_v1 import agent as melon_agent
# from baselines.mixed_v1 import agent as mixed_agent
# from baselines.adaptive_v1 import agent as adaptive_agent
# from baselines.hand_v1 import agent as hand1_agent
# from baselines.hand_v2 import agent as hand2_agent
# from baselines.seed_buffer_v1 import agent as seed_buffer_agent
# from baselines.wheat_v1 import agent as wheat_agent
# from baselines.two_hands_v1 import agent as two_hands_agent
# from baselines.hand_planting_v1 import agent as hand_planting_agent
# from baselines.expanded_wheat_v1 import agent as expanded_wheat_agent
# from baselines.strawberry_v1 import agent as strawberry_agent
# from baselines.three_hands_v1 import agent as three_hands_agent
# from baselines.full_quadrant_strawberry_v1 import agent as full_quad_strawberry_agent
# from baselines.first_cow_v1 import agent as first_cow_agent
# from baselines.two_cows_v1 import agent as two_cows_agent
# from baselines.four_cows_v1 import agent as four_cows_agent
# from baselines.second_quadrant_v1 import agent as second_quadrant_agent
from baselines.low_strawberry_test import agent as low_strawberry_agent
from baselines.adaptive_strawberry_sales_v1 import agent as adaptive_strawberry_sales_agent
from baselines.endgame_liquidation_v1 import agent as endgame_liquidation_agent
from baselines.four_sheep_v1 import agent as four_sheep_agent
from baselines.full_second_quadrant_v1 import agent as second_quadrant_agent
from baselines.adaptive_tomato_v1 import agent as adaptive_tomato_agent
from baselines.adaptive_animal_v1 import agent as adaptive_animal_agent
from baselines.third_quadrant_v1 import agent as third_quadrant_agent
from baselines.strawberry_expansion_v1 import agent as strawberry_expansion_agent
from baselines.hand_weed_clearing_v1 import agent as hand_weed_clearing_agent

# Define variables
SEEDS = list(range(1,21))
# SEEDS = [1]
OPPONENTS = {
    # "starter": "starter",
    # "carrot_v1": carrot_agent,
    # "melon_v1": melon_agent,
    # "mixed_v1": mixed_agent,
    # "adaptive_v1": adaptive_agent,
    # "hand_v1": hand1_agent,
    # "hand_v2": hand2_agent,
    # "seed_buffer_v1": seed_buffer_agent,
    # "wheat_v1": wheat_agent,
    # "two_hands_v1": two_hands_agent,
    # "hand_planting_v1": hand_planting_agent,
    # "expanded_wheat_v1": expanded_wheat_agent,
    # "strawberry_agent_v1": strawberry_agent,
    # "three_hands_agent_v1": three_hands_agent,
    # "full_quad_strawberry_agent_v1": full_quad_strawberry_agent,
    # "first_cow_v1": first_cow_agent,
    # "two_cows_agent": two_cows_agent,
    # "four_cows_agent":four_cows_agent,
    # "second_quadrant_agent":second_quadrant_agent,
    # "low_strawberry_agent":low_strawberry_agent,
    # "adaptive_strawberry_sales_v1": adaptive_strawberry_sales_agent,
    # "endgame_liquidation_sales_v1": endgame_liquidation_agent,
    # "four_sheep_v1": four_sheep_agent,
    # "second_quadrant_v1": second_quadrant_agent,
    # "adaptive_tomato_v1": adaptive_tomato_agent,
    # "adaptive_animal_v1": adaptive_animal_agent,
    # "third_quadrant_v1": third_quadrant_agent,
    # "strawberry_expansion_v1": strawberry_expansion_agent,
    "hand_weed_clearing_v1": hand_weed_clearing_agent,
}    

PRODUCTS_TRACKED = CROPS_MANAGED + ("MILK", "WOOL")

# Define helper functions
def play_match(seed, our_position, opponent):
    if our_position == 0:
        agents = [agent, opponent]
    else:
        agents = [opponent, agent]
    
    env = make(
        "kaggriculture",
        configuration={
            "episodeSteps": 720,
            "seed": seed,
        },
        debug=False,
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
        for crop in PRODUCTS_TRACKED
    }

    for step in env.steps:
        action = step[our_position].action

        if not action:
            continue

        farmer_action = action.get("farmer", [])

        if farmer_action and farmer_action[0] == "HARVEST":
            harvest_count += 1

        for hand_action in action.get("hands", []):
            if hand_action and hand_action[0] == "HARVEST":
                harvest_count += 1

        for market_order in action.get("market", []):
            if (
                len(market_order) >= 3
                and market_order[0] == "SELL"
                and market_order[1] in PRODUCTS_TRACKED
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
        for crop in PRODUCTS_TRACKED
    }

    crops_in_shed = {
        crop: private.shed.get(crop, 0)
        for crop in PRODUCTS_TRACKED
    }

    return {
        "harvests": harvest_count,
        "sold": crops_sold,
        "carried": crops_carried,
        "shed": crops_in_shed,
    }

def average(values):
    if not values:
        return 0.0

    return sum(values) / len(values)


def evaluate_opponent(
        opponent_name,
        opponent,
        seeds,
        verbose=True,
):
    # These must reset for every opponent.
    results = {
        "WIN": 0,
        "LOSS": 0,
        "TIE": 0,
        "ERROR": 0,
    }

    
    # Accumulation count for each plant (dictionaries, one entry for each crop)
    our_scores = []
    opponent_scores = []
    harvest_counts = []

    sold_counts = {crop: [] for crop in PRODUCTS_TRACKED}

    final_carried_counts = {crop: [] for crop in PRODUCTS_TRACKED}

    final_shed_counts = {crop: [] for crop in PRODUCTS_TRACKED}

    for seed in seeds:
        for our_position in (0, 1):
            env, our_state, opponent_state = play_match(
                seed,
                our_position,
                opponent,
            )

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

            diagnostics = collect_diagnostics(
                env,
                our_position,
            )

            harvest_counts.append(diagnostics["harvests"])

            for crop in PRODUCTS_TRACKED:
                sold_counts[crop].append(diagnostics["sold"][crop])
                final_carried_counts[crop].append(diagnostics["carried"][crop])
                final_shed_counts[crop].append(diagnostics["shed"][crop])

            if verbose:
                print(
                    f"opponent={opponent_name}, "
                    f"seed={seed}, "
                    f"position={our_position}, "
                    f"ours={our_state.reward}, "
                    f"opponent_score={opponent_state.reward}, "
                    f"result={result} "
                    f"tomato sold: {diagnostics["sold"]["TOMATO"]}"
                )

    completed_matches = (results["WIN"] + results["LOSS"] + results["TIE"]
    )

    if completed_matches > 0:
        match_score = (results["WIN"] + 0.5 * results["TIE"]) / completed_matches
    else:
        match_score = 0.0

    crop_averages = {}

    for crop in PRODUCTS_TRACKED:
        crop_averages[crop] = {
            "sold": average(sold_counts[crop]),
            "carried": average(final_carried_counts[crop]),
            "shed": average(final_shed_counts[crop]),
        }

    return {
        "opponent": opponent_name,
        "results": results,
        "match_score": match_score,
        "average_ours": average(our_scores),
        "average_opponent": average(opponent_scores),
        "average_harvests": average(harvest_counts),
        "crops": crop_averages,
    }
    
def print_opponent_summary(summary):
    results = summary["results"]

    print(f"\nAgainst {summary['opponent']}")
    print(f"Wins:         {results['WIN']}")
    print(f"Losses:       {results['LOSS']}")
    print(f"Ties:         {results['TIE']}")
    print(f"Errors:       {results['ERROR']}")
    print(
        f"Match score:  "
        f"{100 * summary['match_score']:.1f}%"
    )
    print(
        f"Average ours: "
        f"{summary['average_ours']:.1f}"
    )
    print(
        f"Average opp:  "
        f"{summary['average_opponent']:.1f}"
    )
    print(
        f"Average harvests: "
        f"{summary['average_harvests']:.1f}"
    )

    for crop in PRODUCTS_TRACKED:
        crop_results = summary["crops"][crop]

        print(
            f"Average {crop} sold: "
            f"{crop_results['sold']:.1f}"
        )
        print(
            f"Average {crop} leftover: "
            f"{crop_results['carried'] + crop_results['shed']:.1f}"
        )
        
def main():
    suite_results = []

    for opponent_name, opponent in OPPONENTS.items():
        summary = evaluate_opponent(
            opponent_name,
            opponent,
            SEEDS,
            verbose=True,
        )

        print_opponent_summary(summary)
        suite_results.append(summary)

    macro_match_score = average([
        summary["match_score"]
        for summary in suite_results
    ])

    worst_result = min(
        suite_results,
        key=lambda summary: summary["match_score"],
    )

    total_errors = sum(
        summary["results"]["ERROR"]
        for summary in suite_results
    )

    print("\nSuite summary")
    print(
        f"Macro match score: "
        f"{100 * macro_match_score:.1f}%"
    )
    print(
        f"Worst opponent:    "
        f"{worst_result['opponent']} "
        f"({100 * worst_result['match_score']:.1f}%)"
    )
    print(f"Total errors:      {total_errors}")


if __name__ == "__main__":
    main()
