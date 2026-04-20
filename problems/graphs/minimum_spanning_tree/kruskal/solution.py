import heapq
from typing import List, Tuple

class Solution:
  def solve(self, graph: List[List[Tuple[int, int]]]) -> int:
    num_vertices = len(graph)
    if num_vertices <= 1:
      return 0

    edges = []
    for vertex in range(num_vertices):
      for neighbor, weight in graph[vertex]:
        if neighbor < vertex:
          edges.append((weight, vertex, neighbor))

    edges.sort(key=lambda x: x[0])

    parent = list(range(num_vertices))
    rank = [0] * num_vertices

    def find(element: int) -> int:
      while parent[element] != element:
        parent[element] = parent[parent[element]]
        element = parent[element]
      return element

    def union(first_member: int, second_member: int) -> bool:
      first = find(first_member)
      second = find(second_member)
      if first == second:
        return False
      if rank[first] < rank[second]:
        parent[first] = second
      elif rank[first] > rank[second]:
        parent[second] = first
      else:
        parent[second] = first
        rank[first] += 1
      return True

    total_weight = 0
    for weight, vertex, neighbor in edges:
      if union(vertex, neighbor):
        total_weight += weight
    return total_weight