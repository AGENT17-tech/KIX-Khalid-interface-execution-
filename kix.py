"""
██╗  ██╗██╗██╗  ██╗    ███╗   ███╗██╗  ██╗    ██╗██╗   ██╗
██║ ██╔╝██║╚██╗██╔╝    ████╗ ████║██║ ██╔╝    ██║██║   ██║
█████╔╝ ██║ ╚███╔╝     ██╔████╔██║█████╔╝     ██║██║   ██║
██╔═██╗ ██║ ██╔██╗     ██║╚██╔╝██║██╔═██╗     ██║╚██╗ ██╔╝
██║  ██╗██║██╔╝ ██╗    ██║ ╚═╝ ██║██║  ██╗    ██║ ╚████╔╝
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═══╝

KIX — Khalid Interface eXecution Language
Version: 4.0.0 (MK IV)
Author:  Khalid — AGENT17-tech
GitHub:  https://github.com/AGENT17-tech/kix

MK IV Features:
  ✦ Arrays with indexing + methods (push, pop, len, get, set)
  ✦ for..in..range loops
  ✦ String interpolation  "Hello {name}!"
  ✦ break / continue
  ✦ Compound assign  +=  -=  *=  /=
  ✦ Multiline strings  \" ... \"
  ✦ import system  import "file.kix"
  ✦ Improved error messages with line numbers
  ✦ --version  --help  CLI flags
  ✦ All MK I–III features preserved
"""

import re, sys, math, os, random
import pygame

KIX_VERSION = "4.0.0"
KIX_CODENAME = "MK IV"

# ═══════════════════════════════════════════════════════
#  PYGAME RUNTIME
# ═══════════════════════════════════════════════════════
pygame.init()
_screen = None
_clock  = pygame.time.Clock()
_FPS    = 60
_width  = 800
_height = 600

def _ensure_window(w=800, h=600, title="KIX"):
    global _screen, _width, _height
    if _screen is None:
        _width, _height = int(w), int(h)
        _screen = pygame.display.set_mode((_width, _height))
        pygame.display.set_caption(str(title))

def _parse_color(c):
    COLORS = {
        "black":"#000000","white":"#ffffff","red":"#ff0000",
        "green":"#00ff00","blue":"#0000ff","cyan":"#00ffff",
        "yellow":"#ffff00","magenta":"#ff00ff","gray":"#888888",
        "darkgray":"#444444","lightgray":"#cccccc","orange":"#ff8800",
        "purple":"#8800ff","pink":"#ff44aa","brown":"#8b4513",
        "navy":"#001f8a","teal":"#008080","lime":"#bfff00",
        "gold":"#ffd700","silver":"#c0c0c0","crimson":"#dc143c",
    }
    c = str(c).strip().lower()
    c = COLORS.get(c, c)
    if c.startswith("#") and len(c) == 7:
        return tuple(int(c[i:i+2], 16) for i in (1, 3, 5))
    return (255, 255, 255)

_event_keys_held = set()

def _pump():
    global _event_keys_held
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
            _event_keys_held.add(ev.key)
        if ev.type == pygame.KEYUP:
            _event_keys_held.discard(ev.key)

# ═══════════════════════════════════════════════════════
#  KIX ARRAY OBJECT
# ═══════════════════════════════════════════════════════
class KixArray:
    def __init__(self, items=None):
        self.items = list(items) if items else []

    def get(self, idx):
        i = int(idx)
        if i < 0 or i >= len(self.items):
            raise IndexError(f"Array index {i} out of bounds (size {len(self.items)})")
        return self.items[i]

    def set(self, idx, val):
        i = int(idx)
        if i < 0 or i >= len(self.items):
            raise IndexError(f"Array index {i} out of bounds (size {len(self.items)})")
        self.items[i] = val

    def push(self, val):
        self.items.append(val)
        return val

    def pop(self):
        if not self.items:
            raise RuntimeError("Cannot pop from empty array")
        return self.items.pop()

    def length(self):
        return len(self.items)

    def __repr__(self):
        return f"[{', '.join(repr(x) for x in self.items)}]"

    def __len__(self):
        return len(self.items)

# ═══════════════════════════════════════════════════════
#  BUILTINS
# ═══════════════════════════════════════════════════════
def _builtin_window(w=800, h=600, title="KIX"):
    _ensure_window(w, h, title)

def _builtin_clear(color="black"):
    _ensure_window()
    _pump()
    _screen.fill(_parse_color(color))

def _builtin_rect(x, y, w, h, color="white", border=0):
    _ensure_window()
    pygame.draw.rect(_screen, _parse_color(color),
                     (int(x), int(y), int(w), int(h)), int(border))

def _builtin_circle(x, y, r, color="white", border=0):
    _ensure_window()
    pygame.draw.circle(_screen, _parse_color(color),
                       (int(x), int(y)), int(r), int(border))

def _builtin_line(x1, y1, x2, y2, color="white", thick=1):
    _ensure_window()
    pygame.draw.line(_screen, _parse_color(color),
                     (int(x1), int(y1)), (int(x2), int(y2)), max(1, int(thick)))

def _builtin_triangle(x1,y1,x2,y2,x3,y3,color="white"):
    _ensure_window()
    pygame.draw.polygon(_screen, _parse_color(color),
                        [(int(x1),int(y1)),(int(x2),int(y2)),(int(x3),int(y3))])

def _builtin_text(msg, x, y, color="white", size=24):
    _ensure_window()
    f = pygame.font.SysFont("consolas", int(size))
    surf = f.render(str(msg), True, _parse_color(color))
    _screen.blit(surf, (int(x), int(y)))

