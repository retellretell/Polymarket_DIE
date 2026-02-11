# Polymarket Autonomous Trading Agent (Compliance-First)

This repository contains a **compliance-first autonomous trading agent scaffold** for Polymarket.

## Important disclaimer

- This software is for educational and engineering purposes.
- It does **not** guarantee profits.
- No trading system can safely promise fixed daily returns (e.g., `$1,000/day`).
- You are responsible for legal, tax, and regulatory compliance in your jurisdiction.

## What this agent does

- Pulls market snapshots from Polymarket APIs.
- Runs a simple value strategy based on model-estimated probabilities.
- Applies strict risk controls before any order is sent.
- Enforces compliance gates (jurisdiction allowlist + explicit live-trading acknowledgment).
- Supports paper mode by default.

## Project structure

- `trading_agent/config.py` — strongly typed runtime settings.
- `trading_agent/compliance.py` — compliance checks and live-trading guardrails.
- `trading_agent/polymarket_client.py` — lightweight Polymarket HTTP client.
- `trading_agent/strategy.py` — expected-value signal generation.
- `trading_agent/risk.py` — position sizing and drawdown protection.
- `trading_agent/agent.py` — autonomous loop orchestration.
- `main.py` — CLI entrypoint.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py --paper
```

## Environment variables

- `POLYMARKET_API_BASE` (default: `https://gamma-api.polymarket.com`)
- `POLYMARKET_PRIVATE_KEY` (required for live trading)
- `POLYMARKET_CHAIN_ID` (default: `137`)
- `AGENT_CAPITAL_USD` (default: `10000`)
- `AGENT_MAX_RISK_PER_TRADE` (default: `0.01`)
- `AGENT_MAX_DAILY_DRAWDOWN` (default: `0.03`)
- `AGENT_JURISDICTION` (e.g. `US`, `CA`)

## Running live (intentionally gated)

Live trading is blocked unless both are true:

1. `--live` CLI flag is passed, and
2. `--ack-live-risk` is explicitly provided.

This is to reduce accidental deployment and encourage deliberate review.

## Testing

```bash
pytest -q
```
