package app_tests.java.solution_files;
import java.util.List;
import java.util.Set;

public class Sol22 {
  public static long solve(ListNode input) {
    long total = 0;
    for (TreeNode[][][] a : input.val) {
      for (TreeNode[][] b : a) {
        for (TreeNode[] c : b) {
          for (TreeNode d : c) {
            total += inorderTraverse(d);
          }
        }
      }
    }
    return total;
  }

  private static long inorderTraverse(TreeNode root) {
    if (root == null) {
      return 0;
    }
    long ret = 0;
    ret += inorderTraverse(root.left);
    for (Set<Boolean> a : root.val) {
      for (Boolean b : a) {
        if (b == true) {
          ret += 1;
        }
      }
    }
    ret += inorderTraverse(root.right);
    return ret;
  }

  public static class ListNode {
    public List<TreeNode[][][]> val;
    public ListNode next;

    public ListNode(List<TreeNode[][][]> val, ListNode next) {
      this.val = val;
      this.next = next;
    }
  }

  public static class TreeNode {
    public Set<Boolean>[] val;
    public TreeNode left;
    public TreeNode right;

    public TreeNode(Set<Boolean>[] val, TreeNode left, TreeNode right) {
      this.val = val;
      this.left = left;
      this.right = right;
    }
  }
}
 