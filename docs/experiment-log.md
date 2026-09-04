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
| Second-quadrant expansion candidate | Four cows v1 | 20 | 45.0% | 57861.9 | 227.0 | 27.9 wheat, 114.0 carrot, 78.0 melon, 132.0 strawberry, 120.0 milk | Mirror-match stress test: 18W, 22L; opponent averaged 57256.8; average lead 605.1; 12.1 wheat leftover |
| Delayed Sheep v1 | Second-quadrant expansion v1 | 5 | 100.0% | 58768.6 | 225.0 | 12.0 wheat, 112.0 carrot, 78.0 melon, 121.0 strawberry, 120.0 milk, 36.0 wool | Development test: 10W, 0L; average opponent 56228.0; average lead 2540.6; 8.0 wool leftover |
| Delayed Sheep v1 | Second-quadrant expansion v1 | 20 | 100.0% | 62014.9 | 225.0 | 12.0 wheat, 112.0 carrot, 78.0 melon, 121.0 strawberry, 120.0 milk, 36.0 wool | Focused validation: 40W, 0L; average opponent 59535.1; average lead 2479.8; 8.0 wool leftover |
| Delayed Sheep v1, immediate Strawberry sales | Low-Strawberry test (target 9) | 5 | 80.0% | 54255.7 | 225.0 | 12.0 wheat, 112.0 carrot, 78.0 melon, 121.0 strawberry, 120.0 milk, 36.0 wool | A/B control: 8W, 2L; average opponent 49889.2; average lead 4366.5 |
| Adaptive Strawberry sales candidate | Low-Strawberry test (target 9) | 5 | 100.0% | 55180.3 | 225.0 | 12.0 wheat, 112.0 carrot, 78.0 melon, 121.0 strawberry, 120.0 milk, 36.0 wool | Cap 8: 10W, 0L; average opponent 50116.4; average lead 5063.9 |
| Delayed Sheep v1, immediate Strawberry sales | Low-Strawberry test (target 9) | 20 | 82.5% | 60437.8 | 225.0 | 12.0 wheat, 112.0 carrot, 78.0 melon, 121.0 strawberry, 120.0 milk, 36.0 wool | A/B control: 33W, 7L; average opponent 56903.2; average lead 3534.6 |
| Adaptive Strawberry sales candidate | Low-Strawberry test (target 9) | 20 | 87.5% | 61010.3 | 225.0 | 12.0 wheat, 112.0 carrot, 78.0 melon, 121.0 strawberry, 120.0 milk, 36.0 wool | Cap 8 validation: 35W, 5L; average opponent 57053.7; average lead 3956.6 |
| Adaptive Strawberry sales candidate | Full-quadrant Strawberry v1 | 5 | 100.0% | 61553.5 | 225.0 | 12.0 wheat, 112.0 carrot, 78.0 melon, 121.0 strawberry, 120.0 milk, 36.0 wool | Heavy-opponent development test; average opponent 36495.4 |
| Adaptive Strawberry sales candidate | First cow v1 | 5 | 100.0% | 57333.1 | 225.0 | 12.0 wheat, 112.0 carrot, 78.0 melon, 121.0 strawberry, 120.0 milk, 36.0 wool | Development test; average opponent 43463.4 |
| Adaptive Strawberry sales candidate | Two cows v1 | 5 | 100.0% | 56983.4 | 225.0 | 12.0 wheat, 112.0 carrot, 78.0 melon, 121.0 strawberry, 120.0 milk, 36.0 wool | Development test; average opponent 45723.7 |
| Adaptive Strawberry sales candidate | Four cows v1 | 5 | 80.0% | 57905.9 | 225.0 | 12.0 wheat, 112.0 carrot, 78.0 melon, 121.0 strawberry, 120.0 milk, 36.0 wool | Suite minimum: 8W, 2L; average opponent 51936.5 |
| Adaptive Strawberry sales candidate | Second-quadrant expansion v1 | 5 | 100.0% | 58768.6 | 225.0 | 12.0 wheat, 112.0 carrot, 78.0 melon, 121.0 strawberry, 120.0 milk, 36.0 wool | Heavy-opponent guard preserved the delayed-Sheep result; average opponent 56228.0 |
| Shop-aware seventh hand candidate | Low-Strawberry test (target 9) | 5 | 100.0% | 57958.3 | 260.4 | 52.8 wheat, 148.0 carrot, 78.0 melon, 130.6 strawberry, 120.0 milk, 36.0 wool | 10W, 0L; average opponent 48181.6; average lead 9776.7; 16.8 wheat, 6.6 carrot, 4.6 strawberry, and 8.0 wool leftover |
| Shop-aware seventh hand candidate | Adaptive Strawberry sales v1 | 5 | 100.0% | 61377.8 | 260.6 | 57.6 wheat, 148.0 carrot, 78.0 melon, 129.8 strawberry, 120.0 milk, 36.0 wool | Direct predecessor comparison: 10W, 0L; average opponent 58254.2; average lead 3123.6; zero errors |
| Shop-aware seventh hand candidate | Adaptive Strawberry sales v1 | 20 | 100.0% | 66365.4 | 260.3 | 46.2 wheat, 148.0 carrot, 78.0 melon, 132.0 strawberry, 120.0 milk, 36.0 wool | Focused validation: 40W, 0L; average opponent 63222.6; average lead 3142.8; 15.3 wheat, 6.1 carrot, 5.2 strawberry, and 8.0 wool leftover |
| Endgame liquidation v1 | Adaptive Strawberry sales v1 | 5 | 100.0% | 64646.0 | 258.6 | 70.8 wheat, 151.0 carrot, 78.0 melon, 133.0 strawberry, 120.0 milk, 44.0 wool | 10W, 0L; average opponent 58268.0; average lead 6378.0; zero leftovers and errors |
| Endgame liquidation v1 | Adaptive Strawberry sales v1 | 20 | 100.0% | 69601.0 | 258.3 | 55.5 wheat, 151.1 carrot, 78.0 melon, 136.2 strawberry, 120.0 milk, 44.0 wool | Focused validation: 40W, 0L; average opponent 63236.2; average lead 6364.8; zero leftovers and errors |
| Compact four-Sheep candidate | Endgame liquidation v1 | 20 | 92.5% | 69436.7 | 265.0 | 46.6 wheat, 150.0 carrot, 78.0 melon, 135.6 strawberry, 120.0 milk, 87.0 wool | Focused validation: 37W, 3L; average opponent 64990.9; average lead 4445.8; zero leftovers and errors |
| Compact four-Sheep candidate | Low-Strawberry test (target 9) | 5 | 100.0% | 66726.0 | 265.0 | 52.2 wheat, 150.0 carrot, 78.0 melon, 134.2 strawberry, 120.0 milk, 87.0 wool | Regression test: 10W, 0L; average opponent 49334.6; average lead 17391.4; zero leftovers and errors |
| Compact four-Sheep candidate | Adaptive Strawberry sales v1 | 5 | 100.0% | 64294.0 | 265.0 | 48.2 wheat, 150.6 carrot, 78.0 melon, 135.0 strawberry, 120.0 milk, 87.0 wool | Regression test: 10W, 0L; average opponent 56322.2; average lead 7971.8; zero leftovers and errors |
| Compact four-Sheep candidate | Endgame liquidation v1 | 5 | 100.0% | 63886.2 | 265.0 | 58.6 wheat, 150.0 carrot, 78.0 melon, 132.6 strawberry, 120.0 milk, 87.0 wool | Regression test: 10W, 0L; average opponent 57255.4; average lead 6630.8; zero leftovers and errors |
| Full second-quadrant v1 | Four Sheep v1 | 20 | 100.0% | 72434.9 | 285.2 | 74.7 wheat, 159.1 carrot, 78.0 melon, 145.8 strawberry, 120.0 milk, 87.0 wool | Focused validation: 40W, 0L; average opponent 69889.9; average lead 2545.0; zero leftovers and errors |
| Full second-quadrant v1 | Low-Strawberry test (target 9) | 5 | 100.0% | 67152.8 | 283.6 | 108.2 wheat, 159.0 carrot, 78.0 melon, 135.8 strawberry, 120.0 milk, 87.0 wool | Regression test: 10W, 0L; average opponent 48381.0; average lead 18771.8; zero leftovers and errors |
| Full second-quadrant v1 | Adaptive Strawberry sales v1 | 5 | 100.0% | 61335.5 | 284.2 | 95.4 wheat, 159.0 carrot, 78.0 melon, 139.6 strawberry, 120.0 milk, 87.0 wool | Regression test: 10W, 0L; average opponent 50795.9; average lead 10539.6; zero leftovers and errors |
| Full second-quadrant v1 | Endgame liquidation v1 | 5 | 100.0% | 62998.2 | 283.6 | 108.2 wheat, 159.0 carrot, 78.0 melon, 135.8 strawberry, 120.0 milk, 87.0 wool | Regression test: 10W, 0L; average opponent 56950.4; average lead 6047.8; zero leftovers and errors |
| Full second-quadrant v1 | Four Sheep v1 | 5 | 100.0% | 64640.2 | 284.8 | 82.6 wheat, 159.0 carrot, 78.0 melon, 143.4 strawberry, 120.0 milk, 87.0 wool | Regression test: 10W, 0L; average opponent 62567.2; average lead 2073.0; zero leftovers and errors |
| Immediate one-Tomato candidate | Second-quadrant v1 | 20 | 55.0% | 72030.9 | 284.9 | 73.4 wheat, 156.8 carrot, 78.0 melon, 143.2 strawberry, 3.4 tomato, 120.0 milk, 87.0 wool | Focused validation: 20W, 16L, 4T; average opponent 71965.8; average lead 65.1; zero leftovers and errors |
| Adaptive Tomato v1 | Second-quadrant v1 | 20 | 55.0% | 72086.9 | 285.2 | 73.4 wheat, 157.5 carrot, 78.0 melon, 143.2 strawberry, 3.4 tomato, 120.0 milk, 87.0 wool | Opponent-aware delayed sales: 20W, 16L, 4T; average opponent 71940.3; average lead 146.6; zero leftovers and errors |
| Delayed two-Tomato candidate | Second-quadrant v1 | 20 | 50.0% | 72042.6 | 285.6 | 69.2 wheat, 157.7 carrot, 78.0 melon, 143.0 strawberry, 5.0 tomato, 120.0 milk, 87.0 wool | Rejected 0/1/2 retest: 18W, 18L, 4T; average opponent 71888.1; average lead 154.5; lower match score despite slightly higher mean margin |
| Adaptive Tomato v1 | Adaptive Strawberry sales v1 | 5 | 100.0% | 61243.2 | 284.8 | 89.0 wheat, 158.4 carrot, 78.0 melon, 139.6 strawberry, 2.4 tomato, 120.0 milk, 87.0 wool | Regression test: 10W, 0L; average opponent 50770.4; zero leftovers and errors |
| Adaptive Tomato v1 | Endgame liquidation v1 | 5 | 100.0% | 62894.4 | 284.4 | 97.4 wheat, 157.5 carrot, 78.0 melon, 135.8 strawberry, 4.0 tomato, 120.0 milk, 87.0 wool | Regression test: 10W, 0L; average opponent 56823.4; zero leftovers and errors |
| Adaptive Tomato v1 | Four Sheep v1 | 5 | 100.0% | 64747.4 | 285.2 | 74.6 wheat, 156.6 carrot, 78.0 melon, 143.4 strawberry, 3.2 tomato, 120.0 milk, 87.0 wool | Regression test: 10W, 0L; average opponent 62252.8; zero leftovers and errors |
| Adaptive Tomato v1 | Second-quadrant v1 | 5 | 60.0% | 68280.7 | 284.6 | 88.2 wheat, 158.4 carrot, 78.0 melon, 139.6 strawberry, 2.4 tomato, 120.0 milk, 87.0 wool | Regression test: 5W, 3L, 2T; average opponent 67887.3; zero leftovers and errors |
| Adaptive Tomato v1 | One Tomato v1 | 5 | 50.0% | 68016.7 | 284.4 | 88.2 wheat, 157.8 carrot, 78.0 melon, 139.6 strawberry, 2.4 tomato, 120.0 milk, 87.0 wool | Near-self-play control: 1W, 1L, 8T; opponent average also 68016.7; zero leftovers and errors |
| Eleven hands v1 | Hand weed clearing v1 | 5 | 100.0% | 74445.2 | 337.8 | 181.0 wheat, 154.8 carrot, 79.0 melon, 164.2 strawberry, 2.4 tomato, 127.2 milk, 106.0 wool | Development test: 10W, 0L; average opponent 73526.0; average lead 919.2; zero errors |
| Eleven hands v1 | Hand weed clearing v1 | 20 | 95.0% | 77331.0 | 338.9 | 172.3 wheat, 155.2 carrot, 79.5 melon, 166.8 strawberry, 2.8 tomato, 133.9 milk, 98.2 wool | Focused validation: 38W, 2L; average opponent 76531.2; average lead 799.8; only seed 12 lost; 0.1 wheat leftover and zero errors |
| SW Strawberry allocation v1 | Eleven hands v1 | 20 | 67.5% | 78325.3 | — | — | Focused mirror comparison: 16W, 2L, 22T; average opponent 78041.3; average lead 284.0; only seed 11 lost, by 83 |
| SW Strawberry allocation v1 | Low-Strawberry test | 5 | 100.0% | 71861.7 | 338.2 | 132.4 wheat, 154.8 carrot, 78.0 melon, 151.2 strawberry, 1.4 tomato, 127.2 milk, 100.6 wool | Regression test: 10W, 0L; average opponent 49462.0; average lead 22399.7; zero leftovers and errors |
| SW Strawberry allocation v1 | Adaptive livestock v1 | 5 | 100.0% | 70541.4 | 339.6 | 158.8 wheat, 154.2 carrot, 78.0 melon, 171.4 strawberry, 3.0 tomato, 132.6 milk, 100.6 wool | Regression test: 10W, 0L; average opponent 65457.8; average lead 5083.6; zero leftovers and errors |
| SW Strawberry allocation v1 | Strawberry expansion v1 | 5 | 100.0% | 75500.5 | 339.6 | 160.0 wheat, 154.2 carrot, 78.0 melon, 171.4 strawberry, 2.4 tomato, 132.6 milk, 100.6 wool | Regression test: 10W, 0L; average opponent 72374.5; average lead 3126.0; zero leftovers and errors |
| SW Strawberry allocation v1 | Hand weed clearing v1 | 5 | 100.0% | 74615.6 | 338.6 | 170.0 wheat, 154.8 carrot, 79.0 melon, 167.8 strawberry, 2.4 tomato, 127.2 milk, 106.0 wool | Regression test: 10W, 0L; average opponent 73474.4; average lead 1141.2; zero leftovers and errors |
| Adaptive SW livestock v1 | SW livestock v1 | 20 | 75.0% | 81928.0 | 343.3 | 184.5 wheat, 117.2 carrot, 79.2 melon, 178.0 strawberry, 1.4 tomato, 142.1 milk, 113.4 wool | Focused validation: 25W, 5L, 10T; average opponent 80819.1; average lead 1108.9; 1.6 wheat leftover and zero errors |

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

