from enum import Enum, auto
from typing import Type, TypeVar

E = TypeVar('E', bound=Enum)

SOLUTION_CLASS_NAME = "Solution"
SOLUTION_FUNCTION_NAME = "solve"
TAB = "  "
COMPLEX_TYPES = {"array", "list", "immutable_list", "set", "map", "ListNode", "TreeNode"}


def member_to_string(member: E) -> str:
  return member.name.lower()

def member_name_list(enum: Type[E]) -> list[str]:
  return [member_to_string(member) for member in list(enum)]

def is_member(enum: Type[E], string: str) -> bool:
  try:
    member_from_string(enum, string)
    return True
  except Exception:
    return False
  
def member_from_string(enum: Type[E], string: str) -> E:
  string = string.strip().upper()
  if string in enum.__members__:
    return enum[string]
  else:
    raise ValueError(f"Not a member of {enum.__name__}: {string}.")

class Language(Enum):
  PYTHON = (".py", "#")
  JAVA = (".java", "//")

  @property
  def extension(self) -> str:
    return self.value[0]
  
  @property
  def comment_symbol(self) -> str:
    return self.value[1]
  
class SpecificAlgorithm(Enum):
  BINARY_SEARCH = auto()
  BREADTH_FIRST_SEARCH = auto()
  DEPTH_FIRST_SEARCH = auto()
  MERGE_SORT = auto()

class GeneralAlgorithm(Enum):
  BINARY_SEARCH = auto()
  REACHABLE = auto()
  SORT = auto()

INPUT_ALG_TO_SPECIFIC = {
  "binary search": SpecificAlgorithm.BINARY_SEARCH,
  "bfs": SpecificAlgorithm.BREADTH_FIRST_SEARCH,
  "breadth first search": SpecificAlgorithm.BREADTH_FIRST_SEARCH,
  "dfs": SpecificAlgorithm.DEPTH_FIRST_SEARCH,
  "depth first search": SpecificAlgorithm.DEPTH_FIRST_SEARCH,
  "merge sort": SpecificAlgorithm.MERGE_SORT
}

SPECIFIC_ALG_TO_GENERAL = {
  SpecificAlgorithm.BINARY_SEARCH: GeneralAlgorithm.BINARY_SEARCH,
  SpecificAlgorithm.BREADTH_FIRST_SEARCH: GeneralAlgorithm.REACHABLE,
  SpecificAlgorithm.DEPTH_FIRST_SEARCH: GeneralAlgorithm.REACHABLE,
  SpecificAlgorithm.MERGE_SORT: GeneralAlgorithm.SORT
}

class GlobalCommand(Enum):
  HELP = auto()
  Q = auto()
  QUIT = auto()
  EXIT = auto()
  B = auto()
  BACK = auto()

class MainMenuCommand(Enum):
  LANG = auto()
  LANGUAGE = auto()
  LANGS = auto()
  LANGUAGES = auto()
  ALGS = auto()
  ALGORITHMS = auto()
  S = auto()
  SETTINGS = auto()
  Language

class PracticeCommand(Enum):
  D = auto()
  DONE = auto()
  S = auto()
  SOL = auto()
  SOLUTION = auto()

class SettingsCommand(Enum):
  LIST = auto()
  RESET = auto()

class ParseType(Enum):
  INT = auto()
  LONG = auto()
  BOOLEAN = auto()
  FLOAT = auto()
  STRING = auto()
  ARRAY = auto()
  LIST = auto()
  IMMUTABLE_LIST = auto()
  SET = auto()
  MAP = auto()
  LISTNODE = auto()
  TREENODE = auto()

