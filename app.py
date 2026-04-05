from typing import List
import os.path
import time
import util.get_file_paths as gfp
import sys
import shutil
from util.utils import read_json, copy_file, match_json_keys, no_op, load_module_from_path
from util.exceptions import UnhandledCaseException
from commands.main_menu import handle_commands as main_menu_handle_commands
from commands.practice.practice import handle_commands as practice_handle_commands
from commands.settings import handle_commands as settings_handle_commands
from commands.practice.java import path_to_package
import util.boilerplate as bp

default_settings_path = gfp.get_default_settings_path()
settings_path = gfp.get_settings_path()
if not os.path.exists(settings_path):
  copy_file(default_settings_path, settings_path)

match_json_keys(default_settings_path, settings_path)
settings = read_json(settings_path)

DEBUG = False
ALG_NAME_TO_IDX = {
  "binary search": 0,
  "bfs": 1,
  "breadth first search": 1,
  "dfs": 2,
  "depth first search": 2,
  "merge sort": 3
}
ALG_LIST = [
  "binary_search",
  "breadth_first_search",
  "depth_first_search",
  "merge_sort"
]
NUM_ALGS = len(ALG_LIST)
TAB = "  "
SOLUTION_CLASS_NAME = "Solution"
SOLUTION_FUNCTION_NAME = "solve"
LANGUAGE_LIST = [
  "python",
  "java",
]
LANGUAGES = set(LANGUAGE_LIST)
DEFAULT_LANGUAGE = settings['default_language']
LANGUAGE_TO_EXTENSION_AND_COMMENT_SYMBOL = {
  "python": (".py", "#"),
  "java": (".java", "//"),
}

LANGUAGE = DEFAULT_LANGUAGE
if __name__ == "__main__":
  if len(sys.argv) > 2:
    raise ValueError(f"Usage: python {sys.argv[0]} language (default is python)")
  elif len(sys.argv) == 2:
    lang = sys.argv[1].strip().lower()
    if lang not in LANGUAGE_TO_EXTENSION_AND_COMMENT_SYMBOL:
      if __name__ == "__main__":
        print(f"Unsupported language: {lang}. defaulting to {DEFAULT_LANGUAGE}." + 
              " Type 'languages' for supported languages or <language> to switch to that language.")
    else:
      LANGUAGE = lang

EXTENSION, COMMENT_SYMBOL = LANGUAGE_TO_EXTENSION_AND_COMMENT_SYMBOL[LANGUAGE]
PARAMETER_LINE_PREFIX = COMMENT_SYMBOL + " parameters:"

LOCAL_COMMANDS = {
  "main_menu": {"lang", "language", "langs", "languages", "algs", 
                "algorithms", "s", "settings"},
  "practice": {"d", "done", "s", "sol", "solution"},
  "settings": {"list", "reset"}
}
LOCAL_COMMANDS['main_menu'].update(LANGUAGE_LIST)

def main():  
  try:  
    main_menu_handle_commands(
      LOCAL_COMMANDS['main_menu'],
      get_language,
      LANGUAGE_LIST,
      LANGUAGE_TO_EXTENSION_AND_COMMENT_SYMBOL,
      set_language,
      ALG_LIST,
      ALG_NAME_TO_IDX,
      NUM_ALGS,
      TAB,
      handle_practice,
      handle_settings,
      exit_program
  )
  except (Exception, KeyboardInterrupt) as e:
    if not (isinstance(e, KeyboardInterrupt) or isinstance(e, EOFError)):
      if not DEBUG:
        print(f"Encountered error while running the program:\n{e}", file=sys.stderr)
      else:
        raise e
    else:
      print()
    exit_program(1)

def get_language() -> str:
  return LANGUAGE

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

def handle_practice(alg: str) -> float|None:
  generate_test_file_if_necessary(alg)
  reset_practice_file(alg)
  seconds_spent = practice_handle_commands(
    LOCAL_COMMANDS['practice'],
    alg,
    LANGUAGE,
    EXTENSION,
    delete_all_attempts if settings['delete_attempts'] else no_op,
    load_solution_into_practice,
    exit_program
  )
  return seconds_spent