The second-quadrant expansion candidate increases the NE route to 14 entries,
giving 35 crop tiles after excluding the four pastures. It hires four hands
before the NE unlock and six afterward, and raises the Strawberry target from
23 to 33. A final-day priority fix prevents crop liquidation from overriding
pending cow actions; this restored the complete 120-unit Milk schedule.

Against the very similar Four cows v1 strategy, the candidate won 18 of 40
matches for a 45.0% match score, although it averaged 57861.9 coins and led by
605.1. Wins and losses clustered by seed and were nearly independent of player
position, indicating a shared-market mirror-match interaction rather than an
execution-order failure. In the public competition, however, the candidate
raised the observed score from 570 for Four cows v1 to 663, an increase of 93
points (16.3%). The public result therefore supports the expanded candidate as
the stronger agent for the current opponent population while Four cows v1
remains a useful mirror-match stress test.

Delayed Sheep v1 preserves the opening Melon wave and converts the two future
Sheep tiles only after those Melons are harvested. Sheep setup begins on day 11,
with the first Wool production arriving around day 17. This avoids the severe
opening delay observed when two Sheep were purchased on day 0 while still adding
late-game animal income.

The candidate won all 10 matches in its five-seed development test and all 40
matches in its focused 20-seed validation against Second-quadrant expansion v1,
with zero errors. The 20-seed validation averaged 62014.9 coins and led by
2479.8. It sold 36 Wool per match and finished with 8 Wool on average because
the final Wool batch arrives after the last useful selling opportunity. That
leftover is an endgame-efficiency opportunity rather than a failure of the
delayed-Sheep strategy.

