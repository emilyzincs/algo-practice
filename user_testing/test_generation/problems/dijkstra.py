from user_testing.test_generation.base_generator import BaseGenerator
from typing import override
from util.enums import GeneralAlgorithm
from problems.graphs.shortest_path.dijkstra.solution import Solution
from user_testing.test_generation.util.graph_util import (
  WeightedGraph,
  get_weighted_graphs,
  get_rand_vertices
)


sol = Solution()


class DijkstraGenerator(BaseGenerator):
 
  @override
  def get_all_test_cases(self) -> list[tuple[WeightedGraph, int, int]]:
    test_cases = self.get_edge_cases()
    lo, hi = 0, 100
    graphs: list[WeightedGraph] = get_weighted_graphs(
      directed=True, connected=False, lo=lo, hi=hi)
    rand_vertices = get_rand_vertices(graphs, num_rand_vertices=2)
    test_cases.extend([(g, st[0], st[1]) for g, st in zip(graphs, rand_vertices)])
    return test_cases
  
  @override
  def oracle(self, graph: WeightedGraph, start: int, target: int) -> int:
    return sol.solve(graph, start, target)

  @override
  def get_algorithm(self) -> GeneralAlgorithm:
    return GeneralAlgorithm.DIJKSTRA
  
  def get_edge_cases(self) -> list[tuple[WeightedGraph, int, int]]:
    return [
      ([[]], 0, 0),
      ([[(1, 5)], [(0, 5)]], 0, 1),
      ([[(1, 0)], [(0, 0)]], 0, 1),
      ([[(1, 2)], [(0, 2), (2, 3)], [(1, 3)]], 0, 2),
      ([[(1, 1), (2, 4)], [(0, 1), (2, 1)], [(0, 4), (1, 1)]], 0, 2),
      ([[(1, 1)], [(0, 1), (2, 2)], [(1, 2)]], 0, 0),
      ([[(1, 2)], [(0, 2), (2, 1)], [(1, 1)]], 1, 1),
      ([[(1, 3), (2, 1)], [(0, 3), (2, 1)], [(0, 1), (1, 1)]], 0, 2),
      ([[(1, 1), (3, 4)], [(0, 1), (2, 2)], [(1, 2), (3, 1)], [(0, 4), (2, 1)]], 0, 3),
      ([[(0, 5), (1, 10)], [(0, 10)]], 0, 1),
    ]
