package app_tests.java.solution_files;
import java.util.List;
import java.util.Set;

public class Sol24 {
  public static ListNode solve(ListNode input) {
    return input;
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
 