def _builtin_flip():
    _ensure_window()
    pygame.display.flip()
    _clock.tick(_FPS)

def _builtin_fps(n):
    global _FPS
    _FPS = int(n)

def _builtin_get_fps():
    return int(_clock.get_fps())

def _builtin_width():
    return _width

def _builtin_height():
    return _height

def _builtin_key(k):
    _pump()
    k = str(k).upper()
    MAP = {
        "UP":pygame.K_UP,"DOWN":pygame.K_DOWN,
        "LEFT":pygame.K_LEFT,"RIGHT":pygame.K_RIGHT,
        "SPACE":pygame.K_SPACE,"ESC":pygame.K_ESCAPE,
        "ENTER":pygame.K_RETURN,"BACKSPACE":pygame.K_BACKSPACE,
        "LSHIFT":pygame.K_LSHIFT,"RSHIFT":pygame.K_RSHIFT,
        "TAB":pygame.K_TAB,
    }
    code = MAP.get(k)
    if code is None and len(k) == 1:
        code = getattr(pygame, f"K_{k.lower()}", None)
    if code is None: return 0
    keys = pygame.key.get_pressed()
    return 1 if keys[code] else 0

def _builtin_mouse_x():
    return pygame.mouse.get_pos()[0]

def _builtin_mouse_y():
    return pygame.mouse.get_pos()[1]

def _builtin_mouse_btn(btn=0):
    return 1 if pygame.mouse.get_pressed()[int(btn)] else 0

def _builtin_print(*args):
    print(*[str(a) for a in args])

def _builtin_input(prompt=""):
    return input(str(prompt))

def _builtin_sqrt(x):    return math.sqrt(float(x))
def _builtin_pow(x,n):   return math.pow(float(x), float(n))
def _builtin_floor(x):   return math.floor(float(x))
def _builtin_ceil(x):    return math.ceil(float(x))
def _builtin_round_(x,d=0): return round(float(x), int(d))
def _builtin_abs(x):     return abs(x)
def _builtin_min(*a):    return min(a)
def _builtin_max(*a):    return max(a)
def _builtin_clamp(v,lo,hi): return max(lo, min(hi, v))
def _builtin_sin(x):     return math.sin(float(x))
def _builtin_cos(x):     return math.cos(float(x))
def _builtin_tan(x):     return math.tan(float(x))
def _builtin_int_(x):    return int(float(x))
def _builtin_float_(x):  return float(x)
def _builtin_str_(x):    return str(x)
def _builtin_bool_(x):   return bool(x)
def _builtin_rand():     return random.random()
def _builtin_randint(a,b): return random.randint(int(a), int(b))
def _builtin_len(s):
    if isinstance(s, (KixArray, str)): return len(s)
    raise TypeError(f"len() not supported for {type(s).__name__}")

def _builtin_range(start, stop=None, step=1):
    if stop is None: start, stop = 0, start
    arr = KixArray()
    v = int(start)
    step = int(step) if step != 0 else 1
    while (step > 0 and v < int(stop)) or (step < 0 and v > int(stop)):
        arr.push(v)
        v += step
    return arr

def _builtin_array(*args):
    return KixArray(list(args))

def _builtin_typeof(x):
    if isinstance(x, bool):     return "bool"
    if isinstance(x, int):      return "int"
    if isinstance(x, float):    return "float"
    if isinstance(x, str):      return "str"
    if isinstance(x, KixArray): return "array"
    if isinstance(x, KixObject):return f"class:{x._class}"
    if x is None:               return "null"
    return "unknown"

def _builtin_exit(code=0):
    pygame.quit()
    sys.exit(int(code))

def _builtin_time():
    return pygame.time.get_ticks() / 1000.0

def _builtin_delay(ms):
    pygame.time.delay(int(ms))

def _builtin_upper(s): return str(s).upper()
def _builtin_lower(s): return str(s).lower()
def _builtin_split(s, sep=" "): return KixArray(str(s).split(str(sep)))
def _builtin_join(arr, sep=""): return str(sep).join(str(x) for x in arr.items)
def _builtin_contains(s, sub): return 1 if str(sub) in str(s) else 0
def _builtin_substr(s, start, length=-1):
    s = str(s); start = int(start)
    if length < 0: return s[start:]
    return s[start:start+int(length)]

BUILTINS = {
    # Graphics
    "window":   _builtin_window,
    "clear":    _builtin_clear,
    "rect":     _builtin_rect,
    "circle":   _builtin_circle,
    "line":     _builtin_line,
    "triangle": _builtin_triangle,
    "text":     _builtin_text,
    "flip":     _builtin_flip,
    "fps":      _builtin_fps,
    "get_fps":  _builtin_get_fps,
    "width":    _builtin_width,
    "height":   _builtin_height,
    # Input
    "key":      _builtin_key,
    "mouse_x":  _builtin_mouse_x,
    "mouse_y":  _builtin_mouse_y,
    "mouse_btn":_builtin_mouse_btn,
    # I/O
    "print":    _builtin_print,
    "input":    _builtin_input,
    # Math
    "sqrt":     _builtin_sqrt,
    "pow":      _builtin_pow,
    "floor":    _builtin_floor,
    "ceil":     _builtin_ceil,
    "round":    _builtin_round_,
    "abs":      _builtin_abs,
    "min":      _builtin_min,
    "max":      _builtin_max,
    "clamp":    _builtin_clamp,
    "sin":      _builtin_sin,
    "cos":      _builtin_cos,
    "tan":      _builtin_tan,
    "PI":       math.pi,
    # Type conversion
    "int":      _builtin_int_,
    "float":    _builtin_float_,
    "str":      _builtin_str_,
    "bool":     _builtin_bool_,
    "typeof":   _builtin_typeof,
    # Arrays
    "range":    _builtin_range,
    "array":    _builtin_array,
    # String utils
    "upper":    _builtin_upper,
    "lower":    _builtin_lower,
    "split":    _builtin_split,
    "join":     _builtin_join,
    "contains": _builtin_contains,
    "substr":   _builtin_substr,
    "len":      _builtin_len,
    # Random
    "rand":     _builtin_rand,
    "randint":  _builtin_randint,
    # System
    "exit":     _builtin_exit,
    "time":     _builtin_time,
    "delay":    _builtin_delay,
    # Constants
    "true":     True,
    "false":    False,
    "null":     None,
}

