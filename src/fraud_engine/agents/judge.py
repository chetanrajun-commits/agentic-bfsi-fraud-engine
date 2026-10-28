"""Judge Agent.

Aggregates the risk scores from all specialized agents and makes the final
deterministic decision on whether the transaction is fraudulent.
"""

from __future__ import annotations

from ..models import AgentResult, RiskAssessment


class JudgeAgent:
    name = "JudgeAgent"
    
    # If the combined risk score hits this threshold, we block the transaction.
    FRAUD_THRESHOLD = 70

    def evaluate(self, agent_results: list[AgentResult]) -> RiskAssessment:
        total_risk = sum(result.risk_score for result in agent_results)
        
        # Cap the risk at 100
        total_risk = min(total_risk, 100)
        
        is_fraud = total_risk >= self.FRAUD_THRESHOLD
        
        action = "BLOCK_AND_FREEZE" if is_fraud else "ALLOW"
        
        return RiskAssessment(
            is_fraud=is_fraud,
            total_risk_score=total_risk,
            agent_results=agent_results,
            action_taken=action
        )
