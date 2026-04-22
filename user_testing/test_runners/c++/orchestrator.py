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
from boilerplate.language.cpp import CppBp

from util.enums import ParseType, member_name_list, member_from_string
from boilerplate.util import validate_type

cpp_type_parser = CppBp()

# Returns True if all tests pass, False otherwise.
def main() -> bool:
  practice_file_path = sys.argv[1]
  info_file_path = sys.argv[2]
  test_file_path = sys.argv[3]
  debug = (sys.argv[5] == "True")
  required_class_name = sys.argv[6]
  required_method_name = sys.argv[7]
  type_list_str = sys.argv[8]

  
  
  type_list: list[str] = json.loads(type_list_str)
  if type_list != member_name_list(ParseType):
    raise ValueError(f"type_list does not match expected. Value: {type_list}.")

  with open(info_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)
  
  expected_type = data.get("expected_type")
  input_types = data.get("input_types")

  cpp_expected_type = cpp_type_parser.parse_type_string(expected_type)
  cpp_input_types = (
    [cpp_type_parser.parse_type_string(input_type) for input_type in input_types]
  )



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


# Runs the test runner. Exits with code 1 if any test fails,
# otherwise prints "All tests passed." and exits with code 0.
if __name__ == "__main__":
  if main():
    print("All tests passed.")
  else:
    sys.exit(1)
