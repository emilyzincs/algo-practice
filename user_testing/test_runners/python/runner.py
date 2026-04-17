import json
import sys
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


# Returns True if all tests pass, False otherwise.
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
        raise
      return False

  return True


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

  match curr_type:
    case ParseType.INT | ParseType.LONG | ParseType.FLOAT | ParseType.BOOLEAN | ParseType.STRING:
      return val
    case ParseType.ARRAY | ParseType.LIST:
      return [parse_value(v, typ["items"]) for v in val]
    case ParseType.HASHABLE_LIST:
      return tuple([parse_value(v, typ["items"]) for v in val])
    case ParseType.SET:
      return {parse_value(v, typ["items"]) for v in val}
    case ParseType.HASHABLE_SET:
      return frozenset(parse_value(v, typ["items"]) for v in val)
    case ParseType.MAP:
      if type(val) != list or len(val) != 2 or len(val[0]) != len(val[1]):
        raise ValueError("Maps must be represented as two lists of equal length.")
      keys, values = val
      n = len(keys)
      return {
        parse_value(keys[i], typ["keys"]): parse_value(values[i], typ["values"])
        for i in range(n)
      }
    case _:
      assert_never(curr_type)


# Runs the test runner. Exits with code 1 if any test fails,
# otherwise prints "All tests passed." and exits with code 0.
if __name__ == "__main__":
  if main():
    print("All tests passed.")
  else:
    sys.exit(1)
