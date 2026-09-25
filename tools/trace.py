"""Read-only diagnostics for a kaggriculture match.

One CLI for the views we keep needing, so a regression check is a command
rather than another throwaway script. Changes no agent behaviour.

    python tools/trace.py market --product MILK --seed 1
    python tools/trace.py tiles --at 6,4 6,3 --days 9-16
    python tools/trace.py hands --seed 6
    python tools/trace.py crops --seed 10
    python tools/trace.py h2h --seeds 6,10
    python tools/trace.py isolation --seeds 1-20
    python tools/trace.py mirror --seeds 1-20 --opponent offday_fertilize_sw_v1

Method rules these views exist to enforce (learned the hard way; see
docs/experiment-log.md):

* Always compare HEAD-TO-HEAD against the baseline, never both agents against
  some third opponent. The market is shared, so a third-opponent comparison
  gives each agent its own market and hides every timing effect. It scored one
  change +3,787 on a seed where the head-to-head gave -2,947.
* For anything that changes WHEN produce reaches the shed, read sale HOURS,
  not totals. Identical volume at a different hour is worth thousands on a
  glutted product.
* Confirm non-qualifying seeds are byte-identical before trusting a gated
  experiment (`isolation`).
* A head-to-head win is not income. On a shared market a change can win by
  lowering the opponent's price while earning us nothing (`mirror`): NE
  off-day Fertilizer won seed 1 by +2,048 with our own money up just 6.
* A big single-seed swing may be a re-rolled town, not the strategy: the
  shop draw depends on both farms' empty tiles (docs/mechanics.md). `mirror`
  flags seeds whose shop sequence changed.
"""

import argparse
import contextlib
import importlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# kaggle_environments prints OpenSpiel registration noise on import.
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    from kaggle_environments import make

import main as main_module
from main import SHED_ACCESS_TILES

# Keep this pointed at the current frozen baseline (docs/current_roadmap.md).
# A stale default is how a diagnostic quietly starts measuring the wrong thing.
DEFAULT_OPPONENT = "melon_layout_v1"
MOVES = ("NORTH", "SOUTH", "EAST", "WEST")
PRODUCTS = (
    "WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON",
    "EGG", "MILK", "WOOL", "FERTILIZER",
)


def load_opponent(name):
    module = importlib.import_module("baselines.%s" % name)
    return module.agent


def play(seed, opponent, our_position=0):
    """One head-to-head game. Returns (env, our_position)."""
    agents = (
        [main_module.agent, opponent]
        if our_position == 0
        else [opponent, main_module.agent]
    )
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": 720, "seed": seed},
        debug=False,
    )
    with contextlib.redirect_stdout(io.StringIO()):
        env.run(agents)
    return env


def parse_days(spec):
    if not spec:
        return None
    if "-" in spec:
        lo, hi = spec.split("-", 1)
        return range(int(lo), int(hi) + 1)
    return [int(d) for d in spec.split(",")]


def parse_seeds(spec):
    if "-" in spec:
        lo, hi = spec.split("-", 1)
        return list(range(int(lo), int(hi) + 1))
    return [int(s) for s in spec.split(",")]


def parse_coords(values):
    out = []
    for v in values:
        x, y = v.split(",")
        out.append((int(x), int(y)))
    return out


def unit_actions(step, position):
    """Yield (label, action, coordinate) for the farmer and every hand."""
    action = step[position].action
    if not action:
        return
    farm = step[position].observation["farms"][position]
    farmer_action = action.get("farmer")
    if farmer_action:
        yield "farmer", farmer_action, tuple(farm["farmer"])
    hands = farm["hands"]
    for index, hand_action in enumerate(action.get("hands") or []):
        if hand_action and index < len(hands):
            yield "hand %d" % index, hand_action, tuple(hands[index])


def describe_tile(tile):
    if tile is None:
        return "EMPTY"
    if not isinstance(tile, dict):
        return str(tile)
    if tile.get("animal"):
        return "%s/%s fed=%d cared=%d y=%d" % (
            tile.get("kind"), tile["animal"],
            int(tile.get("fed_today", False)),
            int(tile.get("cared_today", False)),
            tile.get("yield_units", 0),
        )
    if tile.get("kind") == "PLANT":
        return "%s@d%s%s" % (
            tile.get("crop"), tile.get("planted_day"),
            "" if tile.get("watered_today") else " DRY",
        )
    return str(tile.get("kind"))


