import os
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

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

def get_practice_file_dir() -> str:
  return os.path.join(PROJECT_ROOT, "practice")

def get_practice_file_path(lang: str, extension: str) -> str: 
  return os.path.join(get_practice_file_dir(), 
                      to_language_file_case("attempt", lang) + extension)

def get_solution_file_dir(alg: str):
  return os.path.join(PROJECT_ROOT, "problems", alg)

def get_solution_file_path(alg: str, lang: str, extension: str) -> str:
  print("THE SOLUTION FILE PATH EXTENSION IS", extension)
  return os.path.join(get_solution_file_dir(alg),
                      to_language_file_case("solution", lang) + extension)

def get_test_file_path(alg: str) -> str:
  return os.path.join(PROJECT_ROOT, "tests", alg + "_test.json")

def get_test_runner_dir_path(lang: str) -> str:
  return os.path.join(PROJECT_ROOT, "test_runners", lang.lower())

def get_test_runner_file_path(lang: str, extension: str) -> str:
  return os.path.join(get_test_runner_dir_path(lang), "runner" + extension)