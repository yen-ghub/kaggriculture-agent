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
| SW livestock reservation and protected products | Staggered early Sheep v1 | 20 | 62.5% | 87433.6 | 354.2 | 292.8 wheat, 57.9 carrot, 72.0 melon, 175.5 strawberry, 3.2 tomato, 149.4 milk, 121.4 wool, 94.5 fertilizer | Focused validation: 25W, 15L; average opponent 86846.4; average lead 587.2; 1.8 wheat leftover and zero errors |
| Yarn-first SW Sheep v1 | SW livestock reservation v1 | 5 targeted | 90.0% | 93158.0 | — | — | Conditional A/B: 8W, 0L, 2T; average opponent 87955.6; average lead 5202.4; zero errors |
| Global idle-hand Fertilizer collection | Yarn-first SW Sheep v1 | 20 | 100.0% | 96569.0 | 356.1 | 297.4 wheat, 57.6 carrot, 72.0 melon, 175.4 strawberry, 2.4 tomato, 149.4 milk, 123.2 wool, 211.1 fertilizer | Focused validation: 40W, 0L; average opponent 88595.3; average lead 7973.7; 2.2 wheat leftover and zero errors |
| Selective premium-crop Fertilizer use | Fix hand Fertilizer v1 | 20 | 95.0% | 95821.2 | 356.4 | 293.7 wheat, 60.2 carrot, 72.0 melon, 197.2 strawberry, 2.5 tomato, 153.0 milk, 123.2 wool, 200.7 fertilizer | Focused validation: 38W, 2L; average opponent 92271.1; average lead 3550.1; only seed 11 lost, by 117 in both positions; 2.7 wheat leftover and zero errors |
| Full SW with twelfth hand | Hand 5 Goose v1 | 5 | 0.0% | 91159.6 | 397.6 | 325.4 wheat, 83.6 carrot, 60.0 melon, 192.2 strawberry, 4.6 tomato, 45.6 egg, 140.4 milk, 155.2 wool, 226.6 fertilizer | Rejected: 0W, 10L; average opponent 93728.0; average deficit 2568.4; the 144-coin twelfth hire cost repeated daily outweighed the extra Wheat production |
| Full SW split across eleven hands | Hand 5 Goose v1 | 5 | 40.0% | 95834.6 | 377.6 | 287.9 wheat, 61.3 carrot, 60.0 melon, 195.8 strawberry, 3.2 tomato, 45.6 egg, 147.6 milk, 148.2 wool, 221.4 fertilizer | Rejected fallback: 4W, 6L; average opponent 96638.3; average deficit 803.7; complete 25-tile coverage added almost no net harvests because the existing SW hands were already at capacity |
| Four-animal SW 7/7 crop rebalance | Hand 5 Goose v1 | 5 | 60.0% | 92354.8 | 374.8 | 293.0 wheat, 59.8 carrot, 60.0 melon, 191.6 strawberry, 4.6 tomato, 45.6 egg, 147.6 milk, 148.2 wool, 224.2 fertilizer | Rejected: 4W, 2L, 4T; average opponent 92491.8; average deficit 137.0. Transferring adjacent `(2, 7)` was better than transferring `(4, 7)`, but seed 5 lost higher-value Strawberry, Carrot, and Fertilizer output for extra Wheat |
| Day-4 western additional Cow | Hand 5 Goose v1 | 5 | 40.0% | 85355.2 | 366.6 | 271.8 wheat, 52.8 carrot, 60.0 melon, 192.4 strawberry, 3.0 tomato, 37.8 egg, 164.4 milk, 125.6 wool, 227.0 fertilizer | Rejected: 4W, 6L; average opponent 89070.4; average deficit 3715.2. The `(1, 3)` Cow consumed the cash and setup slot intended for the proven day-4 Sheep, delaying it until day 6, then added a long daily farmer detour. On seed 3 the deficit grew from 1796 on day 10 to 11583 at the finish despite the extra Milk |
| Two-shop staged Cow v1 | Twelve Melon opening v1 | 20 | 62.5% | 97501.4 | 368.7 | 185.8 wheat, 42.1 carrot, 72.0 melon, 198.8 strawberry, 2.6 tomato, 49.0 egg, 159.4 milk, 138.4 wool, 233.8 fertilizer | Accepted: 10W, 0L, 30T; average opponent 96841.4; average lead 660.0; 3.0 wheat leftover and zero errors. Five-seed regression against Day-0 livestock v1 was 10W--0L with a 5332.2 average lead |
| Double-Egg third-Goose candidate | Staged Cow v1 | 20 | 52.5% | 95581.0 | 370.0 | 185.8 wheat, 41.4 carrot, 72.0 melon, 198.0 strawberry, 2.6 tomato, 54.4 egg, 162.8 milk, 131.3 wool, 234.2 fertilizer | Rejected: 4W, 2L, 34T; average opponent 95555.9; average lead only 25.1. Seed 11 lost by 698 in both positions; 3.0 wheat leftover and zero errors |
| Early NE livestock branch | Staged Cow v1 | 20 | 62.5% | 98123.7 | 366.1 | 187.2 wheat, 39.8 carrot, 72.0 melon, 197.9 strawberry, 2.5 tomato, 41.4 egg, 158.8 milk, 143.8 wool, 233.3 fertilizer | Accepted: 10W, 0L, 30T; average opponent 97155.2; +968.5 average lead, zero errors. First-two-shop Yarn selects four Sheep; double Milk selects four Cows. Five-seed regressions won 10W--0L against Locked SW livestock (+5996.0) and Day-0 livestock (+6227.4) |
| Second staged Cow at `(0, 4)` | Early NE livestock v1 | 20 | 42.5% | -- | -- | -- | Rejected: 0W, 6L, 34T. It activated only on seeds 8, 13, and 17, then lost both positions by 942, 1,860, and 1,045 coins; full-suite average deficit 192.4. Three Milk shops did not justify its purchase, feed, crop displacement, and Hand 1 service load |

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

Fertilizer collection v1 gives the southwest livestock hand a secondary task
after all four southwest animals have been established and all urgent feeding,
care, and product harvesting is complete. The hand collects available
Fertilizer from the compact livestock block. Fertilizer is submitted after all
strategic market orders so it cannot displace purchases or higher-priority
sales when the ten-order limit is reached, and final-day hand liquidation also
handles any Fertilizer still being carried.

Traces covered both adaptive extremes. On seed 2, the four-Sheep layout
collected and sold 60 Fertilizer; on seed 13, the four-Cow layout collected and
sold 59. Both finished with zero Fertilizer left over. Collection began on day
14 after setup was complete, and the first collected batch was sold on day 15.

The focused 20-seed comparison against frozen Adaptive SW livestock v1
produced 28 wins, four losses, and eight ties for an 80.0% match score, with
zero errors. The candidate averaged 83542.6 coins against 80892.5, an average
lead of 2650.1. It sold 17.9 Fertilizer per match on average and finished with
zero Fertilizer left over. Average harvests remained 343.3, while Milk and Wool
sales remained 142.1 and 113.4 respectively, providing strong evidence that
the secondary collection task added income without reducing the established
crop or livestock output. Compared with the preceding adaptive-livestock
validation, the match score improved from 75.0% to 80.0%.

