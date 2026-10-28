"""End-to-end test of the fraud pipeline."""

from __future__ import annotations

import json
from pathlib import Path

from fraud_engine.orchestrator import Orchestrator


def test_orchestrator_generates_hyperledger_payload(
    workdir: Path, fraud_tx
) -> None:
    # Write the fraud transaction to a temp file
    tx_file = workdir / "fraud.json"
    tx_data = {
        "transaction_id": fraud_tx.transaction_id,
        "user_id": fraud_tx.user_id,
        "amount": fraud_tx.amount,
        "currency": fraud_tx.currency,
        "ip_country": fraud_tx.ip_country,
        "timestamp": fraud_tx.timestamp,
        "user_profile": {
            "home_country": fraud_tx.user_profile.home_country,
            "avg_transaction_amount": fraud_tx.user_profile.avg_transaction_amount,
            "last_transaction_time": fraud_tx.user_profile.last_transaction_time,
        }
    }
    tx_file.write_text(json.dumps(tx_data), encoding="utf-8")

    orchestrator = Orchestrator(workdir)
    exit_code = orchestrator.run(tx_file)
    
    assert exit_code == 0
    
    # Verify the Hyperledger payload was generated
    payload_file = workdir / "tx-fraud-freeze-payload.json"
    assert payload_file.exists()
    
    payload = json.loads(payload_file.read_text())
    assert payload["chaincode"] == "asset_management"
    assert payload["function"] == "freeze_account"
    assert payload["args"]["user_id"] == "user-2"