The adaptive Strawberry sales candidate detects Strawberry-light opponents by
counting their visible plants. Against opponents with fewer than ten Strawberry
plants, it submits at most one Strawberry sale each morning, caps low-price
sales at eight units, and liquidates the remaining inventory on day 29. It
sells immediately when the opponent has at least ten Strawberry plants or when
the current Strawberry price reaches 250. This prevents a heavy producer from
exploiting the temporarily higher price created by our withheld supply.

Against the target-nine Low-Strawberry test, the five-seed A/B improved from
80.0% to 100.0% and increased the average lead by 697.4. In the focused 20-seed
comparison, the cap-eight policy improved the match score from 82.5% to 87.5%,
raised our average money by 572.5, and increased the average lead by 422.0.
Production and leftovers were identical between the configurations, isolating
the gain to market timing. Across the six-opponent, five-seed development suite,
the candidate won 58 of 60 matches for a 96.7% macro match score with zero
errors; Four cows v1 was the minimum at 80.0%.

The shop-aware seventh hand candidate expands the managed NE route from 14 to
20 entries. After excluding the two NE cow pastures, three hands each receive a
six-tile NE crop zone, while the existing four hands retain their NW roles. The
agent always hires the seventh hand after the NE unlock. Hiring can spill into
the following hour, and three later market-order slots are reserved for animal,
feed, and seed purchases. The maximum submitted order count in the validation
trace was nine, below the environment limit of ten.

