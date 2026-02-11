import argparse

from trading_agent.agent import AutonomousAgent
from trading_agent.config import load_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compliance-first Polymarket autonomous trading agent")
    parser.add_argument("--live", action="store_true", help="Enable live mode (gated by --ack-live-risk)")
    parser.add_argument("--ack-live-risk", action="store_true", help="Explicitly acknowledge live trading risk")
    parser.add_argument("--paper", action="store_true", help="Run a single paper cycle then exit")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config()
    agent = AutonomousAgent(config=config, live=args.live, ack_live_risk=args.ack_live_risk)

    if args.paper or not args.live:
        agent.validate_compliance()
        actions = agent.run_once()
        print({"mode": "paper", "actions": actions})
        return

    agent.run_forever()


if __name__ == "__main__":
    main()
