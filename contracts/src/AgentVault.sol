// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

/// @notice Vault whose **off-chain AI agent** can rebalance between
///         two ERC-20 tokens on Somnia (e.g. STT / DAI).
contract AgentVault is Ownable {
    IERC20 public immutable TOKEN_A; // e.g. STT
    IERC20 public immutable TOKEN_B; // e.g. DAI

    uint256 public ratioA;   // basis-points 0-10_000
    uint256 public constant BP = 10_000;
    uint256 public maxNoveltyScore; // e.g. 1000 bp = 10%

    event Rebalanced(uint256 newRatioA, uint256 noveltyScore, uint256 amtA, uint256 amtB);

    constructor(address _a, address _b, uint256 _initialRatioA) {
        TOKEN_A = IERC20(_a);
        TOKEN_B = IERC20(_b);
        ratioA  = _initialRatioA;
        maxNoveltyScore = 1000; // 10% max change
    }

    /// @dev AI agent calls this after off-chain optimisation.
    function rebalance(uint256 _newRatioA, uint256 _noveltyScore) external onlyOwner {
        require(_newRatioA <= BP, "bad ratio");

        uint256 novelty = _newRatioA > ratioA ? _newRatioA - ratioA : ratioA - _newRatioA;
        require(novelty == _noveltyScore, "AgentVault: invalid novelty score");
        require(_noveltyScore <= maxNoveltyScore, "AgentVault: novelty score too high");

        uint256 balA = TOKEN_A.balanceOf(address(this));
        uint256 balB = TOKEN_B.balanceOf(address(this));
        uint256 total = balA + balB;
        require(total > 0, "empty");

        uint256 targetA = (total * _newRatioA) / BP;
        uint256 targetB = total - targetA;

        // atomic re-balancing via swap (dummy for demo)
        if (targetA > balA) {
            uint256 buyA = targetA - balA;
            TOKEN_B.transferFrom(msg.sender, address(this), buyA);
            // swap buyA → TOKEN_A (integrate Somnia DEX later)
        } else if (targetA < balA) {
            uint256 sellA = balA - targetA;
            TOKEN_A.transfer(msg.sender, sellA);
        }
        ratioA = _newRatioA;
        emit Rebalanced(_newRatioA, _noveltyScore, targetA, targetB);
    }

    /// User deposits equal value of A + B
    function deposit(uint256 amtA, uint256 amtB) external {
        TOKEN_A.transferFrom(msg.sender, address(this), amtA);
        TOKEN_B.transferFrom(msg.sender, address(this), amtB);
    }

    /// User withdraws proportional share
    function withdraw(uint256 share) external {
        uint256 balA = TOKEN_A.balanceOf(address(this));
        uint256 balB = TOKEN_B.balanceOf(address(this));
        uint256 outA = (balA * share) / BP;
        uint256 outB = (balB * share) / BP;
        TOKEN_A.transfer(msg.sender, outA);
        TOKEN_B.transfer(msg.sender, outB);
    }
}