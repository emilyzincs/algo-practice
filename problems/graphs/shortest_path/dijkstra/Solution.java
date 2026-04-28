package problems.graphs.shortest_path.dijkstra;

import java.util.List;
import java.util.PriorityQueue;

// Algorithm: Dijkstra.
// Given a digraph with nonnegative edge weights, returns the minimum
// cost of a path from the start vertex
// to the target vertex, or -1 if there is no path.
public class Solution {
  public long solve(List<List<int[]>> graph, int start, int target) {
    int n = graph.size();
    long[] dists = new long[n];
    for (int i = 0; i < n; i++) {
      dists[i] = Long.MAX_VALUE;
    }
    dists[start] = 0;
    PriorityQueue<long[]> pq = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
    pq.offer(new long[] {0, start});

    while (!pq.isEmpty()) {
      long[] current = pq.poll();
      long dist = current[0];
      int curr = (int) current[1];
      if (dist > dists[curr]) {
        continue;
      }

      if (curr == target) {
        return dist;
      }
      for (int[] neighborWeight : graph.get(curr)) {
        int neighbor = neighborWeight[0];
        int weight = neighborWeight[1];
        long potentialNewDist = dist + weight;
        if (potentialNewDist < dists[neighbor]) {
          dists[neighbor] = potentialNewDist;
          pq.offer(new long[] {potentialNewDist, neighbor});
        }
      }
    }

    return -1;
  }
}