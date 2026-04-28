package problems.graphs.shortest_path.floyd_warshall;

import java.util.List;

// Algorithm: Floyd Warshall.
// Given a weighted digraph with n vertices,
// returns an n by n matrix m where m[i][j]
// is the minimum cost of a path from vertex i to vertex j.
// (The minimum distance from one vertex to another is defined to be
// infinity (represented by the provided sentinel) if there is no path
// between them, and negative infinity (represented by the provided sentinel)
// if a path between them goes through a negative cycle).
public class Solution {
  public List<List<Long>> solve(List<List<int[]>> graph, long NEG_INF_SENTINEL, long INF_SENTINEL) {
    int n = graph.size();
    long[][] dist = new long[n][n];
    for (int i = 0; i < n; i++) {
      for (int j = 0; j < n; j++) {
        dist[i][j] = INF_SENTINEL;
      }
    }

    for (int i = 0; i < n; i++) {
      dist[i][i] = 0;
      for (int[] edge : graph.get(i)) {
        int neighbor = edge[0];
        long weight = edge[1];
        dist[i][neighbor] = Math.min(dist[i][neighbor], weight);
      }
    }

    for (int k = 0; k < n; k++) {
      for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
          if (dist[i][k] != INF_SENTINEL && dist[k][j] != INF_SENTINEL) {
            long newDist = dist[i][k] + dist[k][j];
            if (newDist < dist[i][j]) {
              dist[i][j] = newDist;
            }
          }
        }
      }
    }

    for (int k = 0; k < n; k++) {
      if (dist[k][k] < 0) {
        for (int i = 0; i < n; i++) {
          for (int j = 0; j < n; j++) {
            if (dist[i][k] != INF_SENTINEL && dist[k][j] != INF_SENTINEL) {
              dist[i][j] = NEG_INF_SENTINEL;
            }
          }
        }
      }
    }

    List<List<Long>> result = new java.util.ArrayList<>();
    for (long[] row : dist) {
      List<Long> longRow = new java.util.ArrayList<>();
      for (long val : row) {
        longRow.add(val);
      }
      result.add(longRow);
    }
    return result;
  }
}