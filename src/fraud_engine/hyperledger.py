"""Hyperledger Generator.

Simulates the creation of a Hyperledger Fabric chaincode invocation payload.
When a transaction is flagged as fraud, we generate this payload so the
blockchain network can freeze the digital asset.
"""

from __future__ import annotations

import json
from pathlib import Path

from .models import RiskAssessment, Transaction


class HyperledgerGenerator:
    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_freeze_payload(self, tx: Transaction, assessment: RiskAssessment) -> Path:
        """Creates a JSON payload simulating a Hyperledger smart contract call."""
        
        payload = {
            "chaincode": "asset_management",
            "function": "freeze_account",
            "args": {
                "user_id": tx.user_id,
                "transaction_id": tx.transaction_id,
                "reason": f"Risk score {assessment.total_risk_score} exceeded threshold.",
                "risk_factors": [
                    reason for result in assessment.agent_results for reason in result.reasons
                ]
            }
        }

        filename = f"{tx.transaction_id}-freeze-payload.json"
        filepath = self.output_dir / filename
        
        filepath.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return filepath
