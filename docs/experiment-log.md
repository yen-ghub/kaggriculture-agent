# Experiment Log

All evaluations use both player positions.

| Candidate | Opponent | Seeds | Match score | Avg money | Harvests | Units sold | Notes |
|---|---|---:|---:|---:|---:|---:|---|
| Carrot v1 | Starter | 20 | 100% | 7754.1 | 60.0 | 180.0 | Seven tiles |
| Melon, 7 tiles | Carrot v1 | 20 | 100% | 22138.0 | 14.0 | 84.0 | Pure melon |
| Melon, 14 tiles | Carrot v1 | 20 | 100% | 30004.1 | 23.0 | 134.0 | Tile sweep |
| Melon, 15 tiles | Carrot v1 | 20 | 100% | 30011.2 | 23.1 | 134.1 | Current best count |
| Melon, 16 tiles | Carrot v1 | 20 | 100% | 29951.0 | 23.0 | 133.7 | Capacity declining |
| Melon v1 | Melon v1 | 20 | 50% | 16586.6 | 22.9 | 133.2 | Melon market competition |
| Mixed 10M/5C | Melon v1 | 20 | 87.5% | 18222.0 | 38.5 | 63.9 carrot, 100.7 melon | Fixed crop mix |
| Mixed v1 | Mixed v1 | 20 | 50.0% | 19197.4 | 38.5 | 63.8 carrot, 100.8 melon | Baseline self-test |
| Adaptive v1 | Mixed v1 | 20 | 80.0% | 18801.3 | 33.0 | 33.1 carrot, 128.6 melon | Opponent-aware crop selection |
| Adaptive v1 | Melon v1 | 20 | 92.5% | 17832.4 | 34.7 | 44.0 carrot, 117.9 melon | Generalization test |
| Hand v1 | Starter | 20 | 100.0% | 29968.4 | 56.7 | 112.8 carrot, 113.0 melon | Hired hand waters and harvests |
| Hand v1 | Carrot v1 | 20 | 100.0% | 29527.7 | 57.2 | 114.5 carrot, 113.0 melon | Tested against carrot specialist |
| Hand v1 | Melon v1 | 20 | 100.0% | 20046.9 | 61.5 | 130.7 carrot, 101.0 melon | Tested under melon market competition |
| Hand v1 | Mixed v1 | 20 | 100.0% | 20382.7 | 61.5 | 130.6 carrot, 101.0 melon | Tested against fixed crop mix |
| Hand v1 | Adaptive v1 | 20 | 100.0% | 20545.8 | 61.5 | 130.6 carrot, 101.0 melon | Tested against adaptive crop selection |
| Hand v1 | Hand v1 | 20 | 50.0% | 19896.7 | 60.9 | 130.4 carrot, 100.1 melon | Symmetric self-play control |
| Seed buffer v1 | Hand v2 | 5 | 100.0% | 20692.6 | 63.7 | 141.3 carrot, 99.6 melon | Two-seed buffer removes planting-related idle turns |
| Wheat v1 | Starter | 5 | 100.0% | 30788.5 | 58.7 | 41.2 wheat, 79.8 carrot, 114.0 melon | Wheat cap 8; 6.3 carrot leftover |
| Wheat v1 | Carrot v1 | 5 | 100.0% | 29971.0 | 58.7 | 44.4 wheat, 76.2 carrot, 114.0 melon | Wheat cap 8; 7.5 carrot leftover |
| Wheat v1 | Melon v1 | 5 | 100.0% | 20521.3 | 58.9 | 33.2 wheat, 100.8 carrot, 102.0 melon | Wheat cap 8; zero leftovers |
| Wheat v1 | Mixed v1 | 5 | 100.0% | 20686.4 | 59.1 | 34.0 wheat, 100.8 carrot, 102.0 melon | Wheat cap 8; zero leftovers |
| Wheat v1 | Adaptive v1 | 5 | 100.0% | 20776.8 | 59.1 | 34.0 wheat, 100.8 carrot, 102.0 melon | Wheat cap 8; zero leftovers |
| Wheat v1 | Hand v1 | 5 | 100.0% | 22679.7 | 57.4 | 89.2 wheat, 52.2 carrot, 97.2 melon | Wheat cap 8; 4.2 carrot leftover |
| Wheat v1 | Hand v2 | 5 | 100.0% | 22263.9 | 57.2 | 88.8 wheat, 53.7 carrot, 98.4 melon | Wheat cap 8; 2.1 carrot leftover |
| Wheat v1 | Seed buffer v1 | 5 | 100.0% | 21630.9 | 57.2 | 92.8 wheat, 53.1 carrot, 94.2 melon | Wheat cap 8; 1.5 carrot leftover |
| Wheat v1 | Hand v2 | 20 | 97.5% | 22405.5 | 57.8 | 81.2 wheat, 63.0 carrot, 96.0 melon | Release validation; 1.5 carrot leftover |
| Wheat v1 | Seed buffer v1 | 20 | 95.0% | 21633.2 | 58.4 | 82.2 wheat, 65.3 carrot, 94.0 melon | Release validation; 1.0 carrot leftover |
| Hand planting v1 | Melon v1 | 5 | 100.0% | 24706.4 | 82.9 | 64.0 wheat, 136.8 carrot, 126.0 melon | Hands can plant; zero leftovers |
| Hand planting v1 | Mixed v1 | 5 | 100.0% | 25768.6 | 82.9 | 64.0 wheat, 136.8 carrot, 126.0 melon | Hands can plant; zero leftovers |
| Hand planting v1 | Adaptive v1 | 5 | 100.0% | 25795.6 | 82.9 | 64.0 wheat, 136.8 carrot, 126.0 melon | Hands can plant; zero leftovers |
| Hand planting v1 | Hand v1 | 5 | 100.0% | 27240.2 | 80.2 | 98.4 wheat, 101.0 carrot, 126.0 melon | Hands can plant; 1.8 carrot leftover |
| Hand planting v1 | Hand v2 | 5 | 100.0% | 26841.4 | 79.9 | 103.2 wheat, 98.3 carrot, 126.0 melon | Hands can plant; zero leftovers |
| Hand planting v1 | Seed buffer v1 | 5 | 100.0% | 27276.6 | 79.8 | 104.0 wheat, 96.5 carrot, 126.0 melon | Hands can plant; 0.9 carrot leftover |
| Hand planting v1 | Wheat v1 | 5 | 100.0% | 26878.9 | 79.8 | 104.0 wheat, 96.5 carrot, 126.0 melon | Hands can plant; 0.9 carrot leftover |
| Hand planting v1 | Two hands v1 | 5 | 100.0% | 23058.0 | 79.8 | 104.0 wheat, 96.5 carrot, 126.0 melon | Direct predecessor comparison; 0.9 carrot leftover |
| Two hands v1 | Carrot v1 | 5 | 100.0% | 30298.1 | 60.4 | 47.2 wheat, 86.4 carrot, 114.0 melon | Two coordinated hands; sales-first market ordering |
| Two hands v1 | Melon v1 | 5 | 100.0% | 22077.9 | 60.7 | 44.4 wheat, 96.9 carrot, 102.0 melon | Tested under melon market competition |
| Two hands v1 | Mixed v1 | 5 | 100.0% | 22387.7 | 60.1 | 44.0 wheat, 96.3 carrot, 102.0 melon | Tested against fixed crop mix |
| Two hands v1 | Adaptive v1 | 5 | 100.0% | 22192.5 | 60.1 | 44.0 wheat, 96.3 carrot, 102.0 melon | Tested against adaptive crop selection |
| Two hands v1 | Hand v1 | 5 | 100.0% | 24420.7 | 57.8 | 92.4 wheat, 54.2 carrot, 97.2 melon | Tested against one-hand baseline |
| Two hands v1 | Hand v2 | 5 | 100.0% | 24003.9 | 56.0 | 85.2 wheat, 54.6 carrot, 99.0 melon | Tested against expanded one-hand baseline |
| Two hands v1 | Seed buffer v1 | 5 | 100.0% | 23891.5 | 57.5 | 90.4 wheat, 57.6 carrot, 94.2 melon | Tested against seed-buffer baseline |
| Two hands v1 | Wheat v1 | 5 | 100.0% | 23846.8 | 57.5 | 90.4 wheat, 57.6 carrot, 94.2 melon | Sales-first advantage over Wheat v1 |
| Two hands v1 | Two hands v1 | 5 | 50.0% | 21547.5 | 57.5 | 90.4 wheat, 57.6 carrot, 94.2 melon | Symmetric self-play: 2W, 2L, 6T |
| Two hands v1 | Two hands v1 | 20 | 50.0% | 21569.4 | 59.0 | 80.4 wheat, 69.2 carrot, 94.2 melon | Release self-play: 15W, 15L, 10T; 0.2 carrot leftover |
| Three hands v1 | Melon v1 | 5 | 100.0% | 29933.0 | 120.7 | 108.0 wheat, 188.1 carrot, 114.0 melon, 12.0 strawberry | 22 tiles; zero leftovers |
| Three hands v1 | Mixed v1 | 5 | 100.0% | 30746.8 | 120.7 | 108.0 wheat, 187.5 carrot, 114.0 melon, 12.0 strawberry | 22 tiles; 0.6 carrot leftover |
| Three hands v1 | Adaptive v1 | 5 | 100.0% | 30858.3 | 120.9 | 105.6 wheat, 189.9 carrot, 114.0 melon, 12.0 strawberry | 22 tiles; 0.6 carrot leftover |
| Three hands v1 | Two hands v1 | 5 | 100.0% | 29490.8 | 117.1 | 206.8 wheat, 100.8 carrot, 114.0 melon, 12.0 strawberry | 22 tiles; 2.4 carrot leftover |
| Three hands v1 | Hand planting v1 | 5 | 100.0% | 28767.7 | 116.8 | 215.2 wheat, 95.4 carrot, 114.0 melon, 12.0 strawberry | 22 tiles; 0.6 carrot leftover |
| Three hands v1 | Expanded Wheat v1 | 5 | 100.0% | 27894.2 | 117.9 | 182.8 wheat, 123.0 carrot, 114.0 melon, 12.0 strawberry | 22 tiles; 0.6 carrot leftover |
| Three hands v1 | Strawberry v1 | 5 | 100.0% | 27965.2 | 117.8 | 184.4 wheat, 121.5 carrot, 114.0 melon, 12.0 strawberry | Direct predecessor comparison; average lead 3029.5; 0.6 carrot leftover |
| Three hands v1 | Strawberry v1 | 20 | 100.0% | 28337.2 | 117.9 | 432.9 total | Release validation; average opponent 25040.5; average lead 3296.7; 0.9 total leftover |
| Full-quadrant Strawberry v1 | Mixed v1 | 5 | 100.0% | 41279.7 | 150.0 | 106.0 carrot, 84.0 melon, 100.0 strawberry | 25 tiles; zero leftovers |
| Full-quadrant Strawberry v1 | Adaptive v1 | 5 | 100.0% | 42436.3 | 150.0 | 106.0 carrot, 84.0 melon, 100.0 strawberry | 25 tiles; zero leftovers |
| Full-quadrant Strawberry v1 | Two hands v1 | 5 | 100.0% | 40054.3 | 150.0 | 106.0 carrot, 84.0 melon, 100.0 strawberry | 25 tiles; zero leftovers |
| Full-quadrant Strawberry v1 | Hand planting v1 | 5 | 100.0% | 33664.1 | 150.0 | 106.0 carrot, 84.0 melon, 100.0 strawberry | 25 tiles; zero leftovers |
| Full-quadrant Strawberry v1 | Expanded Wheat v1 | 5 | 100.0% | 34976.2 | 150.0 | 106.0 carrot, 84.0 melon, 100.0 strawberry | 25 tiles; zero leftovers |
| Full-quadrant Strawberry v1 | Strawberry v1 | 5 | 100.0% | 34786.6 | 150.0 | 106.0 carrot, 84.0 melon, 100.0 strawberry | Direct predecessor comparison; average lead 4360.8; zero leftovers |
| Full-quadrant Strawberry v1 | Three hands v1 | 5 | 90.0% | 36786.4 | 150.0 | 106.0 carrot, 84.0 melon, 100.0 strawberry | Strongest opponent; average lead 3562.5; zero leftovers |
| First cow v1 | Two hands v1 | 5 | 100.0% | 45659.7 | 149.1 | 8.4 wheat, 103.7 carrot, 78.0 melon, 88.1 strawberry, 36.0 milk | Two-Wheat feed reserve; zero other leftovers |
| First cow v1 | Hand planting v1 | 5 | 100.0% | 43999.4 | 149.0 | 8.0 wheat, 103.7 carrot, 78.0 melon, 88.1 strawberry, 36.0 milk | Two-Wheat feed reserve; zero other leftovers |
| First cow v1 | Expanded Wheat v1 | 5 | 100.0% | 44519.7 | 149.3 | 5.6 wheat, 105.5 carrot, 78.0 melon, 88.4 strawberry, 36.0 milk | Two-Wheat feed reserve; zero other leftovers |
| First cow v1 | Strawberry v1 | 5 | 100.0% | 44305.2 | 149.3 | 5.6 wheat, 105.5 carrot, 78.0 melon, 88.4 strawberry, 36.0 milk | Two-Wheat feed reserve; zero other leftovers |
| First cow v1 | Three hands v1 | 5 | 100.0% | 43524.6 | 149.1 | 7.2 wheat, 104.9 carrot, 78.0 melon, 88.0 strawberry, 36.0 milk | Two-Wheat feed reserve; zero other leftovers |
| First cow v1 | Full-quadrant Strawberry v1 | 5 | 100.0% | 44998.1 | 149.0 | 9.2 wheat, 103.7 carrot, 78.0 melon, 87.8 strawberry, 36.0 milk | Direct predecessor comparison; average lead 12441.0 |
| First cow v1 | First cow v1 | 5 | 50.0% | 42586.8 | 149.0 | 8.0 wheat, 103.7 carrot, 78.0 melon, 88.1 strawberry, 36.0 milk | Symmetric self-play: 1W, 1L, 8T; two-Wheat feed reserve |
| Two cows v1 | Two hands v1 | 5 | 100.0% | 51251.6 | 152.9 | 8.2 wheat, 91.0 carrot, 78.0 melon, 82.6 strawberry, 72.0 milk | Four-Wheat feed reserve; 1.8 strawberry leftover |
| Two cows v1 | Hand planting v1 | 5 | 100.0% | 49875.3 | 152.9 | 7.0 wheat, 90.7 carrot, 78.0 melon, 83.0 strawberry, 72.0 milk | Four-Wheat feed reserve; 1.8 strawberry leftover |
| Two cows v1 | Expanded Wheat v1 | 5 | 100.0% | 48721.0 | 152.8 | 7.0 wheat, 90.7 carrot, 78.0 melon, 82.9 strawberry, 72.0 milk | Four-Wheat feed reserve; 1.8 strawberry leftover |
| Two cows v1 | Strawberry v1 | 5 | 100.0% | 47833.0 | 152.8 | 7.0 wheat, 90.7 carrot, 78.0 melon, 82.9 strawberry, 72.0 milk | Four-Wheat feed reserve; 1.8 strawberry leftover |
| Two cows v1 | Three hands v1 | 5 | 100.0% | 49916.8 | 152.9 | 7.0 wheat, 91.0 carrot, 78.0 melon, 82.9 strawberry, 72.0 milk | Four-Wheat feed reserve; 1.8 strawberry leftover |
| Two cows v1 | Full-quadrant Strawberry v1 | 5 | 100.0% | 51029.7 | 152.9 | 8.2 wheat, 91.0 carrot, 78.0 melon, 82.6 strawberry, 72.0 milk | Four-Wheat feed reserve; 1.8 strawberry leftover |
| Two cows v1 | First cow v1 | 5 | 100.0% | 46933.1 | 152.9 | 7.0 wheat, 91.0 carrot, 78.0 melon, 82.9 strawberry, 72.0 milk | Direct predecessor comparison; average lead 3916.5; 1.8 strawberry leftover |
| Two cows v1 | First cow v1 | 20 | 100.0% | 48021.0 | 152.8 | 6.8 wheat, 90.9 carrot, 78.0 melon, 82.8 strawberry, 72.0 milk | Focused validation: 40W, 0L; average lead 4629.5; 1.9 strawberry leftover |
| Four cows, cow-only NE | Two cows v1 | 5 | 60.0% | 43721.3 | 176.8 | 17.6 wheat, 111.6 carrot, 78.0 melon, 91.4 strawberry, 117.6 milk | Four hands; expansion land used only for cows; eight-Wheat feed reserve |
| Four cows, five NE crops | Two cows v1 | 5 | 80.0% | 52414.0 | 201.8 | 72.8 wheat, 127.8 carrot, 78.0 melon, 92.0 strawberry, 120.0 milk | Five hands; six NE route entries, including one pasture; only eight-Wheat feed reserve remains |
| Four cows v1 | Two cows v1 | 5 | 100.0% | 54260.7 | 204.8 | 84.8 wheat, 127.8 carrot, 78.0 melon, 92.0 strawberry, 120.0 milk | Seven NE route entries; six NE crop tiles; average lead 6709.1 |
| Four cows v1 | Two cows v1 | 20 | 100.0% | 58015.7 | 204.4 | 86.0 wheat, 125.7 carrot, 78.0 melon, 92.0 strawberry, 120.0 milk | Focused validation: 40W, 0L; average lead 9866.3; only eight-Wheat feed reserve remains |

