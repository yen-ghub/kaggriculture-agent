# Kaggriculture Agent

A local Python project for developing and testing an agent for the
[Kaggriculture Kaggle competition](https://www.kaggle.com/competitions/kaggriculture).

The current candidate is a rule-based melon agent managing 15 farm tiles.

## Requirements

- Python 3.12
- Git
- `kaggle-environments==1.32.6`

## Setup

Create and activate a virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Install the required packages:

```powershell
python -m pip install -r requirements.txt
```

## Running the project

Run one local match with detailed tracing:

```powershell
python run_local.py
```

Run the multi-seed evaluation:

```powershell
python evaluate.py
```

Some OpenSpiel warnings may appear when importing `kaggle_environments`.
They are unrelated to Kaggriculture if the match still runs successfully.

## Project structure

- `main.py` — current candidate agent
- `run_local.py` — detailed single-match tracing
- `evaluate.py` — multi-seed, both-position evaluation
- `sweep_tiles.py` — managed-tile-count experiments
- `baselines/carrot_v1.py` — frozen carrot baseline
- `baselines/melon_v1.py` — frozen melon baseline
- `requirements.txt` — Python dependencies


## Current results

All results below use 20 seeds and both player positions, for a total of
40 matches.

| Candidate | Opponent | Match score | Avg money | Avg harvests | Avg units sold |
|---|---|---:|---:|---:|---:|
| Carrot v1 | Starter | 100% | 7754.1 | 60.0 | 180.0 |
| Melon, 7 tiles | Carrot v1 | 100% | 22138.0 | 14.0 | 84.0 |
| Melon, 14 tiles | Carrot v1 | 100% | 30004.1 | 23.0 | 134.0 |
| Melon, 15 tiles | Carrot v1 | 100% | 30011.2 | 23.1 | 134.1 |
| Melon, 16 tiles | Carrot v1 | 100% | 29951.0 | 23.0 | 133.7 |
| Melon v1 | Melon v1 | 50% | 16586.6 | 22.9 | 133.2 |

The melon self-play result shows that competing in the same market lowers both
agents' earnings substantially. This suggests that crop diversification or
market-aware crop selection may be the next useful strategy improvement.