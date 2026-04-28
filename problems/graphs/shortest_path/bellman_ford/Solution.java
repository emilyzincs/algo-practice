package problems.graphs.shortest_path.bellman_ford;

import java.util.*;

public class Solution {
  public int solve(List<List<int[]>> graph, int start, int target, int NEG_INF_SENTINEL, int INF_SENTINEL) {
    int numVertices = graph.size();
    if (numVertices == 0) return INF_SENTINEL;

    double[] dist = new double[numVertices];
    Arrays.fill(dist, Double.POSITIVE_INFINITY);
    dist[start] = 0;

    boolean[] inQueue = new boolean[numVertices];
    int[] relaxationCount = new int[numVertices];
    boolean hasNegativeCycleToTarget = false;

    Deque<Integer> queue = new ArrayDeque<>();
    queue.offer(start);
    inQueue[start] = true;

    while (!queue.isEmpty()) {
      int u = queue.poll();
      inQueue[u] = false;

      for (int[] edge : graph.get(u)) {
        int v = edge[0];
        int weight = edge[1];

        if (dist[u] != Double.POSITIVE_INFINITY && dist[u] + weight < dist[v]) {
          dist[v] = dist[u] + weight;

          if (!inQueue[v]) {
            relaxationCount[v]++;

            if (relaxationCount[v] >= numVertices) {
              if (reachesTarget(graph, v, target)) {
                return NEG_INF_SENTINEL;
              } else {
                continue;
              }
            }

            if (!queue.isEmpty() && dist[v] < dist[queue.peekFirst()]) {
              queue.offerFirst(v);
            } else {
              queue.offer(v);
            }
            inQueue[v] = true;
          }
        }
      }
    }

    return finalizeDistance(dist, target, INF_SENTINEL);
  }

  private boolean reachesTarget(List<List<int[]>> graph, int startNode, int target) {
    Set<Integer> visited = new HashSet<>();
    Deque<Integer> queue = new ArrayDeque<>();
    queue.offer(startNode);
    visited.add(startNode);

    while (!queue.isEmpty()) {
      int u = queue.poll();

      if (u == target) return true;

      for (int[] edge : graph.get(u)) {
        int v = edge[0];

        if (!visited.contains(v)) {
          visited.add(v);
          queue.offer(v);
        }
      }
    }

    return false;
  }

  private int finalizeDistance(double[] distance, int target, int INF_SENTINEL) {
    double d = distance[target];

    if (d == Double.POSITIVE_INFINITY) {
      return INF_SENTINEL;
    }

    return (int) d;
  }
}