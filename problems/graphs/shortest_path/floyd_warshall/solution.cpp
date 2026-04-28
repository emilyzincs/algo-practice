#include <vector>
#include <limits>
#include <stdexcept>

using std::vector;
using std::numeric_limits;

class Solution {
 public:
  vector<vector<long>> solve(vector<vector<vector<int>>>& graph, long NEG_INF_SENTINEL, long INF_SENTINEL) {
    if (graph.empty()) {
      throw std::invalid_argument("Graph is empty");
    }

    int n = graph.size();
    vector<vector<long>> dist(n, vector<long>(n, INF_SENTINEL));

    for (int i = 0; i < n; ++i) {
      dist[i][i] = 0;
      for (const auto& edge : graph[i]) {
        dist[i][edge[0]] = std::min(dist[i][edge[0]], static_cast<long>(edge[1]));
      }
    }

    for (int k = 0; k < n; ++k) {
      for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
          if (dist[i][k] != INF_SENTINEL && dist[k][j] != INF_SENTINEL) {
            long new_dist = dist[i][k] + dist[k][j];
            if (new_dist < dist[i][j]) {
              dist[i][j] = new_dist;
            }
          }
        }
      }
    }

    for (int k = 0; k < n; ++k) {
      if (dist[k][k] < 0) {
        for (int i = 0; i < n; ++i) {
          for (int j = 0; j < n; ++j) {
            if (dist[i][k] != INF_SENTINEL && dist[k][j] != INF_SENTINEL) {
              dist[i][j] = NEG_INF_SENTINEL;
            }
          }
        }
      }
    }

    return dist;
  }
};