from __future__ import annotations 
from typing import Optional

class Solution:
  def solve(self, input):
    return input

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
