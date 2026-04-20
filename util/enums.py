from enum import Enum, auto
from typing import Type, TypeVar, List

E = TypeVar('E', bound=Enum)


# Converts the given enum member to its lowercase name string representation
# and returns it
def member_to_string(member: E) -> str:
  return member.name.lower()


# E.g. SpecificAlgorithm.BINARY_SEARCH -> "Binary Search".
def member_to_capitalized_words(member: E) -> str:
  return " ".join([word.capitalize() for word in member.name.split("_")])


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
  HASHABLE_LIST = auto()
  SET = auto()
  HASHABLE_SET = auto()
  MAP = auto()


class DirectoryType(Enum):
    SPECIFIC = auto()
    GENERAL = auto()


class AlgorithmCategory(Enum):
    ARRAYS = auto()
    GRAPHS = auto()
    STRINGS = auto()


class GeneralAlgorithm(Enum):
    # Format: (Category)
    SEARCH = (AlgorithmCategory.ARRAYS, auto())
    SORT = (AlgorithmCategory.ARRAYS, auto())
    SUBARRAY = (AlgorithmCategory.ARRAYS, auto())
    REACHABLE = (AlgorithmCategory.GRAPHS, auto())
    SHORTEST_PATH = (AlgorithmCategory.GRAPHS, auto())
    MINIMUM_SPANNING_TREE = (AlgorithmCategory.GRAPHS, auto())
    TOPOLOGICAL_SORT = (AlgorithmCategory.GRAPHS, auto())
    MAX_FLOW = (AlgorithmCategory.GRAPHS, auto())
    CONNECTED_COMPONENTS = (AlgorithmCategory.GRAPHS, auto())
    PATTERN_MATCHING = (AlgorithmCategory.STRINGS, auto())

    @property
    def category(self) -> AlgorithmCategory:
        return self.value[0]


class SpecificAlgorithm(Enum):
    # Format: (GeneralType, InfoDir, TestDir, Aliases)
    BINARY_SEARCH = (
        GeneralAlgorithm.SEARCH, DirectoryType.GENERAL, 
        DirectoryType.SPECIFIC, ["binary search"]
    )
    MERGE_SORT = (
        GeneralAlgorithm.SORT, DirectoryType.GENERAL, 
        DirectoryType.GENERAL, ["merge sort"]
    )
    QUICK_SORT = (
        GeneralAlgorithm.SORT, DirectoryType.GENERAL, 
        DirectoryType.GENERAL, ["quick sort"]
    )
    HEAP_SORT = (
        GeneralAlgorithm.SORT, DirectoryType.GENERAL, 
        DirectoryType.GENERAL, ["heap sort"]
    )
    RADIX_SORT = (
        GeneralAlgorithm.SORT, DirectoryType.GENERAL, 
        DirectoryType.GENERAL, ["radix sort"]
    )
    BUCKET_SORT = (
        GeneralAlgorithm.SORT, DirectoryType.SPECIFIC, 
        DirectoryType.SPECIFIC, ["bucket sort"]
    )
    KADANE = (
        GeneralAlgorithm.SUBARRAY, DirectoryType.SPECIFIC, 
        DirectoryType.SPECIFIC, ["kadane", "kadane's"]
    )
    BREADTH_FIRST_SEARCH = (
        GeneralAlgorithm.REACHABLE, DirectoryType.GENERAL, 
        DirectoryType.GENERAL, ["bfs", "breadth first search"]
    )
    DEPTH_FIRST_SEARCH = (
        GeneralAlgorithm.REACHABLE, DirectoryType.GENERAL, 
        DirectoryType.GENERAL, ["dfs", "depth first search"]
    )
    DIJKSTRA = (
        GeneralAlgorithm.SHORTEST_PATH, DirectoryType.SPECIFIC, 
        DirectoryType.SPECIFIC, ["dijkstra", "dijkstra's"]
    )
    BELLMAN_FORD = (
        GeneralAlgorithm.SHORTEST_PATH, DirectoryType.SPECIFIC, 
        DirectoryType.SPECIFIC, ["bellman ford"]
    )
    FLOYD_WARSHALL = (
        GeneralAlgorithm.SHORTEST_PATH, DirectoryType.SPECIFIC, 
        DirectoryType.SPECIFIC, ["floyd warshall"]
    )
    KRUSKAL = (
        GeneralAlgorithm.MINIMUM_SPANNING_TREE, DirectoryType.GENERAL, 
        DirectoryType.GENERAL, ["kruskal", "kruskal's"]
    )
    PRIM = (
        GeneralAlgorithm.MINIMUM_SPANNING_TREE, DirectoryType.GENERAL, 
        DirectoryType.GENERAL, ["prim", "prim's"]
    )
    KAHN = (
        GeneralAlgorithm.TOPOLOGICAL_SORT, DirectoryType.GENERAL, 
        DirectoryType.SPECIFIC, ["kahn", "kahn's"]
    )
    FORD_FULKERSON = (
        GeneralAlgorithm.MAX_FLOW, DirectoryType.GENERAL, 
        DirectoryType.GENERAL, ["ford fulkerson"]
    )
    TARJAN = (
        GeneralAlgorithm.CONNECTED_COMPONENTS, DirectoryType.GENERAL, 
        DirectoryType.GENERAL, ["tarjan", "tarjan's"]
    )
    KNUTH_MORRIS_PRATT = (
        GeneralAlgorithm.PATTERN_MATCHING, DirectoryType.SPECIFIC, 
        DirectoryType.SPECIFIC, ["kmp", "knuth morris pratt"]
    )

    @property
    def general_type(self) -> GeneralAlgorithm:
        return self.value[0]

    @property
    def info_dir(self) -> DirectoryType:
        return self.value[1]

    @property
    def test_dir(self) -> DirectoryType:
        return self.value[2]

    @property
    def aliases(self) -> List[str]:
        return self.value[3]

    @property
    def category(self) -> AlgorithmCategory:
        return self.general_type.category

    @classmethod
    def from_input(cls, user_input: str) -> 'SpecificAlgorithm':
        normalized = user_input.strip().lower()
        for member in cls:
            if normalized in member.aliases:
                return member
        raise ValueError(f"No match for: {user_input}")
    
    @classmethod
    def is_alg(cls, user_input: str) -> bool:
      try:
         cls.from_input(user_input)
         return True
      except ValueError:
         return False
