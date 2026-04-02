import unittest
from unittest.mock import patch
import os
from utils import is_type
from commands.practice.practice import run_tests
from get_file_paths import PROJECT_ROOT, get_solution_file_dir, get_solution_file_path
from typing import Optional
from app import ALG_LIST

class AbstractTestRunTests(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.gfp_base = "commands.practice.practice.gfp."
    self.debug = False
    self.specific_test = os.getenv("SPECIFIC_TEST").strip().lower()

  def abstract_test_run_tests(
      self,
      language: str,
      extension: str, 
      practice_file_dir: str,
      practice_file_name_prefix: str,
      required_class_name_prefix: Optional[str] = None,
  ):
    if self.specific_test and not is_type(self.specific_test, int):
      print("\n\nSKIPPING " + language.upper() + " run_test TESTS.")
      return
    print("\n\nRUNNING " + language.upper() + " run_test TESTS.")
    expected_values = [
      True,
      False,
      False,
      True,
      True, # 5
      True,
      True,
      False,
      True,
      False, # 10
      False,
      True,
      True,
      True, 
      True, # 15
      False,
      True,
      True,
      True,
      True, # 20
      True,
      True,
      True,
      False,
      True, # 25
      False,
    ]
    test_number = int(self.specific_test) if self.specific_test and is_type(self.specific_test, int) else None
    json_path_prefix = self.get_json_path_prefix()
    practice_file_prefix = os.path.join(practice_file_dir, practice_file_name_prefix)
    i = test_number if test_number is not None else 1
    with patch(self.gfp_base + "get_practice_file_dir", return_value=practice_file_dir):
      while True:
        json_path = json_path_prefix + f"{i}.json"
        practice_file_path = practice_file_prefix + f"{i}{extension}"
        if os.path.exists(json_path) != os.path.exists(practice_file_path):
          raise RuntimeError("Json path must exist iff practice file exists." +
                            " Violated for paths:\n" +
                            f"json_path: {json_path},\n" +
                            f"practice_file_path: {practice_file_path}")
        if not os.path.exists(json_path) or test_number and i != test_number:
          print(f"Done.")
          break
        print(f"\nRunning test {i}:")
        with (
          patch(self.gfp_base + "get_test_file_path", return_value=json_path),
          patch(self.gfp_base + "get_practice_file_path", return_value=practice_file_path)
        ):
          result = (
            run_tests("", language, extension, self.debug) if not required_class_name_prefix
            else run_tests("", language, extension, self.debug, required_class_name_prefix + str(i))
          )
        expected = expected_values[i-1]
        error_msg = (f"Expected test {i} to succeed but it failed." 
                    if expected
                    else f"Expected test {i} to fail but it succeeded.")
        self.assertEqual(expected, result, error_msg)
        print("Test passed.")      
        i += 1
  
  def abstract_test_solutions(
      self,
      language: str,
      extension: str   
  ) -> None:
    if self.specific_test and self.specific_test not in ALG_LIST:
      print("\nSKIPPING " + language.upper() + " ALGORITHM SOLUTION TESTS.")
      return
    print("\n\nRUNNING " + language.upper() + " ALGORITHM SOLUTION TESTS.")
    specific_alg = self.specific_test if self.specific_test else None

    def abstract_test_alg_solution(alg: str, language: str, extension: str) -> None:
      print(f"\nTesting solution for {alg}.")
      solution_file_dir = get_solution_file_dir(alg)
      solution_file = get_solution_file_path(alg, language, extension)
      self.assertEqual(True, os.path.exists(solution_file_dir), f"Path {solution_file_dir} does not exist.")
      if not os.path.exists(solution_file):
        print(f"Path {solution_file} does not exist.\nContinuing.")
        return
      with (patch(self.gfp_base + "get_practice_file_dir", 
                  return_value=solution_file_dir), 
            patch(self.gfp_base + "get_practice_file_path", 
                  return_value=solution_file)):
        result = run_tests(alg, language, extension, self.debug)
        error_msg = f"Solution for {alg} in {language} failed."
        self.assertEqual(True, result, error_msg)
        print("Solution correct.")

    if specific_alg is not None:
      abstract_test_alg_solution(specific_alg, language, extension)
    else:
      for alg in ALG_LIST:
        abstract_test_alg_solution(alg, language, extension)
    print("Done.")

  def get_json_path_prefix(self) -> str:
    return os.path.join(PROJECT_ROOT, "tests", "practice_run_tests", "json_files", "test")
