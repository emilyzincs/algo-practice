from typing import List
import os.path
import time
import get_file_paths as gfp
import sys
from utils import read_json, copy_file
from pathlib import Path
from commands.main_menu import handle_commands as main_menu_handle_commands
from commands.practice.practice import handle_commands as practice_handle_commands
from commands.settings import handle_commands as settings_handle_commands

if not os.path.exists(gfp.get_settings_path()):
  actual_settings = gfp.get_settings_path()
  default_settings = gfp.get_default_settings_path()
  copy_file(default_settings, actual_settings)

settings, settings_file = read_json(gfp.get_settings_path())

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
LANGUAGES = set(LANGUAGE_LIST)
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

LOCAL_COMMANDS = {
  "main_menu": {"lang", "language", "langs", "languages", "algs", 
                "algorithms", "settings"},
  "practice": {"d", "done"},
  "settings": ({"list"}, {"default_language"})
}
LOCAL_COMMANDS['main_menu'].update(LANGUAGE_LIST)
settings_file.close()

def main():  
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

def handle_practice(alg: str) -> float:
  reset_practice_file(alg)
  start_time = time.perf_counter()
  completed = practice_handle_commands(
    LOCAL_COMMANDS['practice'],
    alg,
    LANGUAGE,
    EXTENSION,
    exit_program
  )
  end_time = time.perf_counter() if completed else start_time - 1
  total_time = end_time - start_time
  return total_time

def reset_practice_file(alg: str) -> None:
  practice_file = gfp.get_practice_file_path(LANGUAGE, EXTENSION)
  solution_file = gfp.get_solution_file_path(alg, LANGUAGE, EXTENSION)
  with open(practice_file, "w", encoding="utf-8") as f:
    f.write(get_starting_practice_text(solution_file))
    f.close()

def get_starting_practice_text(alg_sol_file: str) -> List[str]:
  line_to_copy = None
  with open(alg_sol_file, "r", encoding="utf-8") as f:
    for line in f:
      line = line.strip()
      if line.startswith(PARAMETER_LINE_PREFIX):
        line_to_copy = line
        break   
  f.close()
  if not line_to_copy:
    raise RuntimeError("Could not find parameters in", alg_sol_file)
  return COMMENT_SYMBOL + " write 'solve' method in 'Attempt' class\n\n\n" + line_to_copy

def handle_settings() -> None:
  settings_handle_commands(
    LOCAL_COMMANDS['settings'],
    LANGUAGES,
    exit_program
  )

def exit_program() -> None:
  sys.exit(0)

if __name__ == "__main__":
  main()