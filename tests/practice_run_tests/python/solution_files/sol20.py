from __future__ import annotations 
from typing import Optional

class TreeNode:
  def __init__(self, val, left: Optional[TreeNode] = None, 
               right: Optional[TreeNode] = None):
    self.val = val
    self.left = left
    self.right = right

class Solution:
  def solve(self, input: set[tuple]) -> Optional[TreeNode]:
    all_vals = []
    for tup in input:
      all_vals.extend(tup)
    all_vals.sort()
    if not all_vals:
      return None

    return TreeNode(all_vals[0], 
              TreeNode(all_vals[1], 
                TreeNode(all_vals[2]), 
                TreeNode(all_vals[3])), 
              TreeNode(all_vals[-1]))
  