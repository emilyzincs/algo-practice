import sys
sys.path.insert(0, ".") # add the project root
import argparse
from util.enums import is_member, member_from_string, Language, SpecificAlgorithm, member_to_string, member_to_capitalized_words
from util.file_paths import get_solution_file_path, PROJECT_ROOT
from boilerplate.boilerplate import get_boilerplate
import os
import subprocess
from app import settings
from util.constants import SOLUTION_CLASS_NAME, SOLUTION_METHOD_NAME
from dev.llm_api.abstract import get_response


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
    generate_specific_solution(
        member_from_string(SpecificAlgorithm, args.alg), lang)
  else:  
    generate_all_solutions(lang)
  

def generate_all_solutions(lang: Language) -> None:
  algs: list[SpecificAlgorithm] = list(SpecificAlgorithm)
  for alg in algs:
    generate_specific_solution(alg, lang)


def generate_specific_solution(alg: SpecificAlgorithm, lang: Language) -> None:
  alg_str = member_to_string(alg)
  lang_str = member_to_string(lang)

  solution_path = get_solution_file_path(alg, lang)
  if os.path.exists(solution_path):
    raise RuntimeError(f"Cannot generate solution when it already exists for {alg_str}.")
  
  # Get boilerplate
  boilerplate: str = get_boilerplate(
    alg,
    lang,
    settings["tab_size"]["value"],
    SOLUTION_CLASS_NAME,
    SOLUTION_METHOD_NAME,
    solution_path
  )

  # Generate with api call
  prompt = get_prompt(alg, lang, boilerplate)
  # response: str = get_response(prompt)

  # Write the solution file
  with open(solution_path, "w", encoding="utf-8") as f:
    f.write(response)

  # Test to ensure success
  cmd = ["python", "test.py", "--test", "run_tests", 
         "--lang", f"{lang_str}", f"--alg", f"{alg_str}"]
  res = subprocess.run(cmd)
  if res.returncode != 0:
    raise RuntimeError(f"Generated solution failed for {alg_str}.")
  else:
    print(f"Generated solution successful for {alg_str}.")


def get_prompt(alg: SpecificAlgorithm, lang: Language, boilerplate: str) -> str:
  # use that every algorithm has a python solution
  python_solution_file = get_solution_file_path(alg, Language.PYTHON)
  with open(python_solution_file, "r", encoding="utf-8") as f:
    python_solution_contents = f.read()

  alg_name = member_to_capitalized_words(alg)
  lang_name = member_to_capitalized_words(lang)
  solution_path = get_solution_file_path(alg, lang)

  prompt = (
    "You are an expert in algorithms and data structures "
    "and you are very familiar with all famous computer science "
    f"algorithms. Write a canonical implementation of the {alg_name} "
    f"algorithm in {lang_name} by filling in the following template:\n"
    f"'{boilerplate}'.\n"
    "You may add to the template, but do NOT change/remove any original part of it. "
    "Use the algorithm description and method signature given in the template "
    "to accurately derive any necessary implementation details that may otherwise "
    "be ambigious. To further disambiguate, the implementation you write should " \
    "exactly match the behavior of the following Python implementation:\n"
    f"'{python_solution_contents}'.\n"
    "Depending on the language, you may also find it useful to know that "
    f"your reponse will be located in a file with path "
    f"{solution_path[len(PROJECT_ROOT):]}. "
    "Respond with only the implementation and nothing else."
  )
  print("PROMPT:", prompt)
  
  return prompt


if __name__ == "__main__":
  main()