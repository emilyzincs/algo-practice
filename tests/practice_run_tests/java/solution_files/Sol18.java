package tests.practice_run_tests.java.solution_files;
import java.util.List;

public class Sol18 {
  public static ListNode solve(List<Long> list) {
    if (list.isEmpty()) return null;
    ListNode ret = new ListNode(list.get(0), null);
    ListNode curr = ret;
    for (int i = 2; i < list.size(); i++) {
      curr.next = new ListNode(list.get(i), null);
      curr = curr.next;
    }
    return ret;
  }

  public static class ListNode {
    public long val;
    public ListNode next;

    public ListNode(long val, ListNode next) {
      this.val = val;
      this.next = next;
    }
  }
}