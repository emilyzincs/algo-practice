from user_testing.test_generation.base_generator import BaseGenerator
from typing import override
from util.enums import GeneralAlgorithm
from problems.floyd_warshall.solution import Solution as FloydWarshallSolution
from problems.bellman_ford.solution import Solution as BellmanFordSolution
from user_testing.test_generation.graph_util import (
  WeightedGraph,
  get_weighted_graphs,
)

floyd_warshall_sol = FloydWarshallSolution()
bellman_ford_sol = BellmanFordSolution()


class FloydWarshallGenerator(BaseGenerator):
 
  @override
  def get_all_test_cases(self) -> list[tuple[WeightedGraph, int, int]]:
    test_cases: list[tuple[WeightedGraph, int, int]] = []

    graphs: list[WeightedGraph] = self.get_edge_cases()
    los_and_his = self.get_los_and_his(graphs)
    self.add_graphs_to_test_cases(graphs, test_cases, los_and_his)

    lo, hi = -100, 100
    graphs = (get_weighted_graphs(
      directed=True, connected=False, lo=lo, hi=hi))
    
    los_and_his = [(lo, hi) for _ in range(len(graphs))]
    self.add_graphs_to_test_cases(graphs, test_cases, los_and_his)
    return test_cases
  
  @override
  def oracle(self, graph: WeightedGraph, 
            NEG_INF_SENTINAL: int, INF_SENTINAL: int) -> list[list[int]]:
    n = len(graph)
    if n <= 20:
      dists: list[list[int]] = []
      for vertex in range(n):
        dists.append([])
        for other in range(n):
          dists[vertex].append(bellman_ford_sol.solve(
            graph, vertex, other, NEG_INF_SENTINAL, INF_SENTINAL
          ))
      return dists
    else:
      return floyd_warshall_sol.solve(
        graph, NEG_INF_SENTINAL, INF_SENTINAL)

  @override
  def get_algorithm(self) -> GeneralAlgorithm:
    return GeneralAlgorithm.FLOYD_WARSHALL
  
  def get_edge_cases(self) -> list[WeightedGraph]:
    return [
      [[]],
      [[]],
      [[(1, 5)], [(0, 5)]],
      [[(1, 0)], [(0, 0)]],
      [[(1, -3)], [(0, -3)]],
      [[(1, 2)], [(0, 2), (2, -4)], [(1, -4)]],
      [[(1, 1)], [(2, 1)], [(0, -3)]],
      [[],
       [(2, 1)],
       [(1, -2)]],
      [[(0, -1), (1, 5)], [(0, 5)]],
      [[(1, 2)], [(0, 2)], []],
      [[(1, 10)], [(2, -8)], [(3, 2)], []],
      [[(1, 0)], [(2, 0)], [(0, 0)]],
      [[(1, 5), (1, -2)], [(0, 5), (0, -2)]],
      [[(1, 10**9)], [(0, 10**9)]],
    ]
  
  def get_los_and_his(self, graphs: list[WeightedGraph]) -> list[tuple[int, int]]:
    los_and_his: list[tuple[int, int]] = []
    for graph in graphs:
      N = len(graph) + 1
      weights = [weight for adj in graph for neighbor, weight in adj]
      if not weights:
        los_and_his.append((-1, 1))
      else:
        los_and_his.append((min(weights), max(weights)))
    return los_and_his

  def add_graphs_to_test_cases(
    self, 
    graphs: list[WeightedGraph], 
    test_cases: list[tuple[WeightedGraph, int, int]],
    los_and_his: list[tuple[int, int]],
  ) -> None:
    for i in range(len(graphs)):
      graph = graphs[i]
      lo, hi = los_and_his[i]
      N = len(graph) + 1

      NEG_INF_SENTINAL = min(lo, 0) * N - 1
      INF_SENTINAL = max(hi, 0) * N + 1
      test_cases.append((graph, NEG_INF_SENTINAL, INF_SENTINAL))
