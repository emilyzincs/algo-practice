from problems.graphs.topological_sort.kahn.solution import Solution

from user_testing.test_generation.util.graph_util import (
  UnweightedGraph,
  get_unweighted_graphs,
  digraph_to_dag
)
from user_testing.test_generation.base_generator import BaseGenerator
from util.enums import GeneralAlgorithm
from typing import override


# Solution instance for reachability
sol = Solution()


# Generator for reachability algorithm tests.
class TopologicalSortGenerator(BaseGenerator):

  @override
  def get_all_test_cases(self) -> list[tuple[UnweightedGraph]]:
    test_cases = self.get_edge_cases()
    graphs: list[UnweightedGraph] = get_unweighted_graphs(
      directed=True, connected=False)
    dags: list[UnweightedGraph] = [digraph_to_dag(graph) for graph in graphs]
    test_cases.extend([(g,) for g in dags])
    return self.remove_duplicate_test_cases(test_cases)
  
  @override
  def oracle(self, graph: list[list[int]]) -> list[int]:
    return list(sol.solve(graph))
  
  @override
  def get_algorithm(self) -> GeneralAlgorithm:
    return GeneralAlgorithm.TOPOLOGICAL_SORT

  def get_edge_cases(self) -> list[tuple[UnweightedGraph]]:
    return [
      ([],),
      ([[]],),
      ([[], []],),
      ([[1], []],),
      ([[1], [2], []],),
      ([[1, 2], [3], [3], []],),
      ([[], [2], []],),
      ([[1, 2], [3], [3], [4], []],),
      ([[1], [2], [3], []],),
      ([[1, 2, 3], [], [], []],),
      ([[1], [2], [3], [4], []],),
      ([[1, 2, 3, 4], [], [], [], []],),
      ([[1], [2], [3], [4], [5], []],),
      ([[1, 2, 3, 4, 5], [], [], [], [], []],),
      ([[], [0], [0, 1]],),
      ([[1, 2, 3], [4], [4], [4], []],),
      ([[1], [2, 3], [4], [4], []],),
      ([[1], [2], [3, 4], [5], [5], []],),
      ([[1, 3], [2], [], [4], []],),
    ]

  def remove_duplicate_test_cases(self, test_cases: list[tuple[UnweightedGraph]]
                                  ) -> list[tuple[UnweightedGraph]]:
    hashable_cases = []
    for graph, in test_cases:
      graph_tuple = tuple(tuple(adj_list) for adj_list in graph)
      hashable_cases.append((graph_tuple,))
    
    unique_cases = list(set(hashable_cases))
    unique_cases.sort(key=lambda x: len(x[0]))

    return [
      ([list(adj_list) for adj_list in g],)
      for g, in unique_cases
    ]