# ═══════════════════════════════════════════════════════
#  LEXER
# ═══════════════════════════════════════════════════════
KEYWORDS = {
    "fn","class","if","else","elif","while","for","in",
    "return","end","break","continue","and","or","not",
    "true","false","null","import","new",
}
TYPES = {"int","float","bool","str","arr"}

TOKEN_PATTERNS = [
    ("COMMENT",   r"//[^\n]*"),
    ("MLSTRING",  r'"""[\s\S]*?"""'),
    ("FSTRING",   r'f"[^"]*"'),
    ("FLOAT",     r"\d+\.\d+"),
    ("INT",       r"\d+"),
    ("STRING",    r'"[^"]*"'),
    ("ARROW",     r"->"),
    ("PLUSEQ",    r"\+="),
    ("MINUSEQ",   r"-="),
    ("STAREQ",    r"\*="),
    ("SLASHEQ",   r"/="),
    ("EQ",        r"=="),
    ("NEQ",       r"!="),
    ("LEQ",       r"<="),
    ("GEQ",       r">="),
    ("AND",       r"&&"),
    ("OR",        r"\|\|"),
    ("ID",        r"[a-zA-Z_][a-zA-Z0-9_]*"),
    ("ASSIGN",    r"="),
    ("LT",        r"<"),
    ("GT",        r">"),
    ("PLUS",      r"\+"),
    ("MINUS",     r"-"),
    ("STAR",      r"\*"),
    ("SLASH",     r"/"),
    ("MOD",       r"%"),
    ("LPAREN",    r"\("),
    ("RPAREN",    r"\)"),
    ("LBRACE",    r"\{"),
    ("RBRACE",    r"\}"),
    ("LBRACKET",  r"\["),
    ("RBRACKET",  r"\]"),
    ("COMMA",     r","),
    ("COLON",     r":"),
    ("SEMICOLON", r";"),
    ("DOT",       r"\."),
    ("NEWLINE",   r"\n"),
    ("SKIP",      r"[ \t\r]+"),
]

_MASTER = re.compile("|".join(f"(?P<{n}>{p})" for n, p in TOKEN_PATTERNS))

class Token:
    __slots__ = ("type","value","line")
    def __init__(self, t, v, line):
        self.type = t; self.value = v; self.line = line
    def __repr__(self):
        return f"Token({self.type},{self.value!r})"

def tokenize(src):
    tokens = []
    line   = 1
    for m in _MASTER.finditer(src):
        kind = m.lastgroup
        val  = m.group()
        if kind in ("SKIP","COMMENT"):
            line += val.count("\n"); continue
        if kind == "NEWLINE":
            line += 1; continue
        if kind == "MLSTRING":
            val = val[3:-3]  # strip """
        elif kind == "FSTRING":
            val = val[2:-1]  # strip f" and "
        elif kind == "STRING":
            val = val[1:-1]
        elif kind == "FLOAT":
            val = float(val)
        elif kind == "INT":
            val = int(val)
        elif kind == "ID":
            if val in KEYWORDS: kind = val.upper()
            elif val in TYPES:  kind = "TYPE"
        tokens.append(Token(kind, val, line))
    tokens.append(Token("EOF","",line))
    return tokens

# ═══════════════════════════════════════════════════════
#  AST NODES
# ═══════════════════════════════════════════════════════
class Node: pass

class Block(Node):
    def __init__(self, stmts): self.stmts = stmts

class VarDecl(Node):
    def __init__(self, type_, name, expr):
        self.type_=type_; self.name=name; self.expr=expr

class Assign(Node):
    def __init__(self, target, expr, op="="):
        self.target=target; self.expr=expr; self.op=op

class IndexAssign(Node):
    def __init__(self, obj, index, expr):
        self.obj=obj; self.index=index; self.expr=expr

class AttrAssign(Node):
    def __init__(self, obj, field, expr, op="="):
        self.obj=obj; self.field=field; self.expr=expr; self.op=op

class FnDecl(Node):
    def __init__(self, name, params, ret, body):
        self.name=name; self.params=params; self.ret=ret; self.body=body

class ClassDecl(Node):
    def __init__(self, name, parent, fields, methods):
        self.name=name; self.parent=parent; self.fields=fields; self.methods=methods

class If(Node):
    def __init__(self, branches, els):
        # branches = [(cond, block), ...]
        self.branches=branches; self.els=els

class While(Node):
    def __init__(self, cond, body): self.cond=cond; self.body=body

class For(Node):
    def __init__(self, var, iterable, body):
        self.var=var; self.iterable=iterable; self.body=body

class Return(Node):
    def __init__(self, expr): self.expr=expr

class Break(Node):    pass
class Continue(Node): pass

class Import(Node):
    def __init__(self, path): self.path=path

class Call(Node):
    def __init__(self, callee, args): self.callee=callee; self.args=args

class MethodCall(Node):
    def __init__(self, obj, method, args):
        self.obj=obj; self.method=method; self.args=args

class Index(Node):
    def __init__(self, obj, idx): self.obj=obj; self.idx=idx

