# AI-Trader Reproduction Guide

This guide explains how to run the agentic trading pipeline and
reproduce the comparison between:

-   `max_steps = 30`
-   `max_steps = 5`

------------------------------------------------------------------------

## 1. Clone Repository

``` bash
git clone https://github.com/yukic993/FTEC5660_IndividualProject
cd AI-Trader
```

------------------------------------------------------------------------

## 2. Create Virtual Environment

``` bash
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
```

------------------------------------------------------------------------

## 3. Install Dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 4. Configure Environment Variables

Copy template:

``` bash
cp .env.example .env
```

Edit `.env` and configure:

    OPENAI_API_BASE= (OpenRouter base URL)
    OPENAI_API_KEY=  (Your OpenRouter key)
    ALPHA_VANTAGE_API_KEY=
    JINA_API_KEY=
    MAX_STEPS=30   # or 5

If OpenAI direct access fails, use OpenRouter + VPN.

------------------------------------------------------------------------

## 5. Modify Max Steps


-   Change `MAX_STEPS` in `.env`
-   Modify `default_hour_config.json`:

``` json
"max_steps": 5
```

------------------------------------------------------------------------

## 6. Set Trading Window

In config:

``` json
"init_date": "2025-11-05 15:00:00",
"end_date": "2025-11-07 15:00:00"
```

------------------------------------------------------------------------

## 7. Run MCP Services

Make scripts executable:

``` bash
chmod +x scripts/*.sh
```
If Use Alpha Vantage and Start MCP services:

``` bash
bash scripts/main.sh
```

Use existing price data of NASDAQ 100 clone and start MCP services:

``` bash
bash scripts/main_step2.sh
```

If it blocks after starting MCP services:

Open a **new terminal window** and run:

``` bash
bash scripts/main_step3.sh
```

------------------------------------------------------------------------

## 8. Output Files

After execution, the system generates:

-   `data/agent_data/gpt-5/position/position.jsonl`
-   Agent logs
-   Tool call traces

Rename results for comparison:

    position_30steps.jsonl
    position_5steps.jsonl

------------------------------------------------------------------------

## 9. Run Performance Analysis

Use the evaluation script:

``` bash
python analyse.py
```

This computes:

-   Portfolio value
-   Total return
-   Sharpe ratio
-   Volatility
-   Max drawdown

Evaluation window:

    2025-11-05 15:00:00 → 2025-11-07 15:00:00

------------------------------------------------------------------------

## Notes & Limitations

-   Alpha Vantage free tier limits real-time data.
-   Replay mode uses historical data from repository.
-   LLM outputs are non-deterministic.
-   VPN may be required for OpenRouter access.

------------------------------------------------------------------------

## Experiment Variable

Only modification between experiments:

    max_steps = 30
    vs
    max_steps = 5

This controls the agent's reasoning depth.
