from problems.connected_components.tarjan.solution import Solution

from user_testing.test_generation.graph_util import (
  UnweightedGraph,
  get_unweighted_graphs,
  get_graphs_with_rand_vertices
)
from user_testing.test_generation.base_generator import BaseGenerator
from util.enums import GeneralAlgorithm
from typing import override, cast


# Solution instance for reachability
sol = Solution()


# Generator for reachability algorithm tests.
class TarjanGenerator(BaseGenerator):

  @override
  def get_all_test_cases(self) -> list[tuple[UnweightedGraph]]:
    test_cases = self.get_edge_cases()
    graphs: list[UnweightedGraph] = get_unweighted_graphs(
      directed=True, connected=False)
    test_cases.extend(get_graphs_with_rand_vertices(graphs, num_rand_vertices=0)) 
    return self.remove_duplicate_test_cases(test_cases)
  
  @override
  def oracle(self, graph: list[list[int]]) -> set[set[int]]:
    return sol.solve(graph)
  
  @override
  def get_algorithm(self) -> GeneralAlgorithm:
    return GeneralAlgorithm.REACHABLE

  def get_edge_cases(self) -> list[tuple[UnweightedGraph]]:
    return [
      ([[]],),
      ([[0]],),
      ([[1], []],),
      ([[1], [0]],),
      ([[0], [1]],),
      ([[0, 1], [0]],),
      ([[0, 1], [0, 1]],),
      ([[1], [0, 1]],),
      ([[0], [0, 1]],),
    ]

  def remove_duplicate_test_cases(self, test_cases: list[tuple[UnweightedGraph]]
                                  ) -> list[tuple[UnweightedGraph]]:
    hashable_cases = []
    for case in test_cases:
      graph = case[0]
      graph_tuple = tuple(tuple(adj_list) for adj_list in graph)
      hashable_cases.append(graph_tuple)

    unique_cases = list(set(hashable_cases))
    unique_cases.sort(key=lambda x: len(x))

    return [( [list(adj_list) for adj_list in g], ) for g in unique_cases]
