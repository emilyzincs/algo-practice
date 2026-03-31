package tests.practice_run_tests.java.solution_files;

public class Sol17 {
  public static ListNode solve(ListNode head) {
    return head != null ? head.next : null;
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