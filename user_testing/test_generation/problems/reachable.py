from problems.reachable.breadth_first_search.solution import Solution

from user_testing.test_generation.graph_util import (
  UnweightedGraph,
  get_unweighted_graphs,
  get_graphs_with_rand_vertex
)
from user_testing.test_generation.base_generator import BaseGenerator
from util.enums import GeneralAlgorithm
from typing import override


# Solution instance for reachability
sol = Solution()


# Generator for reachability algorithm tests.
class ReachableGenerator(BaseGenerator):

  @override
  def get_all_test_cases(self) -> list[tuple[UnweightedGraph, int]]:
    test_cases = self.get_edge_cases()
    graphs: list[UnweightedGraph] = get_unweighted_graphs(
      directed=True, connected=False)
    test_cases.extend(get_graphs_with_rand_vertex(graphs))
    return self.remove_duplicate_test_cases(test_cases)
  
  @override
  def oracle(self, graph: list[list[int]], root: int) -> list[int]:
    return list(sol.solve(graph, root))
  
  @override
  def get_algorithm(self) -> GeneralAlgorithm:
    return GeneralAlgorithm.REACHABLE

  def get_edge_cases(self) -> list[tuple[list[list[int]], int]]:
    return [
      ([[]], 0),
      ([[0]], 0),
      ([[1], []], 1),
      ([[1], [0]], 1),
      ([[0], [1]], 1),
      ([[0, 1], [0]], 1),
      ([[0, 1], [0, 1]], 1),
      ([[1], [0, 1]], 1),
      ([[0], [0, 1]], 1),
    ]

  def remove_duplicate_test_cases(self, test_cases: list[tuple[UnweightedGraph, int]]
                                  ) -> list[tuple[UnweightedGraph, int]]:
    hashable_cases = []
    for graph, root in test_cases:
      graph_tuple = tuple(tuple(adj_list) for adj_list in graph)
      hashable_cases.append((graph_tuple, root))
    
    unique_cases = list(set(hashable_cases))
    unique_cases.sort(key=lambda x: len(x[0]))

    return [
      ([list(adj_list) for adj_list in g], r)
      for g, r in unique_cases
    ]
