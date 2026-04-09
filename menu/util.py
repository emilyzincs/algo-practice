from util.enums import GlobalCommand
from typing import assert_never, Type
from enum import Enum


# Handles global commands (i.e., commands that can be used in all menus). 
# Returns False if the command signals that the calling menu should 
# return to the previous menu.
#
# Parameters:
# - cmd: The GlobalCommand to execute.
# - help_func: Callable that displays help information.
# - exit_func: Callable that exits the program with a status code.
#
# Returns:
#   False if the command is a variant of 'back', otherwise True.
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
    case GlobalCommand.B | GlobalCommand.BACK:
      return False
    case _:
      assert_never(cmd)
  return True


# Converts an Enum into a list of description lines where aliases are grouped
# (e.g., "q/quit/exit: Exits the program"). Assumes that the Enum values are 
# (possibly non-unique) string descriptions. Preserves the order of first
# appearance.
#
# Parameters:
# - enum: The Enum class (e.g., GlobalCommand, SettingsCommand).
#
# Returns:
#   A list of strings, each formatted as "alias1/alias2/...: description".
def to_description_lines(enum: Type[Enum]) -> list[str]:
  # We use lists to preserve ordering and since the enums do not have many fields.
  descriptions: list[str] = []
  names: list[list[str]] = []
  for name, member in enum.__members__.items():
    name = name.strip().lower()
    found = False
    for i, desc in enumerate(descriptions):
      if member.value == desc:
        names[i].append(name)
        found = True
        break
    if not found:
      descriptions.append(member.value)
      names.append([name])
  if len(descriptions) != len(names):
    raise Exception("Descriptions and names lists must be the same size.")
  lines = ["/".join(names[i]) + f": {descriptions[i]}" for i in range(len(names))]
  return lines


# Prints a numbered list of description strings, each on its own line with a
# trailing period.
#
# Parameters:
# - descs: List of description strings to print.
def print_desc(descs: list[str]) -> None:#
  for i, desc in enumerate(descs):
    print(f"{i+1}. {desc}.")
