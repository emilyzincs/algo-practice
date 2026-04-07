import unittest
from enum import Enum
from typing import Type
from util.enums import (
  INPUT_ALG_TO_SPECIFIC, SPECIFIC_ALG_TO_GENERAL, SpecificAlgorithm, GeneralAlgorithm
)

class TestAlgDicts(unittest.TestCase):
  a: str = 1

  def test_input_alg_to_specific(self):
    seen: set[SpecificAlgorithm] = set()
    for input_alg, specific_alg in INPUT_ALG_TO_SPECIFIC.items():
      self.assertEqual(str, type(input_alg))
      self.assertEqual(SpecificAlgorithm, type(specific_alg))
      seen.add(specific_alg)
    self.assertEqual(len(SpecificAlgorithm), len(seen))

  def test_specific_alg_to_general(self):
    specific_seen: set[SpecificAlgorithm] = set()
    general_seen: set[GeneralAlgorithm] = set()
    for specific_alg, general_alg in SPECIFIC_ALG_TO_GENERAL.items():
      self.assertEqual(SpecificAlgorithm, type(specific_alg))
      self.assertEqual(GeneralAlgorithm, type(general_alg))
      specific_seen.add(specific_alg)
      general_seen.add(general_seen)
    self.assertEqual(len(SpecificAlgorithm), len(specific_seen))
    self.assertEqual(len(GeneralAlgorithm), len(general_seen))

