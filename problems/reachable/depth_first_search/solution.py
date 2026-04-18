class Solution:
  def solve(self, graph: list[list[int]], root: int) -> set[int]:
    def dfs(graph: list[list[int]], root: int, reachable: set[int]):
      for neighbor in graph[root]:
        if neighbor not in reachable:
          reachable.add(neighbor)
          dfs(graph, neighbor, reachable)

    reachable: set[int] = set([root])
    dfs(graph, root, reachable)
    return reachable
