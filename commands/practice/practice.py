import sys
import util.get_file_paths as gfp
import subprocess
import time
from commands.practice.java import get_test_cmd as java_get_test_cmd
from util.utils import print_desc, in_either
from commands.command_util import GLOBAL_COMMANDS, handle_global_command, get_global_command_descriptions

def handle_commands(
    local_commands: set[str],
    alg: str,
    language: str,
    extension: str,
    delete_attempts_func,
    load_solution_func,
    exit_func
) -> float|None:
  start_time = time.perf_counter()
  potential_end_time = None
  correct = False
  while not correct:
    user_input = input("Type 'done' when you are finished or 'help' for options:\n")
    if not in_either(user_input, GLOBAL_COMMANDS, local_commands):
      print("Unrecognized input. Type 'help' to see valid inputs.", file=sys.stderr)
      continue
    
    if user_input in GLOBAL_COMMANDS:
      if not handle_global_command(user_input, handle_help, exit_func):
        break
    else:
      match user_input:
        case "d" | "done":
          potential_end_time = time.perf_counter()
          correct = run_tests(alg, language, extension)
        case "s" | "sol" | "solution":
          try:
            load_solution_func(alg)
          except FileNotFoundError:
            print(f"Cannot load solution because it does not exist.", file=sys.stderr)
        case _:
          raise ValueError(f"Unhandled case {user_input}.")
  delete_attempts_func()    
  return potential_end_time - start_time if correct else None

def handle_help():
  command_descriptions = get_global_command_descriptions()
  command_descriptions.extend([
    "d/done: Submits the current practice implementation to be tested",
    "s/sol/solution: Loads the algorithm solution into the file"
  ])
  print("This menu supports the following inputs:")
  print_desc(command_descriptions) 

def run_tests(
    alg: str,
    language: str, 
    extension: str,
    show_subprocess_text: bool = True,
    debug: str = "False",
    required_class_name: str = "Solution",
    required_method_name: str = "solve",
  ) -> bool:
  practice_file_dir = gfp.get_practice_file_dir()
  practice_file = gfp.get_practice_file_path(language, extension)
  test_runner_dir = gfp.get_test_runner_dir_path(language)
  test_runner_file = gfp.get_test_runner_file_path(language, extension)
  info_file = gfp.get_info_file_path(alg)
  test_file = gfp.get_test_file_path(alg)
  match language:
    case "python":
      cmd = ["python", test_runner_file, practice_file, info_file, test_file, gfp.PROJECT_ROOT, debug]
    case "java":
      cmd = java_get_test_cmd(
        alg,
        practice_file_dir,
        practice_file,
        test_runner_dir,
        test_runner_file,
        info_file,
        test_file,
        debug
      )
    case _:
      raise NameError("Could not find language:", language)
  if isinstance(cmd, int):
    return False
  cmd.extend([required_class_name, required_method_name])
  result = subprocess.run(cmd, cwd=test_runner_dir, capture_output=not show_subprocess_text)
  if result.returncode != 0:
    return False
  return True
