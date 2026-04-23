package app_tests.language.java.solution_files;

import java.util.List;
import java.util.ArrayList;

public class Sol14 {
  public List<List<Boolean>> solve(List<boolean[]> input) {
    List<List<Boolean>> ret = new ArrayList<>();
    for (boolean[] arr : input) {
      List<Boolean> curr = new ArrayList<>();
      for (boolean b : arr)
        curr.add(b);
      ret.add(curr);
    }
    return ret;
  }
}
