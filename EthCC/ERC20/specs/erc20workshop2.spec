// erc20 methods
methods {
    balanceOf(address)                    returns (uint256) envfree
    transfer(address,uint256)             returns (bool)

    allowance(address,address)            returns (uint256) envfree
    transferFrom(address,address,uint256) returns (bool)
    approve(address,uint256)              returns (bool)
}

/**** Parametric examples ****/

/// The caller of `approve` must be the owner of the tokens involved.

rule onlyOwnerCanApprove {
    env e;
    address owner;
    address spender;
    uint256 amount;

    uint256 allowanceBefore = allowance(owner, spender);

    approve(e, spender, amount);

    uint256 allowanceAfter = allowance(owner, spender);

    assert allowanceBefore != allowanceAfter => owner == e.msg.sender,
        "The caller of `approve` must be the owner of the tokens involved";
}

/// The caller of a function which changes an allowance must be the owner of the tokens involved.

rule onlyOwnerCanChangeAllowance {
    method f;
    env e;
    calldataarg args;
    address owner;
    address spender;

    uint256 allowanceBefore = allowance(owner, spender);

    f(e, args);

    uint256 allowanceAfter = allowance(owner, spender);

    assert allowanceBefore != allowanceAfter => owner == e.msg.sender,
        "The caller of a function which changes an allowance must be the owner 
        of the tokens involved";
}

/// The caller of a function which increases an allowance must be the owner of the tokens involved.

rule onlyOwnerCanIncreaseAllowance {
    method f;
    env e;
    calldataarg args;
    address owner;
    address spender;

    uint256 allowanceBefore = allowance(owner, spender);

    f(e, args);

    uint256 allowanceAfter = allowance(owner, spender);

    assert allowanceBefore < allowanceAfter => owner == e.msg.sender,
        "The caller of a function which increases an allowance must be the 
        owner of the tokens involved";
}


/// A user's allowance must change only as a result of calls to `approve`, `transferFrom`, `increaseAllowance` or `decreaseAllowance`.

rule onlyCertainMethodsChangeAllowances {
    method f;
    env e;
    calldataarg args;
    address owner;
    address spender;

    uint256 allowanceBefore = allowance(owner, spender);

    f(e, args);

    uint256 allowanceAfter = allowance(owner, spender);    

    assert allowanceBefore != allowanceAfter => 
        (f.selector == approve(address, uint256).selector ||
         f.selector == transferFrom(address, address, uint256).selector ||
         f.selector == increaseAllowance(address, uint256).selector ||
         f.selector == decreaseAllowance(address, uint256).selector),
         "A user's allowance must change only as a result of calls to 
         `approve`, `transferFrom`, `increaseAllowance` or `decreaseAllowance`";
}

/// Without a call to `approve`, `transferFrom`, `increaseAllowance` or `decreaseAllowance`, a user's allowance must not change.

rule withoutCertainMethodsAllowancesDontChange(method f)
filtered {
    f -> f.selector != approve(address, uint).selector
      && f.selector != transferFrom(address, address, uint256).selector
      && f.selector != increaseAllowance(address, uint256).selector
      && f.selector != decreaseAllowance(address, uint256).selector
}
{
    env e;
    calldataarg args;
    address owner;
    address spender;

    uint256 allowanceBefore = allowance(owner, spender);

    f(e, args);

    uint256 allowanceAfter = allowance(owner, spender);    

    assert allowanceBefore == allowanceAfter,
        "Without a call to `approve`, `transferFrom`, `increaseAllowance` or 
        `decreaseAllowance`, a user's allowance must not change";
}

/**** Exercises ****/

/// We have been considering the question: If there is a change in `allowance`, 
/// what else must necessarily be the case?

/// Now consider the question: If there is a change in token balance, what else 
/// must necessarily be the case?

/// Using what we’ve learned, write some parametric rules to test whether the 
/// contract is functioning as it should.


