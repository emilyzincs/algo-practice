from user_testing.test_generation.base_generator import BaseGenerator
from typing import override
from util.enums import GeneralAlgorithm
from problems.minimum_spanning_tree.prim.solution import Solution
from user_testing.test_generation.graph_util import (
  WeightedGraph,
  get_weighted_graphs
)


sol = Solution()


class MinimumSpanningTreeGenerator(BaseGenerator):
 
  @override
  def get_all_test_cases(self) -> list[tuple[WeightedGraph]]:
    unboxed_test_cases = self.get_edge_cases()
    lo, hi = -100, 100
    graphs: list[WeightedGraph] = get_weighted_graphs(
      directed=False, connected=False, lo=lo, hi=hi)
    unboxed_test_cases.extend(graphs)
    return [(graph,) for graph in unboxed_test_cases]
  
  @override
  def oracle(self, graph: WeightedGraph) -> int:
    return sol.solve(graph)

  @override
  def get_algorithm(self) -> GeneralAlgorithm:
    return GeneralAlgorithm.MINIMUM_SPANNING_TREE
  
  def get_edge_cases(self) -> list[WeightedGraph]:
    edge_cases: list[WeightedGraph] = []
    edge_cases.append([])
    edge_cases.append([[]])
    edge_cases.append([[(1, 2)], [(0, 2)]])
    edge_cases.append([[(1, 5), (1, 3)], [(0, 5), (0, 3)]])
    edge_cases.append([[(1, 1)], [(0, 1)], []])
    edge_cases.append([
        [(1, 10), (2, 10)],
        [(0, 10), (2, 10)],
        [(0, 10), (1, 10)]
    ])
    edge_cases.append([
        [(1, -5), (2, 2)],
        [(0, -5), (2, 1)],
        [(0, 2), (1, 1)]
    ])
    edge_cases.append([
        [(1, 0)],
        [(0, 0), (2, 3)],
        [(1, 3)]
    ])
    edge_cases.append([
        [(0, 100), (1, 5)],
        [(0, 5)]
    ])
    huge = 10**9
    edge_cases.append([
        [(1, huge), (2, huge)],
        [(0, huge), (2, huge)],
        [(0, huge), (1, huge)]
    ])
    edge_cases.append([
        [],          
        [(2, 7)],
        [(1, 7)]
    ])
    edge_cases.append([
        [(1, 2)],
        [(0, 2), (2, 3)],
        [(1, 3), (3, 4)],
        [(2, 4)]
    ])
    return edge_cases
