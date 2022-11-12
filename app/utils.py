def coin_change(amount: int, denominations=[5, 10, 20, 50, 100]) -> list:
    goal = 0
    change = []
    denominations_sorted = sorted(denominations)[::-1]
    ix = 0
    while True:
        denom = denominations_sorted[ix]
        if (amount - goal) - denom < 0:
            ix += 1
            continue
        goal += denom
        change.append(denom)
        if sum(change) == amount:
            break
    return change
