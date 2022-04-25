# Change Making Problem: https://en.wikipedia.org/wiki/Change-making_problem)
# find minimum number of coins of given denominations that add up to a given amount

# lets first solve the closely related coin change problem,
# i.e finding number of ways to change

def enum_ways(coins, amount):
    # print(f"amount: {amount}")
    ways = []
    for c in coins:
        if c == amount:
            ways.append([c])
        elif c < amount:
            # print(f"coin: {c}")
            ways_less_c = enum_ways(coins, amount-c)
            # print(ways_less_c)
            if ways_less_c:
                ways.extend(
                    [w + [c] for w in ways_less_c])
    return ways


import random
ways = enum_ways([1,2,4,8], 15)
print(f"{len(ways)} ways. Sample: {random.sample(ways,10)}")

def test():
    # positive, terminate
    return

