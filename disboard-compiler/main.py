#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
No Game No Life — Disboard Compiler (7 Matches, Sora & Shiro Edition)
Modular VS Code project — run main.py, paste your program, then END.
"""

from phases.theme import banner
from phases.input_gate import summon_script_from_human_realm
from phases.phase1_lex import phase1_print
from phases.phase2_parse import extract_print_exprs, phase2_print
from phases.phase3_symbols import phase3_print_and_menu
from phases.phase4_tac import phase4_print
from phases.phase5_opt import phase5_print
from phases.phase6_asm import phase6_print
from phases.phase7_verdict import phase7_print

def main():
    banner("NGNL — Disboard Compiler (Modular)", "♜")
    script_from_other_world = summon_script_from_human_realm()
    print()

    _ = phase1_print(script_from_other_world)

    exprs = extract_print_exprs(script_from_other_world)
    phase2_print(exprs)

    elkia_st = phase3_print_and_menu(script_from_other_world)

    original_tac = phase4_print(exprs) or []

    optimized_tac = phase5_print(original_tac) or []

    phase6_print(optimized_tac)

    phase7_print(script_from_other_world, elkia_st)

if __name__ == "__main__":
    main()
