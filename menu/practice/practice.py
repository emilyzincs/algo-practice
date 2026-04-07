import sys
import util.file_paths as gfp
import subprocess
import time
from menu.practice.java import get_test_cmd as java_get_test_cmd
from util.exceptions import UnhandledCaseException
from menu.util import handle_global_command, get_global_command_descriptions, print_desc
from typing import assert_never
from util.enums import (
  GlobalCommand,
  is_member,
  PracticeCommand,
  member_from_string,
  SpecificAlgorithm,
  Language
)

def handle_commands(
    alg: SpecificAlgorithm,
    language: Language,
    delete_attempts_func,
    load_solution_func,
    exit_func
) -> float|None:
  start_time = time.perf_counter()
  potential_end_time = None
  correct = False
  while not correct:
    user_input = input("Type 'done' when you are finished or 'help' for options:\n")
    input_is_global_cmd = is_member(GlobalCommand, user_input)
    input_is_local_cmd = is_member(PracticeCommand, user_input)
    if not input_is_global_cmd and not input_is_local_cmd:
      print("Unrecognized input. Type 'help' to see valid inputs.", file=sys.stderr)
      continue
    
    if input_is_global_cmd:
      global_cmd: GlobalCommand = member_from_string(GlobalCommand, user_input)
      if not handle_global_command(global_cmd, handle_help, exit_func):
        break
    elif input_is_local_cmd:
      local_cmd: PracticeCommand = member_from_string(PracticeCommand, user_input)
      match local_cmd:
        case PracticeCommand.D | PracticeCommand.DONE:
          potential_end_time = time.perf_counter()
          print("Running tests...")
          correct = run_tests(alg, language)
        case PracticeCommand.S | PracticeCommand.SOL | PracticeCommand.SOLUTION:
          try:
            load_solution_func(alg)
            print("Successfully loaded solution.")
          except FileNotFoundError:
            print(f"Cannot load solution because it does not exist.", file=sys.stderr)
        case _:
          assert_never()
    else:
      raise UnhandledCaseException(user_input, "input")

  delete_attempts_func()    
  if correct:
    if type(potential_end_time) != float:
      raise RuntimeError("Correct is true but potential_end_time is not a float.")
    return potential_end_time - start_time
  return None

def handle_help():
  command_descriptions = get_global_command_descriptions()
  command_descriptions.extend([
    "d/done: Submits the current practice implementation to be tested",
    "s/sol/solution: Loads the algorithm solution into the file"
  ])
  print("This menu supports the following inputs:")
  print_desc(command_descriptions) 

def run_tests(
    alg: SpecificAlgorithm,
    language: Language, 
    show_subprocess_text: bool = True,
    debug: str = "False",
    required_class_name: str = "Solution",
    required_method_name: str = "solve",
  ) -> bool:
  practice_file_dir = gfp.get_practice_file_dir()
  practice_file = gfp.get_practice_file_path(language)
  test_runner_dir = gfp.get_test_runner_dir_path(language)
  test_runner_file = gfp.get_test_runner_file_path(language)
  info_file = gfp.get_info_file_path(alg)
  test_file = gfp.get_test_file_path(alg)
  cmd: list[str]|None
  match language:
    case Language.PYTHON:
      cmd = ["python", test_runner_file, practice_file, info_file, test_file, gfp.PROJECT_ROOT, debug]
    case Language.JAVA:
      cmd = java_get_test_cmd(
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
