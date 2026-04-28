package problems.graphs.shortest_path.dijkstra;

import java.util.*;

// Algorithm: Dijkstra.
// Given a digraph with nonnegative edge weights, returns the minimum
// cost of a path from the start vertex
// to the target vertex, or -1 if there is no path.
public class Solution {
  public int solve(List<List<int[]>> graph, int start, int target) {
    int n = graph.size();
    int[] dists = new int[n];
    Arrays.fill(dists, Integer.MAX_VALUE);
    dists[start] = 0;
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
    pq.offer(new int[] {0, start});

    while (!pq.isEmpty()) {
      int[] curr = pq.poll();
      int dist = curr[0];
      int vertex = curr[1];
      if (dist > dists[vertex]) {
        continue;
      }

      if (vertex == target) {
        return dist;
      }
      for (int[] neighbor : graph.get(vertex)) {
        int weight = neighbor[1];
        int newDist = dist + weight;
        if (newDist < dists[neighbor[0]]) {
          dists[neighbor[0]] = newDist;
          pq.offer(new int[] {newDist, neighbor[0]});
        }
      }
    }

    return -1;
  }
}