from enum import Enum, auto
from typing import Type, TypeVar

E = TypeVar('E', bound=Enum)

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
  HELP = "Lists commands"
  Q = "Exits the program"
  QUIT = "Exits the program"
  EXIT = "Exits the program"
  B = "Returns to the previous menu"
  BACK = "Returns to the previous menu"

class MainMenuCommand(Enum):
  LANG = "Prints the current language"
  LANGUAGE = "Prints the current language"
  LANGS = "Lists the languages this program supports"
  LANGUAGES = "Lists the languages this program supports"
  ALGS = "Lists the algorithms this program supports and their ids"
  ALGORITHMS = "Lists the algorithms this program supports and their ids"
  S = "Goes to the settings menu"
  SETTINGS = "Goes to the settings menu"

class PracticeCommand(Enum):
  D = "Submits the current practice implementation to be tested"
  DONE = "Submits the current practice implementation to be tested"
  S = "Loads the algorithm solution into the file"
  SOL = "Loads the algorithm solution into the file"
  SOLUTION = "Loads the algorithm solution into the file"

class SettingsCommand(Enum):
  LIST = "Shows the current settings"
  RESET = "Resets all settings to default (asks for confirmation)"

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
