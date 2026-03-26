import sys
from typing import List, Tuple

def handle_commands(
    user_input: str,
    commands: set[str],
    language: str,
    language_list: List[str],
    lang_to_ext_and_comment_symbol: dict[str, Tuple[str, str]],
    set_language_func,
    alg_name_to_idx: dict[str, int],
    num_algs: int,
    tab: str  
  ) -> bool:
  user_input = user_input.strip().lower()
  if user_input not in commands:
    return False
  match user_input:
    case "help":
      handle_help()
    case "q":
      sys.exit(0)
    case "exit":
      sys.exit(0)
    case "lang" | "language":
      print(f"The current language is {language}.")
    case "langs" | "languages":
      handle_languages(language_list)
    case "algs" | "algorithms":
      handle_algorithms(alg_name_to_idx, num_algs, tab)
    case _:
      if user_input not in lang_to_ext_and_comment_symbol:
        raise ValueError("Reached default case but input is not a language")
      set_language_func(user_input)
  return True

def handle_help():
  command_descriptions = [
    "help: Lists commands",
    "q/exit: Exits the program.",
    "lang/language: Prints the current language.",
    "langs/languages: Lists the languages this program supports",
    "<language>: Updates the program to use the given language",
    "algs/algorithms: Lists the algorithms this program supports and their ids",
    "<alg id>/<alg name>: Begins a practice session for the given algorithm."
  ]
  print("This program supports the following inputs:")
  print_desc(command_descriptions)

def handle_languages(language_list: List[str]) -> None: 
  print("This program supports the following languages:")
  print_desc(language_list)

def handle_algorithms(alg_name_to_idx: dict[str, int], num_algs: int, tab: str) -> None:
  grouped_alg_names = get_grouped_alg_names(alg_name_to_idx, num_algs)
  print_help_message(grouped_alg_names, tab)

def print_help_message(grouped_alg_names: List[str], tab: str) -> None:
  print("This program supports practicing the following algorithms:")
  for i, grouped_alg_name in enumerate(grouped_alg_names):
    print(f"{tab} ID: {i} {tab} Name: {grouped_alg_name}")
  print()
 
def get_grouped_alg_names(alg_name_to_idx: dict[str, int], num_algs: int) -> List[str]:
  ret = [None for _ in range(num_algs)] 
  for alg_name, idx in alg_name_to_idx.items():
    if not ret[idx]:
      ret[idx] = alg_name
    else:
      ret[idx] += '/' + alg_name
  return ret

def print_desc(descs: List[str]) -> None:
  for i, desc in enumerate(descs):
    print(f"{i+1}. {desc}.")
  print()
