from __future__ import annotations 
from typing import Optional

class Solution:
  def solve(self, head: list[int]):
    if not head:
      return None
    entries = head[1:]
    ret = ListNode(entries[0])
    curr = ret
    for val in entries[1:]:
      curr.next = ListNode(val)
      curr = curr.next
    return ret
  
class ListNode:
  def __init__(self, val, next: Optional[ListNode] = None):
    self.val = val
    self.next = next