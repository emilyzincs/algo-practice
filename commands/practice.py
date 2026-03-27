import sys
from utils import print_desc, in_either
from command_util import GLOBAL_COMMANDS, handle_global_command

def handle_commands(
    local_commands: set[str],
    alg: str,
    run_tests_func,
    exit_func
) -> bool:
  correct = False
  while not correct:
    user_input = input("Type 'done' when you are finished or 'help' for help.\n")
    if not in_either(user_input, GLOBAL_COMMANDS, local_commands):
      print("Unrecognized input. Type 'help' to see valid inputs.", file=sys.stderr)
      continue
    
    if user_input in GLOBAL_COMMANDS:
      if not handle_global_command(user_input, handle_help, exit_func):
        return False
    else:
      match user_input:
        case "d" | "done":
          correct = run_tests_func(alg)
        case _:
          raise ValueError(f"Unhandled case {user_input}.")
    return True

def handle_help():
  command_descriptions = [
    "help: Lists commands",
    "q/quit/exit: Exits the program",
    "b/back: Cancels the current practice session and returns to the main menu",
    "d/done: Submits the current practice implementation to be tested",
  ]
  print("This menu supports the following inputs:")
  print_desc(command_descriptions) 