// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract Pract1 {

    mapping (address => uint256) balances;

    event Paid(address _from, uint _amount);

    struct Person {
        address userAddress;
        uint256 balance;
    }

    function pay() public payable {
        emit Paid(msg.sender, msg.value);
        balances[msg.sender] += msg.value;
    }

    function getBalance() public view returns(uint) {
        return balances[msg.sender];
    }
   
    function withdraw(uint _amount) public payable {
        if (_amount <= balances[msg.sender]) {
        require(_amount > 0, "amount must be not zero value");
        payable(msg.sender).transfer(_amount);
        balances[msg.sender] -= _amount;
        }
    }
}