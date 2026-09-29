"""Margin of several agents against one test opponent, both positions.

    python tools/vs_opponent.py 1-20 opp_melon_wave_v1 main early_melon_pair_v1

"main" is main.py; any other name is a module under baselines/. For a change
aimed at a kind of opponent (a test opponent such as opp_melon_wave_v1),
compare the candidate's average margin with its predecessor's against the
same opponent; a win count against it says little.
"""
import contextlib
import importlib
import io
import os
import sys

sys.path.insert(0, r"D:\GitProjects\kaggriculture")
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    from kaggle_environments import make


def load(name):
    if name == "main":
        return importlib.import_module("main").agent
    return importlib.import_module("baselines.%s" % name).agent


spec = sys.argv[1]
seeds = (list(range(int(spec.split("-")[0]), int(spec.split("-")[1]) + 1))
         if "-" in spec else [int(s) for s in spec.split(",")])
opponent = load(sys.argv[2])
names = sys.argv[3:]
agents = {name: load(name) for name in names}
totals = {name: 0 for name in names}

for seed in seeds:
    cells = []
    for name in names:
        margins = []
        for pos in (0, 1):
            pair = [agents[name], opponent] if pos == 0 else [opponent, agents[name]]
            env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed}, debug=False)
            with contextlib.redirect_stdout(io.StringIO()):
                env.run(pair)
            ours = env.steps[-1][pos].reward
            theirs = env.steps[-1][1 - pos].reward
            margins.append(ours - theirs)
        totals[name] += sum(margins)
        cells.append("%s %+6.0f/%+6.0f" % (name, margins[0], margins[1]))
    print("seed %2d  %s" % (seed, "   ".join(cells)), flush=True)

games = 2 * len(seeds)
print("average margin per game: %s" % "   ".join(
    "%s %+.1f" % (name, totals[name] / games) for name in names))