The base Strawberry target remains 33 while fewer than two Strawberry-consuming
shop instances are unlocked. At two or more instances of Brunch Spot, Ice Cream
Shop, Smoothie Shop, or Farmers Market, the target increases to 39; repeated shop
types count independently. In the trace, the seventh hand initially planted the
six added NE tiles with Carrots while only one qualifying shop was active. A
Smoothie Shop raised the count to two on day 12, triggering the purchase of six
additional Strawberry seeds and conversion of those tiles after the Carrots
matured.

The candidate won all 10 matches against both development opponents. It then
won all 40 matches in the focused 20-seed validation against Adaptive Strawberry
sales v1, with zero errors, averaging 66365.4 coins and leading by 3142.8. Mean
harvests rose from the predecessor's approximately 225 to 260.3. The remaining
15.3 Wheat, 6.1 Carrots, 5.2 Strawberries, and 8.0 Wool identify final-day
liquidation as the next optimization opportunity.

Endgame liquidation v1 adds explicit final-day liquidation for every hand.
Each hand compares its remaining action budget with its distance to a shed-access
tile plus the number of carried product types. When liquidation becomes urgent,
it stops field work, returns to the shed, places each product, and merges the
corresponding sale into any existing sell order for that product. This includes
the Sheep hand's final Wool harvest. On the final day, the Wheat reserve is also
reduced to the number of animals that still require feeding, accounting for
Wheat already carried by the farmer and hands. Surplus Wheat is sold and no
replacement Wheat is purchased unnecessarily.

