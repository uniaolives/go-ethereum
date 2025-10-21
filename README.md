# Somnia AI-Agent DeFi Vault v1.5.0

**Live on Somnia DevNet**
An autonomous AI agent that re-balances a two-token DeFi vault every 5 minutes, now with on-chain risk management via a **Novelty Score**.

## Overview

This project is a complete, deploy-ready AI-agent dApp that demonstrates an autonomous portfolio management system on the Somnia network. The dApp consists of two main components:

1.  **`AgentVault.sol`**: A Solidity smart contract that holds user-deposited assets and allows an authorized AI agent to rebalance its token composition.
2.  **`agent.py`**: An off-chain Python agent that calculates an optimal token ratio and autonomously calls the smart contract to execute the rebalance.

This upgraded version (1.5.0) introduces a **Novelty Score**, an on-chain risk-management mechanism that prevents the AI agent from making excessively volatile or risky trades.

## Key Features

-   **Autonomous Rebalancing**: The Python agent runs in a continuous loop, automatically adjusting the vault's token ratio every 5 minutes.
-   **On-Chain Risk Management**: The `rebalance` function now requires a `noveltyScore`, which is the absolute difference between the current and proposed token ratios. The transaction will revert if this score exceeds a pre-defined `maxNoveltyScore`, providing a crucial safeguard against extreme market volatility or flawed agent logic.
-   **User-Controlled Liquidity**: Users can deposit and withdraw assets from the vault at any time, maintaining full control over their funds.
-   **Deploy-Ready**: The entire system is packaged with Docker and includes simple CLI commands for quick deployment on the Somnia DevNet.

## Quick Start

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/YOUR_NAME/somnia-ai-agent-defi.git
    cd somnia-ai-agent-defi
    ```

2.  **Install Contract Dependencies**:
    ```bash
    cd contracts
    forge install
    ```

3.  **Deploy the `AgentVault` Contract**:
    ```bash
    export RPC=https://devnet.somnia.network
    export PK=<YOUR_PRIVATE_KEY>

    forge create --rpc-url $RPC --private-key $PK \
                 src/AgentVault.sol:AgentVault \
                 --constructor-args 0xSTT_ADDRESS 0xDAI_ADDRESS 5000 \
                 --legacy
    ```
    *(Replace `0xSTT_ADDRESS` and `0xDAI_ADDRESS` with the actual token addresses on Somnia DevNet)*

4.  **Run the AI Agent**:
    Set the required environment variables:
    ```bash
    export VAULT_ADDR=<YOUR_DEPLOYED_VAULT_ADDRESS>
    export PK=<YOUR_PRIVATE_KEY>
    export RPC=https://devnet.somnia.network
    ```
    Build and run the Docker container:
    ```bash
    docker build -t somnia-agent .
    docker run -e PK -e RPC -e VAULT_ADDR somnia-agent
    ```

## How the Novelty Score Works

The Novelty Score is a simple but powerful mechanism to enforce on-chain governance over the AI agent's behavior.

1.  **Off-Chain Calculation**: The Python agent first reads the `ratioA` currently stored in the `AgentVault` contract.
2.  **Score Computation**: It then calculates its desired `newRatio` and computes the `noveltyScore` as `abs(newRatio - current_ratio)`.
3.  **On-Chain Verification**: The agent calls the `rebalance(newRatio, noveltyScore)` function. The smart contract internally recalculates the novelty score and verifies two things:
    -   The score provided by the agent is correct.
    -   The score is less than or equal to `maxNoveltyScore` (hardcoded to 10% in the contract).
4.  **Execution**: If both checks pass, the rebalance is executed. Otherwise, the transaction reverts, protecting the vault from drastic changes.

## Licence

This project is licensed under the MIT License.
