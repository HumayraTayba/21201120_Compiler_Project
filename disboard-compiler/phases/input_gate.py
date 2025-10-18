from typing import List
from .theme import banner, note, ok, S

def summon_script_from_human_realm() -> List[str]:
    banner("Disboard Input Gate", "🎴")
    note("Speak your program unto Tet.")
    print(f"{S.dim}(Ctrl+Z then Enter to end on Windows / Ctrl+D on *nix){S.reset}")
    print(f"{S.dim}Or type {S.bold}END{S.reset}{S.dim} on a new line to finish.{S.reset}")
    pages_of_elkia = []
    try:
        while True:
            line = input(f"{S.cyan}⊳{S.reset} ")
            if line.strip() == "END":
                break
            pages_of_elkia.append(line.rstrip("\n"))
    except EOFError:
        pass
    ok("Disboard has received your manuscript.")
    return pages_of_elkia
