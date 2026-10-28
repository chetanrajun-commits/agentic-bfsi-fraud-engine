"""Shared fixtures for the Fraud Engine test suite."""

from __future__ import annotations

import pytest

from fraud_engine.models import Transaction, UserProfile


@pytest.fixture
def safe_tx() -> Transaction:
    """A standard transaction that should pass all rules."""
    return Transaction(
        transaction_id="tx-safe",
        user_id="user-1",
        amount=50.00,
        currency="USD",
        ip_country="US",
        timestamp="2025-10-28T14:30:00Z",
        user_profile=UserProfile(
            home_country="US",
            avg_transaction_amount=100.00,
            last_transaction_time="2025-10-28T10:00:00Z",
        )
    )


@pytest.fixture
def fraud_tx() -> Transaction:
    """A highly suspicious transaction."""
    return Transaction(
        transaction_id="tx-fraud",
        user_id="user-2",
        amount=25000.00,  # > 10k limit
        currency="USD",
        ip_country="RU",  # != home country
        timestamp="2025-10-28T14:30:00Z",
        user_profile=UserProfile(
            home_country="US",
            avg_transaction_amount=150.00,  # 25000 > 150 * 5
            last_transaction_time="2025-10-28T14:28:00Z",  # Only 2 mins ago
        )
    )
@pytest.fixture
def workdir(tmp_path: Path) -> Path:
    d = tmp_path / "out"
    d.mkdir()
    return d
