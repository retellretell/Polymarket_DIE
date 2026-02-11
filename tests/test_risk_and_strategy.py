from trading_agent.risk import RiskState, can_trade, kelly_fraction, position_size_usd
from trading_agent.strategy import MarketSnapshot, generate_signal


def test_generate_signal_yes():
    s = MarketSnapshot(market_id="1", yes_price=0.40, model_yes_prob=0.50)
    signal = generate_signal(s, min_edge=0.03)
    assert signal is not None
    assert signal.side == "BUY_YES"


def test_generate_signal_none_when_small_edge():
    s = MarketSnapshot(market_id="1", yes_price=0.40, model_yes_prob=0.41)
    assert generate_signal(s, min_edge=0.03) is None


def test_kelly_fraction_non_negative():
    assert kelly_fraction(prob=0.5, price=0.5) >= 0


def test_position_size_caps_risk():
    size = position_size_usd(capital_usd=10000, prob=0.7, price=0.5, max_risk_per_trade=0.01)
    assert size <= 100


def test_drawdown_gate():
    risk = RiskState(start_of_day_equity=10000, current_equity=9500)
    assert not can_trade(risk, max_daily_drawdown=0.03)