class Attr(Node):
    def __init__(self, obj, field): self.obj=obj; self.field=field

class BinOp(Node):
    def __init__(self, op, left, right):
        self.op=op; self.left=left; self.right=right

class UnaryOp(Node):
    def __init__(self, op, operand): self.op=op; self.operand=operand

class ArrayLit(Node):
    def __init__(self, items): self.items=items

class Var(Node):
    def __init__(self, name): self.name=name

class Num(Node):
    def __init__(self, value): self.value=value

class Str(Node):
    def __init__(self, value): self.value=value

class FStr(Node):
    # value = template string with {expr} placeholders
    def __init__(self, value): self.value=value

class MlStr(Node):
    def __init__(self, value): self.value=value

class Bool(Node):
    def __init__(self, value): self.value=value

class Null(Node): pass

class PrintStmt(Node):
    def __init__(self, expr): self.expr=expr

# ═══════════════════════════════════════════════════════
#  PARSER
# ═══════════════════════════════════════════════════════
class KixSyntaxError(Exception):
    def __init__(self, msg, line=0):
        self.line = line
        super().__init__(f"[line {line}] SyntaxError: {msg}")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos    = 0

    def peek(self, offset=0):
        i = self.pos + offset
        return self.tokens[i] if i < len(self.tokens) else Token("EOF","",0)

    def consume(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, *types):
        tok = self.consume()
        if tok.type not in types:
            raise KixSyntaxError(
                f"Expected {' or '.join(types)}, got {tok.type!r} ({tok.value!r})",
                tok.line)
        return tok

    def match(self, *types):
        if self.peek().type in types:
            return self.consume()
        return None

    # ── TOP LEVEL ──
    def parse(self):
        stmts = []
        while self.peek().type != "EOF":
            stmts.append(self.parse_stmt())
        return Block(stmts)

    def parse_block(self):
        stmts = []
        stop = ("END","ELSE","ELIF","EOF")
        while self.peek().type not in stop:
            stmts.append(self.parse_stmt())
        return Block(stmts)

    # ── STATEMENTS ──
    def parse_stmt(self):
        tok = self.peek()

        if tok.type == "TYPE":        return self.parse_vardecl()
        if tok.type == "FN":          return self.parse_fndecl()
        if tok.type == "CLASS":       return self.parse_classdecl()
        if tok.type == "IF":          return self.parse_if()
        if tok.type == "WHILE":       return self.parse_while()
        if tok.type == "FOR":         return self.parse_for()
        if tok.type == "RETURN":
            self.consume()
            expr = self.parse_expr() if self.peek().type not in ("SEMICOLON","END","ELSE","ELIF","EOF") else Null()
            self.match("SEMICOLON")
            return Return(expr)
        if tok.type == "BREAK":
            self.consume(); self.match("SEMICOLON"); return Break()
        if tok.type == "CONTINUE":
            self.consume(); self.match("SEMICOLON"); return Continue()
        if tok.type == "IMPORT":
            self.consume()
            path = self.expect("STRING").value
            self.match("SEMICOLON")
            return Import(path)

        # print shorthand
        if tok.type == "ID" and tok.value == "print":
            self.consume()
            self.expect("LPAREN")
            expr = self.parse_expr()
            self.expect("RPAREN")
            self.match("SEMICOLON")
            return PrintStmt(expr)

        # Expression / assignment
        expr = self.parse_expr()

        # Compound assign
        comp = self.match("PLUSEQ","MINUSEQ","STAREQ","SLASHEQ")
        if comp:
            rhs = self.parse_expr(); self.match("SEMICOLON")
            op  = comp.type  # PLUSEQ etc
            if isinstance(expr, Var):
                return Assign(expr.name, rhs, op)
            if isinstance(expr, Attr):
                return AttrAssign(expr.obj, expr.field, rhs, op)

        # Plain assign
        if self.peek().type == "ASSIGN":
            self.consume()
            rhs = self.parse_expr(); self.match("SEMICOLON")
            if isinstance(expr, Var):
                return Assign(expr.name, rhs)
            if isinstance(expr, Attr):
                return AttrAssign(expr.obj, expr.field, rhs)
            if isinstance(expr, Index):
                return IndexAssign(expr.obj, expr.idx, rhs)
            raise KixSyntaxError("Invalid assignment target", tok.line)

        self.match("SEMICOLON")
        return expr

    def parse_vardecl(self):
        ttype = self.consume().value  # int/float/bool/str/arr
        name  = self.expect("ID").value
        self.expect("ASSIGN")
        expr  = self.parse_expr()
        self.match("SEMICOLON")
        return VarDecl(ttype, name, expr)

    def parse_fndecl(self):
        self.expect("FN")
        name   = self.expect("ID").value
        self.expect("LPAREN")
        params = []
        while self.peek().type != "RPAREN":
            pname = self.expect("ID").value
            ptype = None
            if self.match("COLON"):
                ptype = self.consume().value
            params.append((pname, ptype))
            if not self.match("COMMA"): break
        self.expect("RPAREN")
        ret = None
        if self.match("ARROW"):
            ret = self.consume().value
        self.expect("COLON")
        body = self.parse_block()
        self.expect("END")
        return FnDecl(name, params, ret, body)

    def parse_classdecl(self):
        self.expect("CLASS")
        name   = self.expect("ID").value
        parent = None
        if self.match("COLON") and self.peek().type == "ID":
            # class Dog: Animal:   — inheritance
            parent = self.consume().value
            self.expect("COLON")
        else:
            self.expect("COLON")
        fields  = []
        methods = []
        while self.peek().type not in ("END","EOF"):
            if self.peek().type == "FN":
                methods.append(self.parse_fndecl())
            else:
                # field declaration: name: type; or type name;
                if self.peek().type == "TYPE":
                    ftype = self.consume().value
                    fname = self.expect("ID").value
                else:
                    fname = self.expect("ID").value
                    self.expect("COLON")
                    ftype = self.consume().value
                self.match("SEMICOLON")
                fields.append((fname, ftype))
        self.expect("END")
        return ClassDecl(name, parent, fields, methods)

    def parse_if(self):
        self.expect("IF")
        cond   = self.parse_expr()
        self.expect("COLON")
        then   = self.parse_block()
        branches = [(cond, then)]
        while self.peek().type == "ELIF":
            self.consume()
            ec = self.parse_expr()
            self.expect("COLON")
            eb = self.parse_block()
            branches.append((ec, eb))
        els = None
        if self.match("ELSE"):
            self.expect("COLON")
            els = self.parse_block()
        self.expect("END")
        return If(branches, els)

    def parse_while(self):
        self.expect("WHILE")
        cond = self.parse_expr()
        self.expect("COLON")
        body = self.parse_block()
        self.expect("END")
        return While(cond, body)

    def parse_for(self):
        self.expect("FOR")
        var = self.expect("ID").value
        self.expect("IN")
        iterable = self.parse_expr()
        self.expect("COLON")
        body = self.parse_block()
        self.expect("END")
        return For(var, iterable, body)

    # ── EXPRESSIONS ──
    def parse_expr(self):   return self.parse_or()

    def parse_or(self):
        left = self.parse_and()
        while self.peek().type == "OR":
            self.consume(); left = BinOp("or", left, self.parse_and())
        return left

    def parse_and(self):
        left = self.parse_equality()
        while self.peek().type == "AND":
            self.consume(); left = BinOp("and", left, self.parse_equality())
        return left

    def parse_equality(self):
        left = self.parse_relational()
        while self.peek().type in ("EQ","NEQ"):
            op = self.consume().value
            left = BinOp(op, left, self.parse_relational())
        return left

    def parse_relational(self):
        left = self.parse_additive()
        while self.peek().type in ("LT","GT","LEQ","GEQ"):
            t  = self.consume()
            op = {"LT":"<","GT":">","LEQ":"<=","GEQ":">="}[t.type]
            left = BinOp(op, left, self.parse_additive())
        return left

    def parse_additive(self):
        left = self.parse_multiplicative()
        while self.peek().type in ("PLUS","MINUS"):
            op = self.consume().value
            left = BinOp(op, left, self.parse_multiplicative())
        return left

    def parse_multiplicative(self):
        left = self.parse_unary()
        while self.peek().type in ("STAR","SLASH","MOD"):
            op = self.consume().value
            left = BinOp(op, left, self.parse_unary())
        return left

    def parse_unary(self):
        if self.peek().type == "MINUS":
            self.consume(); return UnaryOp("-", self.parse_unary())
        if self.peek().type == "NOT":
            self.consume(); return UnaryOp("not", self.parse_unary())
        return self.parse_postfix()

    def parse_postfix(self):
        expr = self.parse_primary()
        while True:
            if self.peek().type == "DOT":
                self.consume()
                field = self.expect("ID").value
                if self.peek().type == "LPAREN":
                    self.consume()
                    args = self.parse_arglist()
                    self.expect("RPAREN")
                    expr = MethodCall(expr, field, args)
                else:
                    expr = Attr(expr, field)
            elif self.peek().type == "LBRACKET":
                self.consume()
                idx = self.parse_expr()
                self.expect("RBRACKET")
                expr = Index(expr, idx)
            elif self.peek().type == "LPAREN" and isinstance(expr, Var):
                self.consume()
                args = self.parse_arglist()
                self.expect("RPAREN")
                expr = Call(expr.name, args)
            else:
                break
        return expr

    def parse_arglist(self):
        args = []
        while self.peek().type != "RPAREN":
            args.append(self.parse_expr())
            if not self.match("COMMA"): break
        return args

    def parse_primary(self):
        tok = self.peek()
        if tok.type == "INT":      self.consume(); return Num(tok.value)
        if tok.type == "FLOAT":    self.consume(); return Num(tok.value)
        if tok.type == "STRING":   self.consume(); return Str(tok.value)
        if tok.type == "FSTRING":  self.consume(); return FStr(tok.value)
        if tok.type == "MLSTRING": self.consume(); return MlStr(tok.value)
        if tok.type == "TRUE":     self.consume(); return Bool(True)
        if tok.type == "FALSE":    self.consume(); return Bool(False)
        if tok.type == "NULL":     self.consume(); return Null()
        if tok.type == "NEW":
            self.consume()
            name = self.expect("ID").value
            self.expect("LPAREN")
            args = self.parse_arglist()
            self.expect("RPAREN")
            return Call(name, args)
        if tok.type == "ID":
            self.consume(); return Var(tok.value)
        if tok.type == "LBRACKET":
            self.consume()
            items = []
            while self.peek().type != "RBRACKET":
                items.append(self.parse_expr())
                if not self.match("COMMA"): break
            self.expect("RBRACKET")
            return ArrayLit(items)
        if tok.type == "LPAREN":
            self.consume()
            expr = self.parse_expr()
            self.expect("RPAREN")
            return expr
        raise KixSyntaxError(
            f"Unexpected token {tok.type!r} ({tok.value!r})", tok.line)

