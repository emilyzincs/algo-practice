#include <vector>
#include <queue>

using std::vector, std::queue;

// Algorithm: Kahn.
class Solution {
 public:
  vector<int> solve(vector<vector<int>>& graph) {
    int n = graph.size();
    vector<int> indegs(n, 0);
    for (const auto& neighbors : graph) {
      for (int nei : neighbors) {
        indegs[nei]++;
      }
    }
    queue<int> q;
    vector<int> ret;

    for (int i = 0; i < n; i++) {
      if (indegs[i] == 0) q.push(i);
    }

    while (!q.empty()) {
      int curr = q.front();
      q.pop();
      ret.push_back(curr);

      for (int nei : graph[curr]) {
        if (--indegs[nei] == 0) {
          q.push(nei);
        }
      }
    }

    return ret;
  }
};
