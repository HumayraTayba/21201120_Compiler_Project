import re
from typing import Dict, List, Optional
from .theme import banner, ok, S
from .utils import NUMBER_RE

def optimize_tac(original: List[str]) -> List[str]:
    values: Dict[str, Optional[float]]={}
    const_cse: Dict[str,str]={}
    out=[]
    for line in original:
        if "=" not in line:
            out.append(line); continue
        left, rhs = [x.strip() for x in line.split("=",1)]
        parts = rhs.split()
        def asnum(tok)->Optional[float]:
            return float(tok) if re.fullmatch(NUMBER_RE, tok) else (values.get(tok) if tok in values else None)

        new_line=None
        if len(parts)==1:
            v=asnum(parts[0])
            values[left]=v
            new_line=f"{left} = {int(v) if v is not None and float(v).is_integer() else parts[0]}" if v is not None else f"{left} = {parts[0]}"
        elif len(parts)==2 and parts[0]=="!":
            v=asnum(parts[1])
            if v is not None:
                val = 0.0 if v!=0.0 else 1.0
                values[left]=val
                new_line=f"{left} = {int(val) if float(val).is_integer() else val}"
            else:
                values[left]=None; new_line=f"{left} = ! {parts[1]}"
        elif len(parts)==3:
            a, op, b = parts
            av=asnum(a); bv=asnum(b)
            if op=="*" and (a=="0" or b=="0" or av==0 or bv==0):
                values[left]=0.0; new_line=f"{left} = 0"
            elif op=="+" and (a=="0" or av==0): values[left]=bv; new_line=f"{left} = {b}"
            elif op=="+" and (b=="0" or bv==0): values[left]=av; new_line=f"{left} = {a}"
            elif av is not None and bv is not None:
                r=None
                if op=="+": r=av+bv
                elif op=="-": r=av-bv
                elif op=="*": r=av*bv
                elif op=="/": r=av/bv if bv!=0 else 0.0
                elif op=="%": r=av % bv if bv!=0 else 0.0
                elif op in ("==","!=","<","<=",">",">="):
                    ok_={
                        "==": av==bv,
                        "!=": av!=bv,
                        "<":  av<bv,
                        "<=": av<=bv,
                        ">":  av>bv,
                        ">=": av>=bv
                    }[op]
                    r=1.0 if ok_ else 0.0
                if r is not None:
                    values[left]=r
                    key=f"{a} {op} {b}"
                    if key in const_cse:
                        new_line=f"{left} = {const_cse[key]}"
                    else:
                        if float(r).is_integer(): r=int(r)
                        new_line=f"{left} = {r}"
                        const_cse[key]=left
            if new_line is None:
                values[left]=None; new_line=f"{left} = {a} {op} {b}"
        else:
            values[left]=None; new_line=f"{left} = {rhs}"
        out.append(new_line)
    return out

def phase5_print(original_tac: List[str]):
    banner("【MATCH 5】 Izuna’s Optimizer — No cheats, only brains!", "🦊")
    if not original_tac:
        print("Arena Log\n--- Original TAC ---\n(empty)\n\n--- Optimized TAC ---\n(empty)\n\n")
        return []
    print(f"{S.bold}{S.cyan}Arena Log{S.reset}")
    print(f"{S.bold}--- Original TAC ---{S.reset}")
    for ln in original_tac: print(ln)
    print(f"\n{S.bold}--- Optimized TAC (Tailwind of Wisdom) ---{S.reset}")
    optimized = optimize_tac(original_tac)
    for ln in optimized: print(ln)
    print()
    ok("Izuna purrs. Fewer instructions, same truth.")
    print()
    return optimized
