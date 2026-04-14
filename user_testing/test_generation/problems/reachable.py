from problems.reachable.breadth_first_search.solution import Solution
import user_testing.test_generation.generation_util as util
from user_testing.test_generation.base_generator import BaseGenerator
from util.enums import GeneralAlgorithm
from typing import override


# Solution instance for reachability
sol = Solution()


# Generator for reachability algorithm tests.
class ReachableGenerator(BaseGenerator):

  # Builds the complete list of test cases for reachability.
  #
  # Returns:
  #   A list of (graph, root) tuples covering edge cases, random graphs
  #   of various sizes and densities, and connectedness variations.
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
    test_cases = self.remove_redundant_test_cases(test_cases)
    return test_cases
  
  # Oracle function that returns the list of reachable vertices from root using 'sol'.
  #
  # Parameters:
  # - graph: Adjacency list representation of the graph.
  # - root: Starting vertex index.
  #
  # Returns:
  #   List of vertices reachable from root (order may vary).
  @override
  def oracle(self, graph: list[list[int]], root: int) -> list[int]:
    return list(sol.solve(graph, root))
  
  @override
  def get_algorithm(self) -> GeneralAlgorithm:
    return GeneralAlgorithm.REACHABLE

  # Returns a list of edge-case test inputs for reachability.
  #
  # Returns:
  #   List of (graph, root) tuples covering small graphs and edge cases.
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

  # Appends a specified number of random test cases to the given list.
  #
  # Parameters:
  # - test_cases: List to extend.
  # - n: Number of vertices.
  # - directed: Whether the graph is directed.
  # - edge_prob: Probability of an edge.
  # - num_cases: Number of test cases to add.
  def add_random_cases(self, test_cases: list[tuple[list[list[int]], int]], 
                       n: int, directed: bool, 
                       edge_prob: float, num_cases: int) -> None:
    for _ in range(num_cases):
      test_cases.append(util.rand_graph_and_root(n, directed, edge_prob))

  # Adds a variety of random test cases for a given size, covering different edge probabilities and both directed/undirected.
  # Also adds cases where the graph is forcibly connected for low edge probabilities.
  #
  # Parameters:
  # - test_cases: List to extend.
  # - n: Number of vertices.
  # - num_cases: Number of random cases per configuration.
  def add_random_variety(self, test_cases, n: int, num_cases: int) -> None:
    edge_probs = None
    if n < 20:
      edge_probs = [0, 0.3, 0.5, 0.7, 1]
    elif n < 50:
      edge_probs = [0, 0.1, 0.3, 0.5, 0.7, 0.9, 1]
    else:
      edge_probs = [0, 0.05, 0.15, 0.3, 0.5, 0.7, 0.85, 0.95, 1]
    for directed in [True, False]:
      for edge_prob in edge_probs:
        self.add_random_cases(test_cases, n, directed, edge_prob, num_cases)
        if edge_prob <= 0.3:
          graph, root = util.rand_graph_and_root(n, directed, edge_prob)
          util.connect_graph(graph)
          test_cases.append((graph, root))

  # Removes duplicate test cases (identical graph structure and root) 
  # and sorts by graph size.
  #
  # Parameters:
  # - test_cases: List of (graph, root) tuples with possible duplicates.
  #
  # Returns:
  #   A new list with duplicates removed, sorted by number of vertices.
  def remove_redundant_test_cases(self, test_cases: list[tuple[list[list[int]], int]]
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
