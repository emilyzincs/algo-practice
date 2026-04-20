from collections import deque

class Solution:
  def solve(self, graph: list[list[int]]) -> list[int]:
    n = len(graph)
    indegree = [0] * n
    for u in range(n):
      for v in graph[u]:
        indegree[v] += 1

    q = deque([u for u in range(n) if indegree[u] == 0])
    topo = []

    while q:
      u = q.popleft()
      topo.append(u)
      for v in graph[u]:
        indegree[v] -= 1
        if indegree[v] == 0:
          q.append(v)

    if len(topo) != n:
      raise RuntimeError("Graph contains a cycle.")
    return topo