#include <vector>
#include <deque>
#include <stdexcept>

using std::vector;
using std::deque;

// Algorithm: Breadth First Search.
// Returns the reachable vertices from the given vertex
// in the given digraph, in any order.
class Solution {
 public:
  vector<int> solve(vector<vector<int>>& graph, int root) {
    vector<int> reachable;
    vector<bool> seen(graph.size(), false);
    deque<int> q;
    q.push_back(root);
    seen[root] = true;
    while (!q.empty()) {
      int curr = q.front();
      q.pop_front();
      reachable.push_back(curr);
      for (int neighbor : graph[curr]) {
        if (neighbor < 0 || neighbor >= graph.size()) {
          throw std::invalid_argument("Neighbor is not a vertex: " + std::to_string(neighbor));
        }
        if (!seen[neighbor]) {
          q.push_back(neighbor);
          seen[neighbor] = true;
        }
      }
    }
    return reachable;
  }
};