import re
from typing import List
from .theme import banner, head, ok, err, hr, S
from .utils import NUMBER_RE

class ShiroExprParser:
    def __init__(self, s: str):
        self.tokens = self.tokenize(s)
        self.i = 0
    def tokenize(self, s: str) -> List[str]:
        tok = re.compile(rf'\s*("(?:[^"\\]|\\.)*"|[A-Za-z_]\w*|{NUMBER_RE}|==|!=|<=|>=|[()+\-*/%!<>])')
        out = []; pos=0
        while pos < len(s):
            m = tok.match(s, pos)
            if not m:
                if s[pos].isspace():
                    pos += 1; continue
                raise SyntaxError(f"Bad char: '{s[pos]}'")
            out.append(m.group(1))
            pos = m.end()
        out.append("$")
        return out
    def peek(self): return self.tokens[self.i]
    def eat(self, x=None):
        t = self.peek()
        if x and t != x: raise SyntaxError(f"Expected '{x}', got '{t}'")
        self.i += 1
        return t
    # E → T ((rel|+|-) T)*
    def parse_E(self):
        node=("E",[self.parse_T()])
        while self.peek() in ("+","-","==","!=","<=",">=","<",">"):
            op=self.eat(); node[1].append(op); node[1].append(self.parse_T())
        return node
    # T → F (('*'|'/'|'%') F)*
    def parse_T(self):
        node=("T",[self.parse_F()])
        while self.peek() in ("*","/","%"):
            op=self.eat(); node[1].append(op); node[1].append(self.parse_F())
        return node
    # F → ID | NUMBER | STRING | '!' F | '(' E ')'
    def parse_F(self):
        t=self.peek()
        if re.fullmatch(r'[A-Za-z_]\w*', t): self.eat(); return ("F",[t])
        if re.fullmatch(NUMBER_RE, t): self.eat(); return ("F",[t])
        if re.fullmatch(r'"(?:[^"\\]|\\.)*"', t): self.eat(); return ("F",[t])  # STRING
        if t=="!":
            self.eat("!")
            sub=self.parse_F()
            return ("F",[("NOT",[sub])])
        if t=="(":
            self.eat("("); e=self.parse_E(); self.eat(")")
            return ("F",[e])
        raise SyntaxError(f"Unexpected token: {t}")
    def parse(self):
        e=self.parse_E()
        if self.peek()!="$": raise SyntaxError("Extra tokens")
        return e

def shiro_print_tree(node, indent=0):
    sp="  "*indent
    if isinstance(node, tuple):
        label, kids=node
        print(sp + S.mag + label + S.reset)
        for k in kids: shiro_print_tree(k, indent+1)
    elif isinstance(node, list):
        for k in node: shiro_print_tree(k, indent)
    else:
        print(sp + S.cyan + str(node) + S.reset)

# --- Safe statement splitter (respects strings/escapes/parentheses)
def _split_statements(line: str) -> List[str]:
    parts=[]; buf=[]; depth=0; in_str=False; esc=False
    for ch in line:
        if in_str:
            buf.append(ch)
            if esc:
                esc=False
            elif ch == '\\':
                esc=True
            elif ch == '"':
                in_str=False
        else:
            if ch == '"':
                in_str=True; buf.append(ch)
            elif ch == '(':
                depth += 1; buf.append(ch)
            elif ch == ')':
                depth = max(0, depth-1); buf.append(ch)
            elif ch == ';' and depth == 0:
                stmt = ''.join(buf).strip()
                if stmt:
                    parts.append(stmt)
                buf=[]
            else:
                buf.append(ch)
    tail=''.join(buf).strip()
    if tail:
        parts.append(tail)
    return parts

def extract_print_exprs(elkia_pages: List[str]) -> List[str]:
    exprs=[]
    pat = re.compile(r'^\s*print\s*(?:\((.*?)\)|\s+(.*?))\s*$', re.DOTALL)
    for line in elkia_pages:
        for stmt in _split_statements(line):
            m = pat.match(stmt)
            if m:
                expr = m.group(1) if m.group(1) is not None else m.group(2)
                if expr is not None:
                    exprs.append(expr)
    return exprs

def phase2_print(exprs: List[str]):
    banner("【MATCH 2】 Syntax Duel — Shiro’s Parse Arena", "🗡")
    if not exprs:
        from .theme import warn
        warn("No print-expressions found in your challenge.\n")
        return
    for idx, ex in enumerate(exprs, start=1):
        head(f"Round {idx}: Input Spell", ex)
        print("\nResulting AST (Scroll revealed):")
        try:
            p=ShiroExprParser(ex); tree=p.parse()
            ok("Parse Successful! Behold the Tree:")
            shiro_print_tree(tree)
        except Exception as e:
            err(f"Parse Error: {e}")
        print()
        hr(light=True)
    print()
