// erc20 methods
methods {
    balanceOf(address)                    returns (uint256) envfree
    transfer(address,uint256)             returns (bool)

    allowance(address,address)            returns (uint256) envfree
    transferFrom(address,address,uint256) returns (bool)
    approve(address,uint256)              returns (bool)
}

/**** Exercises ****/

/// if you call transferFrom and the transaction doesn't revert, your balance decreases and recipient's balance increases
rule transferFromSpec(env e, address recipient, uint256 amount) {
    require e.msg.sender != recipient;
    uint256 myBalance = balanceOf(e.msg.sender);
    uint256 recipientBalance = balanceOf(recipient);

    transferFrom(e, e.msg.sender, recipient, amount);

    uint256 myBalanceAfter = balanceOf(e.msg.sender);
    uint256 recipientBalanceAfter = balanceOf(recipient);
    
    assert myBalanceAfter == myBalance - amount;
    assert recipientBalanceAfter == recipientBalance + amount;
}

// link: https://prover.certora.com/output/49230/9e2a588d21484614bcca81cc316d739b?anonymousKey=7fe2efe5fff84e83f72144937b1f3934dd1a5e3e

/// if you call transferFrom and you don't have the funds, the transaction reverts
rule transferFromReverts(env e, address user1, address user2, uint256 amount) {

    uint256 user1Balance = balanceOf(user1);
    require user1Balance <= amount;

    transferFrom@withrevert(e, user1, e.msg.sender, amount); 
    assert lastReverted;
}

// link: https://prover.certora.com/output/49230/3a2cfaf1e2544d67b3f22f0ce8c3ba73?anonymousKey=44abb16652269c43805aa62ff8b3309b4d12bcf1

/// if you call transferFrom and do have enough funds, the transaction doesn't revert
rule transferFromDoesntRevert(env e, address recipient, uint256 amount) {
    uint256 myBalance = balanceOf(e.msg.sender);
    uint256 myAllowance = allowance(e.msg.sender,recipient);
    
    require myBalance >= amount;
    require e.msg.value == 0;

    transferFrom@withrevert(e, e.msg.sender, recipient, amount); 

    assert !lastReverted;
}
