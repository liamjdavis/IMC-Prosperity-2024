def dfs(node, amount, start, maxdepth=10):
    if node == start and len(path) > 1:
        if amount > 1:
            print(f"Arbitrage opportunity: {path} with gain: {amount}")
        return
    if len(path) > maxdepth:
        return
    for neighbour in rates[node]:
        rate = rates[node][neighbour]
        if neighbour not in path:
            path.append(neighbour)
            dfs(neighbour, amount * rate, start, maxdepth)
            path.pop()

currencies = ['pizza', 'wasabi', 'snowballs', 'seashells']
rates = {
    'pizza': {'pizza': 1, 'wasabi': 0.48, 'snowballs': 1.52, 'seashells': 0.71},
    'wasabi': {'pizza': 2.05, 'wasabi': 1, 'snowballs': 3.26, 'seashells': 1.56},
    'snowballs': {'pizza': 0.64, 'wasabi': 0.3, 'snowballs': 1, 'seashells': 0.46},
    'seashells': {'pizza': 1.41, 'wasabi': 0.61, 'snowballs': 2.08, 'seashells': 1}
}

for currency in currencies:
    path = [currency]
    dfs(currency, 1, currency)