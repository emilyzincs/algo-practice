package tests.practice_run_tests.java.solution_files;

public class Sol18 {
  public static ListNode solve(int[] arr) {
    if (arr.length == 0) return null;
    ListNode ret = new ListNode(arr[0], null);
    ListNode curr = ret;
    for (int i = 2; i < arr.length; i++) {
      curr.next = new ListNode(arr[i], null);
      curr = curr.next;
    }
    return ret;
  }

  public static class ListNode {
    public int val;
    public ListNode next;

    public ListNode(int val, ListNode next) {
      this.val = val;
      this.next = next;
    }
  }
}