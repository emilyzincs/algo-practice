from collections import deque

class Solution:
  def solve(self, graph: list[list[int]], root: int) -> set[int]:
    reachable = set()
    seen = [False for vertex in range(len(graph))]
    self.dfs(graph, root, reachable, seen)
    return reachable
  
  def dfs(self, graph: list[list[int]], root: int, 
          reachable: set[int], seen: list[bool]) -> None:
    if root < 0 or len(graph) <= root:
      raise ValueError(f"Root is not a vertex: {root}")
    for neighbor in graph[root]:
      if not seen[neighbor]:
        seen[neighbor] = True
        reachable.add(neighbor)
        self.dfs(graph, neighbor, reachable, seen)
