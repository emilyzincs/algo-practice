from user_testing.test_generation.base_generator import BaseGenerator
from typing import override, cast
from util.enums import SpecificAlgorithm
from user_testing.test_generation.oracles.bellman_ford import bellman_ford_oracle
from user_testing.test_generation.util.graph_util import (
  WeightedGraph,
  get_weighted_graphs,
  get_rand_vertices
)


class BellmanFordGenerator(BaseGenerator):
 
  @override
  def get_all_test_cases(self) -> list[tuple[WeightedGraph, int, int, int, int]]:
    edge_cases: list[tuple[WeightedGraph, tuple[int, int]]] = self.get_edge_cases()
    graphs, starts_and_targets = map(list, zip(*edge_cases))
    graphs = cast(list[WeightedGraph], graphs)
    starts_and_targets = cast(list[tuple[int, int]], starts_and_targets)

    los_and_his = self.get_los_and_his(graphs)
    inf_sentinels = self.get_inf_sentinels(graphs, los_and_his)

    lo, hi = -100, 100
    new_graphs = get_weighted_graphs(
      directed=True, connected=False, lo=lo, hi=hi)
    new_los_and_his = [(lo, hi) for _ in range(len(new_graphs))]
    new_inf_sentinels = self.get_inf_sentinels(new_graphs, new_los_and_his)
    new_starts_and_targets = get_rand_vertices(new_graphs, num_rand_vertices=2)

    graphs.extend(new_graphs)
    inf_sentinels.extend(new_inf_sentinels)
    starts_and_targets.extend(new_starts_and_targets) # type: ignore

    test_cases = [
      (g, st[0], st[1], sent[0], sent[1])
      for g, st, sent in zip(graphs, starts_and_targets, inf_sentinels)
    ]
    return test_cases
  
  @override
  def oracle(self, graph: WeightedGraph, start: int, target: int, 
            NEG_INF_SENTINAL: int, INF_SENTINAL: int) -> int:
    return bellman_ford_oracle(graph, start, target, NEG_INF_SENTINAL, INF_SENTINAL)

  @override
  def get_algorithm(self) -> SpecificAlgorithm:
    return SpecificAlgorithm.BELLMAN_FORD
  
  def get_edge_cases(self) -> list[tuple[WeightedGraph, tuple[int, int]]]:
    return [
      ([[]], (0, 0)),
      ([[]], (0, 0)),
      ([[(1, 5)], [(0, 5)]], (0, 1)),
      ([[(1, 0)], [(0, 0)]], (0, 1)),
      ([[(1, -3)], [(0, -3)]], (0, 1)),
      ([[(1, 2)], [(0, 2), (2, -4)], [(1, -4)]], (0, 2)),
      ([[(1, 1)], [(2, 1)], [(0, -3)]], (0, 2)),
      ([[],
        [(2, 1)],
        [(1, -2)]], (0, 1)),
      ([[(0, -1), (1, 5)], [(0, 5)]], (0, 1)),
      ([[(1, 2)], [(0, 2)], []], (0, 2)),
      ([[(1, 10)], [(2, -8)], [(3, 2)], []], (0, 3)),
      ([[(1, 0)], [(2, 0)], [(0, 0)]], (0, 2)),
      ([[(1, 5), (1, -2)], [(0, 5), (0, -2)]], (0, 1)),
      ([[(1, 10**9)], [(0, 10**9)]], (0, 1)),
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