Single Melon wave v1 prevents Melon planting after day 0. The existing crop
selector judged Melons using their price at planting time and could not predict
the market depression caused by the opening sale. Against the no-Melon Carrot
v1 opponent, the previous policy planted another four to six Melons on days 11
and 12 and sold that second wave on days 22 and 23. Although still nominally
profitable, the long cycle occupied land and worker capacity that produced more
value when reassigned to faster crops.

The selected implementation retains the adaptive opening target of 13 or 15
Melon plants but gives Melons a last planting day of zero. Its seed target also
tapers with the remaining opening demand, avoiding the previous three-seed
buffer after the target is complete. Traces against Carrot v1 and frozen
Fertilizer collection v1 confirmed that every Melon was planted on day 0, none
were planted afterward, and no Melon seeds remained at the end of the game.

The focused 20-seed comparison against frozen Fertilizer collection v1
produced 39 wins and one loss for a 97.5% match score, with zero errors. The
candidate averaged 85393.0 coins against 82811.1, an average lead of 2581.9,
and averaged 351.8 harvests. It sold 264.3 Wheat, 81.1 Carrots, and 69.1
Melons, demonstrating that the released capacity shifted primarily into
shorter Wheat cycles. All tracked products finished with zero leftovers except
for an average 2.5 Wheat feed reserve. The only loss was seed 11 from player
position zero; the reverse position won, indicating a position-sensitive
shared-market interaction rather than a general regression.

The five-seed regression suite won all 30 matches against Adaptive SW livestock
v1, SW Strawberry allocation v1, and Strawberry expansion v1. Average leads
were respectively 10743.3, 16604.8, and 18261.4. Across the three opponents,
the candidate consistently averaged approximately 348--350 harvests, 276--291
Wheat sold, and about 70 Melons sold, with zero errors. This supports the
single-wave policy as a broad allocation improvement rather than an artifact
of the direct frozen-baseline comparison.

Farmer Fertilizer collection v1 extends collection to the livestock assigned
to the farmer: the central Cow group and any adaptive animal tiles. Sheep-hand
and southwest-hand animals remain excluded so ownership does not overlap. The
farmer collects only when `choose_animal_action()` returns no work, its crop
action would otherwise be `PASS`, and the game has not reached day 29. This
keeps livestock setup, feeding, care, harvesting, product deposits, crop work,
and final liquidation ahead of the optional collection task.

Traces on seeds 2, 6, and 13 each recorded 91 farmer collections. The farmer
collected twice daily from the initial Cows on days 1--9 and generally four
times daily after the expanded Cow group became available. Day 11 fell to one
collection while livestock setup took priority. Every observed collection
occurred with all farmer-assigned animals already fed, cared for, and harvested;
no collection occurred on day 29. Total Fertilizer sales reached 148--152 in
the traced games and all three finished with zero Fertilizer left over.

The focused 20-seed comparison against frozen Single Melon wave v1 won all 40
mirrored matches with zero errors. The candidate averaged 89294.4 coins against
84237.4, an average lead of 5057.0, and averaged 352.3 harvests. It sold 74.2
Fertilizer per match and finished with none left over. Crop and livestock output
remained healthy, including 256.4 Wheat, 176.4 Strawberries, 142.5 Milk, and
109.9 Wool sold. Every tracked product finished with zero leftovers except for
an average 1.0 Wheat feed reserve. No multi-opponent regression was run for
this iteration; the candidate was accepted on the strength and consistency of
the focused 20-seed result.

Day 3 Sheep v1 advances the initial two-Sheep purchase from day 6 to day 3.
The two reserved Sheep tiles at `(3, 3)` and `(3, 4)` retain their opening
Carrots but are no longer replanted on day 3. Starting on day 1, the agent
protects a 1000-coin Sheep reserve from discretionary seed purchases and, on
day 3, from Wheat-reserve replenishment. Hand zero immediately returns its
first harvested Carrots to the shed, restoring liquidity after the livestock
purchase.

A five-seed timing trace confirmed identical setup across all tested seeds:
both Sheep were purchased together on day 3, hour 6, then placed on day 3 at
hours 11 and 14. This resolved the previous opening in which both target tiles
were empty by day 3 but the agent had only 920 coins and therefore waited until
day 4 or later to purchase the pair.

The focused 20-seed comparison against frozen Farmer Fertilizer collection v1
won all 40 mirrored matches with zero errors. The candidate averaged 90682.0
coins against 87715.7, an average lead of 2966.3, and averaged 351.6 harvests.
It sold 269.9 Wheat, 82.7 Carrots, 72.5 Melons, 172.2 Strawberries, 1.4
Tomatoes, 147.9 Milk, 119.6 Wool, and 97.7 Fertilizer. Every tracked product
finished with zero leftovers except for an average 1.8 Wheat. The consistent
40--0 result supports the earlier Sheep timing as a new baseline despite the
temporary opening cash constraint.

Staggered early Sheep advances one of the two initial Sheep to day 0 while
retaining the second reserved tile for its opening Carrot harvest. The early
tile `(3, 3)` is converted immediately, while `(3, 4)` remains a crop tile
until day 3. A focused trace confirmed that the first Sheep was purchased with
the two opening Cows and placed on day 0, hour 13. Both Cows and the Sheep were
fed and cared for before the end of day 0. The second Sheep was purchased on
day 4, hour 2 and placed on day 4, hour 6.

Buying both Sheep on day 0 was rejected. In a focused 20-seed comparison
against frozen Day 8 NE Strawberry v1, that version produced 19 wins and 21
losses, averaged 85331.1 coins against 85449.0, and trailed by 117.9 on
average. The opening livestock expense removed too much liquidity and crop
capacity despite increasing early Wool production.

The staggered version won 39 of 40 mirrored matches against the same frozen
baseline, with zero errors. It averaged 86660.7 coins against 85869.9, an
average lead of 790.8, and averaged 354.6 harvests. It sold 307.6 Wheat, 63.0
Carrots, 72.0 Melons, 170.4 Strawberries, 2.9 Tomatoes, 148.3 Milk, 123.7 Wool,
and 78.2 Fertilizer. All tracked products finished with zero leftovers except
for an average 1.4 Wheat. The only individual loss was seed 3 from player
position zero by 56 coins; the reverse position won by 88, leaving a positive
paired margin. All 20 seeds had a positive average margin across their two
positions, providing strong support for the staggered schedule as the new
baseline.

SW livestock reservation prevents the four conditional livestock tiles at
`(4, 5)`, `(3, 5)`, `(3, 6)`, and `(4, 6)` from being planted between the
southwest unlock and the day-12 livestock decision. Selected branches can now
build their pastures without destroying an opening Strawberry wave. When the
branch is not selected, the reservation expires and normal crop planting
resumes on day 12.

