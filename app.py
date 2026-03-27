from typing import List
import os.path
import time
import subprocess
import get_file_paths as gfp
import sys
import shutil
import json
from utils import load_module_from_path
from pathlib import Path
from commands.main_menu import handle_commands as main_menu_handle_commands
from commands.practice import handle_commands as practice_handle_commands

if not os.path.exists(gfp.get_settings_path()):
  actual_settings = gfp.get_settings_path()
  default_settings = gfp.get_default_settings_path()
  try:
    shutil.copyfile(default_settings, actual_settings)
  except PermissionError:
    print(f"Error: do not have permission to copy {default_settings} to {actual_settings}.", file=sys.stderr)
    sys.exit(1)
  except FileNotFoundError:
    print(f"At least one of {actual_settings} and {default_settings} must exist.", file=sys.stderr)
    sys.exit(1)

settings = json.load(gfp.get_settings_path())

ALG_NAME_TO_IDX = {
  "binary search": 0,
}
ALG_LIST = [
  "binary_search"
]
NUM_ALGS = len(ALG_LIST)
TAB = "  "
SOLUTION_FUNCTION_NAME = "solve"
LANGUAGE_LIST = [
  "python",
  "java",
]
DEFAULT_LANGUAGE = settings['default_language']
LANGUAGE_TO_EXTENSION_AND_COMMENT_SYMBOL = {
  "python": (".py", "#"),
  "java": (".java", "//"),
}

LANGUAGE = DEFAULT_LANGUAGE
if len(sys.argv) > 2:
    raise ValueError(f"Usage: python {sys.argv[0]} language (default is python)")
elif len(sys.argv) == 2:
  lang = sys.argv[1].strip().lower()
  if lang not in LANGUAGE_TO_EXTENSION_AND_COMMENT_SYMBOL:
    print(f"Unsupported language: {lang}. defaulting to {DEFAULT_LANGUAGE}." + 
          " Type 'languages' for supported languages or <language> to switch to that language.")
  else:
    LANGUAGE = lang

EXTENSION, COMMENT_SYMBOL = LANGUAGE_TO_EXTENSION_AND_COMMENT_SYMBOL[LANGUAGE]
PARAMETER_LINE_PREFIX = COMMENT_SYMBOL + " parameters:"

COMMANDS = {
  "main_menu": {"help", "q", "quit", "exit", "lang", 
                "language", "langs", "languages", "algs", 
                "algorithms", "settings"},
  "practice": {"help", "q", "quit", "exit", "b", "back"},
  "settings": {}
}
COMMANDS['main_menu'].update(LANGUAGE_LIST)

def main():  
  while True:
    user_input = input("\nEnter the algorithm (name or id) you would like to practice, or 'help' for options:\n")
    while (main_menu_handle_commands(
      user_input,
      COMMANDS['main_menu'],
      LANGUAGE,
      LANGUAGE_LIST,
      LANGUAGE_TO_EXTENSION_AND_COMMENT_SYMBOL,
      set_language,
      ALG_NAME_TO_IDX,
      NUM_ALGS,
      TAB
    )):
      user_input = input("Input: ")

    idx = None
    error_str = "Invalid algorithm id. To list the valid algorithm names and ids, type 'algorithms'." 
    if is_int(user_input):
      idx = int(user_input)
      if idx < 0 or idx >= NUM_ALGS:
        print(error_str, file=sys.stderr)
        continue
    else:
      if user_input not in ALG_NAME_TO_IDX:
        print(error_str, file=sys.stderr)
        continue
      idx = ALG_NAME_TO_IDX[user_input]

    alg = ALG_LIST[idx]
    time_spent = handle_practice(alg)
    if time_spent < 0:
      continue
    print(f"Successfully completed {alg} in {time_spent:.2f} seconds!")

def set_language(lang: str) -> None:
  lang = lang.strip().lower()
  if lang not in LANGUAGE_TO_EXTENSION_AND_COMMENT_SYMBOL:
    raise ValueError(f"Unsupported language: {lang}." + 
          " Type 'languages' for supported languages or <language> to switch to that language.")
  global LANGUAGE, EXTENSION, COMMENT_SYMBOL, PARAMETER_LINE_PREFIX
  LANGUAGE = lang
  EXTENSION, COMMENT_SYMBOL = LANGUAGE_TO_EXTENSION_AND_COMMENT_SYMBOL[LANGUAGE]
  PARAMETER_LINE_PREFIX = COMMENT_SYMBOL + " parameters:"
  print(f"Successfully set language to {lang}.")
  
def is_int(str: str) -> bool:
  try:
    int(str)
    return True
  except ValueError:
    return False

def handle_practice(alg: str) -> float:
  reset_practice_file(alg)
  start_time = time.perf_counter()
  correct = False
  while not correct:
    user_input = input("Type 'done' when you are finished, or 'help' to see all commands.\n")
    while (practice_handle_commands(
      user_input,
      COMMANDS['practice']
    )):
      user_input = input("Input: ")
    if user_input == "back" or user_input == "b":
      return -1
    elif user_input != 'done' and user_input != 'd':
      print("Invalid input.", file=sys.stderr)
      continue
    potential_end_time = time.perf_counter()
    correct = run_tests(alg)
  total_time = potential_end_time - start_time
  return total_time

