package problems.strings.pattern_matching.knuth_morris_pratt;

import java.util.List;
import java.util.ArrayList;

// Algorithm: Knuth Morris Pratt.
// Returns the start indices, in any order, of all occurrences
// of the given pattern in the text.
public class Solution {
  public List<Integer> solve(String text, String pattern) {
    int n = text.length();
    int m = pattern.length();
    if (m == 0) return new ArrayList<>();

    int[] lps = computeLPS(pattern);
    List<Integer> indices = new ArrayList<>();
    int i = 0;
    int j = 0;

    while (i < n) {
      if (pattern.charAt(j) == text.charAt(i)) {
        i++;
        j++;
      }

      if (j == m) {
        indices.add(i - j);
        j = lps[j - 1];
      } else if (i < n && pattern.charAt(j) != text.charAt(i)) {
        if (j != 0) {
          j = lps[j - 1];
        } else {
          i++;
        }
      }
    }
    return indices;
  }

  private int[] computeLPS(String pattern) {
    int m = pattern.length();
    int[] lps = new int[m];
    int length = 0;
    int i = 1;

    while (i < m) {
      if (pattern.charAt(i) == pattern.charAt(length)) {
        length++;
        lps[i] = length;
        i++;
      } else {
        if (length != 0) {
          length = lps[length - 1];
        } else {
          lps[i] = 0;
          i++;
        }
      }
    }
    return lps;
  }
}