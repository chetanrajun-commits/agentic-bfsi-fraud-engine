"""Heuristic Risk Agent.

Scans the raw transaction for immediate red flags (e.g., massive amounts or
unexpected geolocations) without looking at the user's history.
"""

from __future__ import annotations

from ..models import AgentResult, Transaction


class HeuristicAgent:
    name = "HeuristicAgent"

    def evaluate(self, tx: Transaction) -> AgentResult:
        risk_score = 0
        reasons = []

        # Rule 1: Hard limit on transaction amount
        if tx.amount > 10000.00:
            risk_score += 50
            reasons.append(f"Transaction amount (${tx.amount}) exceeds hard limit of $10,000.")

        # Rule 2: Geolocation mismatch
        if tx.ip_country != tx.user_profile.home_country:
            risk_score += 30
            reasons.append(
                f"IP country ({tx.ip_country}) does not match home country ({tx.user_profile.home_country})."
            )

        return AgentResult(agent_name=self.name, risk_score=risk_score, reasons=reasons)
