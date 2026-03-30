from __future__ import annotations 
from typing import Optional

class ListNode:
  def __init__(self, val=0, next: Optional[ListNode] = None):
    self.val = val
    self.next = next

class Solution:
  def solve(self, head: Optional[ListNode]) -> Optional[ListNode]:
    return head.next if head is not None else None