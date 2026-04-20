from user_testing.test_generation.base_generator import BaseGenerator
from typing import override
from util.enums import SpecificAlgorithm
from problems.graphs.shortest_path.floyd_warshall.solution import Solution as FloydWarshallSolution
from user_testing.test_generation.oracles.bellman_ford import bellman_ford_oracle
from user_testing.test_generation.util.graph_util import (
  WeightedGraph,
  get_weighted_graphs,
)

floyd_warshall_sol = FloydWarshallSolution()

class Generator(BaseGenerator):
 
  @override
  def get_all_test_cases(self) -> list[tuple[WeightedGraph, int, int]]:
    graphs = self.get_edge_cases()
    los_and_his = self.get_los_and_his(graphs)
    inf_sentinels = self.get_inf_sentinels(graphs, los_and_his)

    lo, hi = -100, 100
    new_graphs = get_weighted_graphs(
      directed=True, connected=False, lo=lo, hi=hi, max_size=60)
    new_los_and_his = [(lo, hi) for _ in range(len(new_graphs))]
    new_inf_sentinels = self.get_inf_sentinels(new_graphs, new_los_and_his)

    graphs.extend(new_graphs)
    inf_sentinels.extend(new_inf_sentinels)

    test_cases = [
      (g, sent[0], sent[1])
      for g, sent in zip(graphs, inf_sentinels)
    ]
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
          dists[vertex].append(bellman_ford_oracle(
            graph, vertex, other, NEG_INF_SENTINAL, INF_SENTINAL
          ))
      return dists
    else:
      return floyd_warshall_sol.solve(
        graph, NEG_INF_SENTINAL, INF_SENTINAL)

  @override
  def get_algorithm(self) -> SpecificAlgorithm:
    return SpecificAlgorithm.FLOYD_WARSHALL
  
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

  def get_inf_sentinels(
    self, 
    graphs: list[WeightedGraph], 
    los_and_his: list[tuple[int, int]],
  ) -> list[tuple[int, int]]:
    sentinels = []
    for i in range(len(graphs)):
      graph = graphs[i]
      lo, hi = los_and_his[i]
      N = len(graph) + 1

      NEG_INF_SENTINAL = min(lo, 0) * N - 1
      INF_SENTINAL = max(hi, 0) * N + 1
      sentinels.append((NEG_INF_SENTINAL, INF_SENTINAL))
    return sentinels
