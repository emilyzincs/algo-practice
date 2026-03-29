import json
import sys
from collections import deque

if len(sys.argv) != 4:
  print("Must have exactly three command line arguments, was "
        + str(len(sys.argv) - 1), file=sys.stderr)
  sys.exit(1)

PROJECT_ROOT = sys.argv[3]
sys.path.insert(0, PROJECT_ROOT)

from utils import load_module_from_path

# =========================
# TYPE PARSING
# =========================

def parse_value(val, typ):
  match typ["type"]:
    case "int":
      return int(val)
    case "long":
      return int(val)
    case "double":
      return float(val)
    case "boolean":
      return bool(val)
    case "string":
      return str(val)
    case "array":
      return [parse_value(v, typ["items"]) for v in val]
    case "list":
      return [parse_value(v, typ["items"]) for v in val]
    case "set":
      return {parse_value(v, typ["items"]) for v in val}
    case "map":
      return {
        parse_value(k, typ["keys"]): parse_value(v, typ["values"])
        for k, v in val.items()
      }
    case "ListNode":
      return build_listnode(val)
    case "TreeNode":
      return build_treenode(val)
    case _:
      raise Exception(f"Unknown type: {typ["type"]}")


# =========================
# LINKED LIST
# =========================

class ListNode:
  def __init__(self, val=0, next=None):
    self.val = val
    self.next = next


def build_listnode(arr):
  dummy = ListNode()
  cur = dummy
  for x in arr:
    cur.next = ListNode(x)
    cur = cur.next
  return dummy.next


# =========================
# BINARY TREE
# =========================

class TreeNode:
  def __init__(self, val=0, left=None, right=None):
    self.val = val
    self.left = left
    self.right = right


def build_treenode(arr):
  if not arr:
    return None

  nodes = [
    None if x is None else TreeNode(x)
    for x in arr
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

# =========================
# MAIN TEST RUNNER
# =========================

def main():
  practice_file_path = sys.argv[1]
  test_file_path = sys.argv[2]

  practice_module = load_module_from_path("practice_module", practice_file_path)
  incorrect_setup_msg = ("Error: Practice file must contain 'Solution'" + 
                        " class with appropriate 'solve' method.")
  try:
    Solution = practice_module.Solution
  except AttributeError:
    print(incorrect_setup_msg, file=sys.stderr)
    return False 
  with open(test_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

  unique_answer = data["unique_answer"]
  tests = data["tests"]

  input_types = data.get("input_types", [])
  expected_type = data.get("expected_type", None)

  sol = Solution()

  for i, test in enumerate(tests):
    try:
      args = [
        parse_value(v, input_types[idx])
        for idx, v in enumerate(test["inputs"])
      ]
      
      try:
        actual = sol.solve(*args)
      except AttributeError:
        print(incorrect_setup_msg, file=sys.stderr)
        return False
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
        print(f"Test {i + 1} failed. Output: {actual}", file=sys.stderr)
        return False

    except Exception as e:
      print(f"Test {i + 1} runtime error: {e}", file=sys.stderr)
      return False

  return True

if __name__ == "__main__":
  if not main():
    sys.exit(1)
