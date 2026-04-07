import sys
from typing import assert_never

from commands.util import handle_global_command, get_global_command_descriptions, print_desc
from util.file_paths import get_settings_path, get_default_settings_path
from util.file_io import read_json, dump_json, copy_file
from util.types import is_type, string_to_bool
from util.exceptions import UnhandledCaseException
from util.constants import TAB
from util.enums import (
  GlobalCommand,
  is_member,
  SettingsCommand,
  member_from_string,
  Language
)

def handle_commands(
    refresh_settings_func,
    exit_func
) -> None:
  # todo: handle more dynamically
  setting_to_info = {
    "default_language": "The language the program is initially set to when it" +
                        " is started without an explicit language argument.",
    "delete_attempts": "When set to true, clears the practice directory upon completion" +
                       " of an algorithm, when exiting practice of an algorithm, and" +
                       " when exiting the program.",
    "prepopulate_boilerplate": "When set to true, includes the necessary class and method" +
                        " declaration when initializing a practice file, as well as the" +
                        " necessary imports and classes corresponding to the declarations.",
    "tab_size": "The number of spaces to use as a tab when prepopulating a practice" +
                " file with any text."
  }
  
  default_settings_path = get_default_settings_path()
  settings_path = get_settings_path()
  default_settings = read_json(default_settings_path)
  settings = read_json(settings_path)
  if not isinstance(default_settings, dict) or not isinstance(settings, dict):
    raise ValueError("Settings and default settings must be represented as json dicts")

  while True:
    user_input = input("Enter a setting and new corresponding value" + 
                      " (<setting> <new val>)," + 
                      " or 'help' for options:\n").strip().lower().split()
    is_global_cmd = len(user_input) == 1 and is_member(GlobalCommand, user_input[0])
    is_local_cmd = len(user_input) == 1 and is_member(SettingsCommand, user_input[0])  
    is_setting = len(user_input) == 2 and user_input[0] in settings
    is_info = len(user_input) == 2 and user_input[0] == "info" and user_input[1] in settings
    if not (is_global_cmd or is_local_cmd or is_setting or is_info):
      print("Unrecognized input. Type 'help' to see valid inputs.", file=sys.stderr)
      continue
    if is_global_cmd:
      global_cmd: GlobalCommand = member_from_string(GlobalCommand, user_input[0])
      if not handle_global_command(global_cmd, handle_help, exit_func):
        refresh_settings_func()
        return
    elif is_local_cmd:
      local_cmd: SettingsCommand = member_from_string(SettingsCommand, user_input[0])
      match local_cmd:
        case SettingsCommand.LIST:
          print("Current settings:")
          for setting, value in settings.items():
            print(f"{TAB}{setting}: {value}")
        case SettingsCommand.RESET:
          next_input = input("Confirm resetting all settings to default?" +
                            " To confirm type 'y' or 'yes', to cancel" + 
                            " type anything else:\n").strip().lower()
          if next_input == 'y' or next_input == 'yes':
            copy_file(default_settings_path, settings_path)
            settings = default_settings.copy()
            print("Successfully reset settings to default.")
        case _:
          assert_never(local_cmd)
    elif is_setting:
      setting, new_val = user_input
      if new_val == "default":
        settings[setting] = default_settings[setting]
        dump_json(settings_path, settings)
      else:
        match setting:
          case "default_language":
            if not is_member(Language, new_val):
              print(f"Invalid language", file=sys.stderr)
              continue
            settings[setting] = new_val
          case "delete_attempts":
            if not is_type(new_val, string_to_bool):
              print(f"New value must be a bool for this setting.", file=sys.stderr)
              continue
            settings[setting] = string_to_bool(new_val)
          case "prepopulate_boilerplate":
            if not is_type(new_val, string_to_bool):
              print(f"New value must be a bool for this setting.", file=sys.stderr)
              continue
            settings[setting] = string_to_bool(new_val)
          case "tab_size":
            if not is_type(new_val, int):
              print(f"New value must be an integer for this setting.", file=sys.stderr)
              continue
            settings[setting] = int(new_val)
          case _:
            raise UnhandledCaseException(user_input[0], "setting")          
        dump_json(settings_path, settings)
        print(f"Successfully updated {setting} to {new_val}.")
    elif is_info:
      print(f"{user_input[1]}: {setting_to_info[user_input[1]]}")
    else:
      raise UnhandledCaseException(" ".join(user_input), "input")

def handle_help():
  command_descriptions = get_global_command_descriptions()
  command_descriptions.extend([
    "list: Shows the current settings",
    "reset: Resets all settings to default (asks for confirmation)",
    "info <setting>: Prints information regarding the given setting",
    "<setting> default: Changes the given setting to have the default value",
    "<setting> <new value>: Changes the given setting to have the" + 
                          " given new value, if possible"
  ])
  print("This menu supports the following inputs:")
  print_desc(command_descriptions) 
