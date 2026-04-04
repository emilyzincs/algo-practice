import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SPECIFIC_TO_GEN_ALG = {
  "breadth_first_search": "reachable",
  "depth_first_search": "reachable",
  "merge_sort": "sort"
}

def to_language_file_case(str: str, lang: str) -> str:
  words = str.strip().split()
  match lang:
    case "python":
      return "_".join(words).lower()
    case "java":
      for i, word in enumerate(words):
        words[i] = word.capitalize()
        return "".join(words)
    case _:
      raise NameError("Could not find language", lang) 
    

def specific_to_general_alg(specific_alg: str) -> str:
  return SPECIFIC_TO_GEN_ALG.get(specific_alg, specific_alg)


def get_practice_file_dir() -> str:
  return os.path.join(PROJECT_ROOT, "practice")

def get_practice_file_path(lang: str, extension: str) -> str: 
  return os.path.join(get_practice_file_dir(), 
                      to_language_file_case("solution", lang) + extension)

def get_solution_file_dir(specific_alg: str) -> str:
  gen_alg = specific_to_general_alg(specific_alg)
  if gen_alg == specific_alg:
    return os.path.join(PROJECT_ROOT, "problems", specific_alg)
  else:
    return os.path.join(PROJECT_ROOT, "problems", gen_alg, specific_alg)

def get_solution_file_path(alg: str, lang: str, extension: str) -> str:
  return os.path.join(get_solution_file_dir(alg),
                      to_language_file_case("solution", lang) + extension)

def get_info_file_path(specific_alg: str) -> str:
  gen_alg = specific_to_general_alg(specific_alg)
  return os.path.join(get_solution_file_dir(gen_alg), "info.json")

def get_test_file_path(specific_alg: str) -> str:
  gen_alg = specific_to_general_alg(specific_alg)
  return os.path.join(get_solution_file_dir(gen_alg), "test.json")

def get_test_runner_dir_path(lang: str) -> str:
  return os.path.join(PROJECT_ROOT, "test_runners", lang.lower())

def get_test_runner_file_path(lang: str, extension: str) -> str:
  return os.path.join(get_test_runner_dir_path(lang), to_language_file_case("runner", lang) + extension)

def get_settings_path() -> str:
  return os.path.join(PROJECT_ROOT, "program_settings", "current.json")

def get_default_settings_path() -> str:
  return os.path.join(PROJECT_ROOT, "program_settings", "default.json")