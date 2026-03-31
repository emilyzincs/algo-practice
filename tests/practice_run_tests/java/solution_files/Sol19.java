package tests.practice_run_tests.java.solution_files;

public class Sol19 {
  public static TreeNode solve(TreeNode root) {
    if (root == null) return null;
    return root.right;
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
  