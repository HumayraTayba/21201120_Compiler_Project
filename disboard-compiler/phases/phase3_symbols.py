from typing import Any, Dict, List, Tuple
from .theme import banner, head, hr, ok, S
from .utils import sora_scans_lines, NUMBER_RE

class _SymbolTableView:
    def __init__(self, rows: List[Dict[str, Any]]):
        self.scrolls = rows

def normalize_symbol_table(obj: Any) -> _SymbolTableView:
    if hasattr(obj, "scrolls"):
        rows = list(getattr(obj, "scrolls"))
    elif isinstance(obj, list) and (not obj or isinstance(obj[0], dict)):
        rows = list(obj)
    else:
        raise TypeError("Match 3: Unsupported symbol table structure from code-2.")

    # ensure keys
    fixed = []
    addr = 1000
    for r in rows:
        rr = dict(r)
        rr.setdefault("Name",  rr.get("name",  rr.get("id", "<?>")))
        rr.setdefault("Type",  rr.get("type",  "num"))
        rr.setdefault("Size",  rr.get("size",  8))
        rr.setdefault("Dim",   rr.get("dim",   "0D"))
        rr.setdefault("Line",  rr.get("line",  -1))
        rr.setdefault("Address", rr.get("address", rr.get("addr", addr)))
        if "Address" not in r:
            addr += int(rr["Size"]) if isinstance(rr["Size"], int) else 8
        fixed.append(rr)
    return _SymbolTableView(fixed)

def collect_decls(elkia_pages: List[str]) -> List[Tuple[str,int]]:
    import re
    decls=[]
    for i, line in enumerate(elkia_pages, start=1):
        m=re.match(r'\s*let\s+([A-Za-z_]\w*)\s*=', line)
        if m: decls.append((m.group(1), i))
    return decls

def run_match3_and_get_symbol_table(elkia_pages: List[str]) -> Any:
    """
    Symbol table includes:
      - variables declared via: let <id> = ...
      - constants encountered (NUMBER, STRING), typed as int/float
    """
    rows: List[Dict[str, Any]] = []
    addr = 1000

    # declared variables
    for name, ln in collect_decls(elkia_pages):
        rows.append({
            "Name": name, "Type": "var", "Size": 8, "Dim": "0D", "Line": ln, "Address": addr
        })
        addr += 8

    # constants (unique)
    try:
        toks = sora_scans_lines(elkia_pages)
    except Exception:
        toks = []

    seen = set()
    for t in toks:
        if t.typ in ("NUMBER", "STRING"):
            key = (t.typ, t.lex)
            if key in seen:
                continue
            seen.add(key)
            if t.typ == "NUMBER":
                is_float = "." in t.lex
                num_type = "const-float" if is_float else "const-int"
                rows.append({
                    "Name": t.lex, "Type": num_type, "Size": 8, "Dim": "0D",
                    "Line": t.line, "Address": addr
                })
                addr += 8
            else:
                size = max(8, len(t.lex))
                rows.append({
                    "Name": t.lex, "Type": "const-str", "Size": size, "Dim": "0D",
                    "Line": t.line, "Address": addr
                })
                addr += size

    return rows

def phase3_print_and_menu(elkia_pages: List[str]):
    banner("【MATCH 3】 Steph’s Bookkeeping — Elkia Guild Ledger", "📚")
    raw_table = run_match3_and_get_symbol_table(elkia_pages)
    st = normalize_symbol_table(raw_table)

    print(f"\n{S.bold}{S.cyan}--- Elkia Guild Ledger (Symbol Table) ---{S.reset}")
    print("{:<12} {:<9} {:<7} {:<9} {:<7} {:<8}".format(
        "Name","Type","Size","Dim","Line","Address"))
    print(S.dim + "-"*62 + S.reset)
    if not st.scrolls:
        print("(empty)")
    else:
        for r in st.scrolls:
            print("{:<12} {:<9} {:<7} {:<9} {:<7} {:<8}".format(
                r.get("Name","<?>"), r.get("Type","num"), r.get("Size",8),
                r.get("Dim","0D"), r.get("Line",-1), r.get("Address",0)))
    print()
    ok("Guild ledger prepared. Steph smiles (a little).")
    print()
    return st
