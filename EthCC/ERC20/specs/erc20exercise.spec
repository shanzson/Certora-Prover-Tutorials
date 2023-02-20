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
    require user1Balance < amount;

    transferFrom@withrevert(e, user1, e.msg.sender, amount); 
    assert lastReverted;
}

// link: https://prover.certora.com/output/49230/5a3386a9a9c44aa4b5af6518edede442?anonymousKey=c22b3d037279b216ded74ec076af56f50306f585

/// if you call transferFrom and do have enough funds, the transaction doesn't revert
rule transferFromDoesntRevert(env e, address user1, address user2, uint256 amount) {
    uint256 user1Balance = balanceOf(user1);
    uint256 user2Balance = balanceOf(user2);
    require user1Balance >= amount;
    require user2 == e.msg.sender;
    require allowance(user1, user2) >= amount;
    require amount != 0;
    require e.msg.value == 0;
    require balanceOf(user2) + amount < max_uint;
    require user1 != 0;
    require user2 != 0;

    transferFrom@withrevert(e, user1, e.msg.sender, amount); 
    assert !lastReverted;
}

// link: https://prover.certora.com/output/49230/916ea7683f784610a324fd460d611a7f?anonymousKey=a4d9b5e242ad0b10d8f76f681cfd738b0404c9fe