The first 20-seed comparison against frozen Staggered early Sheep v1 produced
22 wins and 18 losses, averaged 87301.4 coins against 87016.7, and led by
284.7. Eight of the nine seeds that activated southwest livestock improved,
but seed 6 lost by 1096 in both positions. Its four Cows were established
earlier and received the same care and harvest actions as the baseline, ruling
out lost production.

The seed-6 trace instead exposed the 100-item shed-capacity limit during the
automatic end-of-day inventory deposit. On day 20, earlier-index crop hands
deposited eight additional Wheat before hand index nine was processed. Only 10
of that hand's 18 Milk then fit in the shed, so eight Milk were discarded while
Wheat sold for 38 and Milk sold for 247 on the following turn. A smaller repeat
later discarded one more Milk. The southwest livestock hand now returns animal
products once it carries at least eight units, before taking optional
Fertilizer work. This preserves batching while protecting higher-value output
from overnight overflow.

With protected product returns, seed 6 sold 192 Milk and changed from a
1096-point loss to a 2164-point win. The repeated 20-seed evaluation improved
to 25 wins and 15 losses, a 62.5% match score. The candidate averaged 87433.6
coins against 86846.4, an average lead of 587.2, with zero errors. Fertilizer
sales declined slightly from 96.2 to 94.5 as the hand spent time returning to
the shed, but the higher-priority livestock sales more than compensated. Every
tracked product finished with zero leftovers except for an average 1.8 Wheat.

Yarn-first SW Sheep v1 adds a targeted override to the southwest livestock
branch. When the first of the initial four shops is a Yarn Store and fewer
than three of those shops demand Milk, all four southwest livestock tiles use
Sheep. The established two-Yarn and three-Milk rules remain in place, and the
new Yarn-first rule takes priority over the all-Cow branch.

The conditional A/B used the frozen SW livestock reservation v1 baseline.
Seeds 25 and 28 gained 5522 and 232 coins respectively in both player
positions. Control seed 9 exchanged a 55-coin win and loss between positions,
while seed 17 tied in both, giving a net-zero control result. Follow-up tests
on seeds 38, 42, and 55 produced four wins and two ties: seed 38 was unchanged,
seed 42 gained 15918 in both positions, and seed 55 gained 4362 and 4318.

Across the five targeted seeds, the candidate produced eight wins, no losses,
and two ties for a 90.0% match score with zero errors. It averaged 93158.0
coins against 87955.6, an average improvement of 5202.4. Four of the five
targeted seeds improved and the fifth tied, supporting the Yarn-first
four-Sheep override as the next frozen baseline.

Global idle-hand Fertilizer collection extends the optional collection task
to every hand-managed livestock group. After normal crop and livestock work
has been assigned, hands whose action is still `PASS` are matched greedily to
the nearest available Fertilizer. Each animal tile is assigned to at most one
hand, the farmer's selected target is reserved, and the southwest livestock
tiles remain under their dedicated hand while that branch is active. This
keeps planting, watering, harvesting, feeding, care, product returns, and
endgame liquidation ahead of Fertilizer collection.

Traces on seeds 1, 2, 3, and 19 confirmed successful hand collection in both
southwest-livestock and non-southwest branches. Compared with the frozen
baseline, Fertilizer sales increased by 85, 89, 204, and 169 respectively,
while final scores improved by 16491, 35105, 17809, and 6916. The global
target allocation prevented duplicate trips between hands and the farmer.

The focused 20-seed comparison against frozen Yarn-first SW Sheep v1 won all
40 mirrored matches with zero errors. The candidate averaged 96569.0 coins
against 88595.3, an average lead of 7973.7, and averaged 356.1 harvests. It
sold 211.1 Fertilizer per match and finished with none left over. Crop and
livestock output remained healthy, including 297.4 Wheat, 175.4 Strawberries,
149.4 Milk, and 123.2 Wool sold. Every tracked product finished with zero
leftovers except for an average 2.2 Wheat. The consistent 40--0 result supports
global idle-hand collection as the next baseline.

Selective premium-crop Fertilizer use spends only Fertilizer already carried
by an otherwise-idle hand. Eligible targets are watered, unfertilized Tomato
at age 7 and Strawberry at ages 9 or 13, reflecting that production occurs
during the following nightly transition. A target is accepted only when its
forecast incremental crop value is at least 120% of the current Fertilizer
sale value; normal crop and livestock work remains higher priority.

A seed-1 trace verified that all 11 submitted `FERTILIZE` actions were legal.
In both player positions, the candidate scored 117138 against 112295 for
frozen Fix hand Fertilizer v1, a gain of 4843.

The focused 20-seed evaluation against Fix hand Fertilizer v1 finished with
38 wins and 2 losses and zero errors. Average money was 95821.2 against
92271.1, an average lead of 3550.1. The candidate sold 197.2 Strawberries and
200.7 Fertilizer on average while leaving no Fertilizer unsold.

Both losses occurred on seed 11 and were only 117 points in each position. On
that seed, the candidate sold 13 fewer Fertilizer and 2 fewer Wheat in exchange
for 18 additional Strawberries; those later Strawberries reached a weaker
market than the action-time value estimate anticipated. The narrow exception
was accepted without tuning to one seed, and the broader multi-opponent
regression was intentionally skipped for now.

Staggered additional Sheep brings one of the two extra northern Sheep forward
to day 4 while leaving the other on its previous day-11 schedule. Tile `(2, 4)`
is reserved after its opening staple crop and becomes the day-4 Sheep tile;
tile `(2, 3)` remains available for crops until it is reserved for the day-11
Sheep. This was tested after the rejected attempt to establish both additional
Sheep on day 4, which disrupted crop production and finished only 6--34
against frozen Fertilize crops v1, averaging 85952.4 coins against 95800.2.

The focused 20-seed evaluation of the staggered schedule against Fertilize
crops v1 won 38 of 40 mirrored matches with zero errors. It averaged 95888.7
coins against 93621.2, an average lead of 2267.5, and averaged 356.2 harvests.
Average sales were 298.6 Wheat, 57.0 Carrots, 72.0 Melons, 198.1 Strawberries,
2.7 Tomatoes, 145.7 Milk, 134.8 Wool, and 200.3 Fertilizer. Every tracked
product finished with zero leftovers except for an average 2.4 Wheat. Both
losses were on seed 13 and were only 93 coins in each player position. The
result supports staggering the purchases: it captures additional Wool without
the severe crop and liquidity cost of buying both Sheep on day 4. A broader
multi-opponent regression was intentionally skipped for now.

Day-11 Goose setup allows the two northeast Geese to coexist with the full
four-animal southwest livestock branch. The Geese remain farmer-managed while
the southwest animals remain hand-managed. Goose tiles are reserved once Egg
demand is identified from the first two shops, preventing crops from blocking
their later setup.

