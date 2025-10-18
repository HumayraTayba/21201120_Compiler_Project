from typing import List
from .theme import banner, head, hr, S
from .utils import sora_scans_lines, imanity_unique

def phase1_print(elkia_pages: List[str]):
    banner("【MATCH 1】 Tet’s Lexical Trial — Scanner of Disboard", "🃏")
    head("Outcome", "Ink crystallized into tokens")
    hr(light=True)

    tokens = sora_scans_lines(elkia_pages)

    keywords    = [t.lex for t in tokens if t.typ == "KEYWORD"]
    identifiers = [t.lex for t in tokens if t.typ == "ID"]
    constants   = [t.lex for t in tokens if t.typ in ("NUMBER","STRING")] + \
                  [t.lex for t in tokens if t.typ == "KEYWORD" and t.lex in ("true","false")]

    arith_map = {"PLUS":"+","MINUS":"-","STAR":"*","SLASH":"/","PERCENT":"%"}
    logic_map = {"EQ":"==","NE":"!=","LE":"<=","GE":">=","LT":"<","GT":">","NOT":"!"}
    punct_map = {"COMMA":",","SEMICOL":";"}
    par_map   = {"LPAREN":"(","RPAREN":")","LBRACE":"{","RBRACE":"}"}

    arith_ops = [arith_map[t.typ] for t in tokens if t.typ in arith_map]
    logic_ops = [logic_map[t.typ] for t in tokens if t.typ in logic_map]
    puncts    = [punct_map[t.typ] for t in tokens if t.typ in punct_map]
    parens    = [par_map[t.typ]   for t in tokens if t.typ in par_map]

    def line(lbl, items):
        u = imanity_unique(items)
        print(f"{S.bold}{lbl}{S.reset} {S.dim}({len(u)}){S.reset}: " + ("  ".join(u) + "  " if u else ""))

    print(f"{S.bold}{S.cyan}--- Token Chronicle (Elkia Ledger) ---{S.reset}")
    line("Sacred Keyword",    keywords)
    line("Named Piece (Identifier)", identifiers)
    line("Arithmetic Sigil", arith_ops)
    line("Logical Sigil",    logic_ops)
    line("Constant Seal",    constants)
    line("Punctuation Mark", puncts)
    line("Bracket Rune",     parens)
    print()
    return tokens
