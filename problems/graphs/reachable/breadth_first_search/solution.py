from collections import deque

class Solution:
  def solve(self, graph: list[list[int]], root: int) -> list[int]:
    reachable = []
    seen = [False for vertex in range(len(graph))]
    q: deque[int] = deque()
    q.append(root)
    seen[root] = True
    while q:
      curr = q.popleft()
      reachable.append(curr)
      for neighbor in graph[curr]:
        if neighbor < 0 or len(graph) <= neighbor:
          raise ValueError(f"Neighbor is not a vertex: {neighbor}")
        if not seen[neighbor]:
          q.append(neighbor)
          seen[neighbor] = True
    return reachable
