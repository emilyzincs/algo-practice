from __future__ import annotations 
from typing import Optional

class Solution:
  def solve(self, input):
    total = 0
    curr = input
    while curr:
      for a in curr.val:
        for b in a:
          for c in b:
            for d in c:
              total += self.inorder_traverse(d)

      curr = curr.next

    return total
  
  def inorder_traverse(self, root: Optional[TreeNode]) -> int:
    if not root:
      return 0
    ret = 0
    ret += self.inorder_traverse(root.left)
    for a in root.val:
      for b in a:
        if b == True:
          ret += 1
    ret += self.inorder_traverse(root.right)
    return ret
  
class ListNode:
  def __init__(self, val, next: Optional[ListNode] = None):
    self.val = val
    self.next = next 

class TreeNode:
  def __init__(self, val, left: Optional[TreeNode] = None, 
               right: Optional[TreeNode] = None):
    self.val = val
    self.left = left
    self.right = right
