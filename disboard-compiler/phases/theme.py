import os, sys

class _Style:
    def __init__(self, on=True):
        self.on = on and not os.environ.get("NGNL_NO_COLOR", "").strip()
        self.reset = "\033[0m" if self.on else ""
        def c(code): return f"\033[{code}m" if self.on else ""
        # Colors
        self.red    = c("31")
        self.green  = c("32")
        self.yellow = c("33")
        self.blue   = c("34")
        self.mag    = c("35")
        self.cyan   = c("36")
        self.white  = c("97")
        # Bold/Dim
        self.bold   = c("1")
        self.dim    = c("2")

S = _Style(on=sys.stdout.isatty())

def banner(title: str, icon: str = "♟", accent=S.mag, edge=S.cyan):
    line = f"{edge}═{S.reset}" * 30
    print(f"{edge}╔{line}{edge}╗{S.reset}")
    print(f"{edge}║{S.reset} {accent}{icon}{S.reset} {S.bold}{title}{S.reset}")
    print(f"{edge}╚{line}{edge}╝{S.reset}")

def note(msg: str, icon="✧"):
    print(f"{S.cyan}{icon}{S.reset} {msg}")

def warn(msg: str):
    print(f"{S.yellow}⚠{S.reset} {msg}")

def err(msg: str):
    print(f"{S.red}✖{S.reset} {msg}")

def ok(msg: str):
    print(f"{S.green}✔{S.reset} {msg}")

def hr(light=False):
    ch = "─" if light else "═"
    print((S.dim if light else S.cyan) + ch*60 + S.reset)

def head(label: str, sub: str = ""):
    print(f"{S.bold}{S.mag}{label}{S.reset}")
    if sub:
        print(f"{S.dim}{sub}{S.reset}")
