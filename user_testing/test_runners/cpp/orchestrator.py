import json
import sys
import os
import subprocess
from typing import Any

# Validate command‑line arguments and print usage if incorrect.
if len(sys.argv) != 9 or (sys.argv[5] != "True" and sys.argv[5] != "False"):
  print("Usage: python runner.py" + 
        " <practiceFilePath>"
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

from util.enums import ParseType, member_name_list

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

  cpp_runner_contents = get_cpp_runner_contents(
    practice_file_path[len(PROJECT_ROOT):], 
    required_class_name,
    required_method_name,
    cpp_input_types,
    cpp_expected_type,
  )
  
  with open("runner.cpp", "w") as f:
      f.write(cpp_runner_contents)

  compile_cmd = [
      "g++", "-std=c++17", "runner.cpp", "helpers.cpp",
      "-o", "runner.exe", f"-I{PROJECT_ROOT}"
  ]
  compilation = subprocess.run(compile_cmd, capture_output=True, text=True)
  
  if compilation.returncode != 0:
    if debug:
      print(f"Compilation Error:\n{compilation.stderr}")
    return False

  run_cmd = ["./runner.exe", str(debug), info_file_path, test_file_path, type_list_str]
  result = subprocess.run(run_cmd, capture_output=False, text=debug)

  return result.returncode == 0


def get_cpp_runner_contents(
  practice_file_path: str,
  required_class_name: str, 
  required_method_name: str,
  cpp_input_types: list[str],
  cpp_expected_type: str,
) -> str:
  declval_list = [f"std::declval<{typ}&>()" for typ in cpp_input_types]
  decltype_args = ", ".join(declval_list)

  arg_extraction = []
  call_args_names = []
  for i, typ in enumerate(cpp_input_types):
      var_name = f"arg{i}"
      arg_extraction.append(f'    auto {var_name} = test["inputs"][{i}].get<{typ}>();')
      call_args_names.append(var_name)
  
  arg_lines = "\n".join(arg_extraction)
  final_args = ", ".join(call_args_names)

  return (
    '#include <iostream>\n' +
    '#include <utility>\n' +
    '#include <unordered_set>\n' +
    '#include <fstream>\n' +
    '#include "json.hpp"\n' +
    '#include "helpers.hpp"\n' +
    '\n' +
    f'#include "../../..{practice_file_path}"\n' +
    '\n' +
    'using json = nlohmann::json;\n' +
    'using\n' +
    '  std::cout,\n' +
    '  std::cerr, \n' +
    '  std::string,\n' +
    '  std::vector,\n' +
    '  std::unordered_map,\n' +
    '  std::unordered_set;\n' +
    '\n' +
    '\n' +
    'int main(int argc, char** argv) {{\n' +
    '  bool debug = string(argv[1]) == "True";\n' +
    '  \n' +
    '  vector<string> parseTypesString = json::parse(argv[4]).get<vector<string>>();\n' +
    '  validateParseTypeEnumList(parseTypesString);\n' +
    '\n' +
    '  string info_path = argv[2];\n' +
    '  string test_path = argv[3];\n' +
    '  json info = getJsonFromPath(info_path);\n' +
    '  json tests = getJsonFromPath(test_path);\n' +
    '\n' +
    '  bool unique = info["unique_answer"];\n' +
    '  json expected_type = info["expected_type"];\n' +
    '\n' +
    '  for (int i = 0; i < tests.size(); i++) {{\n' +
    '    auto& test = tests[i];\n' +
    # '    // 1. Get the actual type returned by the user\'s function\n' +
    # f'    using ActualRetType = decltype({required_class_name}::{required_method_name}({decltype_args}));\n' +
    # f'    using ExpectedRetType = {cpp_expected_type}; \n' +
    # '    static_assert(std::is_same_v<ActualRetType, ExpectedRetType>, \n' +
    # '                  "Return type mismatch! Your function signature does not match the problem definition.");\n' +
    '    \n' +
    arg_lines + "\n" +
    f'    {cpp_expected_type} raw = {required_class_name}::{required_method_name}({final_args});\n' +
    '\n' +
    '    json actual = standardizeOutput(raw, expected_type);\n' +
    '    json expected = test["expected"];\n' +
    '\n' +
    '    if (!validateOutput(actual, expected, unique, i)) {{\n' +
    '      std::exit(1);\n' +
    '    }}\n' +
    '  }}\n' +
    '  return 0;\n' +
    '}}\n'
)

if __name__ == "__main__":
  if main():
    print("All tests passed.")
  else:
    sys.exit(1)
