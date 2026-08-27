# Competitive Agent Roadmap

## Current baseline

Two hands v1:

- 17 managed tiles
- Two hired hands
- Two four-tile hand zones
- Wheat limit 8
- Sales-first market ordering
- Carrot, wheat, and melon
- 20-seed self-play score: 50%

## Public replay observations

Replays examined:

- 100747787
- 100750070

Observed:

- Hands can plant using the shared seed inventory.
- Strong agents position hands before work becomes available.
- Several agents manage multiple quadrants.
- Strawberry is commonly planted.

## Planned experiments

1. Allow hands to plant on the existing 17 tiles.
2. Coordinate seed reservations across farmer and hands.
3. Expand to all 25 tiles in the first quadrant.
4. Add ongoing-crop support.
5. Add Strawberry with a conservative adaptive limit.
6. Evaluate buying additional quadrants.
7. Build baselines based on public opponent strategies.

## Evaluation gates

Each feature must pass:

- Local trace with no duplicate or invalid actions
- Five-seed test against Two hands v1
- Five-seed regression suite
- Twenty-seed validation before merging