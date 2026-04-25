import json
import sys
import traceback
from typing import Any, assert_never

if len(sys.argv) != 9 or (sys.argv[5] != "True" and sys.argv[5] != "False"):
  print("Usage: python runner.py" + 
        " <practiceFilePath>" +
        " <infoFilePath>.json" +
        " <testFilePath>.json" + 
        " <PROJECT_ROOT>" +
        " <debug>, where <debug> is True or False." +
        " <SolutionClassName>" + 
        " <SolutionMethodName>" +
        " <parseTypeList>", file=sys.stderr)
  print(f"Given args: {sys.argv}.", file=sys.stderr)
  sys.exit(1)

PROJECT_ROOT = sys.argv[4]
sys.path.insert(0, PROJECT_ROOT)

from util.general import load_module_from_path
from util.enums import ParseType, member_from_string
from boilerplate.util import validate_type


# Returns True if all tests pass, False otherwise.
def main(
  practice_file_path: str,
  info_file_path: str,
  test_file_path: str,
  PROJECT_ROOT: str,
  debug: bool,
  required_class_name: str,
  required_method_name: str
) -> bool:
  

  practice_module = load_module_from_path("practice_module", practice_file_path)
  incorrect_setup_msg = ("Error: Practice file must contain 'Solution'" +
                        " class with appropriate 'solve' method.")
  try:
    Solution = getattr(practice_module, required_class_name)
  except AttributeError as e:
    print(incorrect_setup_msg, file=sys.stderr)
    if debug:
      traceback.print_exc()
    return False

  with open(info_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
  
  unique_answer = data["unique_answer"]
  input_types = data.get("input_types")
  expected_type = data.get("expected_type")

  with open(test_file_path, "r", encoding="utf-8") as f:
    tests = json.load(f)

  for i, test in enumerate(tests):
    sol = Solution()
    
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
          traceback.print_exc()
        return False
      
      actual = solution_method(*args)
      actual = standardize_output(actual, expected_type)

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
        traceback.print_exc()
      return False

  return True


# Parses a JSON value according to a type definition
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
    case ParseType.ARRAY | ParseType.LIST | ParseType.UNORDERED_LIST:
      return [parse_value(v, typ["items"]) for v in val]
    case _:
      assert_never(curr_type)
  
def standardize_output(val: Any, typ: dict[str, Any]) -> Any:
  validate_type(typ)
  curr_type: ParseType = member_from_string(ParseType, typ["type"])

  match curr_type:
    case ParseType.INT | ParseType.LONG:
      type_assert(val, int)
    case ParseType.FLOAT:
      type_assert(val, float)
    case ParseType.BOOLEAN:
      type_assert(val, bool)
    case ParseType.STRING:
      type_assert(val, str)
    case ParseType.ARRAY | ParseType.LIST:
      type_assert(val, list)
      val = [standardize_output(v, typ["items"]) for v in val]
    case ParseType.UNORDERED_LIST:
      type_assert(val, list)
      return sorted([standardize_output(v, typ["items"]) for v in val])
    case _:
      assert_never(curr_type)
  return val
    
  
def type_assert(val: Any, typ: type):
  if type(val) != typ:
    raise ValueError(f"Expected {val} to have type {typ}, but was {type(val)}.")
  
if __name__ == "__main__":
  args = sys.argv
  success = main(
    practice_file_path = args[1],
    info_file_path = args[2],
    test_file_path = args[3],
    PROJECT_ROOT = args[4],
    debug = args[5] == "True",
    required_class_name = args[6],
    required_method_name = args[7]
  )
  if success:
    print("All tests passed.")
  else:
    sys.exit(1)
