from user_testing.test_generation.base_generator import BaseGenerator
from typing import override
from util.enums import GeneralAlgorithm
from problems.bellman_ford.solution import Solution
from user_testing.test_generation.graph_util import (
  WeightedGraph,
  get_weighted_graphs,
  get_graphs_with_rand_vertices
)


sol = Solution()


class BellmanFordGenerator(BaseGenerator):
 
  @override
  def get_all_test_cases(self) -> list[tuple[WeightedGraph, int, int, int, int]]:
    unpadded_test_cases = self.get_edge_cases()
    lo, hi = -100, 100
    graphs: list[WeightedGraph] = get_weighted_graphs(
      directed=True, connected=False, lo=lo, hi=hi)
    unpadded_test_cases.extend(
      get_graphs_with_rand_vertices(graphs, num_rand_vertices=2))
    
    test_cases = []
    for graph, start, target in unpadded_test_cases:
      N = len(graph) + 1
      NEG_INF_SENTINAL = lo * N - 1
      INF_SENTINAL = hi * N + 1
      test_cases.append((graph, start, target, NEG_INF_SENTINAL, INF_SENTINAL))
    return test_cases
  
  @override
  def oracle(self, graph: WeightedGraph, start: int, target: int, 
            NEG_INF_SENTINAL: int, INF_SENTINAL: int) -> int:
    return sol.solve(graph, start, target, NEG_INF_SENTINAL, INF_SENTINAL)

  @override
  def get_algorithm(self) -> GeneralAlgorithm:
    return GeneralAlgorithm.BELLMAN_FORD
  
  def get_edge_cases(self) -> list[tuple[WeightedGraph, int, int]]:
    return [
      ([[]], 0, 0),
      ([[]], 0, 0),
      ([[(1, 5)], [(0, 5)]], 0, 1),
      ([[(1, 0)], [(0, 0)]], 0, 1),
      ([[(1, -3)], [(0, -3)]], 0, 1),
      ([[(1, 2)], [(0, 2), (2, -4)], [(1, -4)]], 0, 2),
      ([[(1, 1)], [(2, 1)], [(0, -3)]], 0, 2),
      ([[],
        [(2, 1)],
        [(1, -2)]], 0, 1),
      ([[(0, -1), (1, 5)], [(0, 5)]], 0, 1),
      ([[(1, 2)], [(0, 2)], []], 0, 2),
      ([[(1, 10)], [(2, -8)], [(3, 2)], []], 0, 3),
      ([[(1, 0)], [(2, 0)], [(0, 0)]], 0, 2),
      ([[(1, 5), (1, -2)], [(0, 5), (0, -2)]], 0, 1),
      ([[(1, 10**9)], [(0, 10**9)]], 0, 1),
    ]