The single-seed trace finished with all eight inventories and the shed empty.
Against Adaptive Strawberry sales v1, the five-seed comparison remained 10W-0L
and increased average money from 61377.8 to 64646.0, a gain of 3268.2, while
harvests decreased from 260.6 to 258.6. The focused 20-seed validation remained
40W-0L and increased average money from 66365.4 to 69601.0, a gain of 3235.6.
The average lead more than doubled from 3142.8 to 6364.8. Wheat, Carrot, Melon,
Strawberry, Milk, and Wool all finished with zero leftovers, confirming that
the small two-harvest cost is outweighed by complete monetization of production.

The compact four-Sheep candidate preserves the initial Sheep tiles at `(3, 3)`
and `(3, 4)` and adds Sheep at `(2, 3)` and `(2, 4)` after their opening crops
have cleared. The four pastures form a compact two-by-two block. Hand index zero
services the block; its assigned crop zone loses two positions as the additional
pastures activate, aligning its reduced crop workload with the added livestock
work. A one-action final-day liquidation buffer ensures the hand reaches a
shed-access tile early enough to place and sell its last Wool batch. In the
validation trace, all 16 carried Wool was placed and sold on day 29, hour 22.

Against Endgame liquidation v1, the focused 20-seed validation produced 37 wins
and three losses, a 92.5% match score, zero errors, and an average lead of 4445.8.
The candidate averaged 265.0 harvests and sold 87.0 Wool with no leftovers. It
then won all 30 matches in a three-opponent, five-seed regression suite against
Low-Strawberry test, Adaptive Strawberry sales v1, and Endgame liquidation v1.
Every tracked crop and animal product finished with zero leftovers in all three
matchups.

Full second-quadrant v1 expands the managed northeast route from 20 to all 25
positions and hires an eighth hand after the quadrant unlock. Excluding the two
northeast cow pastures leaves 23 crop tiles, divided among the four northeast
hands in zones of six, six, six, and five. The existing crop targets and market
logic remain unchanged, isolating the value of the additional hand and five
managed tiles.

The focused 20-seed validation against Four Sheep v1 produced 40 wins, zero
losses, and zero errors. Average harvests increased from approximately 265 to
285.2, while the complete 120-Milk and 87-Wool schedules were preserved. The
candidate averaged 72434.9 coins and led by 2545.0. It subsequently won all 40
matches in a four-opponent, five-seed regression suite. Combined, the focused
validation and regression suite finished 80W-0L, with zero final leftovers for
every tracked crop and animal product.

