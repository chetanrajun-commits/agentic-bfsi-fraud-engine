"""Behavioral Risk Agent.

Evaluates the transaction against the user's historical profile to detect
anomalies (e.g., spending way above their average or rapid velocity).
"""

from __future__ import annotations

from datetime import datetime

from ..models import AgentResult, Transaction


class BehavioralAgent:
    name = "BehavioralAgent"

    def evaluate(self, tx: Transaction) -> AgentResult:
        risk_score = 0
        reasons = []

        # Rule 1: Amount anomaly (Spending > 5x their average)
        if tx.amount > (tx.user_profile.avg_transaction_amount * 5):
            risk_score += 40
            reasons.append(
                f"Transaction amount (${tx.amount}) is significantly higher than user average "
                f"(${tx.user_profile.avg_transaction_amount})."
            )

        # Rule 2: Velocity check (Two transactions within 5 minutes)
        try:
            tx_time = datetime.fromisoformat(tx.timestamp.replace("Z", "+00:00"))
            last_time = datetime.fromisoformat(tx.user_profile.last_transaction_time.replace("Z", "+00:00"))
            
            time_diff = (tx_time - last_time).total_seconds()
            if time_diff < 300:  # 5 minutes
                risk_score += 20
                reasons.append(
                    f"High velocity: Another transaction was made {time_diff} seconds ago."
                )
        except ValueError:
            reasons.append("Could not parse timestamps for velocity check.")

        return AgentResult(agent_name=self.name, risk_score=risk_score, reasons=reasons)
