# Agentic BFSI Fraud & Tokenization Engine

> A multi-agent AI pipeline for real-time BFSI fraud detection and simulated Hyperledger smart contract generation.

[![CI](https://github.com/chetanrajun-commits/agentic-bfsi-fraud-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/chetanrajun-commits/agentic-bfsi-fraud-engine/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Ruff](https://img.shields.io/badge/lint-ruff-orange.svg)](https://github.com/astral-sh/ruff)

---

## The Problem

In the BFSI sector, fraud detection is traditionally rule-based, rigid, and generates high false-positive rates that frustrate legitimate customers. Conversely, static rules cannot adapt to rapidly evolving fraud patterns (like account takeovers or high-velocity attacks). 

This repository is a **reference implementation** of the fix: a multi-agent AI architecture that evaluates transactions from multiple angles, aggregates the risk, and automatically executes a **Hyperledger smart contract** to freeze compromised accounts before the funds leave the bank.

## What it does

1. **Heuristic Agent:** Scans for immediate hard limits (e.g., transaction amounts exceeding $10k) and geolocation anomalies (e.g., IP country differs from home country).
2. **Behavioral Agent:** Evaluates the transaction against the user's historical profile, flagging spending anomalies (>5x average) and rapid velocity (multiple transactions in under 5 minutes).
3. **Judge Agent:** Aggregates the risk scores. If the total risk exceeds the threshold, it triggers a `BLOCK_AND_FREEZE` action.
4. **Hyperledger Generator:** Generates a JSON payload simulating a Hyperledger Fabric chaincode invocation to freeze the digital asset.

---

## Demo

Because this is a deterministic CLI, you can simulate a high-risk transaction:

```bash
fraud-engine run --tx examples/transaction.json --workdir out