# ═══════════════════════════════════════════════════════
#  ENVIRONMENT
# ═══════════════════════════════════════════════════════
class Env:
    def __init__(self, parent=None):
        self.vars   = {}
        self.parent = parent

    def get(self, name):
        if name in self.vars: return self.vars[name]
        if self.parent:       return self.parent.get(name)
        raise NameError(f"Undefined: '{name}'")

    def set(self, name, val):
        self.vars[name] = val

    def assign(self, name, val):
        if name in self.vars:
            self.vars[name] = val; return
        if self.parent:
            self.parent.assign(name, val); return
        raise NameError(f"Undeclared variable: '{name}'")

class ReturnException(Exception):
    def __init__(self, v): self.value = v

class BreakException(Exception):    pass
class ContinueException(Exception): pass

# ═══════════════════════════════════════════════════════
#  KIX OBJECTS
# ═══════════════════════════════════════════════════════
class KixObject:
    def __init__(self, class_name, fields):
        object.__setattr__(self, "_class",   class_name)
        object.__setattr__(self, "_fields",  dict(fields))
        object.__setattr__(self, "_methods", {})

    def get(self, name):
        if name in self._fields:  return self._fields[name]
        if name in self._methods: return self._methods[name]
        raise AttributeError(f"No attribute '{name}' on {self._class}")

    def set(self, name, val):
        # allow setting new fields dynamically
        self._fields[name] = val

    def bind_method(self, name, fn):
        self._methods[name] = fn

    def __repr__(self):
        return f"<{self._class} {self._fields}>"