def generate_test_file_if_necessary(alg: str) -> None:
  test_file_path = gfp.get_test_file_path(alg)
  if os.path.exists(test_file_path):
    return
  print(f"Generating {alg} tests...")
  test_generator_path = gfp.get_test_generator_path(alg)
  if not os.path.exists(test_generator_path):
    raise RuntimeError(f"Tests for {alg} do not exist (path: {test_file_path})" +
                       f" and test_generator for {alg} does not exist" +
                       f" (path: {test_generator_path})")
  try:
    test_generator = load_module_from_path("generate", test_generator_path)
  except ModuleNotFoundError:
    raise ModuleNotFoundError(f"Test generator for {alg} has no 'generate' method." + 
                              f" Path: {test_generator}.")
  test_generator.generate()

def reset_practice_file(alg: str) -> None:
  practice_file = gfp.get_practice_file_path(LANGUAGE, EXTENSION)
  info_file = gfp.get_info_file_path(alg)
  with open(practice_file, "w", encoding="utf-8") as f:
    f.write(get_starting_practice_text(info_file))
  print(f"Set up practice file: {practice_file} (cmd + click to open).")

def get_starting_practice_text(info_file_path: str) -> List[str]:
  if not os.path.exists(info_file_path):
    raise RuntimeError(f"Info file path does not exist: {info_file_path}.")
  data = read_json(info_file_path)
  parameter_names = data['parameter_names']
  if settings["prepopulate_boilerplate"] == False:
    parameter_info_line = COMMENT_SYMBOL + " Parameters: " + ", ".join(parameter_names) + "."
    return (COMMENT_SYMBOL + 
          f" Write '{SOLUTION_FUNCTION_NAME}' method in '{SOLUTION_CLASS_NAME}' class.\n\n" 
          + parameter_info_line)
  else:
    input_types = data["input_types"]
    expected_type = data["expected_type_wrapper"]
    user_tab_size = settings["tab_size"]
    one_indent = " " * user_tab_size
    return bp.get_boilerplate_text(
      parameter_names,
      input_types, 
      expected_type, 
      one_indent,
      SOLUTION_CLASS_NAME,
      SOLUTION_FUNCTION_NAME,
      LANGUAGE
    )

def load_solution_into_practice(alg: str) -> None:
  practice_file_dir = gfp.get_practice_file_dir()
  practice_file = gfp.get_practice_file_path(LANGUAGE, EXTENSION)
  if not os.path.exists(practice_file):
    raise RuntimeError(f"Practice file does not exist: {practice_file}.")
  solution_file = gfp.get_solution_file_path(alg, LANGUAGE, EXTENSION)
  if not os.path.exists(solution_file):
    raise FileNotFoundError(f"Solution file does not exist: {solution_file}.")
  match LANGUAGE:
    case "python":
      pass
    case "java":
      lines = None
      with open(solution_file, "r", encoding="utf-8") as sol:
        lines = sol.readlines()
        new_package_line = "package " + path_to_package(practice_file_dir, gfp.PROJECT_ROOT) + ";\n"
        replaced_package = False
        for i, line in enumerate(lines):
          if line.strip().startswith("package"):
            lines[i] = new_package_line
            replaced_package = True
        if not replaced_package:
          lines.insert(0, new_package_line)
      if lines is None:
        raise RuntimeError(f"Did not read lines from solution file: {solution_file}.")
      with open(practice_file, "w", encoding="utf-8") as prac:
        prac.writelines(lines)
      return
    case _:
      raise UnhandledCaseException(LANGUAGE, "language")
  copy_file(solution_file, practice_file)


def handle_settings() -> None:
  settings_handle_commands(
    LOCAL_COMMANDS['settings'],
    LANGUAGES,
    TAB,
    refresh_settings,
    exit_program
  )

def refresh_settings() -> None:
  global settings 
  settings = read_json(settings_path)

def delete_all_attempts() -> None:
  practice_file_dir = gfp.get_practice_file_dir()
  if not os.path.exists(practice_file_dir) or not os.path.isdir(practice_file_dir):
    raise RuntimeError(f"Incorrect path: {practice_file_dir}.")
  shutil.rmtree(practice_file_dir)
  os.makedirs(practice_file_dir)

def exit_program(code: int) -> None:
  print("Exiting...")
  if settings['delete_attempts']:
    delete_all_attempts()
  sys.exit(code)

if __name__ == "__main__":
  main()
