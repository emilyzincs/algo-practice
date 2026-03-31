package tests.practice_run_tests.java.solution_files;
import java.util.Set;
import java.util.ArrayList;
import java.util.Collections;

public class Sol20 {
  public static TreeNode solve(Set<int[]> input) {
    ArrayList<Integer> allVals = new ArrayList<>();
    for (int[] currVals : input) {
      for (int val : currVals) {
        allVals.add(val);
      }
    }

    Collections.sort(allVals);
    return new TreeNode(allVals.get(0), 
                new TreeNode(allVals.get(1), 
                  new TreeNode(allVals.get(2), null, null), 
                  new TreeNode(allVals.get(3), null, null)), 
                new TreeNode(allVals.get(4), null, null));
  }

  public static class TreeNode {
    public int val;
    public TreeNode left;
    public TreeNode right;

    public TreeNode(int val, TreeNode left, TreeNode right) {
      this.val = val;
      this.left = left;
      this.right = right;
    }
  }
}
  
  