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
      exit_func()
    case "b" | "back":
      return False
    case _:
      raise ValueError("Reached default case when previous cases should " + 
                       "have handled all global commands")
  return False
