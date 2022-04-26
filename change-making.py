# Change Making Problem: https://en.wikipedia.org/wiki/Change-making_problem)
# find minimum number of coins of given denominations that add up to a given amount

# lets first solve the closely related coin change problem,
# i.e finding number of ways to change

def _enum_ways(coins, amount):

    # print(f"amount: {amount}")
    ways = []
    for c in coins:
        if c == amount:
            ways.append([c])
        elif c < amount:
            # print(f"coin: {c}")
            ways_less_c = _enum_ways(coins, amount-c)
            # print(ways_less_c)
            if ways_less_c:
                ways.extend(
                    [w + [c] for w in ways_less_c])

    return ways

def coin_change(coins, amount):
    coins.sort()
    ways = _enum_sorted(coins,amount)
    print(f"{len(ways)} ways including all orders.")
    ## remove duplicates
    return set([tuple(sorted(w, reverse=True)) for w in ways])

def _enum_sorted(coins, amount):
    """ Assume coins are sorted increasing order and unique """
    ways = []
    print(f"coins={coins}, amount={amount}")
    largest = coins[-1]
    if largest <= amount:
        # pick largest
        if largest == amount:
            ways.append([largest])
        ways.extend([w + [largest] for w in  _enum_sorted(coins,amount-largest)])
    # drop largest
    if len(coins) > 1:
        ways.extend(_enum_sorted(coins[:-1],amount))
    return ways

import random
ways = coin_change([1,2,4,8], 15)
print(f"{len(ways)} ways. Sample: {random.sample(list(ways),10)}")

def test():
    # positive, terminate
    return