class KixClass:
    def __init__(self, decl, parent_class=None):
        self.decl         = decl
        self.parent_class = parent_class
    def __repr__(self): return f"<class {self.decl.name}>"

# ═══════════════════════════════════════════════════════
#  INTERPRETER
# ═══════════════════════════════════════════════════════
class KixRuntimeError(Exception):
    def __init__(self, msg, line=0):
        self.line = line
        super().__init__(f"[line {line}] RuntimeError: {msg}" if line else f"RuntimeError: {msg}")

class Interpreter:
    def __init__(self, base_dir="."):
        self.globals  = Env()
        self.base_dir = base_dir
        self._imported = set()
        for k, v in BUILTINS.items():
            self.globals.set(k, v)

    def run(self, node, env=None):
        if env is None: env = self.globals
        return self._eval(node, env)

    def _eval(self, node, env):
        t = type(node)

        if t is Block:
            r = None
            for s in node.stmts:
                r = self._eval(s, env)
            return r

        if t is Num:    return node.value
        if t is Str:    return node.value
        if t is MlStr:  return node.value
        if t is Bool:   return node.value
        if t is Null:   return None

        if t is FStr:
            return self._interp_fstring(node.value, env)

        if t is ArrayLit:
            return KixArray([self._eval(i, env) for i in node.items])

        if t is Var:
            return env.get(node.name)

        if t is VarDecl:
            val = self._eval(node.expr, env)
            val = self._coerce(node.type_, val)
            env.set(node.name, val)
            return val

        if t is Assign:
            val = self._eval(node.expr, env)
            if node.op != "=":
                cur = env.get(node.target)
                val = self._apply_compound(node.op, cur, val)
            env.assign(node.target, val)
            return val

        if t is IndexAssign:
            obj = self._eval(node.obj, env)
            idx = self._eval(node.index, env)
            val = self._eval(node.expr, env)
            if isinstance(obj, KixArray):
                obj.set(idx, val)
            elif isinstance(obj, str):
                raise KixRuntimeError("Strings are immutable")
            return val

        if t is AttrAssign:
            obj = self._eval(node.obj, env)
            val = self._eval(node.expr, env)
            if node.op != "=":
                cur = obj.get(node.field)
                val = self._apply_compound(node.op, cur, val)
            obj.set(node.field, val)
            return val

        if t is Attr:
            obj = self._eval(node.obj, env)
            return obj.get(node.field)

        if t is Index:
            obj = self._eval(node.obj, env)
            idx = self._eval(node.idx, env)
            if isinstance(obj, KixArray): return obj.get(idx)
            if isinstance(obj, str):      return obj[int(idx)]
            raise KixRuntimeError(f"Cannot index {type(obj).__name__}")

        if t is BinOp:
            return self._binop(node, env)

        if t is UnaryOp:
            v = self._eval(node.operand, env)
            if node.op == "-":   return -v
            if node.op == "not": return not v

        if t is FnDecl:
            env.set(node.name, self._make_fn(node, env))
            return None

        if t is ClassDecl:
            parent = env.get(node.parent) if node.parent else None
            env.set(node.name, KixClass(node, parent))
            return None

        if t is Call:
            fn   = env.get(node.callee)
            args = [self._eval(a, env) for a in node.args]
            return self._call(fn, args, node.callee)

        if t is MethodCall:
            obj  = self._eval(node.obj, env)
            args = [self._eval(a, env) for a in node.args]
            return self._method_call(obj, node.method, args)

        if t is If:
            for cond, blk in node.branches:
                if self._eval(cond, env):
                    return self._eval(blk, Env(env))
            if node.els:
                return self._eval(node.els, Env(env))
            return None

        if t is While:
            while self._eval(node.cond, env):
                try:
                    self._eval(node.body, Env(env))
                except BreakException:
                    break
                except ContinueException:
                    continue
            return None

        if t is For:
            iterable = self._eval(node.iterable, env)
            if isinstance(iterable, KixArray):
                items = iterable.items
            elif isinstance(iterable, str):
                items = list(iterable)
            else:
                raise KixRuntimeError(f"Cannot iterate over {type(iterable).__name__}")
            for item in items:
                local = Env(env)
                local.set(node.var, item)
                try:
                    self._eval(node.body, local)
                except BreakException:
                    break
                except ContinueException:
                    continue
            return None

        if t is Return:
            raise ReturnException(self._eval(node.expr, env))

        if t is Break:
            raise BreakException()

        if t is Continue:
            raise ContinueException()

        if t is Import:
            self._import(node.path)
            return None

        if t is PrintStmt:
            val = self._eval(node.expr, env)
            print(str(val) if not isinstance(val, bool) else ("true" if val else "false"))
            return val

        return None  # expression-as-statement fallthrough

    # ── F-STRING INTERPOLATION ──
    def _interp_fstring(self, template, env):
        result = ""
        i = 0
        while i < len(template):
            if template[i] == "{" and i+1 < len(template):
                end = template.find("}", i)
                if end == -1:
                    result += template[i:]; break
                expr_src = template[i+1:end]
                try:
                    tokens = tokenize(expr_src)
                    val    = self._eval(Parser(tokens).parse_expr(), env)
                    result += str(val)
                except Exception:
                    result += "{" + expr_src + "}"
                i = end + 1
            else:
                result += template[i]; i += 1
        return result

    # ── COMPOUND ASSIGN OPS ──
    def _apply_compound(self, op, left, right):
        if op == "PLUSEQ":  return left + right
        if op == "MINUSEQ": return left - right
        if op == "STAREQ":  return left * right
        if op == "SLASHEQ": return left / right if right != 0 else 0
        return right

    # ── BINARY OPS ──
    def _binop(self, node, env):
        op = node.op
        if op == "and":
            return bool(self._eval(node.left, env)) and bool(self._eval(node.right, env))
        if op == "or":
            return bool(self._eval(node.left, env)) or  bool(self._eval(node.right, env))
        left  = self._eval(node.left,  env)
        right = self._eval(node.right, env)
        if op == "+":
            # String concat support
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
            return left + right
        if op == "-":  return left - right
        if op == "*":  return left * right
        if op == "/":  return left / right if right != 0 else 0
        if op == "%":  return left % right
        if op == "==": return left == right
        if op == "!=": return left != right
        if op == "<":  return left <  right
        if op == ">":  return left >  right
        if op == "<=": return left <= right
        if op == ">=": return left >= right
        raise KixRuntimeError(f"Unknown operator: {op!r}")

    # ── TYPE COERCION ──
    def _coerce(self, type_, val):
        try:
            if type_ == "int":   return int(float(val))   if val is not None else 0
            if type_ == "float": return float(val)         if val is not None else 0.0
            if type_ == "bool":  return bool(val)
            if type_ == "str":   return str(val)           if val is not None else ""
            if type_ == "arr":
                if isinstance(val, KixArray): return val
                return KixArray([val])
        except (ValueError, TypeError):
            pass
        return val

    # ── FUNCTION FACTORY ──
    def _make_fn(self, decl, closure_env):
        interp = self
        def fn(*args):
            local = Env(closure_env)
            for i, (pname, ptype) in enumerate(decl.params):
                v = args[i] if i < len(args) else None
                if ptype: v = interp._coerce(ptype, v)
                local.set(pname, v)
            try:
                interp._eval(decl.body, local)
            except ReturnException as r:
                return r.value
            return None
        fn.__name__ = decl.name
        return fn

    # ── CALL DISPATCH ──
    def _call(self, fn, args, name="?"):
        if isinstance(fn, KixClass):
            return self._instantiate(fn, args)
        if callable(fn):
            try:
                return fn(*args)
            except BreakException: raise
            except ContinueException: raise
            except ReturnException: raise
            except Exception as e:
                raise KixRuntimeError(f"In call to '{name}': {e}")
        raise KixRuntimeError(f"'{name}' is not callable")

    def _method_call(self, obj, method, args):
        # Built-in array methods
        if isinstance(obj, KixArray):
            m = {
                "push":    lambda: obj.push(args[0]),
                "pop":     lambda: obj.pop(),
                "len":     lambda: obj.length(),
                "get":     lambda: obj.get(args[0]),
                "set":     lambda: obj.set(args[0], args[1]),
                "append":  lambda: obj.push(args[0]),
                "clear":   lambda: obj.items.clear() or None,
                "contains":lambda: 1 if args[0] in obj.items else 0,
                "reverse": lambda: obj.items.reverse() or obj,
                "join":    lambda: (args[0] if args else "").join(str(x) for x in obj.items),
            }.get(method)
            if m: return m()
            raise KixRuntimeError(f"Array has no method '{method}'")
        # Built-in string methods
        if isinstance(obj, str):
            m = {
                "upper":    lambda: obj.upper(),
                "lower":    lambda: obj.lower(),
                "len":      lambda: len(obj),
                "split":    lambda: KixArray(obj.split(args[0] if args else " ")),
                "contains": lambda: 1 if (args[0] if args else "") in obj else 0,
                "replace":  lambda: obj.replace(str(args[0]), str(args[1])),
                "trim":     lambda: obj.strip(),
                "startswith":lambda: 1 if obj.startswith(str(args[0])) else 0,
                "endswith": lambda: 1 if obj.endswith(str(args[0])) else 0,
            }.get(method)
            if m: return m()
            raise KixRuntimeError(f"String has no method '{method}'")
        # KixObject methods
        if isinstance(obj, KixObject):
            fn = obj.get(method)
            return self._call(fn, args, method)
        raise KixRuntimeError(f"Cannot call method '{method}' on {type(obj).__name__}")

    # ── CLASS INSTANTIATION ──
    def _instantiate(self, klass, init_args):
        decl = klass.decl
        # Collect fields from parent chain
        all_fields = []
        cur = klass
        chain = []
        while cur:
            chain.insert(0, cur.decl)
            cur = cur.parent_class
        for d in chain:
            all_fields += d.fields

        fields = {f: None for f, _ in all_fields}
        obj    = KixObject(decl.name, fields)

        # Bind all methods (parent first, child overrides)
        all_methods = []
        for d in chain:
            all_methods += d.methods

        interp = self
        for m in all_methods:
            def make_bound(m, obj):
                def bound(*args):
                    local = Env(interp.globals)
                    local.set("self", obj)
                    for i, (pname, ptype) in enumerate(m.params):
                        v = args[i] if i < len(args) else None
                        local.set(pname, v)
                    try:
                        interp._eval(m.body, local)
                    except ReturnException as r:
                        return r.value
                    return None
                return bound
            obj.bind_method(m.name, make_bound(m, obj))

        # Call init() if defined
        if "init" in obj._methods:
            obj._methods["init"](*init_args)

        return obj

    # ── IMPORT ──
    def _import(self, path):
        full = os.path.join(self.base_dir, path)
        if full in self._imported: return
        self._imported.add(full)
        try:
            with open(full, "r") as f:
                src = f.read()
        except FileNotFoundError:
            raise KixRuntimeError(f"Import not found: '{path}'")
        tokens = tokenize(src)
        ast    = Parser(tokens).parse()
        self._eval(ast, self.globals)

