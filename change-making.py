# Change Making Problem: https://en.wikipedia.org/wiki/Change-making_problem)
# find minimum number of coins of given denominations that add up to a given amount

# lets first solve the closely related coin change problem,
# i.e finding number of ways to change


def coin_change(coins, amount):

    assert amount > 0, f"amount not positive: {amount}"
    assert (len(coins) == len(set(coins))), f"denominations not distinct:{coins}"
    for c in coins:
        assert type(c) is int, "denomination not integer: {c}"
        assert c > 0, f"denomination not possitive: {c}"

    coins.sort()
    ways = recurse(coins,amount)
    assert len(ways) == len(set([tuple(sorted(w, reverse=True)) for w in ways])),\
        f"{len(ways)} ways including all orders."

    return ways

def recurse(coins, amount):
    """ Assume coins are sorted increasing order and unique """
    ways = []
    # print(f"coins={coins}, amount={amount}")
    largest = coins[-1]
    if largest <= amount:
        # pick largest
        if largest == amount:
            ways.append([largest])
        ways.extend([w + [largest] for w in  recurse(coins,amount-largest)])
    # drop largest
    if len(coins) > 1:
        ways.extend(recurse(coins[:-1],amount))
    return ways

import random
ways = coin_change([1,2,4,8,16], 32)
print(f"{len(ways)} ways. Sample: {random.sample(list(ways),10)}")

def test():
    # positive, terminate
    return
