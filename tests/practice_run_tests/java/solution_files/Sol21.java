package tests.practice_run_tests.java.solution_files;
import java.util.Map;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.List;

public class Sol21 {
  private static ListNode dummy;
  private static ListNode back;

  public static Map<double[], List<ListNode>> solve(Map<double[][], List<TreeNode>> input) {
    Map<double[], List<ListNode>> ret = new HashMap<>();
    for (double[][] k : input.keySet()) {
      List<TreeNode> v = input.get(k);
      double[] new_k = new double[k.length];
      for (int i = 0; i < k.length; i++) {
        for (double num : k[i]) new_k[i] += num;
      }
      List<ListNode> new_v = new ArrayList<>();
      for (TreeNode root : v) {
        new_v.add(TreeToLinkedList(root));
      }
      ret.put(new_k, new_v);
    }
    return ret;
  }

  public static ListNode TreeToLinkedList(TreeNode root) {
    dummy = new ListNode(0, null);
    back = dummy;
    inorderAddToBack(root);
    return dummy.next;
  }

  public static void inorderAddToBack(TreeNode root) {
    if (root == null) return;
    inorderAddToBack(root.left);
    back.next = new ListNode(root.val, null);
    back = back.next;
    inorderAddToBack(root.right);
  }

  public static class ListNode {
    public int val;
    public ListNode next;

    public ListNode(int val, ListNode next) {
      this.val = val;
      this.next = next;
    }
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
 