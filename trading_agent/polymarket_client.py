from dataclasses import dataclass
import requests


@dataclass(frozen=True)
class Market:
    market_id: str
    question: str
    yes_price: float


class PolymarketClient:
    def __init__(self, api_base: str, timeout_seconds: int = 15) -> None:
        self.api_base = api_base.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def fetch_markets(self, limit: int = 25) -> list[Market]:
        """Fetch active markets from Polymarket Gamma API.

        Endpoint behavior can change; this method is intentionally defensive.
        """
        url = f"{self.api_base}/markets"
        resp = requests.get(url, params={"active": "true", "limit": limit}, timeout=self.timeout_seconds)
        resp.raise_for_status()
        data = resp.json()

        markets: list[Market] = []
        for row in data:
            market_id = str(row.get("id", ""))
            question = str(row.get("question", ""))
            # Common field names observed in public responses.
            yes_price = row.get("lastTradePrice") or row.get("bestAsk") or row.get("yesPrice")
            if market_id and isinstance(yes_price, (int, float)):
                markets.append(Market(market_id=market_id, question=question, yes_price=float(yes_price)))
        return markets

    def submit_order(self, market_id: str, side: str, size_usd: float) -> dict:
        """Placeholder for order submission.

        Real order routing requires authenticated CLOB integration; keep this as a stub
        to avoid accidental unsafe live deployment.
        """
        return {
            "status": "SIMULATED",
            "market_id": market_id,
            "side": side,
            "size_usd": size_usd,
            "note": "Order routing intentionally stubbed pending legal + integration review.",
        }
