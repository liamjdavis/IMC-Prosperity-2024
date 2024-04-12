def bellman_ford(graph, source):
  """
  Implements the Bellman-Ford algorithm.
  """
  V = len(graph)
  distance = [float("inf")] * V
  parent = [-1] * V

  distance[source] = 0
  visited = [False] * V  # Track visited nodes to avoid infinite loop in path reconstruction

  for _ in range(V - 1):
    for u in range(V):
      for v in range(V):
        if distance[u] + graph[u][v] < distance[v] and not visited[v]:
          distance[v] = distance[u] + graph[u][v]
          parent[v] = u
          visited[v] = True  # Mark the visited node

  # Check for negative weight cycles
  for u in range(V):
    for v in range(V):
      if distance[u] + graph[u][v] < distance[v]:
        print("Graph contains negative weight cycle")
        return None  # Indicate negative cycle found

  return distance, parent

def reconstruct_path(parent, destination):
  """
  Reconstructs the shortest path from the source to the destination vertex.

  Args:
      parent: List containing the parent vertex for each vertex in the shortest path tree.
      destination: The destination vertex.

  Returns:
      A list representing the shortest path from source to destination (in reversed order).
  """
  path = []
  current = destination
  while current != -1:
    path.append(current)
    current = parent[current]
  path.reverse()
  return path

def arbitrage_opportunity(currencies, rates, source_currency="seashells"):
  """
  Finds an arbitrage opportunity (profitable currency exchange sequence) using Bellman-Ford.

  Args:
      currencies: List of currency names.
      rates: List of lists representing the exchange rates between currencies.
      source_currency: The starting currency (default: "seashells").

  Prints the arbitrage opportunity details or a message indicating no opportunity found.
  """
  graph = rates
  source_index = currencies.index(source_currency)
  distance, parent = bellman_ford(graph, source_index)

  if distance is None:
    print("Negative weight cycle detected. No valid arbitrage opportunity.")
  elif distance[source_index] == float("inf"):
    print("No arbitrage opportunity found for", source_currency)
  else:
    path = reconstruct_path(parent, source_index)
    print(f"Arbitrage opportunity starting with {source_currency}:")
    for i in range(len(path) - 1):
      print(f"1 {currencies[path[i]]} -> {distance[path[i+1]] * 1:.2f} {currencies[path[i+1]]}")
    print(f"Total gain: {distance[source_index] - 1:.2f} {source_currency}")

# Define currencies and exchange rates
currencies = ["pizza", "wasabi", "snowballs", "seashells"]
rates = [
  [1, 0.48, 1.52, 0.71],
  [2.05, 1, 3.26, 1.56],
  [0.64, 0.3, 1, 0.46],
  [1.41, 0.61, 2.08, 1]
]

# Find arbitrage opportunity starting from seashells
arbitrage_opportunity(currencies, rates)
# no arbitrage opportunities found from seashells to seashells