package problems.graphs.topological_sort.kahn;

import java.util.*;

// Algorithm: Kahn.
// Returns the unique topological ordering of the given DAG
// matching this algorithm (see solution for exact implementation).
public class Solution {
  public List<Integer> solve(List<List<Integer>> graph) {
    int n = graph.size();
    int[] indegree = new int[n];
    for (int u = 0; u < n; u++) {
      for (int v : graph.get(u)) {
        indegree[v]++;
      }
    }

    Queue<Integer> q = new LinkedList<>();
    for (int u = 0; u < n; u++) {
      if (indegree[u] == 0) {
        q.add(u);
      }
    }
    List<Integer> topo = new ArrayList<>();

    while (!q.isEmpty()) {
      int u = q.poll();
      topo.add(u);
      for (int v : graph.get(u)) {
        indegree[v]--;
        if (indegree[v] == 0) {
          q.add(v);
        }
      }
    }

    if (topo.size() != n) {
      throw new RuntimeException("Graph contains a cycle.");
    }
    return topo;
  }
}