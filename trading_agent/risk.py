from dataclasses import dataclass


@dataclass
class RiskState:
    start_of_day_equity: float
    current_equity: float

    @property
    def drawdown_pct(self) -> float:
        if self.start_of_day_equity <= 0:
            return 1.0
        return max(0.0, (self.start_of_day_equity - self.current_equity) / self.start_of_day_equity)


def kelly_fraction(prob: float, price: float) -> float:
    """Approximate Kelly fraction for binary contract with payout 1 and cost=price."""
    if price <= 0 or price >= 1:
        return 0.0
    b = (1 - price) / price
    q = 1 - prob
    k = (b * prob - q) / b
    return max(0.0, k)


def position_size_usd(capital_usd: float, prob: float, price: float, max_risk_per_trade: float) -> float:
    raw_fraction = kelly_fraction(prob=prob, price=price)
    capped_fraction = min(raw_fraction, max_risk_per_trade)
    return max(0.0, capital_usd * capped_fraction)


def can_trade(risk_state: RiskState, max_daily_drawdown: float) -> bool:
    return risk_state.drawdown_pct < max_daily_drawdown
