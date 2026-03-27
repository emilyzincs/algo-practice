import sys
from utils import print_desc

def handle_commands(
    user_input: str,
    commands: set[str]
) -> bool:
  if user_input not in commands:
    return False
  match user_input:
    case "help":
      handle_help()
    case "q" | "quit" | "exit":
      sys.exit(0)
    case "b" | "back":
      return False
    case _:
      raise ValueError("Reached default case when previous cases should have handled all commands")
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