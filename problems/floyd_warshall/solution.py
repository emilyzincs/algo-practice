class Solution:
  def solve(
    self,
    graph: list[list[tuple[int, int]]],
    NEG_INF_SENTINAL: int,
    INF_SENTINAL: int
  ) -> list[list[int]]:
    n = len(graph)
    
    dist = [[INF_SENTINAL] * n for _ in range(n)]
    
    for i in range(n):
      dist[i][i] = 0
      for neighbor, weight in graph[i]:
        dist[i][neighbor] = min(dist[i][neighbor], weight)

    for k in range(n):
      for i in range(n):
        for j in range(n):
          if dist[i][k] != INF_SENTINAL and dist[k][j] != INF_SENTINAL:
            new_dist = dist[i][k] + dist[k][j]
            if new_dist < dist[i][j]:
              dist[i][j] = new_dist

    for k in range(n):
      if dist[k][k] < 0:
        for i in range(n):
          for j in range(n):
            if dist[i][k] != INF_SENTINAL and dist[k][j] != INF_SENTINAL:
              dist[i][j] = NEG_INF_SENTINAL

    return dist