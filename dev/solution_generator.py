import argparse
from util.enums import is_member, member_from_string, Language, SpecificAlgorithm, member_to_string
from util.file_paths import get_solution_file_path
from boilerplate.boilerplate import get_boilerplate
import os
import subprocess
from app import settings
from util.constants import SOLUTION_CLASS_NAME, SOLUTION_METHOD_NAME

def main() -> None:
  parser = argparse.ArgumentParser()
  parser.add_argument("--lang")
  parser.add_argument("--alg")

  args = parser.parse_args()
  if not args.lang or not is_member(Language, args.lang):
    raise RuntimeError("A valid language must be provided for solution generation.")
  lang: Language = member_from_string(Language, args.lang)
  
  if args.alg and not is_member(SpecificAlgorithm, args.alg):
    raise RuntimeError("The provided algorithm is invalid.")

  if args.alg:
    generate_specific_language_solution(
        member_from_string(SpecificAlgorithm, args.alg), lang)
  else:  
    generate_all_language_solutions(lang)
  
def generate_all_language_solutions(lang: Language) -> None:
  algs: list[SpecificAlgorithm] = list(SpecificAlgorithm)
  for alg in algs:
    generate_specific_language_solution(alg, lang)

def generate_specific_language_solution(alg: SpecificAlgorithm, lang: Language) -> None:
  alg_str = member_to_string(alg)
  lang_str = member_to_string(lang)

  solution_path = get_solution_file_path(alg, lang)
  if os.path.exists(solution_path):
    raise RuntimeError(f"Cannot generate solution when it already exists for {alg_str}.")
  
  # Get boilerplate
  template: str = get_boilerplate(
    alg,
    lang,
    settings["tab_size"]["value"],
    SOLUTION_CLASS_NAME,
    SOLUTION_METHOD_NAME
  )

  # Generate with api call
  

  # Test to ensure success
  cmd = ["python", "test.py", "--test", "run_tests", 
         "--lang", f"{lang_str}", f"--alg", f"{alg_str}"]
  res = subprocess.run(cmd)
  if res.returncode != 0:
    raise RuntimeError(f"Generated solution failed for {alg_str}.")
  else:
    print(f"Generated solution successful for {alg_str}.")


if __name__ == "__main__":
  main()