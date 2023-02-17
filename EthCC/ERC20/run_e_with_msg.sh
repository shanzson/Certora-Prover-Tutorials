if [[ "$1" ]]
then
    RULE="--rule $1"
fi

certoraRun contracts/ERC20.sol:ERC20 \
    --verify ERC20:specs/erc20exercise.spec \
    --cloud \
    --optimistic_loop \
    --loop_iter 1 \
    $RULE \
    --send_only \
    --msg "ERC20_exercise: My 3rd exercise"
