import sys
from typing import assert_never
from commands.util import handle_global_command, print_desc
from util.types import is_type
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
          print(f"The current language is {get_language_func()}.")
          input_message = responses[1]
        case MainMenuCommand.LANGS | MainMenuCommand.LANGUAGES:
          handle_languages(member_name_list(Language))
          input_message = responses[0]
        case MainMenuCommand.ALGS | MainMenuCommand.ALGORITHMS:
          handle_algorithms()
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
        else list(SpecificAlgorithm)[int(user_input)] # todo: make better somehow?
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

def get_alg(user_input: str, alg_list: list[str], alg_name_to_idx: dict[str, int], num_algs) -> str|None:
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

def handle_languages(language_list: list[str]) -> None: 
  print("This program supports the following languages:")
  print_desc(language_list)

def handle_algorithms() -> None:
  grouped_alg_names = get_grouped_alg_names()
  print_help_message(grouped_alg_names)

def print_help_message(grouped_alg_names: list[str]) -> None:
  print("This program supports practicing the following algorithms:")
  for i, grouped_alg_name in enumerate(grouped_alg_names):
    print(f"{TAB} ID: {i} {TAB} Name: {grouped_alg_name}")
 
def get_grouped_alg_names() -> list[str]:
  ret = ["" for _ in range(len(SpecificAlgorithm))]
  for (alg_name, alg) in INPUT_ALG_TO_SPECIFIC.items():
    idx = alg.value - 1
    if ret[idx] == "":
      ret[idx] = alg_name
    else:
      ret[idx] += '/' + alg_name
  return ret
