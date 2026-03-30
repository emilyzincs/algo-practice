from __future__ import annotations 
from typing import Optional

class TreeNode:
  def __init__(self, val, left: Optional[TreeNode] = None, 
               right: Optional[TreeNode] = None):
    self.val = val
    self.left = left
    self.right = right

class Solution:
  def solve(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
    if not root or not root.right:
      return None
    return root.right