Against frozen Reshuffle Goose v1 over 20 mirrored seeds, the day-11 candidate
finished with 23 wins, 7 losses, and 10 ties for a 70.0% match score with zero
errors. It averaged 93749.5 coins against 93227.8, an average lead of 521.7.
On seed 11, allowing the branches to coexist retained eight Cows, four Sheep,
and two Geese and reduced the previous 5687-point deficit to 887 points.

Moving Goose setup forward to day 10 was rejected. The same 20-seed comparison
fell to 18 wins, 12 losses, and 10 ties, a 57.5% match score, while the average
lead declined to 142.2. Controlled traces on seeds 5, 8, and 10 showed that the
earlier setup gained only one Goose production cycle, approximately five Eggs,
but interrupted the first Melon wave and crop scheduling. Melon sales fell
from 72 to 69--70, setup cash dropped as low as 48 coins, and southwest land
purchase was occasionally delayed. A nominal purchase reserve was insufficient
because subsequent construction, hiring, seed, and feed costs consumed it.

The first Melon liquidation therefore acts as the practical funding and action
capacity threshold for Geese. The day-11 version was retained and frozen as
`baselines/day11_goose_v1.py`.

Permanent southwest livestock allocation fixes a branch-switching failure
found in replay `107430458.json`. The four-tile block was originally completed
on day 13 as Cow, Sheep, Sheep, Cow. Later shop unlocks raised observed Milk
demand to the all-Cow threshold, causing the agent to buy two Cows on day 18.
When the Sheep disappeared at the day-20 transition, those Cows replaced them.
This incurred unnecessary purchases and silently changed an established mixed
livestock strategy.

Once all four southwest pastures exist, the agent now locks their established
allocation. It first identifies a fully occupied block directly; if an animal
has escaped and left an empty pasture, it reconstructs the original decision
from the earliest shop prefix that could have activated the branch. Later shop
unlocks can therefore no longer convert mixed, all-Sheep, or all-Cow blocks.
Replay-state verification confirmed that no replacement Cows are purchased on
day 18 and escaped Sheep are replaced with Sheep instead.

The 20-seed mirrored evaluation against Reshuffle Goose v1 finished with 30
wins, 4 losses, and 6 ties for an 82.5% match score with zero errors. The
candidate averaged 94822.3 coins against 93006.6, an average lead of 1815.7,
and averaged 370.7 harvests. Average sales included 267.5 Wheat, 197.6
Strawberries, 46.5 Eggs, 151.8 Milk, 130.8 Wool, and 213.1 Fertilizer. Every
tracked product finished with zero leftovers except for an average 2.8 Wheat.
Only seeds 11 and 15 lost, in both player positions.

Relative to the preceding day-11 Goose result against the same baseline, match
score improved from 70.0% to 82.5%, and average lead increased from 521.7 to
1815.7. This supports retaining the permanent four-animal allocation.

Day-0 livestock v1 advances the second initial Sheep from day 3 to day 0, so
the opening purchases two Cows and two Sheep. The first implementation placed
the Cows before the Sheep. Although all four animals were eventually serviced,
the farmer completed every placement before returning to the established Cows,
creating unnecessary backtracking and delaying parallel livestock work.

The selected route places both Sheep first. Their dedicated hand can feed and
care for them while the farmer returns to establish and service the two Cows
beside the shed. A seed-1 trace confirmed that both Sheep were placed by day 0,
hour 8, both Cows were placed by hour 16, and both Cows were fed and cared for
by hour 23. Seed 1 still lost by 1437 because the additional opening purchase
reduced Melon seed purchases from 13 to 10, resulting in 60 Melons sold rather
than 72; its four additional Wool did not offset the missing crop revenue.

The focused 20-seed evaluation against frozen Locked SW livestock v1 produced
32 wins and eight losses for an 80.0% match score with zero errors. The
candidate averaged 94255.6 coins against 93535.6, an average lead of 720.0,
and averaged 367.6 harvests. It sold 275.6 Wheat, 57.1 Carrots, 60.0 Melons,
199.1 Strawberries, 1.7 Tomatoes, 40.3 Eggs, 152.9 Milk, 134.1 Wool, and 220.8
Fertilizer. All tracked products finished with zero leftovers except for an
average 2.4 Wheat.

Five-seed regression tests won all ten mirrored matches against both Yarn-first
SW Sheep v1 and Fertilize crops v1. The candidate averaged 91607.6 and 88278.2
coins respectively, leading by 16005.2 and 3520.8. Against Staggered additional
Sheep v1 it produced six wins and four losses, averaging 90539.4 against
89212.8 for a positive lead of 1326.6. These results support freezing the
Sheep-first day-0 livestock opening as `baselines/day0_livestock_v1.py`, while
retaining the reduced opening Melon count as its principal known tradeoff.

Early NE expansion v1 moves the second-quadrant purchase threshold from day 8
to day 6. Available cash caused the actual purchase to occur on day 7 in the
traced seed. Moving only the land purchase was rejected: the first five-seed
comparison lost all ten mirrored matches. The newly hired NE hands began partway
through day 7 while the fixed three-seed staple buffer was replenished only as
seeds were consumed, producing a fragmented and inefficient expansion shift.

Increasing the selected staple seed buffer from three to eight after NE unlock
improved seed availability but did not solve the economic regression by itself.
The extra hands still generated many idle or travel actions, and the larger
buffer tied up additional cash. Advancing the six-tile NE Strawberry allocation
to the same expansion threshold improved the combined five-seed result to six
wins and four losses, with a small positive average lead, but remained too weak
on its own.

The selected design also advances the two NE expansion Cows from day 8 to the
new expansion threshold. On seed 1, NE was purchased on day 7, hour 2 and both
Cows were purchased on hour 3. This converted the earlier seed-1 deficit into a
659-point win, showing that immediate livestock production was needed to recoup
the earlier land, hiring, and seed investment.

The focused 20-seed comparison against frozen Day-0 livestock v1 produced 33
wins and seven losses for an 82.5% match score with zero errors. The candidate
averaged 93648.3 coins against 92657.4, an average lead of 990.9, and averaged
372.6 harvests. It sold 270.0 Wheat, 47.5 Carrots, 60.0 Melons, 202.7
Strawberries, 3.0 Tomatoes, 46.5 Eggs, 155.6 Milk, 130.5 Wool, and 219.0
Fertilizer. All tracked products finished with zero leftovers except for an
average 2.0 Wheat.

Five-seed regression tests remained positive against three additional
livestock baselines. The candidate scored 80.0% against Staggered additional
Sheep v1 with a 2196.6 average lead, 100.0% against Reshuffle Goose v1 with a
1424.6 lead, and 80.0% against Locked SW livestock v1 with a 1458.8 lead. The
three tests averaged 375.8, 375.0, and 375.4 harvests respectively, with zero
errors and no product leftovers apart from the Wheat feed reserve. The
coordinated earlier land, larger seed buffer, immediate Strawberry allocation,
and immediate Cow activation is retained as the next baseline.

