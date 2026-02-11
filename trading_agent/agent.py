import random
import time

from .compliance import check_jurisdiction, check_live_ack
from .config import AgentConfig, DEFAULT_ALLOWED_JURISDICTIONS
from .polymarket_client import PolymarketClient
from .risk import RiskState, can_trade, position_size_usd
from .strategy import MarketSnapshot, generate_signal


class AutonomousAgent:
    def __init__(self, config: AgentConfig, live: bool, ack_live_risk: bool) -> None:
        self.config = config
        self.live = live
        self.ack_live_risk = ack_live_risk
        self.client = PolymarketClient(api_base=config.api_base)
        self.risk_state = RiskState(
            start_of_day_equity=config.capital_usd,
            current_equity=config.capital_usd,
        )

    def validate_compliance(self) -> None:
        j = check_jurisdiction(self.config.jurisdiction, DEFAULT_ALLOWED_JURISDICTIONS)
        if not j.ok:
            raise RuntimeError(j.reason)

        l = check_live_ack(self.live, self.ack_live_risk)
        if not l.ok:
            raise RuntimeError(l.reason)

    def estimate_probability(self, yes_price: float) -> float:
        """Placeholder model: mean-reverting synthetic estimator.

        Replace with tested, externally validated research model before production.
        """
        noise = random.uniform(-0.05, 0.05)
        return min(0.99, max(0.01, yes_price + noise))

    def run_once(self) -> list[dict]:
        if not can_trade(self.risk_state, self.config.max_daily_drawdown):
            return [{"status": "HALTED", "reason": "Max daily drawdown reached."}]

        actions = []
        markets = self.client.fetch_markets(limit=20)
        for m in markets:
            model_prob = self.estimate_probability(m.yes_price)
            snapshot = MarketSnapshot(market_id=m.market_id, yes_price=m.yes_price, model_yes_prob=model_prob)
            signal = generate_signal(snapshot)
            if signal is None:
                continue

            trade_prob = model_prob if signal.side == "BUY_YES" else 1.0 - model_prob
            trade_price = m.yes_price if signal.side == "BUY_YES" else 1.0 - m.yes_price
            size = position_size_usd(
                capital_usd=self.risk_state.current_equity,
                prob=trade_prob,
                price=trade_price,
                max_risk_per_trade=self.config.max_risk_per_trade,
            )
            if size <= 0:
                continue

            order = self.client.submit_order(market_id=m.market_id, side=signal.side, size_usd=round(size, 2))
            actions.append(order)

        return actions

    def run_forever(self) -> None:
        self.validate_compliance()
        while True:
            actions = self.run_once()
            print({"actions": actions, "equity": self.risk_state.current_equity})
            time.sleep(self.config.poll_interval_seconds)
