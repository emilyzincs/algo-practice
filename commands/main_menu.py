import sys
from typing import List, Tuple
from utils import print_desc, is_type, in_either
from commands.command_util import GLOBAL_COMMANDS, handle_global_command

def handle_commands(
    local_commands: set[str],
    get_language_func: str,
    language_list: List[str],
    lang_to_ext_and_comment_symbol: dict[str, Tuple[str, str]],
    set_language_func,
    alg_list: List[str],
    alg_name_to_idx: dict[str, int],
    num_algs: int,
    tab: str,
    handle_practice_func,
    handle_settings_func,
    exit_func
  ) -> None:
  responses = [
    "\nEnter the algorithm (name or id) you" +
                  " would like to practice, or 'help' for options:\n",
    "Input: "
  ]
  input_message = responses[0]
  while True:
    input_message = responses[0]
    user_input = input(input_message).strip().lower()
    input_is_alg_id = is_type(user_input, int) and 0 <= int(user_input) < num_algs
    if (not in_either(user_input, GLOBAL_COMMANDS, local_commands) and 
                    user_input not in lang_to_ext_and_comment_symbol and
                    user_input not in alg_name_to_idx and
                    not input_is_alg_id):
      print(f"Invalid algorithm name or id: {user_input}.", file=sys.stderr)
      input_message = responses[0]

    if user_input in GLOBAL_COMMANDS:
      if not handle_global_command(user_input, handle_help, exit_func):
        return
      input_message = responses[1]
    else:
      match user_input:
        case "lang" | "language":
          print(f"The current language is {get_language_func()}.")
          input_message = responses[1]
        case "langs" | "languages":
          handle_languages(language_list)
          input_message = responses[0]
        case "algs" | "algorithms":
          handle_algorithms(alg_name_to_idx, num_algs, tab)
          input_message = responses[0]
        case "s" | "settings":
          handle_settings_func()
          input_message = responses[0]
        case _:
          if user_input in lang_to_ext_and_comment_symbol:
            set_language_func(user_input)
            input_message = responses[0]
          elif user_input in alg_name_to_idx or is_type(user_input, int):
            alg = get_alg(user_input, alg_list, alg_name_to_idx, num_algs)
            if alg is not None:
              time_spent = handle_practice_func(alg)
              if time_spent >= 0:
                print(f"Successfully completed {alg} in {time_spent:.2f} seconds!")
            else:
              print(f"Invalid algorithm name or id: {user_input}.", file=sys.stderr)
            input_message = responses[0]

def get_alg(user_input: str, alg_list: List[str], alg_name_to_idx: dict[str, int], num_algs) -> str|None:
  if is_type(user_input, int):
    idx = int(user_input)
    if idx < 0 or idx >= num_algs:
      return None
  else:
    if user_input not in alg_name_to_idx:
      return None
    idx = alg_name_to_idx[user_input]
  return alg_list[idx]

def handle_help():
  command_descriptions = [
    "help: Lists commands",
    "q/quit/exit: Exits the program",
    "lang/language: Prints the current language",
    "langs/languages: Lists the languages this program supports",
    "<language>: Updates the program to use the given language",
    "algs/algorithms: Lists the algorithms this program supports and their ids",
    "<alg id>/<alg name>: Begins a practice session for the given algorithm",
    "s/settings: Goes to the settings menu"
  ]
  print("This menu supports the following inputs:")
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
 
def get_grouped_alg_names(alg_name_to_idx: dict[str, int], num_algs: int) -> List[str]:
  ret = [None for _ in range(num_algs)] 
  for alg_name, idx in alg_name_to_idx.items():
    if not ret[idx]:
      ret[idx] = alg_name
    else:
      ret[idx] += '/' + alg_name
  return ret
