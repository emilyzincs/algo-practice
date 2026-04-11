from enum import Enum, auto
from typing import Type, TypeVar

E = TypeVar('E', bound=Enum)


# Converts the given enum member to its lowercase name string representation
# and returns it
def member_to_string(member: E) -> str:
  return member.name.lower()


# Returns a list of all enum member names in order in lowercase 
# for the given enum.
def member_name_list(enum: Type[E]) -> list[str]:
  return [member_to_string(member) for member in list(enum)]


# Returns whether the given string corresponds to any member of 
# the given enum, case-insensitively.
def is_member(enum: Type[E], string: str) -> bool:
  try:
    member_from_string(enum, string)
    return True
  except Exception:
    return False


# Converts the given string to the corresponding member of the given enum,
# ignoring case and leading/trailing whitespace, then returns that member.
# 
# Raises ValueError if the string does not match any member name in the enum.
def member_from_string(enum: Type[E], string: str) -> E:
  string = string.strip().upper()
  if string in enum.__members__:
    return enum[string]
  else:
    raise ValueError(f"Not a member of {enum.__name__}: {string}.")


# Enum for supported programming languages, storing file extension and comment symbol.
class Language(Enum):
  PYTHON = (".py", "#")
  JAVA = (".java", "//")

  # Returns the file extension for this language.
  @property
  def extension(self) -> str:
    return self.value[0]
  
  # Returns the line comment symbol for this language.
  @property
  def comment_symbol(self) -> str:
    return self.value[1]


# Enum for specific algorithms that can be practiced.
class SpecificAlgorithm(Enum):
  BINARY_SEARCH = auto()
  BREADTH_FIRST_SEARCH = auto()
  DEPTH_FIRST_SEARCH = auto()
  MERGE_SORT = auto()


# Enum for general algorithm categories.
class GeneralAlgorithm(Enum):
  BINARY_SEARCH = auto()
  REACHABLE = auto()
  SORT = auto()


# Map from recognized user input strings to SpecificAlgorithm members.
INPUT_ALG_TO_SPECIFIC = {
  "binary search": SpecificAlgorithm.BINARY_SEARCH,
  "bfs": SpecificAlgorithm.BREADTH_FIRST_SEARCH,
  "breadth first search": SpecificAlgorithm.BREADTH_FIRST_SEARCH,
  "dfs": SpecificAlgorithm.DEPTH_FIRST_SEARCH,
  "depth first search": SpecificAlgorithm.DEPTH_FIRST_SEARCH,
  "merge sort": SpecificAlgorithm.MERGE_SORT
}


# Maps each specific algorithm to its corresponding general category.
SPECIFIC_ALG_TO_GENERAL = {
  SpecificAlgorithm.BINARY_SEARCH: GeneralAlgorithm.BINARY_SEARCH,
  SpecificAlgorithm.BREADTH_FIRST_SEARCH: GeneralAlgorithm.REACHABLE,
  SpecificAlgorithm.DEPTH_FIRST_SEARCH: GeneralAlgorithm.REACHABLE,
  SpecificAlgorithm.MERGE_SORT: GeneralAlgorithm.SORT
}


# Enum for commands that are valid from any menu (global commands).
class GlobalCommand(Enum):
  HELP = "Lists commands"
  Q = "Exits the program"
  QUIT = "Exits the program"
  EXIT = "Exits the program"
  B = "Returns to the previous menu"
  BACK = "Returns to the previous menu"


# Enum for commands specific to the main menu.
class MainMenuCommand(Enum):
  LANG = "Prints the current language"
  LANGUAGE = "Prints the current language"
  LANGS = "Lists the languages this program supports"
  LANGUAGES = "Lists the languages this program supports"
  ALGS = "Lists the algorithms this program supports and their ids"
  ALGORITHMS = "Lists the algorithms this program supports and their ids"
  S = "Goes to the settings menu"
  SETTINGS = "Goes to the settings menu"


# Enum for commands available during practice (while solving an algorithm).
class PracticeCommand(Enum):
  D = "Submits the current practice implementation to be tested"
  DONE = "Submits the current practice implementation to be tested"
  S = "Loads the algorithm solution into the file"
  SOL = "Loads the algorithm solution into the file"
  SOLUTION = "Loads the algorithm solution into the file"


# Enum for commands specific to the settings menu.
class SettingsCommand(Enum):
  LIST = "Shows the current settings"
  RESET = "Resets all settings to default (asks for confirmation)"


# Enum for all language-agnostic data types that can appear
# in problem input/output definitions.
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