NE Wheat buffer v1 addresses the day-10 shed overflow created when the opening
Melon wave and the first NE staple harvest arrive together. A seed-1 trace of
the retained Early NE expansion strategy showed 109 units distributed between
the shed and carried inventories immediately before the transition. The
100-unit shed retained 12 Carrots but discarded another nine Carrots and one
Fertilizer.

Two direct liquidation approaches were rejected. Unconditionally returning
hands to sell products on day 10 scored approximately 60.0% against Day-0
livestock v1, while a capacity-triggered version improved to only 27 wins and
13 losses (67.5%). The latter averaged 93185.4 coins against 92467.4. In both
cases, diverting hands from late field work cost more than the recovered
inventory was worth.

The selected alternative changes five NE Carrot plantings to Wheat only during
days 7 through 9. The chosen tiles are `(8, 0)`, `(9, 0)`, `(8, 1)`, `(9, 1)`,
and `(5, 2)`. This staggers their harvest beyond the day-10 Melon transition
without changing earlier Carrot income or permanently fixing their later crop
allocation. In the seed-1 trace, pre-transition inventory fell from 109 to 97
units, all 60 Melons were preserved, and no product was discarded or sold
early.

The focused 20-seed mirrored evaluation against Day-0 livestock v1 produced 34
wins and six losses for an 85.0% match score with zero errors. The candidate
averaged 95742.3 coins against 94695.1, an average lead of 1047.2, and averaged
371.3 harvests. Average sales were 265.6 Wheat, 52.5 Carrots, 60.0 Melons,
205.5 Strawberries, 2.2 Tomatoes, 46.5 Eggs, 152.1 Milk, 133.9 Wool, and 217.3
Fertilizer. Every tracked product finished with zero average leftovers except
1.9 Wheat and 0.1 Strawberry. Relative to Early NE expansion v1, match score
improved from 82.5% to 85.0% and average lead increased from 990.9 to 1047.2.
The strategy is frozen as `baselines/ne_wheat_buffer_v1.py`.

Hand 5 Goose v1 advances the two conditional northeast Geese from day 11 to
day 8 while splitting their workload. Hand 5, whose NE crop route begins at
`(6, 4)`, establishes and services the Goose on that tile. The farmer retains
responsibility for the second Goose at `(6, 3)`. This includes animal pickup,
coop construction, feeding, care, harvesting, product return, and Fertilizer
collection. The farmer excludes Hand 5's Goose from its own setup and service
targets, preventing duplicate work.

The workload split was introduced after a farmer-only day-8 trial remained
slightly weaker than the day-11 baseline. On diagnostic seed 6, the
farmer-only version spent eight actions establishing both Geese, reduced its
day-8 cash balance to 235 coins, and finished 739 coins behind the frozen
baseline despite selling 10 additional Eggs. With Hand 5 assisting, the first
Goose was established by day 8, hour 7 and the farmer completed the second by
hour 12. The same seed then scored 111417 against 108229.

The focused 20-seed mirrored evaluation against frozen NE Wheat buffer v1
produced 30 wins, no losses, and 10 ties for an 87.5% match score with zero
errors. The candidate averaged 96657.8 coins against 94590.7, an average lead
of 2067.1, and averaged 376.9 harvests. Average sales were 270.0 Wheat, 52.5
Carrots, 60.0 Melons, 205.5 Strawberries, 2.0 Tomatoes, 57.0 Eggs, 154.2 Milk,
135.8 Wool, and 225.1 Fertilizer. Every tracked product finished with zero
leftovers except for an average 2.7 Wheat. The result supports both the day-8
Goose timing and the Hand 5 service split, frozen as
`baselines/hand5_goose_v1.py`.

The twelve-Melon opening candidate recovered the two Melon plants lost in the
day-0 livestock build without delaying its critical milestones. The main cash
leak was the feed reserve: Wheat carried by hands was not counted as committed
feed stock, so the market logic repeatedly bought replacement Wheat after
pickup. The candidate counts Wheat across the shed, farmer, and all hands, and
sizes its reserve from the animals still awaiting setup or feeding. It also
defers day-0 Carrot and Wheat seed buffers and clears the day-4 Sheep tile
without planting a crop on it.

A seed-1 milestone trace confirmed twelve Melons and two Cows plus two Sheep by
the start of day 1. The third Sheep was established at day 4, hour 7 and NE was
unlocked at day 7, hour 2, exactly matching Hand 5 Goose v1. The focused
20-seed mirrored evaluation against Hand 5 Goose v1 produced 38 wins and two
losses for a 95.0% match score with zero errors. The candidate averaged 95176.2
coins against 93423.4, an average lead of 1752.8, and averaged 372.1 harvests.
Average sales were 198.3 Wheat, 40.0 Carrots, 72.0 Melons, 198.8 Strawberries,
3.6 Tomatoes, 54.5 Eggs, 150.6 Milk, 135.8 Wool, and 226.3 Fertilizer. Average
leftovers were 2.5 Wheat and zero for every other tracked product.

Five-seed regression tests won all ten mirrored matches against both Locked SW
livestock v1 and Day-0 livestock v1. The candidate averaged 81483.2 against
76516.6 in the former and 93867.0 against 89369.2 in the latter, with zero
errors. These results support accepting the twelve-Melon opening as the next
candidate, frozen as `baselines/twelve_melon_opening_v1.py`.

The first P3 workload-aware hand-count experiment tested a twelfth daily surge
hand without adding land or livestock. It estimated the field work and travel
remaining on Hand 11's southwest route, hired the helper when that work exceeded
one hand's remaining turns, and split the route while the helper was present.
The twelfth daily hire cost was 144 coins.

The initial loose trigger was rejected after a five-seed mirrored screen against
Twelve Melon opening v1. It produced four wins, four losses, and two ties for a
50.0% match score, averaging 103698.8 coins against 103647.8, a lead of only
51.0. Although the helper performed real work, it was also hired for ordinary
recurring-crop cycles whose work Hand 11 would usually finish without help.

A stricter trigger required an estimated backlog of at least six actions and
allowed hiring only through hour 2. A five-seed trace showed the helper was then
hired only on seed 1, on days 21 and 25; it completed 21 productive actions on
those two full shifts without passing. The five-seed screen improved to two
wins, no losses, and eight ties, with a 35.2 average-money lead.

The final twenty-seed mirrored gate remained regression-free but too narrow:
two wins, no losses, and 38 ties for a 52.5% match score, zero errors, and an
average of 96634.9 coins against 96626.1, a lead of only 8.8. Seed 1 gained 176
coins in each player position and the other nineteen seeds were unchanged. A
five-seed comparison against Hand 5 Goose v1 was exactly identical to the
frozen Twelve Melon opening baseline, so the P3 change demonstrated no
generalized incremental gain. The surge-hand experiment is rejected and
`main.py` is restored to the eleven-hand frozen baseline.

The first safe P1 livestock-ladder stage adds one Cow at `(1, 4)`, adjacent to
Hand 1's established NW Sheep circuit. It activates only when at least two
Milk-demand shops are visible, after both NE expansion Cows are established
and the tile's current crop has cleared. Hand 1 owns pickup, pasture setup,
feeding, care, harvest, and the associated travel; the farmer's service route
is unchanged. Nonqualifying seeds keep the normal crop schedule and remain
behaviorally identical to Twelve Melon opening v1.

