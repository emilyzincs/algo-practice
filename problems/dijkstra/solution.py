import heapq

class Solution:
  def solve(self, graph: list[list[tuple[int, int]]], start: int, target: int) -> int:
    n = len(graph)
    dists = [float('inf') if vertex != start else 0 for vertex in range(n)]
    pq = [(0, start)]

    while pq:
      dist, curr = heapq.heappop(pq)
      if dist > dists[curr]:
        continue

      if curr == target:
        return dist
      for neighbor, weight in graph[curr]:
        potential_new_dist = dist + weight
        if potential_new_dist < dists[neighbor]:
          dists[neighbor] = potential_new_dist
          heapq.heappush(pq, (potential_new_dist, neighbor))

    return -1
