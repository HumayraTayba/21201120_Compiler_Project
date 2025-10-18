from typing import List, Tuple
from .theme import banner, head, hr, S
from .phase2_parse import ShiroExprParser

tet_temp_counter=0
def new_temp()->str:
    global tet_temp_counter
    tet_temp_counter += 1
    return f"t{tet_temp_counter}"

def tac_for_expr(expr: str) -> Tuple[List[str], str]:
    p=ShiroExprParser(expr)
    tree=p.parse()

    def emit_E(node)->Tuple[List[str],str]:
        code, t = emit_T(node[1][0])
        i=1
        while i<len(node[1]):
            op=node[1][i]; right=node[1][i+1]
            rcode, rt = emit_T(right)
            out=new_temp(); code+=rcode
            code.append(f"{out} = {t} {op} {rt}")
            t=out; i+=2
        return code, t

    def emit_T(node)->Tuple[List[str],str]:
        code, t = emit_F(node[1][0])
        i=1
        while i<len(node[1]):
            op=node[1][i]; right=node[1][i+1]
            rcode, rt = emit_F(right)
            out=new_temp(); code+=rcode
            code.append(f"{out} = {t} {op} {rt}")
            t=out; i+=2
        return code, t

    def emit_F(node)->Tuple[List[str],str]:
        child=node[1][0]
        if isinstance(child, tuple):
            if child[0]=="NOT":
                scode, stmp = emit_F(child[1][0])
                out=new_temp()
                scode.append(f"{out} = ! {stmp}")
                return scode, out
            return emit_E(child)
        else:
            t=new_temp()
            return [f"{t} = {child}"], t

    code, out = emit_E(tree)
    return code, out

def phase4_print(exprs: List[str]):
    from .theme import banner, head, hr, S
    banner("【MATCH 4】 TAC Tactics — ‘Blank’ Writes the Moves", "♞")
    if not exprs:
        from .theme import warn
        warn("No print-expressions to translate into TAC.\n")
        return

    global tet_temp_counter
    tet_temp_counter=0
    all_tac=[]
    for ex in exprs:
        head("Incantation", ex)
        print(f"{S.bold}{S.cyan}--- Three Address Code (Battle Log) ---{S.reset}")
        code, res = tac_for_expr(ex)
        for ln in code: print(ln)
        print(f"\n{S.bold}Result bound in:{S.reset} {S.green}{res}{S.reset}\n")
        hr(light=True)
        all_tac.extend(code)
    print()
    return all_tac