Seed buffer v1 completed a 70-match, seven-opponent development suite with a 100.0% macro match score, zero errors, and zero final crop leftovers.

Wheat v1 uses a concurrent wheat-plant cap of eight. It completed an 80-match, eight-opponent development suite with a 100.0% macro match score and zero errors. Its 20-seed validation against Hand v2 and Seed buffer v1 produced a 96.2% macro match score with zero errors. Wheat and melon had no final leftovers; small carrot leftovers remain an endgame optimization opportunity.

Three hands v1 manages 22 tiles and hires three hands per day for a total
daily hire cost of four. The hand zones contain five, four, and four tiles;
the third zone contains only the four expansion tiles, preserving the two
established hand routes and the farmer's ownership of the tenth Melon tile.
The agent maintains a target of three Strawberry plants beginning on day 10.

The candidate won all 40 matches in its focused 20-seed validation against
Strawberry v1, with zero errors. It then won all 70 matches in a seven-opponent,
five-seed development suite. All expected Strawberry and Melon production was
sold with zero leftovers for those crops. The maximum observed number of
market orders submitted during a turn was six, below the limit of ten.

Full-quadrant Strawberry v1 manages all 25 tiles with three hands. The evaluated
hand zones contain six, five, and seven tiles, leaving seven tiles to the farmer.
It targets 25 Strawberry plants beginning on day 10. Across the seven-opponent,
five-seed suite shown above, it won 69 of 70 matches for a 98.6% macro match
score with zero errors. Production was consistent in every matchup: 106 carrots,
84 melons, and 100 strawberries sold from 150 harvests, with no wheat production
and zero final leftovers.

