import unittest
import os
from app import LANGUAGE_TO_EXTENSION_AND_COMMENT_SYMBOL, ALG_LIST, LANGUAGE_LIST
from util.utils import is_type, string_to_bool


class BaseTest(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def setUp(self):
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
  