# ═══════════════════════════════════════════════════════
#  PIPELINE
# ═══════════════════════════════════════════════════════
def execute(src, interp=None, base_dir="."):
    if interp is None:
        interp = Interpreter(base_dir=base_dir)
    tokens = tokenize(src)
    ast    = Parser(tokens).parse()
    interp.run(ast)
    return interp

# ═══════════════════════════════════════════════════════
#  REPL
# ═══════════════════════════════════════════════════════
BANNER = f"""
╔══════════════════════════════════════════════╗
║  ██╗  ██╗██╗██╗  ██╗                        ║
║  ██║ ██╔╝██║╚██╗██╔╝                        ║
║  █████╔╝ ██║ ╚███╔╝   MK IV  v{KIX_VERSION}        ║
║  ██╔═██╗ ██║ ██╔██╗                         ║
║  ██║  ██╗██║██╔╝ ██╗   by  AGENT17-tech     ║
║  ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝                        ║
║  github.com/AGENT17-tech/kix                 ║
╚══════════════════════════════════════════════╝
  type 'exit' to quit  |  'help' for commands
"""

HELP_TEXT = """
KIX MK IV — Command Reference
──────────────────────────────
Types:      int  float  bool  str  arr
Blocks:     if ... elif ... else ... end
Loops:      while ... end | for x in arr: ... end
Functions:  fn name(a: int) -> int: ... end
Classes:    class Name: field: type; fn method(): end
Arrays:     arr x = [1, 2, 3];  x.push(4);  x[0]
Strings:    f"Hello {name}!"   (f-strings)
Import:     import "utils.kix"
Ops:        +  -  *  /  %  ==  !=  <  >  <=  >=
Compound:   +=  -=  *=  /=
Logic:      and  or  not  &&  ||
Control:    break  continue  return
Graphics:   window  clear  rect  circle  line  text  flip
Input:      key("W")  mouse_x()  mouse_btn()
Math:       sqrt  pow  sin  cos  abs  floor  ceil  clamp
"""

