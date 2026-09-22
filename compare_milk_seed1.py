"""One-seed sanity comparison: main.py candidate vs the frozen predecessor.

Not a gate -- just the single-seed money check that accompanies the trace.
"""

import contextlib
import io

from kaggle_environments import make

import main
from baselines.locked_sw_livestock_v1 import agent as opponent_agent
from baselines.ne_goose_coexist_v1 import agent as baseline_agent

SEED = 1


def run(our_agent, label):
    env = make(
        "kaggriculture",
        configuration={
            "episodeSteps": 720,
            "seed": SEED,
        },
        debug=False,
    )

    with contextlib.redirect_stdout(io.StringIO()):
        env.run([our_agent, opponent_agent])

    ours = env.steps[-1][0].reward
    theirs = env.steps[-1][1].reward
    print(f"{label:12s} ours={ours:10.1f} opp={theirs:10.1f} diff={ours - theirs:+10.1f}")

    return ours


before = run(baseline_agent, "baseline")
after = run(main.agent, "candidate")

print(f"\ndelta: {after - before:+.1f}")
