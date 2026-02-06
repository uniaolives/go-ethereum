# Somnia AI-Agent DeFi Vault v2.0.0 (D-CODE 2.0 / Avalon)

**Live on Somnia DevNet**
An autonomous AI agent that re-balances a two-token DeFi vault, now upgraded to the **D-CODE 2.0** protocol, featuring advanced Avalon state-management and risk-management mechanisms.

## Overview

This project is a complete, deploy-ready AI-agent dApp that demonstrates an autonomous portfolio management system on the Somnia network. The dApp consists of two main components:

1.  **`AgentVault.sol`**: A Solidity smart contract that holds user-deposited assets. Now includes the **Diamond Stability Criterion**, which enforces on-chain safety using Avalon's geometric constraint principles.
2.  **`agent.py`**: An off-chain Python agent refactored using the **D-CODE 2.0** framework. It uses modular components like `Manifold3x3`, `SilentMining`, and `AtomicGesture` to perform rebalancing with high precision and coherence.

## Key Features (D-CODE 2.0)

-   **Manifold 3x3 State Tracking**: The agent now tracks its internal state across Sensorial, Control, and Action axes to maintain high operational coherence.
-   **Silent Mining Protocol**: Optimal rebalancing ratios are "mined" using block-state insights, ensuring a stable and data-driven approach.
-   **Diamond Stability Criterion**: On-chain verification that prevents excessively large or volatile trades, ensuring the vault remains in a stable "Diamond" state.
-   **Atomic Gestures**: Every rebalance is executed as an "irreducible gesture", with metrics tracked in a real-time **Sovereignty Dashboard**.
-   **Quantum Leap Detection**: Significant portfolio adjustments are flagged as "Quantum Leaps" on-chain for transparent governance.

## Quick Start

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/YOUR_NAME/somnia-ai-agent-defi.git
    cd somnia-ai-agent-defi
    ```

2.  **Install Contract Dependencies**:
    ```bash
    cd contracts
    npm install @openzeppelin/contracts
    # Configure foundry.toml remappings if needed
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

## D-CODE 2.0 Protocols

This version implements the following protocols from the Avalon Compendium:
- **PRL Principle**: State exclusion through geometric constraints.
- **Sanctuary Cycles**: Operational rhythms defined by Avalon constants.
- **Sovereignty Dashboard**: Real-time monitoring of field coherence and energy flow.

## Licence

This project is licensed under the MIT License.
