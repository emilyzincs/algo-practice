#include <vector>

using std::vector;

class Solution {
 public:
  static long solve(double f, vector<double> a) {
    double ret = f;
    for (double d : a) {
      ret += d;
    }
    return (long) ret;
  }
};

