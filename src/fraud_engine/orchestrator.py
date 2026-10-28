"""Orchestrator.

Wires the Heuristic, Behavioral, and Judge agents into a single loop.
"""

from __future__ import annotations

import json
from pathlib import Path

from .agents.behavioral import BehavioralAgent
from .agents.heuristic import HeuristicAgent
from .agents.judge import JudgeAgent
from .hyperledger import HyperledgerGenerator
from .models import Transaction, UserProfile


class Orchestrator:
    def __init__(self, workdir: Path) -> None:
        self.workdir = workdir
        self.workdir.mkdir(parents=True, exist_ok=True)
        self.heuristic = HeuristicAgent()
        self.behavioral = BehavioralAgent()
        self.judge = JudgeAgent()
        self.generator = HyperledgerGenerator(self.workdir)

    def run(self, tx_path: Path) -> int:
        # 1. Load Transaction
        try:
            data = json.loads(tx_path.read_text(encoding="utf-8"))
            profile = UserProfile(**data.pop("user_profile"))
            tx = Transaction(**data, user_profile=profile)
        except Exception as e:
            print(f"[ERROR] Failed to parse transaction: {e}")
            return 1

        print(f"[ORCHESTRATOR] Processing Transaction: {tx.transaction_id} | Amount: ${tx.amount}")

        # 2. Run Agents
        print("[AGENTS]       Running Heuristic Agent...")
        h_result = self.heuristic.evaluate(tx)
        
        print("[AGENTS]       Running Behavioral Agent...")
        b_result = self.behavioral.evaluate(tx)

        # 3. Judge Evaluation
        assessment = self.judge.evaluate([h_result, b_result])
        print(f"[JUDGE]        Total Risk Score: {assessment.total_risk_score}/100")
        
        for result in assessment.agent_results:
            for reason in result.reasons:
                print(f"[JUDGE]          - {reason}")

        # 4. Take Action
        if assessment.is_fraud:
            print(f"[ORCHESTRATOR] 🛑 FRAUD DETECTED. Action: {assessment.action_taken}")
            payload_path = self.generator.generate_freeze_payload(tx, assessment)
            print(f"[HYPERLEDGER]  Generated chaincode payload: {payload_path.name}")
        else:
            print(f"[ORCHESTRATOR] ✅ Transaction Approved. Action: {assessment.action_taken}")

        print("[ORCHESTRATOR] Pipeline complete.")
        return 0
