from util.enums import GlobalCommand
from typing import assert_never, Type
from enum import Enum

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

def to_description_lines(enum: Type[Enum]) -> list[str]:
  # use lists to preserve ordering and since the enums do not have many fields
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

def print_desc(descs: list[str]) -> None:#
  for i, desc in enumerate(descs):
    print(f"{i+1}. {desc}.")