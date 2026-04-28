package problems.graphs.minimum_spanning_tree.prim;

import java.util.*;

public class Solution {
  public int solve(List<List<int[]>> graph) {
    int n = graph.size();
    if (n == 0) {
      return 0;
    }

    long totalMSTWeight = 0;

    boolean[] processed = new boolean[n];
    for (int vertex = 0; vertex < n; vertex++) {
      totalMSTWeight += prim(graph, vertex, processed);
    }

    for (boolean b : processed) {
      if (!b) {
        throw new RuntimeException("Did not process all vertices!");
      }
    }

    if (totalMSTWeight > Integer.MAX_VALUE) {
      throw new RuntimeException("MST weight overflow");
    }
    return (int) totalMSTWeight;
  }

  private long prim(List<List<int[]>> graph, int vertex, boolean[] processed) {
    if (processed[vertex]) {
      return 0;
    }

    long componentMSTWeight = 0;
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> a[0] - b[0]);
    pq.add(new int[] {0, vertex});
    while (!pq.isEmpty()) {
      int[] entry = pq.poll();
      int weight = entry[0];
      int currVertex = entry[1];
      if (processed[currVertex]) {
        continue;
      }

      for (int[] neighbor : graph.get(currVertex)) {
        if (currVertex != neighbor[0] && !processed[neighbor[0]]) {
          pq.add(new int[] {neighbor[1], neighbor[0]});
        }
      }
      processed[currVertex] = true;
      componentMSTWeight += weight;
    }
    return componentMSTWeight;
  }
}