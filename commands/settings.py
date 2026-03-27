import sys
from command_util import GLOBAL_COMMANDS, handle_global_command
def handle_commands(
    local_commands: set[str],
    exit_func
) -> None:
  while True:
    user_input = input("Input: ").strip().lower().split()
    first_cond = len(user_input) == 1 and user_input[0] in GLOBAL_COMMANDS
    second_cond = len(user_input) == 2 and user_input[0] in local_commands 
    if not first_cond and not second_cond:
      print("Unrecognized input. Type 'help' to see valid inputs.", file=sys.stderr)
      continue
    if user_input[0] in GLOBAL_COMMANDS:
      if not handle_global_command(user_input[0], handle_help, exit_func):
        return
    else:
      match user_input[0]:
        case "default_language":
          # todo
        case _:
          raise ValueError(f"Unhandled case {user_input}.")