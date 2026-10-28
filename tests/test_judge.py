"""Tests for the Judge Agent."""

from __future__ import annotations

from fraud_engine.agents.judge import JudgeAgent
from fraud_engine.models import AgentResult


def test_judge_blocks_high_risk() -> None:
    judge = JudgeAgent()
    results = [
        AgentResult(agent_name="A", risk_score=50, reasons=[]),
        AgentResult(agent_name="B", risk_score=30, reasons=[]),
    ]
    
    assessment = judge.evaluate(results)
    
    # 50 + 30 = 80, which is >= 70 threshold
    assert assessment.total_risk_score == 80
    assert assessment.is_fraud is True
    assert assessment.action_taken == "BLOCK_AND_FREEZE"


def test_judge_allows_low_risk() -> None:
    judge = JudgeAgent()
    results = [
        AgentResult(agent_name="A", risk_score=10, reasons=[]),
        AgentResult(agent_name="B", risk_score=20, reasons=[]),
    ]
    
    assessment = judge.evaluate(results)
    
    # 10 + 20 = 30, which is < 70 threshold
    assert assessment.total_risk_score == 30
    assert assessment.is_fraud is False
    assert assessment.action_taken == "ALLOW"


def test_judge_caps_score_at_100() -> None:
    judge = JudgeAgent()
    results = [
        AgentResult(agent_name="A", risk_score=80, reasons=[]),
        AgentResult(agent_name="B", risk_score=80, reasons=[]),
    ]
    
    assessment = judge.evaluate(results)
    
    # 80 + 80 = 160, but should cap at 100
    assert assessment.total_risk_score == 100
    assert assessment.is_fraud is True
