"""Write baselines/opp_melon_wave_v1.py: a test opponent built from
late_melon_four_v2 that plays the ladder's Melon pattern
(replays/5melon_starter_milk_heavy.json, 5melon_starter_milk_wool_heavy.json):
5 opening Melons, 12 Melons replanted on day 10 and sold as they are
harvested on day 20, no late Melons. Everything else is our own agent.
"""
import io

ROOT = r"D:\GitProjects\kaggriculture"
s = io.open(ROOT + r"\baselines\late_melon_four_v2.py", encoding="utf-8", newline="").read()


def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:80])
    s = s.replace(old, new)


header = '''# TEST OPPONENT, not one of our baselines. Built from late_melon_four_v2 by
# tools/make_opp_melon_wave.py: the ladder's Melon pattern
# (replays/5melon_starter_*.json) -- 5 opening Melons, 12 replanted on day 10
# and sold as harvested on day 20, no late Melons. Rest is our own agent.
'''
s = header + s

# 1. Five opening Melons, on the five tiles nearest the shed.
rep("DAY0_MELON_TARGET = 10\n", "DAY0_MELON_TARGET = 5\n")
rep('''DAY0_MELON_TILES = frozenset((
    (4, 2), (3, 2), (2, 2), (2, 3),
    (4, 1), (3, 1), (2, 1),
    (1, 3), (1, 2),
    (0, 4),
))''', '''DAY0_MELON_TILES = frozenset((
    (4, 2), (3, 2), (2, 2), (2, 3),
    (4, 1),
))''')

# 2. The late-Melon machinery becomes the day-10 second wave: 12 Melons, no
#    price floor, no opponent test (a Melon of ours planted on day 9 must not
#    switch it off), and it replaces Strawberry plantings too.
rep("LATE_MELON_PLANTING_DAY = FINAL_DAY - CROP_CONFIGS[\"MELON\"][\"harvest_day\"]\n",
    "LATE_MELON_PLANTING_DAY = MELON_HARVEST_DAY\n")
rep("LATE_MELON_COUNT = 4\n", "LATE_MELON_COUNT = 12\n")
rep("LATE_MELON_MIN_PRICE = 120\n", "LATE_MELON_MIN_PRICE = 0\n")
rep("        and not opponent_melon_wave\n", "")
rep('''            crop in STAPLE_CROPS
            and late_melons_to_plant[0] > 0''', '''            crop in STAPLE_CROPS + ("STRAWBERRY",)
            and late_melons_to_plant[0] > 0''')

#    Days 10-11: on day 10 the hands are on the Melon crew and the tiles only
#    clear at h18-h23 (7 of 12 planted on seed 2); the replay had all 12 up by
#    day 11.
rep('''            and tile.get("planted_day") == LATE_MELON_PLANTING_DAY''',
    '''            and LATE_MELON_PLANTING_DAY
                <= tile.get("planted_day", -1)
                <= LATE_MELON_PLANTING_DAY + 1''')
rep('''        and obs["day"] == LATE_MELON_PLANTING_DAY''',
    '''        and LATE_MELON_PLANTING_DAY <= obs["day"] <= LATE_MELON_PLANTING_DAY + 1''')
rep('''            last_planting_day = LATE_MELON_PLANTING_DAY''',
    '''            last_planting_day = LATE_MELON_PLANTING_DAY + 1''')

# 3. Days 20-21: bring the wave to the shed as harvested, like day 10.
rep('''        if obs["day"] != MELON_HARVEST_DAY:
            return None

        melon_carried = hand_inventory.get("MELON", 0)''', '''        if obs["day"] not in (
            MELON_HARVEST_DAY,
            LATE_MELON_PLANTING_DAY + CROP_CONFIGS["MELON"]["harvest_day"],
            LATE_MELON_PLANTING_DAY + CROP_CONFIGS["MELON"]["harvest_day"] + 1,
        ):
            return None

        melon_carried = hand_inventory.get("MELON", 0)''')

#    Only ripe Melons hold the walk back: the day-11 ones are still growing
#    on day 20.
rep('''            if (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and tile.get("crop") == "MELON"
            ):
                return True

        return False''', '''            if (
                isinstance(tile, dict)
                and tile.get("kind") == "PLANT"
                and tile.get("crop") == "MELON"
                and crop_is_harvestable(tile)
            ):
                return True

        return False''')

io.open(ROOT + r"\baselines\opp_melon_wave_v1.py", "w", encoding="utf-8", newline="").write(s)
print("wrote baselines/opp_melon_wave_v1.py")
