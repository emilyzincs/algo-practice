package problems.graphs.shortest_path.bellman_ford;

import java.util.List;
import java.util.Arrays;
import java.util.Deque;
import java.util.ArrayDeque;

// Algorithm: Bellman Ford.
// Given a weighted digraph, returns the minimum cost of a path
// from the start vertex to the target vertex.
// (The minimum distance from one vertex to another is defined to be
// infinity (represented by the provided sentinel) if there is no path
// between them, and negative infinity (represented by the provided sentinel)
// if a path between them goes through a negative cycle).
public class Solution {
  public long solve(List<List<int[]>> graph, int start, int target, long NEG_INF_SENTINEL, long INF_SENTINEL) {
    int numVertices = graph.size();
    if (numVertices == 0) return INF_SENTINEL;

    long[] dist = new long[numVertices];
    Arrays.fill(dist, Long.MAX_VALUE);
    dist[start] = 0;

    boolean[] inQueue = new boolean[numVertices];
    int[] relaxationCount = new int[numVertices];

    Deque<Integer> queue = new ArrayDeque<>();
    queue.addLast(start);
    inQueue[start] = true;

    while (!queue.isEmpty()) {
      int u = queue.pollFirst();
      inQueue[u] = false;

      List<int[]> edges = graph.get(u);
      if (edges != null) {
        for (int[] edge : edges) {
          int v = edge[0];
          int weight = edge[1];

          if (dist[u] != Long.MAX_VALUE && dist[u] + (long) weight < dist[v]) {
            dist[v] = dist[u] + weight;

            if (!inQueue[v]) {
              relaxationCount[v]++;

              // Negative cycle detected
              if (relaxationCount[v] >= numVertices) {
                // Check if this cycle can actually reach the target
                if (reachesTarget(graph, v, target)) {
                  return NEG_INF_SENTINEL;
                } else {
                  // If it doesn't reach target, we continue but stop 
                  // exploring this specific path to avoid infinite loops
                  continue;
                }
              }

              // Small SPFA optimization (SLF - Small Label First)
              if (!queue.isEmpty() && dist[v] < dist[queue.peekFirst()]) {
                queue.addFirst(v);
              } else {
                queue.addLast(v);
              }
              inQueue[v] = true;
            }
          }
        }
      }
    }

    if (dist[target] == Long.MAX_VALUE) {
      return INF_SENTINEL;
    }
    return dist[target];
  }

  private boolean reachesTarget(List<List<int[]>> graph, int startNode, int target) {
    int numVertices = graph.size();
    boolean[] visited = new boolean[numVertices];
    Deque<Integer> q = new ArrayDeque<>();
    q.addLast(startNode);
    visited[startNode] = true;

    while (!q.isEmpty()) {
      int u = q.pollFirst();
      if (u == target) return true;
      List<int[]> edges = graph.get(u);
      if (edges != null) {
        for (int[] edge : edges) {
          int v = edge[0];
          if (!visited[v]) {
            visited[v] = true;
            q.addLast(v);
          }
        }
      }
    }
    return false;
  }
}