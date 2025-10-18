import re
from dataclasses import dataclass
from typing import List

# Shared regexes/tokens
NUMBER_RE = r'\d+(?:\.\d+)?'  # unified number regex (int or float)

ELKIA_BOOK_OF_TOKENS = [
    ("STRING",   r'"(?:[^"\\]|\\.)*"'),
    ("NUMBER",   NUMBER_RE),
    ("ID",       r'[A-Za-z_][A-Za-z0-9_]*'),
    ("EQ",       r'=='),
    ("NE",       r'!='),
    ("LE",       r'<='),
    ("GE",       r'>='),
    ("LT",       r'<'),
    ("GT",       r'>'),
    ("ASSIGN",   r'='),
    ("PLUS",     r'\+'),
    ("MINUS",    r'-'),
    ("STAR",     r'\*'),
    ("SLASH",    r'/'),
    ("PERCENT",  r'%'),
    ("NOT",      r'!'),
    ("COMMA",    r','),
    ("SEMICOL",  r';'),
    ("LPAREN",   r'\('),
    ("RPAREN",   r'\)'),
    ("LBRACE",   r'\{'),
    ("RBRACE",   r'\}'),
    ("WS",       r'[ \t\r\n]+'),
    ("COMMENT",  r'//[^\n]*'),
]

DISBOARD_KEYWORDS = {"let","print","if","else","while","true","false","int","void","return","main"}

GOD_TET_REGEX = re.compile("|".join(f"(?P<{n}>{r})" for n, r in ELKIA_BOOK_OF_TOKENS))

@dataclass
class ManaToken:
    typ: str
    lex: str
    line: int
    col: int

def sora_scans_lines(lines: List[str]) -> List[ManaToken]:
    tokens: List[ManaToken] = []
    for li, line in enumerate(lines, start=1):
        i = 0
        while i < len(line):
            m = GOD_TET_REGEX.match(line, i)
            if not m:
                snippet = line[i:i+20]
                raise SyntaxError(f"Lex error on line {li}, near: '{snippet}'")
            kind = m.lastgroup
            lexeme = m.group()
            start = m.start()
            i = m.end()
            if kind in ("WS", "COMMENT"):
                continue
            if kind == "ID" and lexeme in DISBOARD_KEYWORDS:
                tokens.append(ManaToken("KEYWORD", lexeme, li, start+1))
            else:
                tokens.append(ManaToken(kind, lexeme, li, start+1))
    return tokens

def imanity_unique(seq):
    seen = set()
    out = []
    for x in seq:
        if x not in seen:
            seen.add(x); out.append(x)
    return out
