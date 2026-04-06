from util.enums import GlobalCommand
from typing import assert_never

def handle_global_command(
  cmd: GlobalCommand,
  help_func,
  exit_func,
) -> bool:
  
  match cmd:
    case GlobalCommand.HELP:
      help_func()
    case GlobalCommand.Q | GlobalCommand.QUIT | GlobalCommand.EXIT:
      exit_func(0)
    case GlobalCommand.B | GlobalCommand.BACK :
      return False
    case _:
      assert_never(cmd)
  return True

def get_global_command_descriptions() -> list[str]:
  return [
    "help: Lists commands",
    "q/quit/exit: Exits the program",
    "b/back: Returns to the previous menu",
  ]