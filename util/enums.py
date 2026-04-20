from enum import Enum, auto
from typing import Type, TypeVar

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


# Enum for specific algorithms that can be practiced.
class SpecificAlgorithm(Enum):
  BINARY_SEARCH = auto()
  MERGE_SORT = auto()
  QUICK_SORT = auto()
  HEAP_SORT = auto()
  RADIX_SORT = auto()
  BUCKET_SORT = auto()
  KADANE = auto()
  BREADTH_FIRST_SEARCH = auto()
  DEPTH_FIRST_SEARCH = auto()
  DIJKSTRA = auto()
  BELLMAN_FORD = auto()
  FLOYD_WARSHALL = auto()
  KRUSKAL = auto()
  PRIM = auto()
  KAHN = auto()
  FORD_FULKERSON = auto()
  TARJAN = auto()
  KNUTH_MORRIS_PRATT = auto()
  

class GeneralAlgorithm(Enum):
  SEARCH = auto()
  SORT = auto()
  SUBARRAY = auto()
  REACHABLE = auto()
  SHORTEST_PATH = auto()
  MINIMUM_SPANNING_TREE = auto()
  TOPOLOGICAL_SORT = auto()
  MAX_FLOW = auto()
  CONNECTED_COMPONENTS = auto()
  PATTERN_MATCHING = auto()


class AlgorithmCategory(Enum):
  ARRAYS = auto()
  GRAPHS = auto()
  STRINGS = auto()


# Map from recognized user input strings to SpecificAlgorithm members.
INPUT_ALG_TO_SPECIFIC = {
  "binary search": SpecificAlgorithm.BINARY_SEARCH,
  "merge sort": SpecificAlgorithm.MERGE_SORT,
  "quick sort": SpecificAlgorithm.QUICK_SORT,
  "heap sort": SpecificAlgorithm.HEAP_SORT,
  "radix sort": SpecificAlgorithm.RADIX_SORT,
  "bucket sort": SpecificAlgorithm.BUCKET_SORT,
  "kadane": SpecificAlgorithm.KADANE,
  "kadane's": SpecificAlgorithm.KADANE,
  "bfs": SpecificAlgorithm.BREADTH_FIRST_SEARCH,
  "breadth first search": SpecificAlgorithm.BREADTH_FIRST_SEARCH,
  "dfs": SpecificAlgorithm.DEPTH_FIRST_SEARCH,
  "depth first search": SpecificAlgorithm.DEPTH_FIRST_SEARCH,
  "dijkstra": SpecificAlgorithm.DIJKSTRA,
  "dijkstra's": SpecificAlgorithm.DIJKSTRA,
  "bellman ford": SpecificAlgorithm.BELLMAN_FORD,
  "floyd warshall": SpecificAlgorithm.FLOYD_WARSHALL,
  "kruskal": SpecificAlgorithm.KRUSKAL,
  "kruskal's": SpecificAlgorithm.KRUSKAL,
  "prim": SpecificAlgorithm.PRIM,
  "prim's": SpecificAlgorithm.PRIM,
  "kahn": SpecificAlgorithm.KAHN,
  "kahn's": SpecificAlgorithm.KAHN,
  "ford fulkerson": SpecificAlgorithm.FORD_FULKERSON,
  "tarjan": SpecificAlgorithm.TARJAN,
  "tarjan's": SpecificAlgorithm.TARJAN,
  "kmp": SpecificAlgorithm.KNUTH_MORRIS_PRATT,
  "knuth morris pratt": SpecificAlgorithm.KNUTH_MORRIS_PRATT,
}


SPECIFIC_ALG_TO_GENERAL = {
  SpecificAlgorithm.BINARY_SEARCH: GeneralAlgorithm.SEARCH,
  SpecificAlgorithm.MERGE_SORT: GeneralAlgorithm.SORT,
  SpecificAlgorithm.QUICK_SORT: GeneralAlgorithm.SORT,
  SpecificAlgorithm.HEAP_SORT: GeneralAlgorithm.SORT,
  SpecificAlgorithm.RADIX_SORT: GeneralAlgorithm.SORT,
  SpecificAlgorithm.BUCKET_SORT: GeneralAlgorithm.SORT,
  SpecificAlgorithm.KADANE: GeneralAlgorithm.SUBARRAY,
  SpecificAlgorithm.BREADTH_FIRST_SEARCH: GeneralAlgorithm.REACHABLE,
  SpecificAlgorithm.DEPTH_FIRST_SEARCH: GeneralAlgorithm.REACHABLE,
  SpecificAlgorithm.DIJKSTRA: GeneralAlgorithm.SHORTEST_PATH,
  SpecificAlgorithm.BELLMAN_FORD: GeneralAlgorithm.SHORTEST_PATH,
  SpecificAlgorithm.FLOYD_WARSHALL: GeneralAlgorithm.SHORTEST_PATH,
  SpecificAlgorithm.KRUSKAL: GeneralAlgorithm.MINIMUM_SPANNING_TREE,
  SpecificAlgorithm.PRIM: GeneralAlgorithm.MINIMUM_SPANNING_TREE,
  SpecificAlgorithm.KAHN: GeneralAlgorithm.TOPOLOGICAL_SORT,
  SpecificAlgorithm.FORD_FULKERSON: GeneralAlgorithm.MAX_FLOW,
  SpecificAlgorithm.TARJAN: GeneralAlgorithm.CONNECTED_COMPONENTS,
  SpecificAlgorithm.KNUTH_MORRIS_PRATT: GeneralAlgorithm.PATTERN_MATCHING,
}


GENERAL_ALG_TO_CATEGORY = {
  GeneralAlgorithm.SEARCH: AlgorithmCategory.ARRAYS,
  GeneralAlgorithm.SORT: AlgorithmCategory.ARRAYS,
  GeneralAlgorithm.SUBARRAY: AlgorithmCategory.ARRAYS,
  GeneralAlgorithm.REACHABLE: AlgorithmCategory.GRAPHS,
  GeneralAlgorithm.SHORTEST_PATH: AlgorithmCategory.GRAPHS,
  GeneralAlgorithm.MINIMUM_SPANNING_TREE: AlgorithmCategory.GRAPHS,
  GeneralAlgorithm.TOPOLOGICAL_SORT: AlgorithmCategory.GRAPHS,
  GeneralAlgorithm.MAX_FLOW: AlgorithmCategory.GRAPHS,
  GeneralAlgorithm.CONNECTED_COMPONENTS: AlgorithmCategory.GRAPHS,
  GeneralAlgorithm.PATTERN_MATCHING: AlgorithmCategory.STRINGS,
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
  HASHABLE_LIST = auto()
  SET = auto()
  HASHABLE_SET = auto()
  MAP = auto()
