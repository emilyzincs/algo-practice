import sys
from util.utils import print_desc, read_json, dump_json, copy_file, is_type, string_to_bool
from commands.command_util import GLOBAL_COMMANDS, handle_global_command, get_global_command_descriptions
from util.get_file_paths import get_settings_path, get_default_settings_path

def handle_commands(
    local_commands_and_actual_settings: tuple[set[str], set[str]],
    languages,
    tab: str,
    refresh_settings_func,
    exit_func
) -> None:
  local_commands, actual_settings = local_commands_and_actual_settings 
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
    is_global_cmd = len(user_input) == 1 and user_input[0] in GLOBAL_COMMANDS
    is_local_cmd = len(user_input) == 1 and user_input[0] in local_commands 
    is_setting = len(user_input) == 2 and user_input[0] in actual_settings
    if not (is_global_cmd or is_local_cmd or is_setting):
      print("Unrecognized input. Type 'help' to see valid inputs.", file=sys.stderr)
      continue
    if is_global_cmd:
      if not handle_global_command(user_input[0], handle_help, exit_func):
        refresh_settings_func()
        return
    elif is_local_cmd:
      match user_input[0]:
        case "list":
          print("Current settings:")
          for setting, value in settings.items():
            print(f"{tab}{setting}: {value}")
        case "reset":
          next_input = input("Confirm resetting all settings to default?" +
                            " To confirm type 'y' or 'yes', to cancel" + 
                            " type anything else:\n").strip().lower()
          if next_input == 'y' or next_input == 'yes':
            copy_file(default_settings_path, settings_path)
            settings = default_settings.copy()
            print("Successfully reset settings to default.")
        case _:
          raise ValueError(f"Unhandled local command: {user_input[0]}.")
    elif is_setting:
      setting, new_val = user_input
      if new_val == "default":
        settings[setting] = default_settings[setting]
        dump_json(settings_path, settings)
      else:
        match setting:
          case "default_language":
            if new_val not in languages:
              print(f"Invalid language", file=sys.stderr)
              continue
          case "delete_attempts":
            if not is_type(new_val, string_to_bool):
              print(f"New value must be a bool for this setting.", file=sys.stderr)
              continue
            new_val = string_to_bool(new_val)
          case _:
            raise ValueError(f"Unhandled setting: {user_input[0]}.")
          
        settings[setting] = new_val
        dump_json(settings_path, settings)
        print(f"Successfully updated {setting} to {new_val}.")
    else:
      raise ValueError(f"Unhandled case: {user_input}")

def handle_help():
  command_descriptions = get_global_command_descriptions()
  command_descriptions.extend([
    "list: Shows the current settings",
    "reset: Resets all settings to default (asks for confirmation)",
    "<setting> default: Changes the given setting to have the default value",
    "<setting> <new value>: Changes the given setting to have the" + 
                          " given new value, if possible"

  ])
  print("This menu supports the following inputs:")
  print_desc(command_descriptions) 
