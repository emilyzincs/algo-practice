import json
import sys
from collections import deque
from typing import Any, assert_never

# Validate command‑line arguments and print usage if incorrect.
if len(sys.argv) != 9 or (sys.argv[5] != "True" and sys.argv[5] != "False"):
  print("Usage: python runner.py" + 
        " <practiceFilePackage>" +
        " <infoFilePath>.json" +
        " <testFilePath>.json" + 
        " <PROJECT_ROOT>" +
        " <debug>, where <debug> is True or False." +
        " <SolutionClassName>" + 
        " <SolutionMethodName>" +
        " <ParseTypes list string>", file=sys.stderr)
  print(f"Given args: {sys.argv}.", file=sys.stderr)
  sys.exit(1)


PROJECT_ROOT = sys.argv[4]
sys.path.insert(0, PROJECT_ROOT)

from util.general import load_module_from_path
from util.enums import ParseType, member_name_list, member_from_string
from boilerplate.util import validate_type

# Global variables that will hold the user's classes (if they exist)
USER_LISTNODE = None
USER_TREENODE = None


# Main test runner: loads the user's module, parses test cases, invokes the solution method,
# and compares results. Returns True if all tests pass, False otherwise.
def main() -> bool:
  practice_file_path = sys.argv[1]
  info_file_path = sys.argv[2]
  test_file_path = sys.argv[3]
  debug = (sys.argv[5] == "True")
  required_class_name = sys.argv[6]
  required_method_name = sys.argv[7]
  type_list_str = sys.argv[8]

  practice_module = load_module_from_path("practice_module", practice_file_path)
  incorrect_setup_msg = ("Error: Practice file must contain 'Solution'" +
                        " class with appropriate 'solve' method.")
  try:
    Solution = getattr(practice_module, required_class_name)
  except AttributeError as e:
    print(incorrect_setup_msg, file=sys.stderr)
    if debug:
      raise
    return False
  
  type_list: list[str] = json.loads(type_list_str)
  if type_list != member_name_list(ParseType):
    raise ValueError(f"type_list does not match expected. Value: {type_list}.")

  # Load the user's ListNode and TreeNode classes (if defined)
  global USER_LISTNODE, USER_TREENODE
  USER_LISTNODE = getattr(practice_module, "ListNode", None)
  USER_TREENODE = getattr(practice_module, "TreeNode", None)

  # Add cycle-aware __eq__ methods if applicable
  add_cycle_aware_eq(USER_LISTNODE)
  add_cycle_aware_eq(USER_TREENODE)

  with open(info_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
  
  unique_answer = data["unique_answer"]
  input_types = data.get("input_types")
  expected_type = data.get("expected_type")

  with open(test_file_path, "r", encoding="utf-8") as f:
    tests = json.load(f)

  sol = Solution()

  for i, test in enumerate(tests):
    try:
      args = [
        parse_value(v, input_types[idx])
        for idx, v in enumerate(test["inputs"])
      ]

      try:
        solution_method = getattr(sol, required_method_name)
      except AttributeError:
        print(incorrect_setup_msg, file=sys.stderr)
        if debug:
          raise
        return False
      
      actual = solution_method(*args)

      expected = test["expected"]
      if expected_type:
        if isinstance(expected, list) and not unique_answer:
          expected = [
            parse_value(e, expected_type)
            for e in expected
          ]
        else:
          expected = parse_value(expected, expected_type)

      ok = (
        actual == expected if unique_answer
        else actual in expected
      )

      if not ok:
        print(f"Test {i + 1} failed.\nExpected {expected}.\nBut was {actual}.", file=sys.stderr)
        return False

    except Exception as e:
      print(f"Test {i + 1} runtime error: {e}", file=sys.stderr)
      if debug:
        raise e
      return False

  return True


# Adds a cycle‑aware __eq__ method to a class (ListNode or TreeNode) to handle recursive
# structures without infinite loops. Overrides any existing __eq__.
#
# Parameters:
# - cls: The class to modify (ListNode or TreeNode), or None.
def add_cycle_aware_eq(cls):
  """Add a cycle-aware __eq__ method to a class if it doesn't already have one."""
  if cls is None:
    return

  if cls.__name__ == 'ListNode':
    def __eq__(self, other, visited=None):
      if self is None and other is None:
        return True
      if self is None or other is None:
        return False
      if visited is None:
        visited = set()
      pair_id = (id(self), id(other))
      if pair_id in visited:
        return True
      visited.add(pair_id)
      if not isinstance(other, cls):
        return False
      if self.val != other.val:
        return False
      return __eq__(self.next, other.next, visited)

    cls.__eq__ = __eq__

  elif cls.__name__ == 'TreeNode':
    def __eq__(self, other, visited=None):
      if self is None and other is None:
        return True
      if self is None or other is None:
        return False
      if visited is None:
        visited = set()
      pair_id = (id(self), id(other))
      if pair_id in visited:
        return True
      visited.add(pair_id)
      if not isinstance(other, cls):
        return False
      if self.val != other.val:
        return False
      if not __eq__(self.left, other.left, visited):
        return False
      return __eq__(self.right, other.right, visited)

    cls.__eq__ = __eq__


# Parses a JSON value according to a type definition, converting it into a Python object
# (primitive, list, set, dict, ListNode, TreeNode, etc.).
#
# Parameters:
# - val: The raw JSON value.
# - typ: The corresponding type definition dictionary.
#
# Returns:
#   The fully parsed python value.
def parse_value(val: Any, typ: dict[str, Any]) -> Any:
  validate_type(typ)
  curr_type: ParseType = member_from_string(ParseType, typ["type"])

  if curr_type is not ParseType.STRING and isinstance(val, str):
    try:
      val = json.loads(val)
    except json.JSONDecodeError:
      raise Exception(f"Could not parse string as JSON: {val}.")

  match curr_type:
    case ParseType.INT | ParseType.LONG | ParseType.FLOAT | ParseType.BOOLEAN | ParseType.STRING:
      return val
    case ParseType.ARRAY | ParseType.LIST:
      return [parse_value(v, typ["items"]) for v in val]
    case ParseType.IMMUTABLE_LIST:
      return tuple([parse_value(v, typ["items"]) for v in val])
    case ParseType.SET:
      return {parse_value(v, typ["items"]) for v in val}
    case ParseType.MAP:
      return {
        parse_value(k, typ["keys"]): parse_value(v, typ["values"])
        for k, v in val.items()
      }
    case ParseType.LISTNODE:
      if USER_LISTNODE is None:
        raise Exception("ListNode class not defined in the practice module")
      dummy = USER_LISTNODE(0, None)
      cur = dummy
      for x in val:
        cur.next = USER_LISTNODE(parse_value(x, typ["val"]), None)
        cur = cur.next
      return dummy.next

    case ParseType.TREENODE:
      if USER_TREENODE is None:
        raise Exception("TreeNode class not defined in the practice module")
      if not val:
        return None

      nodes = [
        None if x is None else USER_TREENODE(parse_value(x, typ["val"]), None, None)
        for x in val
      ]

      children = deque(nodes[1:])
      root = nodes[0]
      queue = deque([root])

      while queue and children:
        node = queue.popleft()
        if node is None:
          continue

        if children:
          node.left = children.popleft()
          queue.append(node.left)

        if children:
          node.right = children.popleft()
          queue.append(node.right)

      return root

    case _:
      assert_never(curr_type)


# Runs the test runner. Exits with code 1 if any test fails,
# otherwise prints "All tests passed." and exits with code 0.
if __name__ == "__main__":
  if not main():
    print("Runner must be run directly.", file=sys.stderr)
    sys.exit(1)
  else:
    print("All tests passed.")
