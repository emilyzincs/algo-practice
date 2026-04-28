package problems.graphs.max_flow.ford_fulkerson;

import java.util.ArrayList;
import java.util.List;

// Algorithm: Ford Fulkerson.
// Returns the maximum flow on the given network.
public class Solution {
  private static class Edge {
    int to;
    int cap;
    int rev;

    Edge(int to, int cap, int rev) {
      this.to = to;
      this.cap = cap;
      this.rev = rev;
    }
  }

  public int solve(List<List<int[]>> graph, int s, int t) {
    if (s == t) {
      return 0;
    }

    int n = graph.size();
    List<List<Edge>> adj = new ArrayList<>(n);
    for (int i = 0; i < n; i++) {
      adj.add(new ArrayList<>());
    }

    for (int u = 0; u < n; u++) {
      for (int[] edgeInfo : graph.get(u)) {
        int v = edgeInfo[0];
        int cap = edgeInfo[1];
        int forwardIdx = adj.get(u).size();
        int backwardIdx = adj.get(v).size();
        
        adj.get(u).add(new Edge(v, cap, backwardIdx));
        adj.get(v).add(new Edge(u, 0, forwardIdx));
      }
    }

    int maxFlow = 0;
    int INF = Integer.MAX_VALUE;

    while (true) {
      boolean[] visited = new boolean[n];
      int pathFlow = dfs(s, t, INF, visited, adj);
      if (pathFlow == 0) {
        break;
      }
      maxFlow += pathFlow;
    }

    return maxFlow;
  }

  private int dfs(int u, int t, int flow, boolean[] visited, List<List<Edge>> adj) {
    if (u == t) {
      return flow;
    }

    visited[u] = true;

    for (Edge edge : adj.get(u)) {
      if (!visited[edge.to] && edge.cap > 0) {
        int bottleneck = dfs(edge.to, t, Math.min(flow, edge.cap), visited, adj);

        if (bottleneck > 0) {
          edge.cap -= bottleneck;
          adj.get(edge.to).get(edge.rev).cap += bottleneck;
          return bottleneck;
        }
      }
    }

    return 0;
  }
}