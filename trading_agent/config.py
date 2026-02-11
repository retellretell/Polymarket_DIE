from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AgentConfig:
    api_base: str
    private_key: str | None
    chain_id: int
    capital_usd: float
    max_risk_per_trade: float
    max_daily_drawdown: float
    jurisdiction: str
    poll_interval_seconds: int


DEFAULT_ALLOWED_JURISDICTIONS = {
    "CA",
    "FR",
    "DE",
    "JP",
    "SG",
    "UK",
}


def load_config() -> AgentConfig:
    return AgentConfig(
        api_base=os.getenv("POLYMARKET_API_BASE", "https://gamma-api.polymarket.com"),
        private_key=os.getenv("POLYMARKET_PRIVATE_KEY"),
        chain_id=int(os.getenv("POLYMARKET_CHAIN_ID", "137")),
        capital_usd=float(os.getenv("AGENT_CAPITAL_USD", "10000")),
        max_risk_per_trade=float(os.getenv("AGENT_MAX_RISK_PER_TRADE", "0.01")),
        max_daily_drawdown=float(os.getenv("AGENT_MAX_DAILY_DRAWDOWN", "0.03")),
        jurisdiction=os.getenv("AGENT_JURISDICTION", "UNKNOWN").upper(),
        poll_interval_seconds=int(os.getenv("AGENT_POLL_INTERVAL_SECONDS", "60")),
    )
