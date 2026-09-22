from kaggle_environments import make
from main import agent, CROPS_MANAGED
from baselines.full_second_quadrant_v1 import agent as second_quadrant_agent
from baselines.third_quadrant_v1 import agent as third_quadrant_agent
from baselines.strawberry_expansion_v1 import agent as strawberry_expansion_agent
from baselines.hand_weed_clearing_v1 import agent as hand_weed_clearing_agent
from baselines.eleven_hand_v1 import agent as eleven_hand_agent
from baselines.sw_strawberry_allocation_v1 import agent as sw_strawberry_allocation_agent
from baselines.early_sheep_v1 import agent as early_sheep_agent
from baselines.early_sw_v1 import agent as early_sw_agent
from baselines.melon_first_v1 import agent as melon_first_agent
from baselines.adaptive_sw_livestock import agent as adaptive_sw_livestock_agent
from baselines.fertilizer_collection_v1 import agent as fertilizer_collection_agent
from baselines.melon_single_wave_v1 import agent as melon_single_wave_agent
from baselines.farmer_fertilizer_v1 import agent as farmer_fertilizer_agent
from baselines.day3_sheep_v1 import agent as day3_sheep_agent
from baselines.day8_ne_strawberry_v1 import agent as day8_ne_strawberry_agent
from baselines.staggered_early_sheep_v1 import agent as staggered_early_sheep_agent
from baselines.sw_livestock_reservation_v1 import agent as sw_livestock_reservation_agent
from baselines.yarn_first_sw_sheep_v1 import agent as yarn_first_sw_sheep_agent
from baselines.fix_hand_fertilizer_v1 import agent as fix_hand_fertilizer_v1_agent
from baselines.fertilize_crops_v1 import agent as fertilize_crops_v1_agent
from baselines.staggered_additional_sheep_v1 import agent as staggered_additional_sheep_v1_agent
from baselines.reshuffle_goose_v1 import agent as reshuffle_goose_v1_agent
from baselines.locked_sw_livestock_v1 import agent as locked_sw_livestock_v1_agent
from baselines.day0_livestock_v1 import agent as day0_livestock_v1_agent
from baselines.ne_wheat_buffer_v1 import agent as ne_wheat_buffer_v1_agent
from baselines.twelve_melon_opening_v1 import agent as twelve_melon_opening_v1_agent
from baselines.staged_cow_v1 import agent as staged_cow_v1_agent
from baselines.early_ne_livestock_v1 import agent as early_ne_livestock_v1_agent
from baselines.early_ne_single_milk_v1 import agent as early_ne_single_milk_v1_agent
from baselines.melon_early_return_v1 import agent as melon_early_return_v1_agent
from baselines.crop_sale_priority_v1 import agent as crop_sale_priority_v1_agent
from baselines.early_nw_strawberry_v1 import agent as early_nw_strawberry_v1_agent
from baselines.wheat_feed_cash_reserve_v1 import agent as wheat_feed_cash_reserve_v1_agent
from baselines.water_slack_v1 import agent as water_slack_v1_agent
from baselines.water_slack_v2 import agent as water_slack_v2_agent
from baselines.ne_goose_coexist_v1 import agent as ne_goose_coexist_v1_agent

# Define variables
SEEDS = list(range(1,21))
# SEEDS = [1, 2, 3, 4, 5]
OPPONENTS = {
    # "second_quadrant_v1": second_quadrant_agent,
    # "third_quadrant_v1": third_quadrant_agent,
    # "strawberry_expansion_v1": strawberry_expansion_agent,
    # "hand_weed_clearing_v1": hand_weed_clearing_agent,
    # "eleven_hand_v1": eleven_hand_agent,
    # "sw_strawberry_allocation_v1": sw_strawberry_allocation_agent,
    # "early_sheep_v1": early_sheep_agent,
    # "melon_first_v1": melon_first_agent,
    # "adaptive_sw_livestock_v1": adaptive_sw_livestock_agent,
    # "fertilizer_collection_v1": fertilizer_collection_agent,
    # "melon_single_wave_v1": melon_single_wave_agent,
    # "farmer_fertilizer_v1": farmer_fertilizer_agent,
    # "day3_sheep_v1": day3_sheep_agent,
    # "day8_ne_strawberry_v1": day8_ne_strawberry_agent,
    # "staggered_early_sheep_v1": staggered_early_sheep_agent,
    # "sw_livestock_reservation_v1": sw_livestock_reservation_agent,
    # "yarn_first_sw_sheep_v1": yarn_first_sw_sheep_agent,
    # "fix_hand_fertilizer_v1": fix_hand_fertilizer_v1_agent,
    # "fertilize_crops_v1": fertilize_crops_v1_agent,
    # "staggered_additional_sheep_v1": staggered_additional_sheep_v1_agent,
    # "reshuffle_goose_v1": reshuffle_goose_v1_agent,
    # "locked_sw_livestock_v1": locked_sw_livestock_v1_agent,
    # "day0_livestock_v1": day0_livestock_v1_agent,
    # "ne_wheat_buffer_v1": ne_wheat_buffer_v1_agent,
    # "twelve_melon_opening_v1": twelve_melon_opening_v1_agent,
    # "staged_cow_v1": staged_cow_v1_agent,
    # "early_ne_livestock_v1": early_ne_livestock_v1_agent,
    # "early_ne_single_milk_v1": early_ne_single_milk_v1_agent,
    # "melon_early_return_v1": melon_early_return_v1_agent,
    # "early_nw_strawberry_v1": early_nw_strawberry_v1_agent,
    # "crop_sale_priority_v1": crop_sale_priority_v1_agent,
    # Cumulative: everything in main.py since the last frozen reference.
    # "wheat_feed_cash_reserve_v1": wheat_feed_cash_reserve_v1_agent,
    # Incremental: main.py at the NE Goose coexistence gate (commit a825256),
    # so a candidate is measured against that work rather than through it.
    # Not a promoted baseline -- its five-seed regressions were skipped.
    "ne_goose_coexist_v1": ne_goose_coexist_v1_agent,
    # Frozen baseline + the alternate-day watering rule only. Identical to the
    # current main.py, so leave it commented out unless main.py moves on.
    # "water_slack_v1": water_slack_v1_agent,
    # As v1 but skippable tiles are dropped from the route entirely instead of
    # being topped up when idle. Frees ~1,300 hand actions on seed 1 with no
    # loss of harvests or extra weeds -- but they all become PASS, so expect
    # neutral, not a win, until paired with an action-hungry feature.
    # "water_slack_v2": water_slack_v2_agent,
}

PRODUCTS_TRACKED = CROPS_MANAGED + (
    "EGG",
    "MILK",
    "WOOL",
    "FERTILIZER",
)

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
        verbose=False,
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
                    # f"tomato sold: {diagnostics["sold"]["TOMATO"]}"
                    f"sberry sold: {diagnostics["sold"]["STRAWBERRY"]}"
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