Adaptive Tomato v1 reserves at most one of the 39 premium-crop positions for a
Tomato when at least one Pizza Shop or Farmers Market is unlocked early enough
to complete a production cycle. Strawberry retains priority for the remaining
premium positions. The late-shop control bought no Tomato seeds, while the
one-plant trace bought exactly one seed, completed all four scheduled harvests,
and sold four Tomatoes with no leftovers.

The initial 0/3/6 allocation was too aggressive, producing a 40.0% five-seed
score against Second-quadrant v1. A 20-seed 0/1/2 test also scored 40.0% and
averaged 76.8 fewer coins than the opponent; games producing eight Tomatoes were
the clear weakness. Reducing the policy to 0/1/1 raised the focused 20-seed score
to 55.0% and produced a 65.1 average lead.

The final policy also adapts Tomato sale timing. When the opponent has no active
Tomato plants, the agent holds its small harvest until day 29; otherwise it sells
immediately. Against the Tomato-free Second-quadrant baseline, this retained the
55.0% match score while increasing the average lead from 65.1 to 146.6. Restoring
a second Tomato reduced the score to 50.0%, so the one-plant cap was retained.
Against One Tomato v1, the adaptive seller produced exact average-score parity
and a 50.0% match score, confirming that it switches safely to immediate sales.
The final five-opponent regression suite finished 36W-4L-10T for an 82.0% macro
match score, with zero errors and zero final leftovers for every tracked product.

Adaptive livestock v1 reserves the northeast tiles `(6, 4)` and `(6, 3)` for
two additional animals after the four-Cow, four-Sheep base setup is complete.
When a Yarn Store is visible, the tiles receive Sheep; otherwise, two or more
Milk-demanding shops trigger Cows. Purchases may begin from day 12 through day
15. From day 12 onward, qualifying adaptive tiles are withheld from hand
replanting, preventing freshly planted Strawberries from being immediately dug
up during pasture conversion.

The first scheduling version serviced existing animals before every incomplete
pasture. Although this protected the established herd, it also delayed the four
base Sheep: the frozen baseline placed all four by day 11, hour 15, while the
candidate did not finish until day 12, hour 21. That version scored only 32.5%
in a 20-seed comparison against Adaptive Tomato v1, averaging 71347.5 coins and
trailing by 699.8. Disabling the adaptive animals entirely scored 0.0% in the
five-seed control, showing that the extra livestock was beneficial but was
masking a more fundamental setup-priority regression.

The final scheduler uses hybrid priority: incomplete base-animal setup comes
first, followed by routine feeding, care, harvesting, and product placement;
adaptive-animal setup is handled afterward. The trace again completed all four
base Sheep by day 11, hour 15. On the Yarn-heavy seed 2, the two adaptive Sheep
were bought on day 12, with the first placed on day 12 and the second on day 13;
all final Milk and Wool were sold.

The corrected candidate won all 10 five-seed development matches and all 40
matches in its focused 20-seed validation against Adaptive Tomato v1, with zero
errors. The 20-seed run averaged 73490.6 coins, led by 2066.4, and averaged
277.1 harvests, 136.7 Milk sold, and 96.8 Wool sold. Every tracked crop and
animal product finished with zero leftovers except for an average 1.4 Wheat,
which remains a small feed-reserve liquidation opportunity.

Strawberry expansion v1 uses the additional capacity created by Third quadrant
v1 to raise the normal Strawberry target from 33 to 39 and the high-demand
target from 39 to 45. The shared premium-crop capacity rises from 39 to 45 so
the extra Strawberry allocation does not remove the existing Tomato reservation.
Strawberry planting is allowed through day 18 instead of requiring enough time
for every possible ongoing production cycle; a day-18 planting can still
complete a profitable harvest before the final liquidation.

A focused 20-seed sweep compared Strawberry bonuses of zero, three, six, and
nine against frozen Third quadrant v1. The respective match scores were 82.5%,
92.5%, 95.0%, and 90.0%. Bonus three produced the highest average money at
77198.2, but bonus six was only 234.9 lower, produced the strongest match score,
and led by 1889.0 on average. Bonus nine sold more Strawberries but reduced both
money and match score, demonstrating diminishing returns and greater crop
displacement. The six-plant bonus was therefore selected.

