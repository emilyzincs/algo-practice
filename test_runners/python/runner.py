import json
import sys
from collections import deque

if len(sys.argv) != 8 or (sys.argv[5] != "True" and sys.argv[5] != "False"):
  print("Usage: python runner.py" + 
        " <practiceFilePackage>" +
        " <infoFilePath>.json" +
        " <testFilePath>.json" + 
        " <PROJECT_ROOT>" +
        " <debug>, where <debug> is True or False." +
        " <SolutionClassName>" + 
        " <SolutionMethodName>", file=sys.stderr)
  sys.exit(1)

PROJECT_ROOT = sys.argv[4]
sys.path.insert(0, PROJECT_ROOT)

from util.utils import load_module_from_path

# Global variables that will hold the user's classes (if they exist)
USER_LISTNODE = None
USER_TREENODE = None


def add_cycle_aware_eq(cls):
  """Add a cycle-aware __eq__ method to a class if it doesn't already have one."""
  if cls is None:
    return
  # Override any existing __eq__ (the user's might not handle cycles)
  if cls.__name__ == 'ListNode':
    def __eq__(self, other, visited=None):
      # Handle None
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
      # Recursively compare next
      return __eq__(self.next, other.next, visited)

    cls.__eq__ = __eq__

  elif cls.__name__ == 'TreeNode':
    def __eq__(self, other, visited=None):
      # Handle None
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
      # Recursively compare left and right
      if not __eq__(self.left, other.left, visited):
        return False
      return __eq__(self.right, other.right, visited)

    cls.__eq__ = __eq__


# =========================
# TYPE PARSING
# =========================

def parse_value(val, typ):
   # If the expected type is complex and val is a string, try to parse it as JSON
  # print("val:", val)
  # print("typ:", typ)
  # print()
  complex_types = {"array", "list", "immutable_list", "set", "map", "ListNode", "TreeNode"}
  if typ["type"] in complex_types and isinstance(val, str):
    try:
      val = json.loads(val)  # Convert string to Python object
    except json.JSONDecodeError:
      raise Exception(f"Could not parse string as JSON: {val}")

  match typ["type"]:
    case "int":
      return int(val)
    case "long":
      return int(val)
    case "float":
      return float(val)
    case "boolean":
      return bool(val)
    case "string":
      return str(val)
    case "array":
      return [parse_value(v, typ["items"]) for v in val]
    case "list":
      return [parse_value(v, typ["items"]) for v in val]
    case "immutable_list":
      return tuple([parse_value(v, typ["items"]) for v in val])
    case "set":
      return {parse_value(v, typ["items"]) for v in val}
    case "map":
      return {
        parse_value(k, typ["keys"]): parse_value(v, typ["values"])
        for k, v in val.items()
      }
    case "ListNode":
      if USER_LISTNODE is None:
        raise Exception("ListNode class not defined in the practice module")
      dummy = USER_LISTNODE(0, None)
      cur = dummy
      for x in val:
        cur.next = USER_LISTNODE(parse_value(x, typ["val"]), None)
        cur = cur.next
      return dummy.next

    case "TreeNode":
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
      raise Exception(f"Unknown type: {typ["type"]}")


# =========================
# MAIN TEST RUNNER
# =========================

def main():
  practice_file_path = sys.argv[1]
  info_file_path = sys.argv[2]
  test_file_path = sys.argv[3]
  debug = (sys.argv[5] == "True")
  required_class_name = sys.argv[6]
  required_method_name = sys.argv[7]

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

  # Load the user's ListNode and TreeNode classes (if defined)
  global USER_LISTNODE, USER_TREENODE
  USER_LISTNODE = getattr(practice_module, "ListNode", None)
  USER_TREENODE = getattr(practice_module, "TreeNode", None)

  # Add cycle-aware __eq__ methods (overrides any existing)
  add_cycle_aware_eq(USER_LISTNODE)
  add_cycle_aware_eq(USER_TREENODE)

  with open(info_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
  
  unique_answer = data["unique_answer"]
  input_types = data.get("input_types")
  expected_type = data.get("expected_type_wrapper")

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
        # actual = sol.solve(*args)
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

if __name__ == "__main__":
  if not main():
    sys.exit(1)
  else:
    print("All tests passed.")