from collections import deque

class Solution:
  def solve(self, graph: list[list[int]], root: int) -> set[int]:
    reachable: set[int] = set([root])
    q: deque[int] = deque([root])
    while q:
      curr = q.popleft()
      for neighbor in graph[curr]:
        if neighbor not in reachable:
          reachable.add(neighbor)
          q.append(neighbor)

    return reachable
