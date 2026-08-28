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