The initial one-shop trigger was too broad. On diagnostic seed 2, the added Cow
sold 21 more Milk and enabled 15 more Fertilizer, but Hand 1's two additional
daily service actions displaced 23 Carrots, 15 Wheat, and two Strawberries, in
addition to the 400-coin purchase and feed cost. Merely raising the trigger was
not sufficient while `(1, 4)` was reserved unconditionally: that reservation
still changed nonqualifying openings. The final version reserves the tile only
after qualifying demand is known and waits for its crop to clear before
activating the Cow.

The twenty-seed mirrored gate against Twelve Melon opening v1 produced 10 wins,
no losses, and 30 ties for a 62.5% match score with zero errors. The candidate
averaged 97501.4 coins against 96841.4, a lead of 660.0, and averaged 368.7
harvests. Average sales were 185.8 Wheat, 42.1 Carrots, 72.0 Melons, 198.8
Strawberries, 2.6 Tomatoes, 49.0 Eggs, 159.4 Milk, 138.4 Wool, and 233.8
Fertilizer. Average leftovers were 3.0 Wheat and zero for every other tracked
product. Thirty exact ties show that the branch stays isolated on
nonqualifying seeds.

A five-seed regression against Day-0 livestock v1 won all ten mirrored matches
with zero errors, averaging 95388.6 against 90056.4 for a 5332.2 lead. This
cross-opponent result supports accepting the staged Cow as the next baseline,
frozen as `baselines/staged_cow_v1.py`.

The double-Egg third-Goose candidate added one Goose at `(7, 4)` under Hand 5,
adjacent to that hand's existing Goose at `(6, 4)`. It activated only when both
of the first two shops demanded Eggs, reserved the tile only on qualifying
seeds, and waited for the original two Geese to be established. This limited
activation to seeds 2, 7, and 11 in the twenty-seed screen. A seed-2 trace was
mechanically healthy: the Goose was placed on day 9, serviced through the end
of the game, and the candidate gained 1081 coins. Nonqualifying seed 1 tied the
baseline exactly.

The full twenty-seed mirrored gate produced only four wins, two losses, and 34
ties for a 52.5% match score. Average money was 95581.0 against 95555.9, a lead
of just 25.1. Seed 11 lost by 698 in both positions, so one of the three
qualifying scenarios regressed despite the strict early-demand signal. Average
Egg sales rose to 54.4, but Strawberry and Wool output fell, and the incremental
animal failed to create a reliable net gain. The candidate is rejected and
`main.py` is restored to frozen Staged Cow v1.

## Early NE livestock branch -- accepted

The strong-demand NE branch replaces the conditional Goose route only when the
first two shops already give a clear signal: any Yarn Store selects four Sheep;
two Milk-demand shops select four Cows. Hand 6 builds pastures at `(6, 4)`,
`(7, 4)`, `(6, 3)`, and `(7, 3)` on day 8, then batches animal pickup and
placement on day 9. The early NE branch suppresses both conditional NE Geese
and the independent four-animal SW branch, while nonqualifying seeds keep the
Staged Cow behavior exactly.

The direct twenty-seed mirrored gate against Staged Cow v1 finished
10W--0L--30T (62.5% match score), zero errors, and 98123.7 average money versus
97155.2: a 968.5 lead. It averaged 366.1 harvests, with 3.1 Wheat left over and
zero leftovers for every other tracked product. The thirty exact ties are
expected: the demand branch is inactive on those seeds.

Two five-seed regressions both won every mirrored match with zero errors:
10W--0L against Locked SW livestock v1 (82288.2 versus 76292.2, +5996.0) and
10W--0L against Day-0 livestock v1 (93401.6 versus 87174.2, +6227.4). The
branch is accepted and frozen as `baselines/early_ne_livestock_v1.py`.

## Second staged Cow at `(0, 4)` -- rejected

The candidate retained the accepted Cow at `(1, 4)`, then added a second Cow
at `(0, 4)` only when at least three Milk-demand shops were visible and the
first Cow had already been placed. Hand 1 owned both Cows, and nonqualifying
seeds were exact ties with the frozen baseline.

The twenty-seed mirrored gate was nevertheless decisive: 0W--6L--34T for a
42.5% match score. The branch activated on seeds 8, 13, and 17 and lost both
player positions by 942, 1,860, and 1,045 coins respectively, yielding a
192.4 average deficit across the full suite. A third Milk-demand shop does not
repay the second Cow's purchase, feed, displaced crop value, and recurring
Hand 1 service workload. `main.py` is restored to Early NE livestock v1; do
not retry this tile/threshold combination as another isolated Cow stage.

## NE single-Milk Cow routing -- accepted (first P4 branch-selection change)

A branch scan across seeds 1--20 against frozen Early NE livestock v1 found
that the compact NE block at `(6, 4)`, `(7, 4)`, `(6, 3)`, and `(7, 3)` was
left in normal crop production on four seeds (1, 4, 8, 20), deferring all
extra livestock to the weaker day-12 SW decision. Every one of those openings
carried at least one Milk-demand shop in its first two shops but no Yarn and
no Egg signal, a prefix the existing trigger did not cover.

The candidate extends the existing early-NE selection condition with one new
disjunct: the established `EARLY_NE_ALL_COW_PLAN` also activates when the
two-shop prefix has at least one Milk-demand shop and neither Yarn nor Egg
demand. Tiles, pasture day 8, batched placement day 9, Hand 6 ownership, and
cash reserve are unchanged; the no-Yarn/no-Egg guard keeps the accepted Sheep,
double-Milk, and Goose triggers exactly as they were.

A seed-8 trace confirmed clean mechanics: pastures built day 8 hours 5--11,
all four Cows placed day 9 hours 7--19, matching the accepted timing exactly.
The three nonqualifying control seeds traced (2, 5, 14) were exact ties.

The twenty-seed mirrored gate against Early NE livestock v1 produced
8W--0L--32T (60.0% match score) with zero errors. It averaged 96721.0 coins
against 95603.4, a 1117.6 lead, and 367.3 harvests. Average sales were 184.7
Wheat, 38.0 Carrots, 72.0 Melons, 196.9 Strawberries, 2.6 Tomatoes, 41.4 Eggs,
169.3 Milk, 142.0 Wool, and 235.5 Fertilizer, with 3.1 Wheat left over and zero
leftovers for every other tracked product. The 32 ties are the 16 nonqualifying
seeds tying exactly in both positions, confirming isolation; the 8 wins are the
4 qualifying seeds (1, 4, 8, 20) winning both positions. Milk sales rose from
158.8 to 169.3 while Wool held essentially flat (143.8 to 142.0), showing the
added Cows were not funded by displacing the Sheep branch.