The selected candidate won all 30 matches in the five-seed regression against
Four Sheep v1, Second quadrant v1, and Adaptive Tomato v1. Against Third
quadrant v1 it won eight of ten matches, with both losses coming from the known
seed-2 stress case; across the full 20-seed sweep it won 38 of 40. In the
five-seed regression it averaged approximately 312--313 harvests and 163--165
Strawberries sold, with no Strawberry, Tomato, Milk, or Wool leftovers and only
0.4 Wheat left against Third quadrant v1.

Hand weed clearing v1 fixes a responsibility gap in the farm-hand scheduler.
Hands previously handled empty and planted tiles but silently ignored `WEED`
tiles in their assigned zones. Although the farmer could detect those weeds,
livestock work and the daily position reset made distant hand-owned tiles
impractical for the farmer to recover. In the seed-2 trace, the outer northeast
hand watered `(5, 0)` through `(7, 0)` and then passed beside persistent weeds
at `(8, 0)` and `(9, 0)`.

Each hand now maintains local weed targets and uses the priority harvest, water,
dig, then plant. The farmer excludes currently hand-owned weeds from its own
targets, preventing duplicate travel. In the validation trace, the two outer
northeast tiles became weeds on day 13; hand index seven dug, replanted with
Strawberry, and watered both by hour 21. All five outer tiles were productive
again on day 14.

Against frozen Strawberry expansion v1, the focused 20-seed validation produced
38 wins and two losses, a 95.0% match score, zero errors, and an average lead of
2406.0. The candidate averaged 77097.5 coins and 322.7 harvests, sold 168.4
Strawberries, and finished with zero leftovers for every tracked crop and animal
product. The harvest gain reflects weed recovery across all hand-managed zones,
not only the originally observed northeast corner.

Eleven hands v1 extends the managed southwest route from 12 to 18 crop tiles
and hires an eleventh hand after that quadrant is unlocked. The new hand owns
the six added outer tiles. Hiring completes by hour 2, and the largest observed
market submission contained nine orders, below the limit of ten. The hand
established all six tiles by day 16 and handled routine watering comfortably.
On synchronized Wheat harvest days, the combined water, harvest, replant, and
rewater workload can leave part of the zone unattended, but the additional
production still outweighed this routing inefficiency.

The five-seed development comparison against Hand weed clearing v1 produced ten
wins from ten games and an average lead of 919.2. The focused 20-seed validation
produced 38 wins and two losses, a 95.0% match score, zero errors, and an average
lead of 799.8. Both losses were the two player positions of seed 12 and had the
same 259-point deficit, indicating a seed-specific scenario rather than a
position-order weakness. The candidate averaged 338.9 harvests and finished
with only 0.1 Wheat left over on average.

SW Strawberry allocation v1 adds three plants to both Strawberry targets only
when the southwest quadrant is unlocked, at least three Strawberry-demand shops
are visible, and one of the six outer southwest crop tiles is still empty. The
premium-crop capacity rises by the same amount, preserving the existing Tomato
reservation. Requiring immediately usable capacity prevents a late shop unlock
from buying three Strawberry seeds after those tiles have already been filled
with Wheat.

An unconditional three-plant bonus scored 70.0% against Eleven hands v1 but
lost six of 20 seed scenarios, including deficits of 1369 on seed 2 and 2207 on
seed 18. Adding only the shop guard reduced the score to 60.0% and exposed exact
300-point losses caused by three purchased but unplanted seeds. The final
shop-and-capacity guard produced 16 wins, two losses, and 22 ties in the 40-game
mirror comparison, for a 67.5% match score and an average lead of 284.0. It
activated in nine seed scenarios and won eight; the sole loss was seed 11 by
only 83 points.

The candidate then won all 40 matches in a four-opponent, five-seed regression
suite against Low-Strawberry test, Adaptive livestock v1, Strawberry expansion
v1, and Hand weed clearing v1. It recorded zero errors and zero final leftovers
for every tracked crop and animal product. These results support the guarded
policy as a low-risk use of the eleventh hand's late southwest capacity.

Early Sheep v1 reserves the initial Sheep tiles at `(3, 3)` and `(3, 4)` for
Carrots instead of Melons. Two Carrot cycles fit before conversion: the first is
harvested and replanted on day 3, the second is harvested on day 6, and two
Sheep are purchased and placed on day 7. The Sheep hand feeds and cares for
both animals on their setup day.

The first implementation exposed a setup-scheduler loop. When the agent could
not yet afford the Sheep, the farmer repeatedly travelled between an incomplete
pasture and the shed instead of servicing the existing Cows. Setup now yields
control whenever its required animal is neither carried nor available in the
shed. This preserves routine Cow care while waiting for the purchase to become
affordable. The corrected trace kept both Cows healthy throughout the opening.

