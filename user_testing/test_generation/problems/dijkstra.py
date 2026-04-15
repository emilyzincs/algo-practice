from user_testing.test_generation.base_generator import BaseGenerator
from typing import override
from util.enums import GeneralAlgorithm
from problems.dijkstra.solution import Solution
from user_testing.test_generation.graph_util import (
  WeightedGraph,
  get_weighted_graphs,
  get_graphs_with_rand_vertices
)


sol = Solution()


class DijkstraGenerator(BaseGenerator):
 
  @override
  def get_all_test_cases(self) -> list[tuple[WeightedGraph, int, int]]:
    test_cases = self.get_edge_cases()
    lo, hi = 0, 100
    graphs: list[WeightedGraph] = get_weighted_graphs(
      directed=True, connected=True, lo=lo, hi=hi)
    test_cases.extend(get_graphs_with_rand_vertices(graphs, num_rand_vertices=2))
    return test_cases
  
  @override
  def oracle(self, graph, start):
    return sol.solve(graph, start)

  @override
  def get_algorithm(self) -> GeneralAlgorithm:
    return GeneralAlgorithm.DIJKSTRA
  
  def get_edge_cases(self) -> list[tuple[WeightedGraph, int, int]]:
    return []
