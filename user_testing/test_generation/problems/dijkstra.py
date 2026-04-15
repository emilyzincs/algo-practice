from user_testing.test_generation.base_generator import BaseGenerator
from user_testing.test_generation.problems.reachable import ReachableGenerator
from typing import override
from util.enums import GeneralAlgorithm
from problems.dijkstra.solution import Solution
import random


reachable_generator = ReachableGenerator()
sol = Solution()


class DijkstraGenerator(BaseGenerator):

  # TODO: factor out getting weighted/unweighted graph cases (at scale) to generation_util
  # and use that instead
  # weighted, unweighted, connected, directed
  @override
  def get_all_test_cases(self) -> list[tuple[list[list[tuple[int, float]]], int]]:
    test_cases: list[tuple[list[list[tuple[int, float]]], int]] = []
    reachable_tests: list[tuple[list[list[int]], int]] = (
      reachable_generator.get_all_test_cases()
    )
    for unweighted_graph, start in reachable_tests:
      weighted_graph = []
      for neighbor_list in unweighted_graph:
        weighted_graph.append([(vertex, random.uniform(0, 100)) for vertex in neighbor_list])
      test_cases.append((weighted_graph, start))
    return test_cases
  
  @override
  def oracle(self, graph, start):
    return sol.solve(graph, start)

  @override
  def get_algorithm(self) -> GeneralAlgorithm:
    return GeneralAlgorithm.DIJKSTRA
