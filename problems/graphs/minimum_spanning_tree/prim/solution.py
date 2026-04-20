import heapq

class Solution:
  def solve(self, graph: list[list[tuple[int, int]]]) -> int:
    n = len(graph)
    if n == 0:
      return 0
    
    total_mst_weight = 0
    
    processed = [False for _ in range(n)]
    for vertex in range(n):
      total_mst_weight += self.prim(graph, vertex, processed)
    
    if False in processed:
      raise RuntimeError("Did not process all vertices!")
    
    return total_mst_weight

  def prim(self, graph: list[list[tuple[int, int]]], vertex: int,
           processed: list[bool]) -> int: 
    if processed[vertex]:
      return 0
    
    component_mst_weight = 0
    pq = [(0, vertex)]
    while pq:
      weight, curr_vertex = heapq.heappop(pq)
      if processed[curr_vertex]:
        continue

      for neighbor, neighbor_weight in graph[curr_vertex]:
        if curr_vertex != neighbor and not processed[neighbor]:
          heapq.heappush(pq, (neighbor_weight, neighbor))
      processed[curr_vertex] = True
      component_mst_weight += weight
    return component_mst_weight
    