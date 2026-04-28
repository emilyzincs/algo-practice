#include <vector>
#include <algorithm>

using std::vector;

// Algorithm: Tarjan.
// Returns the strongly connected components of the given digraph
// in any order.
class Solution {
 public:
  vector<vector<int>> solve(vector<vector<int>>& graph) {
    int n = graph.size();
    int index = 0;
    vector<int> indices(n, -1);
    vector<int> lowlink(n, 0);
    vector<bool> on_stack(n, false);
    vector<int> stack;
    vector<vector<int>> sccs;

    for (int v = 0; v < n; v++) {
      if (indices[v] == -1) {
        strongconnect(v, graph, index, indices, lowlink, on_stack, stack, sccs);
      }
    }

    return sccs;
  }

 private:
  void strongconnect(int v, const vector<vector<int>>& graph, int& index,
                     vector<int>& indices, vector<int>& lowlink,
                     vector<bool>& on_stack, vector<int>& stack,
                     vector<vector<int>>& sccs) {
    indices[v] = index;
    lowlink[v] = index;
    index++;
    stack.push_back(v);
    on_stack[v] = true;

    for (int w : graph[v]) {
      if (indices[w] == -1) {
        strongconnect(w, graph, index, indices, lowlink, on_stack, stack, sccs);
        lowlink[v] = std::min(lowlink[v], lowlink[w]);
      } else if (on_stack[w]) {
        lowlink[v] = std::min(lowlink[v], indices[w]);
      }
    }

    if (lowlink[v] == indices[v]) {
      vector<int> scc;
      while (true) {
        int w = stack.back();
        stack.pop_back();
        on_stack[w] = false;
        scc.push_back(w);
        if (w == v) break;
      }
      sccs.push_back(scc);
    }
  }
};