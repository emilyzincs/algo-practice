import unittest
from unittest.mock import patch
import os
from util.utils import is_type, string_to_bool
from commands.practice.practice import run_tests
from util.get_file_paths import (PROJECT_ROOT, get_solution_file_dir, 
                                 get_solution_file_path, to_language_file_case,
                                 get_abstract_test_dir)
from typing import Optional
from app import ALG_LIST, LANGUAGE_LIST, LANGUAGE_TO_EXTENSION_AND_COMMENT_SYMBOL

UNIT_TESTS = {"run_tests", "solution"}

class AbstractTestRunTests(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def setUp(self):
    self.gfp_base = "commands.practice.practice.gfp."
    self.language = os.environ["TEST_LANGUAGE"] if "TEST_LANGUAGE" in os.environ else None
    self.num = os.environ["TEST_NUM"] if "TEST_NUM" in os.environ else None
    self.alg = os.environ["TEST_ALG"] if "TEST_ALG" in os.environ else None
    self.do_debug = os.environ["TEST_DEBUG"] if "TEST_DEBUG" in os.environ else "False"

    if self.language is not None and self.language not in LANGUAGE_TO_EXTENSION_AND_COMMENT_SYMBOL:
      raise ValueError(f"Unrecognized language: {self.language}.")
    
    if self.num is not None and not is_type(self.num, int):
      raise ValueError(f"Num must be of type int. Was {type(self.num)}." +
                       f" Value: {self.num}.")
    if self.num is not None:
      self.num = int(self.num)

    if self.alg is not None and self.alg not in ALG_LIST:
      raise ValueError(f"Unrecognized alg: {self.alg}.")
    
    self.do_debug = string_to_bool(self.do_debug)

  
  def test_main(self) -> None:
    if self.language is not None:
      self.run_language_tests(self.language)
    else:
      for language in LANGUAGE_LIST:
        self.run_language_tests(language)

  def run_language_tests(self, language: str):
    extension = LANGUAGE_TO_EXTENSION_AND_COMMENT_SYMBOL[language][0]
    practice_file_name_prefix = to_language_file_case("sol", language)
    required_class_name_prefix = None
    practice_file_dir = os.path.join(get_abstract_test_dir(), language, "solution_files")

    if language == "java":
      required_class_name_prefix = "Sol"
    self.abstract_test_run_tests(
      language,
      extension,
      practice_file_dir,
      practice_file_name_prefix,
      required_class_name_prefix
    )
    self.abstract_test_solutions(language, extension)  

  def specific_test_run_test(
      self,
      test_number: int,
      language: str,
      expected: bool,
      extension: str, 
      info_path: str,
      test_path: str,
      practice_file_path: str,
      required_class_name_prefix: Optional[str] = None,
  ) -> None:
      print(f"\nRunning {language} run_test test {test_number}:")
      with (
        patch(self.gfp_base + "get_test_file_path", return_value=test_path),
        patch(self.gfp_base + "get_info_file_path", return_value=info_path),
        patch(self.gfp_base + "get_practice_file_path", return_value=practice_file_path)
      ):
        result = (
          run_tests("", language, extension, self.do_debug, str(self.do_debug)) if not required_class_name_prefix
          else run_tests("", language, extension, self.do_debug, 
                          str(self.do_debug), required_class_name_prefix + str(test_number))
        )
      error_msg = (f"Expected test {test_number} to succeed but it failed." 
                  if expected
                  else f"Expected test {test_number} to fail but it succeeded.")
      self.assertEqual(expected, result, error_msg)
      print("Test passed.")      

  def abstract_test_run_tests(
      self,
      language: str,
      extension: str, 
      practice_file_dir: str,
      practice_file_name_prefix: str,
      required_class_name_prefix: Optional[str] = None,
  ) -> None:
    expected_values = [None, # 0
      True, False, True, True, True, # 5
      True, True, False, True, False, # 10
      False, True, True, True,  True, # 15
      False, True, True, True, True, # 20
      True, True, True, False, True, # 25
      False,
    ]
    info_path_prefix = self.get_info_path_prefix()
    test_path_prefix = self.get_test_path_prefix()
    practice_file_prefix = os.path.join(practice_file_dir, practice_file_name_prefix)
    with patch(self.gfp_base + "get_practice_file_dir", return_value=practice_file_dir):
      if self.num is not None:
        if self.num < 0 or len(expected_values) <= self.num:
          raise ValueError(f"Invalid test number: {self.num}.")
        info_path, test_path, practice_file_path = self.get_paths(
          info_path_prefix, 
          test_path_prefix, 
          practice_file_prefix,
          self.num,
          extension,
          expected_values
        )
        self.specific_test_run_test(
          self.num,
          language,
          expected_values[self.num],
          extension,
          info_path,
          test_path,
          practice_file_path,
          required_class_name_prefix
        )
      else: 
        print("\n\nRUNNING " + language.upper() + " run_test TESTS.")
        for i in range(1, len(expected_values)):
          info_path, test_path, practice_file_path = self.get_paths(
            info_path_prefix, 
            test_path_prefix, 
            practice_file_prefix,
            i,
            extension,
            expected_values
          )

          self.specific_test_run_test(
            i,
            language,
            expected_values[i],
            extension,
            info_path,
            test_path,
            practice_file_path,
            required_class_name_prefix
          )
        print("Done.")

  def get_paths(
    self,
    info_path_prefix: str, 
    test_path_prefix: str, 
    practice_file_prefix: str, 
    i: int, 
    extension: str,
    expected_values: list[bool]
  ):
    if i < 1 or len(expected_values) <= i:
      raise RuntimeError(f"Invalid test number: {i}.")
    info_path = info_path_prefix + f"{i}.json"
    test_path = test_path_prefix + f"{i}.json"
    practice_file_path = practice_file_prefix + f"{i}{extension}"
    if not (os.path.exists(test_path) == 
            os.path.exists(info_path) == os.path.exists(practice_file_path)):
      raise RuntimeError("Test file must exist iff info file exists iff practice file exists." +
                        " Violated for paths:\n" +
                        f"test_path: {test_path},\n" +
                        f"info_path: {info_path},\n" +
                        f"practice_file_path: {practice_file_path}")
    if not os.path.exists(test_path): 
      raise RuntimeError(f"Files for test {i} do not exist.")
    return info_path, test_path, practice_file_path

  def specific_test_solution(self, alg: str, language: str, extension: str) -> None:
    print(f"\nTesting {language} solution for {alg}.")
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
      result = run_tests(alg, language, extension, self.do_debug)
      error_msg = f"Solution for {alg} in {language} failed."
      self.assertEqual(True, result, error_msg)
      print("Solution correct.")

  def abstract_test_solutions(
      self,
      language: str,
      extension: str   
  ) -> None:
    if self.alg is not None:
      self.specific_test_solution(self.alg, language, extension)
    else:
      print("\n\nRUNNING " + language.upper() + " ALGORITHM SOLUTION TESTS.")
      for alg in ALG_LIST:
        self.specific_test_solution(alg, language, extension)
      print("Done.")

  def get_test_path_prefix(self) -> str:
    return os.path.join(PROJECT_ROOT, "tests", "json_files", "test")
  
  def get_info_path_prefix(self) -> str:
    return os.path.join(PROJECT_ROOT, "tests", "json_files", "info")
