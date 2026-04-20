from user_testing.test_generation.base_generator import BaseGenerator
from typing import override
from util.enums import GeneralAlgorithm
from problems.graphs.max_flow.ford_fulkerson.solution import Solution
from user_testing.test_generation.util.graph_util import (
  WeightedGraph,
  get_weighted_graphs,
)
import random


sol = Solution()


class MaxFlowGenerator(BaseGenerator):
 
  @override
  def get_all_test_cases(self) -> list[tuple[WeightedGraph, int, int]]:
    test_cases = self.get_edge_cases()
    lo, hi = 0, 20
    graphs: list[WeightedGraph] = get_weighted_graphs(
      directed=True, connected=True, lo=lo, hi=hi)

    for graph in graphs:
      n = len(graph)
      vertices: list[int] = list(range(n))
      graph.extend([[], []])
      s, t = n, n + 1
      num_src_edges = min(random.randint(1, 15), n)
      num_sink_edges = min(random.randint(1, 15), n)
      src_neighbors = random.sample(vertices, num_src_edges)
      sink_neighbors = random.sample(vertices, num_sink_edges)
      CAPACITY_MULTIPLIER = 1.5
      for src_neighbor in src_neighbors:
        graph[s].append((src_neighbor, 
             random.randint(lo, int(hi * CAPACITY_MULTIPLIER))))
      for sink_neighbor in sink_neighbors:
        graph[sink_neighbor].append((t, 
             random.randint(lo, int(hi * CAPACITY_MULTIPLIER))))
      test_cases.append((graph, s, t))

    return test_cases
  
  @override
  def oracle(self, graph: WeightedGraph, start: int, target: int) -> int:
    return sol.solve(graph, start, target)

  @override
  def get_algorithm(self) -> GeneralAlgorithm:
    return GeneralAlgorithm.MAX_FLOW
  
  def get_edge_cases(self) -> list[tuple[WeightedGraph, int, int]]:
    cases = []

    graph1: WeightedGraph = [[], []]
    cases.append((graph1, 0, 1))
    
    graph2 = [[(1, 10)], []]
    cases.append((graph2, 0, 1))

    graph3 = [[(1, 5)], [(2, 3)], []]
    cases.append((graph3, 0, 2))

    graph4 = [[(1, 10), (2, 5)], [(3, 6)], [(3, 8)], []]
    cases.append((graph4, 0, 3))

    graph5 = [[(1, 0)], [(2, 5)], []]
    cases.append((graph5, 0, 2))

    graph6 = [[(1, 10)], [], []]
    cases.append((graph6, 0, 2))

    graph7 = [[(1, 5), (1, 3)], [(2, 7)], []]
    cases.append((graph7, 0, 2))

    return cases 
