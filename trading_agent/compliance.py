from dataclasses import dataclass


@dataclass(frozen=True)
class ComplianceResult:
    ok: bool
    reason: str


def check_jurisdiction(jurisdiction: str, allowed: set[str]) -> ComplianceResult:
    if jurisdiction in allowed:
        return ComplianceResult(ok=True, reason="Jurisdiction allowed by local policy.")
    return ComplianceResult(
        ok=False,
        reason=(
            f"Jurisdiction '{jurisdiction}' is not in allowlist. "
            "Do not run live trading until legal review is complete."
        ),
    )


def check_live_ack(live: bool, ack_live_risk: bool) -> ComplianceResult:
    if not live:
        return ComplianceResult(ok=True, reason="Paper mode selected.")
    if ack_live_risk:
        return ComplianceResult(ok=True, reason="Live mode risk acknowledgment present.")
    return ComplianceResult(
        ok=False,
        reason="Live mode requested without --ack-live-risk acknowledgment.",
    )
