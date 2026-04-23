#include <vector>

using std::vector;

class Solution {
 public:
  long solve(double f, vector<double> a) {
    double ret = f;
    for (double d : a) {
      ret += d;
    }
    return (long) ret;
  }
};

