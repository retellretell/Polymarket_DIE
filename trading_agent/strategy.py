from dataclasses import dataclass


@dataclass(frozen=True)
class MarketSnapshot:
    market_id: str
    yes_price: float
    model_yes_prob: float


@dataclass(frozen=True)
class TradeSignal:
    market_id: str
    side: str
    edge: float


def generate_signal(snapshot: MarketSnapshot, min_edge: float = 0.03) -> TradeSignal | None:
    """Generate a directional signal from model-vs-market edge.

    edge = expected_prob - market_implied_prob
    """
    edge = snapshot.model_yes_prob - snapshot.yes_price

    if edge >= min_edge:
        return TradeSignal(market_id=snapshot.market_id, side="BUY_YES", edge=edge)

    if -edge >= min_edge:
        return TradeSignal(market_id=snapshot.market_id, side="BUY_NO", edge=-edge)

    return None
