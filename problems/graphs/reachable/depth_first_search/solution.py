class Solution:
  def solve(self, graph: list[list[int]], root: int) -> list[int]:
    reachable: list[int] = []
    seen = [False for vertex in range(len(graph))]
    seen[root] = True
    self.dfs(graph, root, reachable, seen)
    return reachable
  
  def dfs(self, graph: list[list[int]], root: int, 
          reachable: list[int], seen: list[bool]) -> None:
    reachable.append(root)
    for neighbor in graph[root]:
      if not seen[neighbor]:
        seen[neighbor] = True
        self.dfs(graph, neighbor, reachable, seen)