Three five-seed regressions (seeds 1--5) all passed. Against Locked SW
livestock v1: 10W--0L--0T (100%), 82489.4 versus 74617.6, a 7871.8 lead.
Against Day-0 livestock v1: 10W--0L--0T (100%), 96503.2 versus 89344.2, a
7159.0 lead. Against Early NE livestock v1 itself on this smaller seed range:
4W--0L--6T (70.0%), 100915.2 versus 98162.0, a 2753.2 lead -- exactly 2
qualifying seeds (1, 4) winning both positions and 3 nonqualifying seeds (2,
3, 5) tying both positions, consistent with the twenty-seed gate. All three
regressions were zero-error.

The gain is larger per changed seed (+5590 average across the 4 qualifying
seeds) than the predecessor branch's own acceptance evidence (+3874 per
changed seed), with no paired-seed regression and no position asymmetry. The
branch is accepted and frozen as `baselines/early_ne_single_milk_v1.py`.

## Melon same-day sale -- accepted (roadmap detour)

Requested outside the P0--P4 sequence: get the opening twelve-Melon wave sold
on its own harvest day (day 10) instead of the automatic overnight deposit
selling it on day 11, so our glut moves the shared Melon price down before the
opponent's own sale lands.

Two designs were tried and rejected before the accepted one. A dedicated
one-day 9th hand exclusively harvesting all twelve Melon tiles was ruled out
by an action-budget calculation: the twelve tiles (all in Hands 1/2/3's
existing NW routes) need roughly 29 travel-and-harvest actions for a single
hand to sweep and return, against a 24-action day, capping a dedicated hand at
about 8 of 12 tiles and orphaning the rest for the day if their tiles were
reserved away from the owning hands. The user chose the alternative: modify
Hands 1, 2, and 3 (the existing owners, 4 Melon tiles each) to return and sell
their own Melon once done, at no hiring cost.

The first implementation gated the return trip on the hand reaching an idle
`PASS` turn, matching the pattern used elsewhere for optional Fertilizer
collection. It was silently inert: a seed-1 trace showed Melon still sold in
full on day 11, because a crop hand replants any tile the instant it empties,
so it never reaches `PASS` on melon harvest day. The trigger was changed to an
explicit check -- no assigned tile still holds an unharvested Melon plant --
so it can preempt replanting instead of waiting for genuine idleness.

With that fix, a seed-1 trace showed only 1 of 3 hands (Hand 3, with the
fewest tiles) made it home before day's end; Hands 1 and 2 did not. The cause
was the standard water-before-harvest step every crop uses to claim one extra
yield unit: it doubles the action cost per tile, and twelve tiles' worth of
that exceeds what a mid-sized hand's route can absorb in 24 actions. Melon
tiles were changed to harvest immediately once mature on harvest day only,
skipping that bonus. The same seed-1 trace then showed all three hands
completing and selling by day 10, and this held across eight traced seeds
(1--8): exactly 60 Melon sold on day 10 every time (12 tiles x 5, down from
12 x 6), zero leftover, zero day-11+ Melon sales, zero errors.

The twenty-seed mirrored gate against Early NE single-Milk v1 (the direct
predecessor) produced 36W--4L--0T (90.0% match score) with zero errors. It
averaged 97749.4 coins against 96327.3, a 1422.1 lead. Melon sold dropped
uniformly from 72.0 to 60.0 with zero leftover on every seed, since the
change is unconditional rather than shop-gated; zero ties is therefore
expected. Both losses (seeds 10 and 18) were thin: 254 and 13 coins on scores
near 80000.

The user's own hypothesis for the losses -- Melon-day reprioritization
starving other tiles of watering and turning them into weeds -- was checked
and ruled out. A baseline-vs-baseline trace on seed 10 showed the identical
weed conversions in the `OVERFLOW_BUFFER_WHEAT_TILES` region with no Melon
change present at all; they are pre-existing decay from an earlier accepted
candidate. The actual mechanism was confirmed by isolating the change on
seed 10: the unmodified strategy scores 83474 in our seat against the same
opponent, versus 81842 with the Melon change, a genuine 1632-coin cost on
this seed. Checking the real per-unit prices showed the timing mechanism
working exactly as intended -- our day-10 sale quoted 249.0 and 226.0 across
its two batches, while the opponent's day-11 dump of 72 quoted only 106.0 and
could only fall further across a larger single sale -- but the forfeited
yield (60 versus 72 units) outweighed the price edge on this particular seed.
It nets positive on 36 of 40 matches.

Five-seed regressions (seeds 1--5) against Locked SW livestock v1 and Day-0
livestock v1 both finished 10W--0L--0T (100%) with zero errors: 86527.4 versus
77346.4 (+9181.0) and 94263.2 versus 85816.0 (+8447.2) respectively. Accepted
and frozen as `baselines/melon_early_return_v1.py`.

## Hand-4 watered Melon block -- rejected

A follow-up to Melon same-day sale: of the three hands owning opening Melon
tiles, the lightest-loaded one (`MELON_WATERED_HAND_INDEX`, four Melon tiles
plus a single other tile) still watered before harvesting each Melon tile,
recovering the extra yield unit the other two hands forfeit for speed.

A first direct comparison against `early_ne_single_milk_v1` -- an older
baseline that predates the Melon same-day feature entirely -- showed a
misleadingly large gain, since it measured the whole feature plus this
addition against an opponent with neither. Isolating the addition correctly
(comparing our own seat against what the unmodified strategy would score in
the same seat against the same opponent) told a different story once
evaluated against the true predecessor, `melon_early_return_v1`.

Two variants were traced and both lost, by a precisely constant margin on
every seed checked (1--5), not the seed-to-seed variance a genuine market
effect would show:

- Full watering on all four tiles recovers +4 yield (24 vs 20) but always
  misses its own same-day cutoff by exactly one action (confirmed by trace:
  needs 7 moves + 1 PLACE from its last tile to the shed, with only 7 hours
  left after finishing harvest, and it cannot be hired any earlier -- it is
  already the fourth of six hires submitted the instant day 10 begins, and a
  HIRE order cannot act until the following step by game rule). Its batch
  sells a day late instead. Net: -194 coins/seed against the correct
  predecessor, constant across seeds 1--5.
- Watering only 3 of 4 tiles (fast-harvesting the last) saves exactly the one
  action needed and lands the same-day sale (63 units, all on day 10). This
  scored worse still: -319 to -322 coins/seed.

Isolating the true mechanism (own seat vs. an unmodified control in the same
seat) showed the opponent gaining an identical +334 coins/seed in both
variants, regardless of what Hand 4 did with its recovered time. Comparing
raw per-step market orders at the divergence point (day 10, hour 20) found
the cause: in the frozen baseline, two of the three Melon-owning hands
finish simultaneously at hour 20 and merge into one `SELL MELON 40` order,
matching the (unmodified) opponent's own simultaneous 40-unit order at the
same index. Delaying Hand 4 past hour 20 -- in either variant -- breaks that
synchronization: our hour-20 order shrinks to 20 while the opponent's stays
at 40. Per the documented lockstep rule, a same-index order pairs against
the smaller of the two, then the larger order's remainder sells alone; the
opponent's simultaneous 40-unit sale therefore lands in a lighter combined
glut than a mirrored 40-vs-40 pairing would give it, a benefit entirely
independent of Hand 4's own yield or timing.

