from typing import List
from .theme import banner, warn, S

def asm_from_optimized_tac(opt_tac: List[str]) -> List[str]:
    asm=[]
    regA="R1"; regB="R2"
    for ln in opt_tac:
        if "=" not in ln: continue
        left, rhs = [x.strip() for x in ln.split("=",1)]
        parts = rhs.split()
        if len(parts)==1:
            asm.append(f"MOV {regA}, {parts[0]}        ; {left} = {parts[0]}")
        elif len(parts)==2 and parts[0]=="!":
            asm.append(f"MOV {regA}, {parts[1]}        ; {left} = ! {parts[1]}")
            asm.append(f"CMP {regA}, 0        ; set {left} to 1 if zero else 0 (toy)")
        elif len(parts)==3:
            a, op, b = parts
            if op=="*":
                asm.append(f"MOV {regA}, {a}        ; {regA} = {a}")
                asm.append(f"IMUL {regA}, {b}       ; {regA} = {a} * {b}")
                asm.append(f"; {left} ← {regA}")
            elif op=="+":
                asm.append(f"MOV {regB}, {a}        ; {regB} = {a}")
                asm.append(f"ADD {regB}, {b}        ; {regB} = {a} + {b}")
                asm.append(f"; {left} ← {regB}")
            elif op=="-":
                asm.append(f"MOV {regB}, {a}        ; {regB} = {a}")
                asm.append(f"SUB {regB}, {b}        ; {regB} = {a} - {b}")
                asm.append(f"; {left} ← {regB}")
            elif op=="/":
                asm.append(f"MOV {regA}, {a}        ; {regA} = {a}")
                asm.append(f"IDIV {regA}, {b}       ; {regA} = {a} / {b}")
                asm.append(f"; {left} ← {regA}")
            elif op=="%":
                asm.append(f"MOV {regA}, {a}        ; {regA} = {a}")
                asm.append(f"IMOD {regA}, {b}       ; {regA} = {a} % {b}")
                asm.append(f"; {left} ← {regA}")
            else:
                asm.append(f"MOV {regA}, {a}        ; {regA} = {a}")
                asm.append(f"CMP {regA}, {b}        ; compare, {left} = ({a} {op} {b})")
    return asm

def phase6_print(optimized_tac: List[str]):
    banner("【MATCH 6】 Jibril’s Assembly — Transmuting Wisdom to Steel", "📜")
    if not optimized_tac:
        warn("No optimized TAC to invoke the Flugel forge.\n")
        return
    print(f"{S.bold}Optimized TAC Ledger:{S.reset}\n")
    for ln in optimized_tac: print(ln)
    print(f"\n{S.bold}{S.cyan}✧ Flugel Smithy Output (Toy Assembly) ✧{S.reset}\n")
    asm = asm_from_optimized_tac(optimized_tac)
    for ln in asm: print(ln)
    print(f"\n{S.dim}; Results live in temps noted in comments. Praise the library!{S.reset}\n")
