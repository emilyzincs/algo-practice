import subprocess
import util.file_paths as fp
from json import dumps
from typing import assert_never
from util.enums import SpecificAlgorithm, Language, member_name_list, ParseType
from user_testing.test_commands.java import get_test_command as java_get_test_command
from util.constants import SOLUTION_CLASS_NAME, SOLUTION_FUNCTION_NAME
from util.general import load_module_from_path


# Runs the test suite for a given algorithm and language by executing the appropriate
# test runner. Returns True if all tests pass, False otherwise.
#
# Parameters:
# - alg: The SpecificAlgorithm being tested.
# - language: The Language in which the solution is written.
# - show_subprocess_text: If True, subprocess output is printed to the console;
# - debug: string "True" or "False" – enables detailed error logging in the runner.
# - required_class_name: Name of the class containing the solution method
#                        (defaults to SOLUTION_CLASS_NAME).
# - required_method_name: Name of the method to test
#                         (defaults to SOLUTION_FUNCTION_NAME).
#
# Returns:
#   True if the subprocess returns exit code 0 (all tests passed), False otherwise.
def run_tests(
  alg: SpecificAlgorithm,
  language: Language, 
  show_subprocess_text: bool = True,
  debug: str = "False",
  required_class_name: str = SOLUTION_CLASS_NAME,
  required_method_name: str = SOLUTION_FUNCTION_NAME,
) -> bool:
  if (debug != "False" and debug != "True"):
    raise ValueError(f"Debug must be a string that is either 'False' or 'True', was {debug}.")

  practice_file_dir = fp.get_practice_file_dir()
  practice_file = fp.get_practice_file_path(language)
  test_runner_dir = fp.get_test_runner_dir_path(language)
  test_runner_file = fp.get_test_runner_file_path(language)
  info_file = fp.get_info_path(alg)
  test_file = fp.get_test_path(alg)

  parse_types_list: list[str] = member_name_list(ParseType)
  additional_args = [
    required_class_name,
    required_method_name,
    dumps(parse_types_list)
  ]
  cmd: list[str]|None
  match language:
    case Language.PYTHON | Language.CPP:
      module = load_module_from_path("run", test_runner_file)
      runner_func = getattr(module, "main")
      return runner_func(
        debug == "True",
        practice_file,
        info_file,
        test_file,
        fp.PROJECT_ROOT,
        dumps(parse_types_list),
        required_class_name,
        required_method_name,
      )
    case Language.JAVA:
      cmd = java_get_test_command(
        practice_file_dir,
        practice_file,
        test_runner_dir,
        test_runner_file,
        info_file,
        test_file,
        debug
      )
    case _:
      assert_never(language)
  if cmd is None:
    return False
  cmd.extend(additional_args)
  result = subprocess.run(cmd, cwd=test_runner_dir, capture_output=not show_subprocess_text)
  return result.returncode == 0
