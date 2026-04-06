import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from util.exceptions import UnhandledCaseException
from typing import assert_never
from util.enums import (
  SpecificAlgorithm,
  GeneralAlgorithm,
  SPECIFIC_ALG_TO_GENERAL,
  Language,
  member_to_string
)

def to_language_file_case(string: str, lang: Language) -> str:
  words = string.strip().split()
  match lang:
    case Language.PYTHON:
      return "_".join(words).lower()
    case Language.JAVA:
      for i, word in enumerate(words):
        words[i] = word.capitalize()
      return "".join(words)
    case _:
      assert_never()
    
def get_practice_file_dir() -> str:
  return os.path.join(PROJECT_ROOT, "practice")

def get_practice_file_path(lang: Language) -> str:
  return os.path.join(get_practice_file_dir(), 
                      to_language_file_case("solution", lang) + lang.extension)

def get_solution_file_dir(specific_alg: SpecificAlgorithm) -> str:
  gen_alg: GeneralAlgorithm = SPECIFIC_ALG_TO_GENERAL[specific_alg]
  if gen_alg == specific_alg:
    return os.path.join(PROJECT_ROOT, "problems", member_to_string(specific_alg))
  else:
    return os.path.join(PROJECT_ROOT, "problems", member_to_string(gen_alg), 
                        member_to_string(specific_alg))

def get_solution_file_path(alg: SpecificAlgorithm, lang: Language) -> str:
  return os.path.join(get_solution_file_dir(alg),
                      to_language_file_case("solution", lang) + lang.extension)

def get_gen_alg_dir(alg: GeneralAlgorithm) -> str:
  return os.path.join(PROJECT_ROOT, "problems", member_to_string(alg))

def get_info_file_path(specific_alg: SpecificAlgorithm) -> str:
  gen_alg: GeneralAlgorithm = SPECIFIC_ALG_TO_GENERAL[specific_alg]
  return os.path.join(get_gen_alg_dir(gen_alg), "info.json")

def get_test_file_path(specific_alg: SpecificAlgorithm) -> str:
  gen_alg: GeneralAlgorithm = SPECIFIC_ALG_TO_GENERAL[specific_alg]
  return os.path.join(get_gen_alg_dir(gen_alg), "test.json")

def get_test_runner_dir_path(lang: Language) -> str:
  return os.path.join(PROJECT_ROOT, "test_runners", member_to_string(lang))

def get_test_runner_file_path(lang: Language) -> str:
  return os.path.join(get_test_runner_dir_path(lang), 
                      to_language_file_case("runner", lang) + lang.extension)

def get_settings_path() -> str:
  return os.path.join(PROJECT_ROOT, "program_settings", "current.json")

def get_default_settings_path() -> str:
  return os.path.join(PROJECT_ROOT, "program_settings", "default.json")

def get_abstract_test_dir() -> str:
  return os.path.join(PROJECT_ROOT, "tests")

def get_test_generator_path(specific_alg: SpecificAlgorithm) -> str:
  gen_alg = SPECIFIC_ALG_TO_GENERAL[specific_alg]
  return os.path.join(PROJECT_ROOT, "test_generation", "problems", 
                      member_to_string(gen_alg) + ".py")