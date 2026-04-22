import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from typing import assert_never
from util.enums import (
  DirectoryType,
  SpecificAlgorithm,
  GeneralAlgorithm,
  AlgorithmCategory,
  Language,
  member_to_string
)


# Changes the given 'string' to have capitalization consistent
# with a file name in the given Language, and returns it.
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
      assert_never(lang)


# ==============================================================
# PATHS
# =============================================================


def get_practice_file_dir() -> str:
  return os.path.join(PROJECT_ROOT, "practice")


def get_practice_file_path(lang: Language) -> str:
  return os.path.join(get_practice_file_dir(), 
                      to_language_file_case("solution", lang) + lang.extension)


def get_problems_dir() -> str:
  return os.path.join(PROJECT_ROOT, "problems")


def get_specific_alg_dir(specific_alg: SpecificAlgorithm) -> str:
  gen_alg: GeneralAlgorithm = specific_alg.general_type
  category: AlgorithmCategory = gen_alg.category

  return os.path.join(get_problems_dir(),
                        member_to_string(category),
                        member_to_string(gen_alg), 
                        member_to_string(specific_alg))


def get_solution_file_dir(specific_alg: SpecificAlgorithm) -> str:
  return get_specific_alg_dir(specific_alg)


def get_solution_file_path(alg: SpecificAlgorithm, lang: Language) -> str:
  return os.path.join(get_solution_file_dir(alg),
                      to_language_file_case("solution", lang) + lang.extension)


def get_category_dir(alg: SpecificAlgorithm):
  return os.path.join(get_problems_dir(), member_to_string(alg.category))


def get_gen_alg_dir(alg: SpecificAlgorithm) -> str:
  return os.path.join(get_category_dir(alg), member_to_string(alg.general_type))


def get_info_path(alg: SpecificAlgorithm) -> str:
  dir_type: DirectoryType = alg.info_dir
  dir_path: str
  match dir_type:
    case DirectoryType.SPECIFIC:
      dir_path = get_specific_alg_dir(alg)
    case DirectoryType.GENERAL:
      dir_path = get_gen_alg_dir(alg)
    case _:
      assert_never(dir_type)
  return os.path.join(dir_path, "info.json")


def get_test_path(alg: SpecificAlgorithm) -> str:
  dir_type: DirectoryType = alg.test_dir
  dir_path: str
  match dir_type:
    case DirectoryType.SPECIFIC:
      dir_path = get_specific_alg_dir(alg)
    case DirectoryType.GENERAL:
      dir_path = get_gen_alg_dir(alg)
    case _:
      assert_never(dir_type)
  return os.path.join(dir_path, "test.json")


def get_test_runner_dir_path(lang: Language) -> str:
  return os.path.join(PROJECT_ROOT, "user_testing", 
                      "test_runners", member_to_string(lang))


def get_test_runner_file_path(lang: Language) -> str:
  orch_path = os.path.join(get_test_runner_dir_path(lang), "orchestrator.py")
  if os.path.exists(orch_path):
    return orch_path
  else:
    return os.path.join(get_test_runner_dir_path(lang), 
                      to_language_file_case("runner", lang) + lang.extension)


def get_settings_path() -> str:
  return os.path.join(PROJECT_ROOT, "user_settings", "current.json")


def get_default_settings_path() -> str:
  return os.path.join(PROJECT_ROOT, "user_settings", "default.json")


def get_abstract_test_dir() -> str:
  return os.path.join(PROJECT_ROOT, "app_tests")


def get_test_generator_dir() -> str:
  return os.path.join(PROJECT_ROOT, "user_testing", "test_generation")


def get_test_generator_path(alg: SpecificAlgorithm) -> str:
  return os.path.join(get_test_generator_dir(),
                      "problems",
                      member_to_string(alg.category),
                      member_to_string(alg.general_type),
                      alg.generator_file_name + ".py")


def get_boilerplate_dir() -> str:
  return os.path.join(PROJECT_ROOT, "boilerplate")


def get_boilerplate_language_file_path(lang: Language) -> str:
  return os.path.join(get_boilerplate_dir(), "language", 
                                            member_to_string(lang) + ".py")
