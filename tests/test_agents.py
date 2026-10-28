"""Tests for the individual risk agents."""

from __future__ import annotations

from fraud_engine.agents.behavioral import BehavioralAgent
from fraud_engine.agents.heuristic import HeuristicAgent
from fraud_engine.models import Transaction


def test_heuristic_flags_fraud(fraud_tx: Transaction) -> None:
    agent = HeuristicAgent()
    result = agent.evaluate(fraud_tx)
    
    # 50 for amount + 30 for geo = 80
    assert result.risk_score == 80
    assert len(result.reasons) == 2


def test_heuristic_passes_safe(safe_tx: Transaction) -> None:
    agent = HeuristicAgent()
    result = agent.evaluate(safe_tx)
    
    assert result.risk_score == 0
    assert len(result.reasons) == 0


def test_behavioral_flags_fraud(fraud_tx: Transaction) -> None:
    agent = BehavioralAgent()
    result = agent.evaluate(fraud_tx)
    
    # 40 for anomaly + 20 for velocity = 60
    assert result.risk_score == 60
    assert len(result.reasons) == 2


def test_behavioral_passes_safe(safe_tx: Transaction) -> None:
    agent = BehavioralAgent()
    result = agent.evaluate(safe_tx)
    
    assert result.risk_score == 0
    assert len(result.reasons) == 0