def reset_practice_file(alg: str) -> None:
  practice_file = gfp.get_practice_file_path(LANGUAGE, EXTENSION)
  solution_file = gfp.get_solution_file_path(alg, LANGUAGE, EXTENSION)
  with open(practice_file, "w") as f:
    f.write(get_starting_practice_text(solution_file))
    f.close()

def get_starting_practice_text(alg_sol_file: str) -> List[str]:
  line_to_copy = None
  with open(alg_sol_file, "r") as f:
    for line in f:
      line = line.strip()
      if line.startswith(PARAMETER_LINE_PREFIX):
        line_to_copy = line
        break   
  f.close()
  if not line_to_copy:
    raise RuntimeError("Could not find parameters in", alg_sol_file)
  return COMMENT_SYMBOL + " write 'solve' method in 'Attempt' class\n\n\n" + line_to_copy

def run_tests(alg: str) -> bool:
  practice_file_dir = gfp.get_practice_file_dir()
  practice_file = gfp.get_practice_file_path(LANGUAGE, EXTENSION)
  solution_file_dir = gfp.get_solution_file_dir(alg)
  solution_file = gfp.get_solution_file_path(alg, LANGUAGE, EXTENSION)
  test_file = gfp.get_test_file_path(alg)
  test_runner_dir = gfp.get_test_runner_dir_path(LANGUAGE)
  test_runner_file = gfp.get_test_runner_file_path(LANGUAGE, EXTENSION)
  match LANGUAGE:
    case "python":
      cmd = ["python", test_runner_file, practice_file, test_file]
    case "java":
      try:
        java_compile_if_necessary(practice_file, practice_file_dir)
      except RuntimeError as e:
        print(f"User code compilation failed:\n{e}", file=sys.stderr)
        return False
      try:
        java_compile_if_necessary(solution_file, solution_file_dir)
      except RuntimeError as e:
        print(f"Failed to compile solution for {alg}:\n", file=sys.stderr)
        raise e
      additional_dependencies = [practice_file_dir]
      try:
        java_compile_if_necessary(test_runner_file, test_runner_dir, additional_dependencies) 
      except RuntimeError as e:
        print(f"Failed the compile java test runner:\n")
        raise e
      runtime_cp_entries =[
        gfp.PROJECT_ROOT,
        test_runner_dir,
        practice_file_dir,
        solution_file_dir
      ]
      java_add_jars(runtime_cp_entries, test_runner_dir)

      additional_args = [alg, test_file]
      class_path_for_cmd = os.path.join(test_runner_dir, "Runner")
      class_path_for_cmd = class_path_for_cmd.replace(gfp.PROJECT_ROOT, "")
      class_path_for_cmd = class_path_for_cmd.replace(os.sep, "", 1)
      class_path_for_cmd = class_path_for_cmd.replace(os.sep, ".")
      gfp.PROJECT_ROOT
      cmd = ["java", "-cp", os.pathsep.join(runtime_cp_entries), class_path_for_cmd] + additional_args
    case _:
      raise NameError("Could not find language:", LANGUAGE)
    
  result = subprocess.run(cmd, cwd=test_runner_dir)
  if result.returncode != 0:
    print("Failed tests.", file=sys.stderr)
    return False
  return True

def java_to_class_path(file: str) -> str:
  if EXTENSION != ".java":
    raise ValueError("Only applicable for java.")
  if not file.endswith(EXTENSION):
    raise ValueError("file path must end in .java! given:", file)
  return file[:-len(EXTENSION)] + ".class"

def java_compile_if_necessary(java_file: str, cwd: str, additional_dependencies: List[str] = None) -> None:
  if not os.path.exists(java_file):
    raise ValueError(f"Could not find {java_file}")

  class_path = java_to_class_path(java_file)
  print("CLASS PATH", class_path)
  if os.path.exists(class_path) and os.path.getmtime(java_file) > os.path.getmtime(class_path):
    os.remove(class_path)
  if not os.path.exists(class_path): 
    cp_entries = [cwd]
    java_add_jars(cp_entries, cwd)
    if additional_dependencies:
      for d in additional_dependencies:
        cp_entries.append(d)
    cp = os.pathsep.join(cp_entries)
    compile_cmd = ["javac", "-cp", cp, java_file]
    result = subprocess.run(compile_cmd, cwd=cwd, capture_output=True, text=True) 
    if result.returncode == 0 and not os.path.exists(class_path):
      raise RuntimeError(f"Failed to compile into file {class_path}." +
                         " ensure the .java file contains a public class with the same name as the file")
    if result.returncode != 0:
      raise RuntimeError(f"Compilation failed:\n{result.stderr}")
  
def java_add_jars(cp_entries: List[str], dir: str) -> None:
  lib_dir = os.path.join(dir, "lib")
  if os.path.exists(lib_dir):
    for f in Path(lib_dir).iterdir(): 
      if f.name.endswith(".jar"):
        cp_entries.append(os.path.join(lib_dir, f.name))

if __name__ == "__main__":
  main()