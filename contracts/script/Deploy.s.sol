// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;
import "../src/AgentVault.sol";
import "forge-std/Script.sol";

contract Deploy is Script {
    function run() external {
        vm.startBroadcast();
        // Somnia DevNet STT / mock DAI (create if needed)
        address STT  = 0xEeeeeEeeeeEeeeeEeeeeEeeeeEeeeeEeeeeEeeeeEeeeeEeeeeEeeeeE; // placeholder
        address DAI  = 0xDA100000000000000000000000000000000000000000000000000000000000000;
        AgentVault vault = new AgentVault(STT, DAI, 5000); // 50 % A / 50 % B
        console.log("AgentVault deployed at:", address(vault));
        vm.stopBroadcast();
    }
}