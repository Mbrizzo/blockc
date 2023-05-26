// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract SimpleToken {
    mapping(address => uint256) balances;

    constructor() {
        balances[msg.sender] = 1000;
    }

    function transfer(address to, uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");

        balances[msg.sender] -= amount;
        balances[to] += amount;
    }

    function getBalance(address account) public view returns (uint256) {
        return balances[account];
    }
}