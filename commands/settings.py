import sys
from utils import print_desc, read_json, dump_json, copy_file
from commands.command_util import GLOBAL_COMMANDS, handle_global_command
from get_file_paths import get_settings_path, get_default_settings_path

def handle_commands(
    local_commands_and_actual_settings: tuple[set[str], set[str]],
    languages,
    exit_func
) -> None:
  local_commands, actual_settings = local_commands_and_actual_settings 
  default_settings_path = get_default_settings_path()
  settings_path = get_settings_path()
  default_settings, default_settings_file = read_json(default_settings_path)
  settings, settings_file = read_json(settings_path)
  
  while True:
    if not isinstance(default_settings, dict) or not isinstance(settings, dict):
      raise ValueError("Settings and default settings must be represented as json dicts")
    user_input = input("Input: ").strip().lower().split()
    is_global_cmd = len(user_input) == 1 and user_input[0] in GLOBAL_COMMANDS
    is_local_cmd = len(user_input) == 2 and user_input[0] in local_commands 
    is_setting = len(user_input) == 1 and user_input[0] in actual_settings
    if not (is_global_cmd or is_local_cmd or is_setting):
      print("Unrecognized input. Type 'help' to see valid inputs.", file=sys.stderr)
      continue
    if is_global_cmd:
      if not handle_global_command(user_input[0], handle_help, exit_func):
        default_settings_file.close()
        settings_file.close()
        return
    elif is_local_cmd:
      match user_input[0]:
        case "list":
          for setting, value in settings.items():
            print(f"{setting}: {value}")
        case "reset":
          next_input = input("Confirm resetting all settings to default?" +
                             " To confirm type 'y' or 'yes', to cancel" + 
                             " type anything else.").strip().lower()
          if next_input == 'y' or next_input == 'yes':
            settings_file.close()
            copy_file(default_settings_path, settings_path)
            settings, settings_file = read_json(settings_path)          
        case _:
          raise ValueError(f"Unhandled local command: {user_input[0]}.")
    elif is_setting:
      setting, new_val = user_input
      if new_val == "default":
        settings[setting] = default_settings[setting]
        settings_file.close()
        dump_json(settings_path, settings)
        settings, settings_file = read_json(settings_path)
      else:
        match setting:
          case "default_language":
            if setting not in languages:
              print(f"Invalid language", file=sys.stderr)
              continue
            else:
              settings[setting] = new_val
              settings_file.close()
              dump_json(settings_path, settings)
              settings, settings_file = read_json(settings_path)
          case _:
            raise ValueError(f"Unhandled setting: {user_input[0]}.")
    else:
      raise ValueError(f"Unhandled case: {user_input}")

def handle_help():
  command_descriptions = [
    "list: Shows the current settings.",
    "reset: Resets all settings to default (asks for confirmation).",
    "<setting> default: Changes the given setting to have the default value.",
    "<setting> <new value>: Changes the given setting to have the" + 
                          " given new value, if possible."

  ]
  print("This menu supports the following inputs:")
  print_desc(command_descriptions) 
