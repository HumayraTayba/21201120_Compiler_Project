NGNL — Disboard Compiler (Modular, VS Code-friendly)

How to run (SUPER EASY, no PowerShell needed):
1) Unzip this folder anywhere (e.g., Desktop).
2) Open the folder in VS Code (File → Open Folder… → select "disboard-compiler").
3) Run "main.py":
   - EASIEST: In VS Code, open main.py and click "Run ▶" (top-right) or press F5 and choose "Python File".
   - Or via Command Prompt (NOT PowerShell): type  cd path\to\disboard-compiler  then  py main.py

4) Paste your program, one or more lines, then type END on a new line and press Enter.

Sample input you can paste:
print("hello World");
print("A" + "B");
print(5 + 7);
print("num=" + 42);
print(3.14 + 2.86);
print("pi≈" + 3.1416);
END

Project layout:
disboard-compiler/
  main.py
  phases/
    __init__.py
    theme.py
    utils.py
    input_gate.py
    phase1_lex.py
    phase2_parse.py
    phase3_symbols.py
    phase4_tac.py
    phase5_opt.py
    phase6_asm.py
    phase7_verdict.py
