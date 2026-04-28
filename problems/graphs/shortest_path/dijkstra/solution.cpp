#include <vector>
#include <queue>
#include <limits>

using std::vector;
using std::priority_queue;
using std::numeric_limits;

// Algorithm: Dijkstra.
// Given a digraph with nonnegative edge weights, returns the minimum
// cost of a path from the start vertex
// to the target vertex, or -1 if there is no path.
class Solution {
 public:
  long solve(vector<vector<vector<int>>>& graph, int start, int target) {
    int n = graph.size();
    vector<long> dists(n, numeric_limits<long>::max());
    dists[start] = 0;

    priority_queue<vector<long>, vector<vector<long>>, std::greater<vector<long>>> pq;
    pq.push({0, static_cast<long>(start)});

    while (!pq.empty()) {
      long dist = pq.top()[0];
      int curr = pq.top()[1];
      pq.pop();
      if (dist > dists[curr]) {
        continue;
      }

      if (curr == target) {
        return dist;
      }
      for (const auto& edge : graph[curr]) {
        int neighbor = edge[0];
        long weight = edge[1];
        long potential_new_dist = dist + weight;
        if (potential_new_dist < dists[neighbor]) {
          dists[neighbor] = potential_new_dist;
          pq.push({potential_new_dist, static_cast<long>(neighbor)});
        }
      }
    }

    return -1;
  }
};