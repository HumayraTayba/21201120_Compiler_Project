from typing import Any, Dict, List, Tuple, Set
from .theme import banner, ok, err, S
from .utils import sora_scans_lines, DISBOARD_KEYWORDS
from .phase3_symbols import collect_decls

def collect_uses(elkia_pages: List[str]) -> List[Tuple[str,int]]:
    tokens = sora_scans_lines(elkia_pages)
    decls_on_line: Dict[int, set] = {}
    for name, ln in collect_decls(elkia_pages):
        decls_on_line.setdefault(ln, set()).add(name)
    uses: List[Tuple[str,int]] = []
    for t in tokens:
        if t.typ == "ID" and t.lex not in DISBOARD_KEYWORDS:
            if t.line in decls_on_line and t.lex in decls_on_line[t.line]:
                continue
            uses.append((t.lex, t.line))
    return uses

def phase7_print(elkia_pages: List[str], st: Any):
    banner("【MATCH 7】 Tet’s Verdict — Audit of Names & Sins", "⚖")
    print(f"{S.bold}Elkia Ledger Snapshot:{S.reset}\n")
    print("Identifier   | Type | Scope   | Address")
    print("-"*39)
    scrolls = getattr(st, "scrolls", [])
    for r in scrolls:
        scope="local"
        print(f"{r.get('Name','<?>'):<12} | {r.get('Type','num'):<4} | {scope:<7} | {r.get('Address',0)}")
    if not scrolls:
        print("(none)")
    print(f"\n{S.bold}Error Scrolls:{S.reset}\n")
    declared: Set[str] = {
        r.get("Name")
        for r in scrolls
        if r.get("Type") in ("var", "num")
    }
    errors=[]
    for name, ln in collect_uses(elkia_pages):
        if name not in declared:
            errors.append(f"Error: Undeclared identifier '{name}' at line {ln}")
    if errors:
        for e in errors: err(e)
    else:
        ok("No semantic errors detected by Tet.")
    print()
    print(f"{S.bold}{S.green}Tet’s Verdict delivered. The game was beautiful.{S.reset} (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧")
    print()