# ---------------------------------------------------------------- views


def view_tiles(args, opponent):
    env = play(args.seed, opponent)
    coords = parse_coords(args.at)
    days = parse_days(args.days)
    print("seed %d, end of each day" % args.seed)
    for index, step in enumerate(env.steps):
        if index % 24 != 23:
            continue
        day = index // 24
        if days is not None and day not in days:
            continue
        farm = step[0].observation["farms"][0]
        cells = [
            "(%d,%d)=%s" % (x, y, describe_tile(farm["tiles"][y][x]))
            for x, y in coords
        ]
        print("day %2d: %s" % (day, "  |  ".join(cells)))


def view_market(args, opponent):
    """Every sale with its HOUR and price -- the view that catches timing."""
    env = play(args.seed, opponent)
    wanted = args.product.upper() if args.product else None

    for position, label in ((0, "OURS"), (1, "OPPONENT")):
        revenue, quantity, sales = {}, {}, []
        for index, step in enumerate(env.steps):
            action = step[position].action
            if not action:
                continue
            prices = step[position].observation["market"]["prices"]
            for order in action.get("market", []):
                if len(order) < 3 or order[0] != "SELL":
                    continue
                item, count = order[1], order[2]
                price = prices.get(item, 0)
                revenue[item] = revenue.get(item, 0) + count * price
                quantity[item] = quantity.get(item, 0) + count
                if wanted and item == wanted:
                    sales.append((index // 24, index % 24, count, price))

        print("\n=== %s (reward %.0f) ===" % (label, env.steps[-1][position].reward))
        for item in PRODUCTS:
            if quantity.get(item):
                print("    %-11s qty %4d  revenue %8d  avg %6.1f"
                      % (item, quantity[item], revenue[item],
                         revenue[item] / quantity[item]))
        if wanted:
            print("    %s sales (day.hour xqty @price):" % wanted)
            print("      " + "  ".join(
                "d%d.h%02d x%d @%d" % s for s in sales[:args.limit]))


def view_hands(args, opponent):
    env = play(args.seed, opponent)
    shed = set(SHED_ACCESS_TILES)
    stats = {}
    for step in env.steps:
        for label, action, coordinate in unit_actions(step, 0):
            entry = stats.setdefault(label, {"mix": {}, "shed": 0, "was_shed": False})
            entry["mix"][action[0]] = entry["mix"].get(action[0], 0) + 1
            in_shed = coordinate in shed
            if in_shed and not entry["was_shed"]:
                entry["shed"] += 1
            entry["was_shed"] = in_shed

    print("seed %d -- per-unit workload (idle%% is the capacity signal)" % args.seed)
    for label in sorted(stats, key=lambda k: (k != "farmer", k)):
        mix = stats[label]["mix"]
        total = sum(mix.values())
        moves = sum(mix.get(d, 0) for d in MOVES)
        idle = mix.get("PASS", 0)
        top = sorted(mix.items(), key=lambda kv: -kv[1])[:5]
        print("%-8s total %4d  idle %4d (%4.1f%%)  move %4d  productive %4d  "
              "shed-trips %3d  %s"
              % (label, total, idle, 100.0 * idle / max(total, 1), moves,
                 total - moves - idle, stats[label]["shed"],
                 dict(top)))


def view_crops(args, opponent):
    env = play(args.seed, opponent)
    plantings, sold, weeds, dry = set(), {}, {}, {}
    for index, step in enumerate(env.steps):
        farm = step[0].observation["farms"][0]
        action = step[0].action
        if action:
            for order in action.get("market", []):
                if len(order) >= 3 and order[0] == "SELL":
                    sold[order[1]] = sold.get(order[1], 0) + order[2]
        for y, row in enumerate(farm["tiles"]):
            for x, tile in enumerate(row):
                if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                    plantings.add((tile["crop"], (x, y), tile.get("planted_day")))
        if index % 24 == 23:
            day = index // 24
            weeds[day] = sum(
                1 for row in farm["tiles"] for t in row
                if isinstance(t, dict) and t.get("kind") == "WEED"
            )
            dry[day] = sum(
                1 for row in farm["tiles"] for t in row
                if isinstance(t, dict) and t.get("kind") == "PLANT"
                and not t.get("watered_today", False)
            )

    counts = {}
    for crop, _, _ in plantings:
        counts[crop] = counts.get(crop, 0) + 1
    print("seed %d" % args.seed)
    print("  plantings: %s" % dict(sorted(counts.items())))
    print("  sold     : %s" % {k: sold[k] for k in PRODUCTS if sold.get(k)})
    print("  weeds by day (>=10): %s"
          % {d: v for d, v in weeds.items() if d >= 10 and v})
    print("  unwatered plants at end of day (>=10): %s"
          % {d: v for d, v in dry.items() if d >= 10 and v})


def view_h2h(args, opponent):
    print("head-to-head vs %s (both positions)" % args.opponent)
    total = 0
    for seed in parse_seeds(args.seeds):
        for position in (0, 1):
            env = play(seed, opponent, position)
            ours = env.steps[-1][position].reward
            theirs = env.steps[-1][1 - position].reward
            delta = ours - theirs
            total += delta
            verdict = "WIN " if delta > 0 else ("LOSS" if delta < 0 else "TIE ")
            print("  seed %2d pos %d  %s  ours %8.0f  opp %8.0f  delta %+8.0f"
                  % (seed, position, verdict, ours, theirs, delta))
    print("  sum of deltas: %+.0f" % total)


def view_isolation(args, opponent):
    """Which seeds actually changed? A gated experiment must tie elsewhere.

    Compares against the baseline playing ITSELF, not against the other
    player in the same game: some seeds are position-asymmetric (16, and 9
    at 132,407 vs 131,727), so an unchanged agent can still score differently
    from its opponent. Two games per seed.
    """
    print("isolation vs %s -- IDENTICAL means the change did not fire"
          % args.opponent)
    changed = []
    for seed in parse_seeds(args.seeds):
        env = play(seed, opponent)
        ours = env.steps[-1][0].reward
        theirs = env.steps[-1][1].reward
        mirror_env = make(
            "kaggriculture",
            configuration={"episodeSteps": 720, "seed": seed},
            debug=False,
        )
        with contextlib.redirect_stdout(io.StringIO()):
            mirror_env.run([opponent, opponent])
        mirror = (mirror_env.steps[-1][0].reward, mirror_env.steps[-1][1].reward)
        if (ours, theirs) == mirror:
            print("  seed %2d  %9.0f / %9.0f  IDENTICAL" % (seed, ours, theirs))
        else:
            changed.append(seed)
            print("  seed %2d  ours %9.0f  opp %9.0f  delta %+8.0f"
                  "  (mirror %.0f / %.0f)"
                  % (seed, ours, theirs, ours - theirs, mirror[0], mirror[1]))
    print("  changed seeds: %s" % (changed or "none"))


def view_shops(args, opponent):
    """Which seeds carry which demand prefix -- i.e. which seeds a gated
    experiment can even fire on.

    Runs a short episode per seed, since only the first two shops matter.
    CAVEAT: the shop draw advances with board state, so a prefix scanned
    against one opponent need not match another. Scan against the opponent you
    will actually gate against -- a mirror scan said only seeds 6 and 10
    qualified where the head-to-head also had 16.
    """
    from main import EGG_DEMAND_SHOPS, MILK_DEMAND_SHOPS, WOOL_DEMAND_SHOPS

    print("first two shops vs %s (short episodes)" % args.opponent)
    for seed in parse_seeds(args.seeds):
        env = make(
            "kaggriculture",
            configuration={"episodeSteps": 240, "seed": seed},
            debug=False,
        )
        with contextlib.redirect_stdout(io.StringIO()):
            env.run([main_module.agent, opponent])
        shops = list(env.steps[-1][0].observation["town"]["unlocked_shops"])[:2]
        flags = []
        if any(s in EGG_DEMAND_SHOPS for s in shops):
            flags.append("EGG")
        if any(s in WOOL_DEMAND_SHOPS for s in shops):
            flags.append("WOOL")
        milk = sum(s in MILK_DEMAND_SHOPS for s in shops)
        if milk:
            flags.append("MILKx%d" % milk)
        print("  seed %2d  %-28s %s"
              % (seed, ",".join(shops), "+".join(flags) or "-"))


def view_mirror(args, opponent):
    """Whose money moved? Splits a head-to-head delta into our own gain and
    the opponent's loss, both measured from the baseline playing itself.

    Two games per seed: candidate vs baseline, and baseline vs baseline.
      own    = ours      - mirror    (money the change earned us)
      taken  = mirror    - theirs    (money it cost the opponent)
      delta  = own + taken
    A seed whose shop sequence differs from the mirror's re-rolled the town
    (docs/mechanics.md); its split is not a like-for-like comparison. Its
    delta still is, since both players share the re-rolled town.

    Small-sample warning: a change that moves many tiles early re-rolls most
    towns. Planting twelve NE Strawberry on day 7 re-rolled 16 of 20, leaving
    four readable seeds. Judge such a change by its delta across all seeds and
    treat the own/taken average as indicative only.
    """
    print("mirror vs %s -- own = ours - mirror, taken = mirror - theirs"
          % args.opponent)
    totals = {"own": 0, "taken": 0, "seeds": 0}
    rerolled = []

    for seed in parse_seeds(args.seeds):
        env = play(seed, opponent)
        mirror_env = make(
            "kaggriculture",
            configuration={"episodeSteps": 720, "seed": seed},
            debug=False,
        )
        with contextlib.redirect_stdout(io.StringIO()):
            mirror_env.run([opponent, opponent])

        ours = env.steps[-1][0].reward
        theirs = env.steps[-1][1].reward
        mirror = mirror_env.steps[-1][0].reward
        own, taken = ours - mirror, mirror - theirs

        same_town = (
            env.steps[-1][0].observation["town"]["unlocked_shops"]
            == mirror_env.steps[-1][0].observation["town"]["unlocked_shops"]
        )
        if not same_town:
            rerolled.append(seed)

        print("  seed %2d  mirror %9.0f  ours %9.0f  theirs %9.0f  "
              "own %+7.0f  taken %+7.0f  delta %+7.0f%s"
              % (seed, mirror, ours, theirs, own, taken, own + taken,
                 "" if same_town else "  TOWN RE-ROLLED"))

        if same_town:
            totals["own"] += own
            totals["taken"] += taken
            totals["seeds"] += 1

    n = totals["seeds"]
    if n:
        print("  average over %d like-for-like seeds: own %+.1f  taken %+.1f  "
              "delta %+.1f" % (n, totals["own"] / n, totals["taken"] / n,
                               (totals["own"] + totals["taken"]) / n))
    print("  re-rolled towns (excluded from the average): %s"
          % (rerolled or "none"))


VIEWS = {
    "shops": view_shops,
    "tiles": view_tiles,
    "market": view_market,
    "hands": view_hands,
    "crops": view_crops,
    "h2h": view_h2h,
    "isolation": view_isolation,
    "mirror": view_mirror,
}


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("view", choices=sorted(VIEWS))
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--seeds", default="1",
                        help="for h2h/isolation/mirror: 6,10 or 1-20")
    parser.add_argument("--opponent", default=DEFAULT_OPPONENT,
                        help="module under baselines/ (default: %s)" % DEFAULT_OPPONENT)
    parser.add_argument("--days", help="for tiles: 9-16 or 9,10,11")
    parser.add_argument("--at", nargs="+", default=["6,4"],
                        help="for tiles: coordinates as x,y")
    parser.add_argument("--product", help="for market: restrict sale list")
    parser.add_argument("--limit", type=int, default=16,
                        help="for market: how many sales to list")
    return parser


def cli(argv=None):
    args = build_parser().parse_args(argv)
    opponent = load_opponent(args.opponent)
    VIEWS[args.view](args, opponent)


if __name__ == "__main__":
    cli()
