def bellman_ford_oracle(graph, start, target, neg_inf, pos_inf):
  n = len(graph)
  dist = [float('inf')] * n
  dist[start] = 0
  
  # Standard V-1 relaxations
  for _ in range(n - 1):
    for u in range(n):
      for v, w in graph[u]:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
          dist[v] = dist[u] + w
          
  # Check if any edge can still be relaxed
  for u in range(n):
    for v, w in graph[u]:
      if dist[u] != float('inf') and dist[u] + w < dist[v]:
        # If this edge is part of/reachable from a negative cycle,
        # see if it can reach the target.
        if _can_reach(graph, v, target):
          return neg_inf
          
  return int(dist[target]) if dist[target] != float('inf') else pos_inf

def _can_reach(graph, start_node, target):
  visited = {start_node}
  stack = [start_node]
  while stack:
    u = stack.pop()
    if u == target: return True
    for v, _ in graph[u]:
      if v not in visited:
        visited.add(v)
        stack.append(v)
  return False