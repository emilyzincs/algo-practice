package tests.java.solution_files;
import java.util.Set;
import java.util.ArrayList;
import java.util.List;
import java.util.Collections;

public class Sol20 {
  public static TreeNode solve(Set<String[]> input) {
    List<String> allVals = new ArrayList<>();
    for (String[] currVals : input) {
      for (String val : currVals) {
        allVals.add(val);
      }
    }
    if (allVals.isEmpty()) {
      return null;
    }

    Collections.sort(allVals);
    return new TreeNode(allVals.get(0), 
                new TreeNode(allVals.get(1), 
                  new TreeNode(allVals.get(2), null, null), 
                  new TreeNode(allVals.get(3), null, null)), 
                new TreeNode(allVals.get(4), null, null));
  }

  public static class TreeNode {
    public String val;
    public TreeNode left;
    public TreeNode right;

    public TreeNode(String val, TreeNode left, TreeNode right) {
      this.val = val;
      this.left = left;
      this.right = right;
    }
  }
}
  
  