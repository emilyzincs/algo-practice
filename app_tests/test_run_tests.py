from unittest.mock import patch
import os
from menu.practice import run_tests
from util.file_paths import (PROJECT_ROOT, get_solution_file_dir, 
                                 get_solution_file_path, to_language_file_case,
                                 get_abstract_test_dir)
from typing import Optional, assert_never
from app import generate_test_file_if_necessary
from app_tests.base_test import BaseTest as parent
from util.enums import (
  Language,
  member_to_string,
  SpecificAlgorithm,
  member_to_capitalized_words
)


# Tests that testing user implementations works correctly.
class TestRunTests(parent):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def setUp(self) -> None:
    super().setUp()
    self.fp_base = "user_testing.test.fp."  # for mocking file paths for the tests

  # Runs the tests.
  def test_run_tests(self) -> None:
    if self.language is not None:
      self.run_language_tests(self.language)
    else:
      for language in Language:
        self.run_language_tests(language)

  # Runs tests for the given Language.
  def run_language_tests(self, language: Language):
    practice_file_name_prefix = to_language_file_case("sol", language)
    required_class_name_prefix = None
    practice_file_dir = os.path.join(get_abstract_test_dir(), "language",
                                     member_to_string(language), "solution_files")
    match language:
      case Language.PYTHON:
        pass
      case Language.JAVA:
        required_class_name_prefix = "Sol"
      case _:
        assert_never(language)

    self.language_test_run_tests(
      language,
      practice_file_dir,
      practice_file_name_prefix,
      required_class_name_prefix
    )
    self.language_test_solutions(language)  

  # Runs test number 'test_number' for language 'language' that does not correspond
  #   to an actual algorithm implementation.
  # Returns True if the test is successful, False if the info, test, and practice
  #   files for the test do not exist.
  # Raises and error if the test fails for other reasons.
  def specific_test_run_test(
      self,
      test_number: int,
      language: Language,
      expected: bool,
      info_path_prefix: str,
      test_path_prefix: str,
      practice_file_path_prefix: str,
      total_tests,
      required_class_name_prefix: Optional[str] = None,
  ) -> None:
      print(f"\nRunning {member_to_capitalized_words(language)} run_test test {test_number}:")
      info_path, test_path, practice_file_path = self.get_paths(
        info_path_prefix, 
        test_path_prefix, 
        practice_file_path_prefix,
        test_number,
        language.extension,
        total_tests
      )
      with (
        patch(self.fp_base + "specific_alg_to_test_path", return_value=test_path),
        patch(self.fp_base + "specific_alg_to_info_path", return_value=info_path),
        patch(self.fp_base + "get_practice_file_path", return_value=practice_file_path)
      ):
        dummy: SpecificAlgorithm = SpecificAlgorithm.BINARY_SEARCH
        result = (
          run_tests(dummy, language, self.do_debug, str(self.do_debug)) if not required_class_name_prefix
          else run_tests(dummy, language, self.do_debug, 
                          str(self.do_debug), required_class_name_prefix + str(test_number))
        )
      error_msg = (f"Expected test {test_number} to succeed but it failed." 
                  if expected
                  else f"Expected test {test_number} to fail but it succeeded.")
      self.assertEqual(expected, result, error_msg)
      print("Test passed.")      

  # Runs tests for the given Language that do not correspond to actual
  # algorithm implementations. 
  def language_test_run_tests(
      self,
      language: Language,
      practice_file_dir: str,
      practice_file_name_prefix: str,
      required_class_name_prefix: Optional[str] = None,
  ) -> None:
    expected_values = [
      True, False, True, True, True, # 5
      True, True, False, True, False, # 10
      False, True, True, True,  True, # 15
      False, True, True, False, False, # 20
      True
    ]
    total_tests = len(expected_values)
    info_path_prefix = self.get_info_path_prefix()
    test_path_prefix = self.get_test_path_prefix()
    practice_file_path_prefix = os.path.join(practice_file_dir, practice_file_name_prefix)
    with patch(self.fp_base + "get_practice_file_dir", return_value=practice_file_dir):
      if self.num is not None:
        self.specific_test_run_test(
          self.num,
          language,
          expected_values[self.num-1],
          info_path_prefix,
          test_path_prefix,
          practice_file_path_prefix,
          total_tests,
          required_class_name_prefix
        )
      elif self.alg is not None:
        return
      else: 
        print("\n\nRUNNING " + member_to_capitalized_words(language) + " run_test TESTS.")
        for i in range(1, len(expected_values) + 1):
          self.specific_test_run_test(
            i,
            language,
            expected_values[i-1],
            info_path_prefix,
            test_path_prefix,
            practice_file_path_prefix,
            total_tests,
            required_class_name_prefix
          )
        print("Done.")

  # Returns a tuple containing the info, test, and practice file path strings corresponding
  #   to the given prefixes, number, and extension, or None if all paths do not exist.
  # Raises RuntimeError if exactly one or two of the file paths exist.
  def get_paths(
    self,
    info_path_prefix: str, 
    test_path_prefix: str, 
    practice_file_prefix: str, 
    i: int, 
    extension: str,
    total_tests: int
  ) -> tuple[str, str, str]:
    if i < 1 or total_tests + 1 <= i:
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

  def specific_test_solution(self, alg: SpecificAlgorithm, language: Language) -> None:
    print(f"\nTesting {member_to_capitalized_words(language)} solution for {member_to_capitalized_words(alg)}.")
    solution_file_dir = get_solution_file_dir(alg)
    solution_file = get_solution_file_path(alg, language)
    self.assertEqual(True, os.path.exists(solution_file_dir), f"Path {solution_file_dir} does not exist.")
    if not os.path.exists(solution_file):
      print(f"Path {solution_file} does not exist.\nContinuing.")
      return
    generate_test_file_if_necessary(alg)
    with (patch(self.fp_base + "get_practice_file_dir", 
                return_value=solution_file_dir), 
          patch(self.fp_base + "get_practice_file_path", 
                return_value=solution_file)):
      result = run_tests(alg, language, self.do_debug, str(self.do_debug))
      error_msg = f"Solution for {member_to_capitalized_words(alg)} in {member_to_capitalized_words(language)} failed."
      self.assertEqual(True, result, error_msg)
      print("Solution correct.")

  # Runs tests for the given Language that correspond to actual
  # algorithm implementations. 
  # If a solution for an algorithm has not been written in the given Language, skips it.
  def language_test_solutions(
      self,
      language: Language, 
  ) -> None:
    if self.alg is not None:
      self.specific_test_solution(self.alg, language)
    elif self.num is not None:
      return
    else:
      print("\n\nRUNNING " + member_to_capitalized_words(language) + " ALGORITHM SOLUTION TESTS.")
      for alg in SpecificAlgorithm:
        self.specific_test_solution(alg, language)
      print("Done.")

  # Returns the prefix string for paths to test files for these tests.
  def get_test_path_prefix(self) -> str:
    return os.path.join(PROJECT_ROOT, "app_tests", "json_files", "test")
  
  # Returns the prefix string for paths to info files for these tests.
  def get_info_path_prefix(self) -> str:
    return os.path.join(PROJECT_ROOT, "app_tests", "json_files", "info")