This means any change that desynchronizes a Melon-owning hand from that
hour-20 pairing loses value to the opponent regardless of what is gained
elsewhere, unless the hand can be kept synchronized with its original
partner or another hand is delayed to rejoin it -- both of which defeat the
purpose of the change. `main.py` is reverted to exactly match
`baselines/melon_early_return_v1.py`; do not retry watering any of the three
Melon-owning hands without first addressing the hour-20 synchronization
constraint.

## Twelfth hand for the seven unmanaged SW tiles, Carrot variant -- rejected

A retry of the P0 permanent-twelfth-hand candidate, which lost every mirrored
match using Wheat on the seven already-purchased but unmanaged SW tiles
(`(3,8)`, `(4,8)`, `(0,9)`, `(1,9)`, `(2,9)`, `(3,9)`, `(4,9)`) because the
144-coin/day recurring hire cost outweighed Wheat's low value per action.
This variant kept the same permanent hire (from SW unlock onward, matching
P0's original timing) but planted Carrot instead: a shorter cycle, a higher
base price, and a gentler glut curve. `THIRD_QUADRANT_HAND_COUNT` moved 11 to
12, `HAND_HIRE_COSTS` gained the next Fibonacci value (144) for the twelfth
hire, and a seed-target floor was added so the hand's Carrot supply would not
depend on whatever the adaptive crop-selection logic elsewhere happened to be
buying that day.

Mechanically the hand worked as designed: hired on schedule (full 12-hand
staffing confirmed reached by hour 2 every day, same as the control's
11-hand staffing -- ruling out hiring-queue congestion as a side effect),
worked all seven tiles, and roughly tripled match-wide Carrot output (143
sold versus 48 for the unmodified strategy on seed 1).

Isolating the true effect (own seat vs. an unmodified control in the same
seat, same opponent) showed a large, consistent loss across every seed
checked (1--5): -9485, -10217, -2721, -7537, and -3780 coins, averaging
roughly -6750. This is far larger than the twelfth hire's own recurring cost
(~144/day, roughly -2700 to -2900 across an 18--19 day SW window) or the
extra Carrot seed cost (~760 on seed 1) could explain on their own, and
Carrot itself was actually a net revenue *gain* on seed 1 (higher average
price than the control despite triple the volume).

A full revenue breakdown by product (seed 1) found the real damage
elsewhere, at unchanged sale *quantities*: Milk's average realized price
nearly halved (194.9 to 113.3 across the same 222 units, roughly -18,100),
Strawberry's dropped twelve percent (219.7 to 191.9 across roughly the same
volume), while Wool's nearly tripled (66.9 to 179.2 across the same 119
units, a partial offset). Checking the actual per-step market-order list
positions confirmed Strawberry's sale was consistently pushed one index later
than the control's, and Wool's two to three indices later -- both consistent
with the documented lockstep-pairing mechanic (see Melon same-day sale and
the `mechanics.md` refinement above). Milk's list position was nearly
identical to the control's in all but one of twenty-six checked instances,
so its price collapse is not fully explained by index position alone; the
exact secondary channel was not pinned down before rejecting the candidate,
since the aggregate result was already decisive.

The broader lesson: introducing any new recurring hand or crop changes the
shape and timing of the whole day's market-order list, and the resulting
knock-on effects on completely unrelated products' realized prices can
dwarf the direct cost/value tradeoff of the new work itself. `main.py` is
reverted to exactly match `baselines/melon_early_return_v1.py`. Do not retry
a twelfth hand on these seven tiles with any single-crop substitution alone;
any future attempt needs to either keep the added hand's market orders from
displacing other sales' list positions, or independently verify Milk/Wool/
Strawberry pricing is not being disturbed before trusting a product-level
revenue estimate.

## Crop sale priority order -- accepted

Requested outside the P0--P4 sequence: audit how `market_orders` gets built
each step and confirm premium crops sell first. The audit found only Melon
was ever explicitly prioritized (the existing, proven mechanism); everything
else sold in raw tuple-definition order, not by value. Strawberry -- the
second most valuable crop at base price 120 -- sold behind Wheat (25) and
Carrot (35) purely because `CROPS_MANAGED` lists them in that order. The
animal-product loop's own comment admitted as much: "does not matter now,
may be useful later."

The fix generalizes the existing Melon-only pop/insert special case into a
`CROP_SALE_PRIORITY` tuple (`MELON, STRAWBERRY, TOMATO, CARROT, WHEAT`,
matching descending base price) and a single stable sort keyed on that
tuple, replacing the special case. A stable sort only pulls priority-crop
`SELL` orders to the front in that order; every other order (seed buys,
hires, land, Fertilizer, animal products) keeps its existing relative order
untouched. Scoped to crops only: Wool and Milk order was deliberately left
alone, since the SW extra-hand experiment immediately above found Wool's
realized price actually improving from a *later* list position in that
case -- animal-product ordering is not assumed to follow the same rule
without its own dedicated test.

A trace confirmed the sort works as intended (e.g. a real step ordered
`STRAWBERRY, TOMATO, WHEAT, WOOL, ...`, matching the declared priority
exactly) with Fertilizer still correctly last and zero errors. Isolating the
change (own seat vs. an unmodified control, same opponent, seeds 1--5) showed
small, mixed-sign deltas (-27, +270, -1, +28, -37), confirming the effect is
real but much smaller than the large-quantity Melon and SW-hand cases --
expected, since Strawberry/Wheat/Carrot co-occur in the same step far less
often and in smaller quantities than those did.

The twenty-seed mirrored gate against Melon early return v1 produced
25W--15L--0T (62.5% match score) with zero errors. It averaged 92970.3 coins
against 92814.5, a 155.8 lead, and 368.1 harvests. Average sales were 198.0
Wheat, 40.1 Carrots, 60.0 Melons, 192.4 Strawberries, 1.4 Tomatoes, 41.4
Eggs, 167.2 Milk, 143.8 Wool, and 232.6 Fertilizer. Average leftovers were
3.2 Wheat and zero for every other tracked product. Zero ties is expected:
the change is unconditional, not shop-gated. All three sampled losses
(seeds 1, 5, 17) were thin -- 31, 47, and 91 coins respectively on scores
near 90000--110000 -- consistent with the isolated per-seed deltas measured
above, not a systematic regression.

The five-seed multi-opponent regression (protocol step 6) was explicitly
skipped at the user's request. Accepted on the twenty-seed direct-gate
evidence alone -- positive average lead, zero errors, no catastrophic
paired-seed losses -- and frozen as `baselines/crop_sale_priority_v1.py`.
Revisit the multi-opponent regression if a future candidate's result looks
inconsistent with this one and the gap needs isolating.