def repl():
    print(BANNER)
    interp = Interpreter()
    buf    = []
    depth  = 0

    while True:
        try:
            prompt = "KIX> " if depth == 0 else f"...{'  '*depth}"
            line   = input(prompt)
        except (KeyboardInterrupt, EOFError):
            print("\n[KIX offline]"); break

        stripped = line.strip()
        if stripped == "exit":
            print("[KIX offline]"); break
        if stripped == "help":
            print(HELP_TEXT); continue
        if stripped == "clear":
            os.system("cls" if os.name == "nt" else "clear"); continue
        if stripped.startswith("run "):
            run_file(stripped[4:].strip()); continue

        buf.append(line)
        opens  = len(re.findall(r'\b(if|while|for|fn|class)\b', line))
        closes = len(re.findall(r'\bend\b', line))
        depth  = max(0, depth + opens - closes)

        if depth <= 0:
            depth = 0
            src   = "\n".join(buf); buf.clear()
            if src.strip():
                try:
                    execute(src, interp)
                except (KixSyntaxError, KixRuntimeError, NameError) as e:
                    print(f"  {e}")
                except Exception as e:
                    print(f"  Error: {e}")

# ═══════════════════════════════════════════════════════
#  FILE RUNNER
# ═══════════════════════════════════════════════════════
def run_file(path):
    if not os.path.exists(path):
        print(f"kix: file not found: '{path}'"); return
    base = os.path.dirname(os.path.abspath(path))
    try:
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        execute(src, base_dir=base)
    except (KixSyntaxError, KixRuntimeError) as e:
        print(f"\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        raise

# ═══════════════════════════════════════════════════════
#  CLI ENTRY POINT
# ═══════════════════════════════════════════════════════
def main():
    args = sys.argv[1:]

    if not args:
        repl(); return

    if args[0] in ("--version", "-v"):
        print(f"KIX {KIX_VERSION} ({KIX_CODENAME}) — AGENT17-tech"); return

    if args[0] in ("--help", "-h"):
        print(HELP_TEXT); return

    if args[0] == "--check":
        # Syntax check only, no execution
        if len(args) < 2:
            print("Usage: kix --check <file.kix>"); return
        try:
            with open(args[1]) as f: src = f.read()
            tokenize(src)
            Parser(tokenize(src)).parse()
            print(f"OK: {args[1]}")
        except (KixSyntaxError, Exception) as e:
            print(f"FAIL: {e}"); sys.exit(1)
        return

    run_file(args[0])

if __name__ == "__main__":
    main()
