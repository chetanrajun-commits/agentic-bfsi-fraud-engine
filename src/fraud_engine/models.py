"""Domain models for the Fraud Engine."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class UserProfile:
    home_country: str
    avg_transaction_amount: float
    last_transaction_time: str  # ISO 8601 format


@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    user_id: str
    amount: float
    currency: str
    ip_country: str
    timestamp: str  # ISO 8601 format
    user_profile: UserProfile


@dataclass
class AgentResult:
    """Uniform output for all risk agents."""
    agent_name: str
    risk_score: int  # 0 to 100
    reasons: list[str] = field(default_factory=list)


@dataclass
class RiskAssessment:
    """Final aggregated decision."""
    is_fraud: bool
    total_risk_score: int
    agent_results: list[AgentResult]
    action_taken: str
