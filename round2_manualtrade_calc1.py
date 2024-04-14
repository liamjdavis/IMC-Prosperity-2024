import numpy as np

def floyd_warshall(currencies, rates):
    num_currencies = len(currencies)
    log_rates = -np.log(rates)

    # Initialize distance and next matrices
    distances = np.copy(log_rates)
    next = np.arange(num_currencies).reshape(-1, 1) * np.ones(num_currencies, dtype=int)

    # Floyd-Warshall
    for k in range(num_currencies):
        for i in range(num_currencies):
            for j in range(num_currencies):
                if distances[i][j] > distances[i][k] + distances[k][j]:
                    distances[i][j] = distances[i][k] + distances[k][j]
                    next[i][j] = next[k][j]

    # Check for negative cycles
    start_index = currencies.index('seashells')  # Start from 'seashells'
    for i in range(num_currencies):
        if i == start_index and distances[i][i] < 0:
            # Reconstruct path
            path = [currencies[start_index]]
            while path[0] != currencies[next[start_index][start_index]]:
                path.insert(0, currencies[next[start_index][start_index]])
            return True, path

    return False, None

currencies = ['pizza', 'wasabi', 'snowballs', 'seashells']
rates = np.array([
    [1, 0.48, 1.52, 0.71],
    [2.05, 1, 3.26, 1.56],
    [0.64, 0.3, 1, 0.46],
    [1.41, 0.61, 2.08, 1]
])

has_arbitrage, path = floyd_warshall(currencies, rates)

if has_arbitrage:
    print(f"Arbitrage opportunity detected: {' -> '.join(path)} -> seashells")
else:
    print("No arbitrage opportunity detected.")