A direct 20-seed comparison selected a replant cutoff of day 4 over day 3.
Cutoff 4 won 32 of 40 mirrored matches and averaged 77520.9 coins against
77458.3, a small 62.6 average advantage. In the seed-2 trace, it sold 101
Carrots versus 81, finished 690 coins ahead, and both variants unlocked the
northeast quadrant on day 9. This confirmed that the extra Carrots are
profitable and that land timing depends on the shared market rather than the
cutoff alone.

The selected cutoff then won all 120 matches in a three-opponent, 20-seed
validation suite, with zero errors. Against Hand weed clearing v1, Eleven hands
v1, and SW Strawberry allocation v1, its average leads were respectively
4096.8, 2993.2, and 2767.2. It averaged approximately 328 harvests, 115
Carrots, 171 Strawberries, 131 Milk, and 111 Wool sold. All tracked products
finished with zero leftovers except for an average 2.1 Wheat feed reserve.

Early SW v1 advances the southwest-quadrant purchase window from day 15 to day
11. A seed-2 trace confirmed that the additional early income comfortably
supports the faster expansion: the northeast quadrant was purchased on day 11,
hour 2, the last required base animal was placed on day 11, hour 19, and the
southwest quadrant was purchased immediately afterward at hour 20. The land
purchase reduced available money from 10102 to 8102, leaving substantially more
than the configured 1000 working-capital reserve.

Against frozen Early Sheep v1, the focused 20-seed validation won all 40
mirrored matches with zero errors. The candidate averaged 77362.7 coins against
74431.1, an average lead of 2931.6, and averaged 340.2 harvests. It sold 207.7
Wheat, 108.5 Carrots, 79.2 Melons, 171.2 Strawberries, 2.8 Tomatoes, 129.0 Milk,
and 110.2 Wool. Every tracked product finished with zero leftovers except for
an average 0.6 Wheat.

Melon first v1 gives every Melon sale index-zero priority while preserving the
relative order of all other market actions. The day-11 trace had previously
submitted the six-Carrot sale before the 78-Melon sale, allowing an opponent's
Melons to reach the shared market first. Moving the Melon order to the front
raised the candidate's post-turn seed-2 balance from 16142 to 20216, a gain of
4074 on that sale turn.

The focused 20-seed comparison against frozen Early SW v1 won all 40 mirrored
matches with zero errors. The candidate averaged 86100.2 coins against 77824.8,
an average lead of 8275.4, and averaged 343.8 harvests. It sold 193.4 Wheat,
118.1 Carrots, 79.5 Melons, 176.9 Strawberries, 2.5 Tomatoes, 133.1 Milk, and
111.3 Wool, with only 0.2 Wheat left over on average.

The five-seed regression suite added another 30 wins from 30 matches against
Eleven hands v1, SW Strawberry allocation v1, and Early Sheep v1. Average leads
were respectively 13876.2, 13708.6, and 11201.1, with zero errors. This confirms
that the improvement is not confined to the direct Early SW comparison and
that explicit market priority is a major strategic lever.

Adaptive SW livestock v1 varies the four southwest livestock tiles according
to visible shop demand. At least three Milk-demand shops select four Cows; at
least two Yarn Stores select four Sheep; otherwise the existing two-Cow,
two-Sheep plan remains. The all-Cow condition has precedence when both special
conditions are present. Hand index nine continues to own setup and care for the
compact block.

The first composition lock treated a partially placed mixed plan as all-Cow
because its first placed animal was a Cow. This unintentionally converted the
mixed branches on seeds 6 and 9 and caused large regressions. The corrected
lock retains an all-Cow plan only when the placed animals are Cows and the
three-shop Milk condition is still visible. Sheep-only groups retain the
all-Sheep plan, while other partial or mixed groups retain the two-and-two plan.
Traces confirmed mixed layouts on seeds 6 and 9, four Sheep on seed 2, and four
Cows on seed 13.

The corrected 20-seed comparison against frozen SW livestock v1 produced 25
wins, five losses, and ten ties for a 75.0% match score, with zero errors. The
candidate averaged 81928.0 coins against 80819.1, an average lead of 1108.9,
and averaged 343.3 harvests. It sold 142.1 Milk and 113.4 Wool with no animal-
product leftovers; only 1.6 Wheat remained on average. Seed 20 was the only
consistent two-position loss, trailing by 729 in each position.
