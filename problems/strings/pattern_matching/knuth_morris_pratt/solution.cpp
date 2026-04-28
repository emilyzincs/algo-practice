#include <string>
#include <vector>

using std::string, std::vector;

// Algorithm: Knuth Morris Pratt.
// Returns the start indices, in any order, of all occurrences
// of the given pattern in the text.
class Solution {
 public:
  vector<int> solve(string text, string pattern) {
    int n = text.length(), m = pattern.length();
    if (m == 0) return {};

    vector<int> lps(m, 0);
    int length = 0;
    int i = 1;

    while (i < m) {
      if (pattern[i] == pattern[length]) {
        length += 1;
        lps[i] = length;
        i += 1;
      } else {
        if (length != 0) {
          length = lps[length - 1];
        } else {
          lps[i] = 0;
          i += 1;
        }
      }
    }

    vector<int> indices;
    i = 0;
    int j = 0;

    while (i < n) {
      if (pattern[j] == text[i]) {
        i += 1;
        j += 1;
      }

      if (j == m) {
        indices.push_back(i - j);
        j = lps[j - 1];
      } else if (i < n && pattern[j] != text[i]) {
        if (j != 0) {
          j = lps[j - 1];
        } else {
          i += 1;
        }
      }
    }
    return indices;
  }
};