import unittest
import os
from util.type_check import is_type, string_to_bool
from util.enums import Language, SpecificAlgorithm, is_member, Language, member_from_string
from abc import ABC, abstractmethod


# A class which factors out the logic for initiazing the environment variables.
# Meant to be extended by test classes which use the environment variables,
#   but this class does not hold tests itself.
class BaseTest(unittest.TestCase, ABC):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  @abstractmethod
  def setUp(self) -> None:
    self.language: Language | None = None
    self.alg: SpecificAlgorithm | None = None
    self.num: int | None = None
    self.do_debug: bool = False

    if "TEST_LANGUAGE" in os.environ:
      string: str = os.environ["TEST_LANGUAGE"]
      if not is_member(Language, string):
        raise ValueError(f"Unrecognized language: {string}.")
      self.language = member_from_string(Language, string)

    if "TEST_ALG" in os.environ:
      string = os.environ["TEST_ALG"]
      if not is_member(SpecificAlgorithm, string):
        raise ValueError(f"Unrecognized algorithm: {string}.")
      self.alg = member_from_string(SpecificAlgorithm, string)

    if "TEST_NUM" in os.environ:
      string = os.environ["TEST_NUM"]
      if not is_type(string, int):
        raise ValueError(f"Num must be of type int. Value: {string}.")
      self.num = int(string)
    
    if "TEST_DEBUG" in os.environ:
      string = os.environ["TEST_DEBUG"]
      if not is_type(string, string_to_bool):
        raise ValueError(f"Debug must be of type bool. Value: {string}.")
      self.do_debug = string_to_bool(string)
  