from typing import List

GLOBAL_COMMANDS = {"help", "q", "quit", "exit", "b", "back"}

def handle_global_command(
  cmd: str,
  help_func,
  exit_func,
) -> bool:
  if cmd not in GLOBAL_COMMANDS:
    raise ValueError(f"Not a global command: {cmd}.")

  match cmd:
    case "help":
      help_func()
    case "q" | "quit" | "exit":
      exit_func(0)
    case "b" | "back":
      return False
    case _:
      raise ValueError("Reached default case when previous cases should " + 
                       "have handled all global commands")
  return True

def get_global_command_descriptions() -> List[str]:
  return [
    "help: Lists commands",
    "q/quit/exit: Exits the program",
    "b/back: Returns to the previous menu",
  ]