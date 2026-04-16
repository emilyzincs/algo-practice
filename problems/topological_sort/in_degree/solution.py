class Solution:
  def solve(self, graph: list[list[int]]) -> int:
    n = len(graph)
    in_degrees = [0] * n
    for vertex, neighbors in enumerate(graph):
      for neighbor in neighbors:
        in_degrees[neighbor] += 1
    
    