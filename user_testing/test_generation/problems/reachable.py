from problems.reachable.breadth_first_search.solution import Solution
import user_testing.test_generation.generation_util as util
from user_testing.test_generation.base_generator import BaseGenerator
from util.enums import GeneralAlgorithm
from typing import override


# Solution instance for reachability
sol = Solution()


# Generator for reachability algorithm tests.
class ReachableGenerator(BaseGenerator):

  @override
  def get_all_test_cases(self) -> list[tuple[list[list[int]], int]]:
    test_cases = self.get_edge_cases()
    for i in range(3, 8):
      self.add_random_variety(test_cases, i, 2)
    for i in range(15, 18):
      self.add_random_variety(test_cases, i, 2)
    for i in range(49, 52):
      self.add_random_variety(test_cases, i, 3)
    for i in range(99, 102):
      self.add_random_variety(test_cases, i, 3)
    self.add_random_variety(test_cases, 250, 3)
    test_cases = self.remove_duplicate_test_cases(test_cases)
    return test_cases
  
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

  def add_random_cases(self, test_cases: list[tuple[list[list[int]], int]], 
                       num_vertices: int, directed: bool, 
                       edge_prob: float, num_cases: int) -> None:
    for _ in range(num_cases):
      test_cases.append(util.rand_graph_and_root(num_vertices, directed, edge_prob))

  def add_random_variety(self, test_cases, num_vertices: int, num_cases: int) -> None:
    edge_probs = None
    if num_vertices < 20:
      edge_probs = [0, 0.3, 0.5, 0.7, 1]
    elif num_vertices < 50:
      edge_probs = [0, 0.1, 0.3, 0.5, 0.7, 0.9, 1]
    else:
      edge_probs = [0, 0.05, 0.15, 0.3, 0.5, 0.7, 0.85, 0.95, 1]
    for directed in [True, False]:
      for edge_prob in edge_probs:
        self.add_random_cases(test_cases, num_vertices, directed, edge_prob, num_cases)
        if edge_prob <= 0.3:
          graph, root = util.rand_graph_and_root(num_vertices, directed, edge_prob)
          util.connect_graph(graph, directed)
          test_cases.append((graph, root))

  def remove_duplicate_test_cases(self, test_cases: list[tuple[list[list[int]], int]]
                                  ) -> list[tuple[list[list[int]], int]]:
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