First cow v1 replaces one crop tile at `(4, 4)` with a pasture and one cow. The
farmer buys Wheat from the market, feeds and cares for the cow daily, and
harvests the six-unit first Milk yield followed by ten three-unit yields. The
agent sold all 36 expected Milk units in every match with no Milk leftovers or
errors. It won all 60 matches in the six-opponent development suite shown above.
Against Full-quadrant Strawberry v1 it averaged 44998.1 coins, a lead of 12441.0.
Its symmetric self-play produced a 50.0% match score and 42586.8 average coins
despite combined market supply of 72 Milk. The two Wheat remaining at season end
are the deliberately maintained feed reserve; all other final leftovers were zero.

Two cows v1 replaces the first two crop tiles, `(4, 4)` and `(3, 4)`, with
pastures. The farmer services both cows while three hands manage crop zones of
seven, six, and seven route positions; the two pasture positions in the first
zone are skipped, giving effective hand workloads of five, six, and seven crop
tiles. The farmer retains five crop tiles in addition to the two cows.

Both cows completed their full production schedules in every reported match,
producing and selling all 72 expected Milk units with no Milk leftovers. The
candidate won all 70 matches in the seven-opponent, five-seed suite shown above,
with zero errors. It also won all 40 matches in its focused 20-seed validation
against First cow v1, averaging 48021.0 coins and leading by 4629.5. The four
Wheat remaining at season end are the deliberate two-cow feed reserve. Average
Strawberry leftovers were 1.8 in the development suite and 1.9 in the focused
validation.

Four cows v1 retains the initial pastures at `(4, 4)` and `(4, 3)`, unlocks the
NE quadrant on day 9, and adds cows at `(5, 4)` and `(5, 3)`. Delaying the second
pair staggers their Milk production relative to the initial pair. The farmer is
dedicated to the four cows, while five hands manage 23 NW crop tiles and six NE
crop tiles. The candidate maintains a target of 23 Strawberry plants and an
eight-Wheat feed reserve.

Using the expansion land only for cows produced a 60.0% match score against Two
cows v1. Adding a fifth hand and five NE crop tiles raised the score to 80.0%.
Adding one further NE crop tile raised the five-seed result to 100.0% and fixed
the previously losing seed. In the focused 20-seed validation, Four cows v1 won
all 40 matches with zero errors, averaged 58015.7 coins, and led by 9866.3. It
sold all 120 expected Milk units with no Milk, Carrot, Melon, or Strawberry
leftovers. The eight Wheat remaining at season end are the deliberately
maintained four-cow feed reserve.
