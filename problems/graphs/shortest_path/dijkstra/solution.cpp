#include <vector>
#include <queue>
#include <limits>
#include <functional>
#include <utility>

using std::vector, std::priority_queue, std::pair;

// Algorithm: Dijkstra.
class Solution {
 public:
  int solve(vector<vector<vector<int>>>& graph, int start, int target) {
    int n = graph.size();
    vector<int> dists(n, std::numeric_limits<int>::max());
    dists[start] = 0;

    priority_queue<pair<int, int>, vector<pair<int, int>>, 
        std::greater<pair<int, int>>> pq;
    pq.push({0, start});

    while (!pq.empty()) {
      auto [d, v] = pq.top();
      pq.pop();

      if (d > dists[v]) continue;
      if (v == target) return d;

      for (const auto& nei_and_weight : graph[v]) {
        int nei = nei_and_weight[0], weight = nei_and_weight[1];
        int dist = d + weight;
        if (dist < dists[nei]) {
          dists[nei] = dist;
          pq.push({dist, nei});
        }
      }
    }
    return -1;
  }
};
