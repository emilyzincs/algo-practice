import sys
from typing import assert_never
from menu.util import handle_global_command, print_desc, to_description_lines

from util.type_check import is_type
from util.constants import TAB
from util.exceptions import UnhandledCaseException

from util.enums import (
  MainMenuCommand, 
  INPUT_ALG_TO_SPECIFIC, 
  SpecificAlgorithm, 
  is_member, 
  GlobalCommand, 
  Language,
  member_name_list,
  member_from_string,
  member_to_string
)


# Loops, processing user input in the main command-line menu.
# 
# Parameters:
# - get_language_func: Callable that returns the current Language.
# - set_language_func: Callable that sets the current Language.
# - handle_practice_func: Callable that starts practice for a SpecificAlgorithm,
#                         returns seconds spent or None.
# - handle_settings_func: Callable that handles settings menu.
# - exit_func: Callable that exits the program.
def handle_commands(
    get_language_func,
    set_language_func,
    handle_practice_func,
    handle_settings_func,
    exit_func
  ) -> None:
  responses = [
    "\nEnter the algorithm (name or id) you" +
                  " would like to practice, or 'help' for options:\n",
    "Input: "
  ]
  num_algs = len(SpecificAlgorithm)
  input_message = responses[0]
  while True:
    input_message = responses[0]
    user_input = input(input_message).strip().lower()

    input_is_global_cmd = is_member(GlobalCommand, user_input)
    input_is_local_cmd = is_member(MainMenuCommand, user_input)
    input_is_language = is_member(Language, user_input)
    input_is_input_alg = user_input in INPUT_ALG_TO_SPECIFIC
    input_is_alg_id = is_type(user_input, int) and 0 <= int(user_input) < num_algs

    if not (
      input_is_global_cmd or
      input_is_local_cmd or
      input_is_language or
      input_is_input_alg or
      input_is_alg_id
    ):
      print(f"Invalid algorithm name or id: {user_input}.", file=sys.stderr)
      input_message = responses[0]
      continue

    if input_is_global_cmd:
      global_cmd: GlobalCommand = member_from_string(GlobalCommand, user_input)
      if not handle_global_command(global_cmd, handle_help, exit_func):
        print("Cannot go back from root menu.", file=sys.stderr)
      input_message = responses[0]
    elif input_is_local_cmd:
      local_cmd: MainMenuCommand = member_from_string(MainMenuCommand, user_input)
      match local_cmd:
        case MainMenuCommand.LANG | MainMenuCommand.LANGUAGE:
          print(f"The current language is {member_to_string(get_language_func())}.")
          input_message = responses[1]
        case MainMenuCommand.LANGS | MainMenuCommand.LANGUAGES:
          print_languages(member_name_list(Language))
          input_message = responses[0]
        case MainMenuCommand.ALGS | MainMenuCommand.ALGORITHMS:
          print_algorithms()
          input_message = responses[0]
        case MainMenuCommand.S | MainMenuCommand.SETTINGS:
          handle_settings_func()
          input_message = responses[0]
        case _:
          assert_never(local_cmd)
    elif input_is_language:
      language: Language = member_from_string(Language, user_input)
      set_language_func(language)
      input_message = responses[0]
    elif input_is_input_alg or input_is_alg_id:
      alg: SpecificAlgorithm = (
        INPUT_ALG_TO_SPECIFIC[user_input] if input_is_input_alg
      else list(SpecificAlgorithm)[int(user_input)]
      )
      print(f"Starting {member_to_string(alg)} practice.")
      seconds_spent = handle_practice_func(alg)
      if seconds_spent is not None:
        minutes = round(seconds_spent // 60)
        seconds = seconds_spent % 60
        if minutes == 0:
          print(f"Successfully completed {member_to_string(alg)} in {seconds_spent:.2f} seconds!")
        else:
          seconds = int(seconds)
          print(f"Successfully completed {member_to_string(alg)} in {minutes}m" +
                f" {seconds}s!")
    else:
      raise UnhandledCaseException(user_input, "input")


# Validates and extracts an algorithm name from user input.
# 
# Parameters:
# - user_input: Raw input string (algorithm name, ID, or alias).
# - alg_list: List of algorithm names indexed by ID.
# - alg_name_to_idx: Dictionary mapping algorithm names to indices.
# - num_algs: Total number of algorithms.
# 
# Returns:
#   The algorithm name string if valid, otherwise None.
def get_alg(user_input: str, alg_list: list[str], 
            alg_name_to_idx: dict[str, int], num_algs) -> str|None:
  if is_type(user_input, int):
    idx = int(user_input)
    if idx < 0 or idx >= num_algs:
      return None
  else:
    if user_input not in alg_name_to_idx:
      return None
    idx = alg_name_to_idx[user_input]
  return alg_list[idx]


# Prints the help menu listing all global commands, main menu commands,
# and the language change option.
def handle_help():
  description_lines = to_description_lines(GlobalCommand)
  description_lines.extend(to_description_lines(MainMenuCommand))
  description_lines.extend([
    "<language>: Updates the program to use the given language",
  ])
  print("This menu supports the following inputs:")
  print_desc(description_lines)


# Prints the list of supported languages, using 'language_list'.
def print_languages(language_list: list[str]) -> None: 
  print("This program supports the following languages:")
  print_desc(language_list)


# Prints the available algorithms grouped by ID with '/'-delimited aliases.
def print_algorithms() -> None:
  grouped_alg_names: list[str] = get_grouped_alg_names()
  print("This program supports practicing the following algorithms:")
  for i, grouped_alg_name in enumerate(grouped_alg_names):
    print(f"{TAB} ID: {i} {TAB} Name: {grouped_alg_name}")  
 

# Returns a list of strings where each index (0‑based) corresponds to an algorithm's ID
# and contains the algorithm's '/'-delimited aliases.
def get_grouped_alg_names() -> list[str]:
  ret = ["" for _ in range(len(SpecificAlgorithm))]
  for (alg_name, alg) in INPUT_ALG_TO_SPECIFIC.items():
    idx = alg.value - 1
    if ret[idx] == "":
      ret[idx] = alg_name
    else:
      ret[idx] += '/' + alg_name
  return ret
