from problems.connected_components.tarjan.solution import Solution

from user_testing.test_generation.util.graph_util import (
  UnweightedGraph,
  get_unweighted_graphs,
)
from user_testing.test_generation.base_generator import BaseGenerator
from util.enums import GeneralAlgorithm
from typing import override, cast


# Solution instance for reachability
sol = Solution()


# Generator for reachability algorithm tests.
class ConnectedComponentsGenerator(BaseGenerator):

  @override
  def get_all_test_cases(self) -> list[tuple[UnweightedGraph]]:
    test_cases = self.get_edge_cases()
    graphs: list[UnweightedGraph] = get_unweighted_graphs(
      directed=True, connected=False)
    test_cases.extend((graph,) for graph in graphs) 
    return self.remove_duplicate_test_cases(test_cases)
  
  @override
  def oracle(self, graph: list[list[int]]) -> list[list[int]]:
    components: set[frozenset[int]] = sol.solve(graph)
    return [list(component) for component in components]

  
  @override
  def get_algorithm(self) -> GeneralAlgorithm:
    return GeneralAlgorithm.CONNECTED_COMPONENTS

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
