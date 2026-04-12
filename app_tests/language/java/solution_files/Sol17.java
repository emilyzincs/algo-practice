package app_tests.language.java.solution_files;

import java.util.Set;
import java.util.HashSet;

public class Sol17 {
  public static Set<String> solve(Set<String[]> input) {
    Set<String> ret = new HashSet<>();
    for (String[] arr : input) {
      for (String s : arr) {
        ret.add(s);
      }
    }
    return ret;
  }
}
