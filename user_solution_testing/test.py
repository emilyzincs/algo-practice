import subprocess
import util.file_paths as fp
from typing import assert_never
from util.enums import SpecificAlgorithm, Language
from user_solution_testing.test_commands.java import get_test_command as java_get_test_command

def run_tests(
    alg: SpecificAlgorithm,
    language: Language, 
    show_subprocess_text: bool = True,
    debug: str = "False",
    required_class_name: str = "Solution",
    required_method_name: str = "solve",
  ) -> bool:
  practice_file_dir = fp.get_practice_file_dir()
  practice_file = fp.get_practice_file_path(language)
  test_runner_dir = fp.get_test_runner_dir_path(language)
  test_runner_file = fp.get_test_runner_file_path(language)
  info_file = fp.get_info_file_path(alg)
  test_file = fp.get_test_file_path(alg)
  cmd: list[str]|None
  match language:
    case Language.PYTHON:
      cmd = ["python", test_runner_file, practice_file, info_file, test_file, fp.PROJECT_ROOT, debug]
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
      assert_never()
  if cmd is None:
    return False
  cmd.extend([required_class_name, required_method_name])
  result = subprocess.run(cmd, cwd=test_runner_dir, capture_output=not show_subprocess_text)
  if result.returncode != 0:
    return False
  return True
