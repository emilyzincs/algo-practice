from __future__ import annotations 
from typing import Optional

class TreeNode:
  def __init__(self, val, left: Optional[TreeNode] = None, 
               right: Optional[TreeNode] = None):
    self.val = val
    self.left = left
    self.right = right

class ListNode:
  def __init__(self, val, next: Optional[ListNode] = None):
    self.val = val
    self.next = next 

class Solution:
  def solve(self, input: dict[tuple[tuple[float]], 
                              list[Optional[TreeNode]]]) -> list[tuple[float], list[ListNode]]:
    ret = {}
    for k, v in input.items():
      new_k = tuple([sum(tup) for tup in k])
      new_v = [self.tree_to_linked_list(tree) for tree in v]
      ret[k] = v
    return ret

  def tree_to_linked_list(self, root: Optional[TreeNode]) -> Optional[ListNode]:
    self.dummy = ListNode(0)
    self.back = self.dummy
    self.preorder_add_to_back(root)

  def preorder_add_to_back(self, root: Optional[TreeNode]) -> None:
    if root is None:
      return
    self.preorder_add_to_back(root.left)
    self.back.next = ListNode(root.val)
    self.back = self.back.next
    self.preorder_add_to_back(root.right)