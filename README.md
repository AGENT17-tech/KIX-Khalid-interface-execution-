# KIX — Khalid Interface eXecution Language

```
██╗  ██╗██╗██╗  ██╗    ███╗   ███╗██╗  ██╗    ██╗██╗   ██╗
██║ ██╔╝██║╚██╗██╔╝    ████╗ ████║██║ ██╔╝    ██║██║   ██║
█████╔╝ ██║ ╚███╔╝     ██╔████╔██║█████╔╝     ██║██║   ██║
██╔═██╗ ██║ ██╔██╗     ██║╚██╔╝██║██╔═██╗     ██║╚██╗ ██╔╝
██║  ██╗██║██╔╝ ██╗    ██║ ╚═╝ ██║██║  ██╗    ██║ ╚████╔╝
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═══╝
```

> **A custom interpreted programming language with C++-inspired syntax, built-in graphics, and a Pong game written entirely in itself.**

**Author:** Khalid — [AGENT17-tech](https://github.com/AGENT17-tech)  
**Version:** 4.0.0 (MK IV)  
**Extension:** `.kix`

---

## Features — MK IV

| Feature | Status |
|---|---|
| Static types: `int` `float` `bool` `str` `arr` | ✅ |
| Functions with return types | ✅ |
| Classes with inheritance | ✅ |
| Arrays with methods (`push`, `pop`, `len`, ...) | ✅ |
| `for x in arr:` loops | ✅ |
| `break` / `continue` | ✅ |
| Compound assign `+=` `-=` `*=` `/=` | ✅ |
| F-strings `f"Hello {name}!"` | ✅ |
| Multiline strings `"""..."""` | ✅ |
| `import "file.kix"` system | ✅ |
| Built-in 2D graphics (pygame) | ✅ |
| Mouse + keyboard input | ✅ |
| Math builtins: `sin` `cos` `sqrt` `clamp` ... | ✅ |
| REPL with multi-line support | ✅ |
| `--check` syntax validator | ✅ |

---

## Quick Start

```bash
# Install dependency
pip install pygame

# Run REPL
python kix.py

# Run a file
python kix.py pong.kix

# Syntax check only
python kix.py --check myfile.kix

# Version
python kix.py --version
```

---

## Syntax Overview

```kix
// Variables — typed
int    score = 0;
float  speed = 3.5;
bool   alive = true;
str    name  = "Khalid";

// F-strings
str msg = f"Score: {score}";

// Arrays
arr nums = [1, 2, 3];
nums.push(4);
print(nums.len());   // 4
print(nums[0]);      // 1

// For loop
for x in range(5):
    print(x);
end

// While + break/continue
while true:
    if score > 10: break; end
end

// Compound assign
score += 1;
speed *= 1.1;

// Functions
fn greet(name: str) -> str:
    return f"Hello {name}!";
end
print(greet("Khalid"));

// if / elif / else
if score > 100:
    print("legendary");
elif score > 50:
    print("solid");
else:
    print("keep going");
end

// Classes
class Ball:
    x: float;
    y: float;
    vx: float;
    vy: float;

    fn init(sx: float, sy: float):
        self.x  = sx;
        self.y  = sy;
        self.vx = 5;
        self.vy = 3;
    end

    fn move():
        self.x += self.vx;
        self.y += self.vy;
    end
end

Ball b = new Ball(400, 300);
b.move();
print(b.x);

// Import
import "utils.kix";

// Graphics
window(800, 600, "My Game");
fps(60);

while true:
    clear("black");
    rect(100, 100, 50, 50, "cyan");
    circle(400, 300, 20, "white");
    text(f"Score: {score}", 10, 10, "white", 24);
    flip();
end
```

---

## Built-in Functions

### Graphics
| Function | Description |
|---|---|
| `window(w, h, title)` | Open game window |
| `clear(color)` | Fill screen with color |
| `rect(x, y, w, h, color)` | Draw rectangle |
| `circle(x, y, r, color)` | Draw circle |
| `line(x1,y1,x2,y2,color)` | Draw line |
| `triangle(x1,y1,x2,y2,x3,y3,color)` | Draw triangle |
| `text(msg, x, y, color, size)` | Render text |
| `flip()` | Render frame (call every loop) |
| `fps(n)` | Set target FPS |

### Input
| Function | Description |
|---|---|
| `key("W")` | Returns 1 if key held |
| `mouse_x()` / `mouse_y()` | Cursor position |
| `mouse_btn(0)` | Mouse button state |

### Math
`sqrt` `pow` `sin` `cos` `tan` `abs` `floor` `ceil` `round` `min` `max` `clamp` `rand` `randint` `PI`

### Arrays
`.push(x)` `.pop()` `.len()` `.get(i)` `.set(i,v)` `.contains(x)` `.reverse()` `.join(sep)`

### Strings
`.upper()` `.lower()` `.split(sep)` `.replace(a,b)` `.trim()` `.contains(sub)` `.len()`

### Types
`int(x)` `float(x)` `str(x)` `bool(x)` `typeof(x)` `range(n)` `range(start,stop,step)`

---

## Project Structure

```
kix/
├── kix.py            ← interpreter (single file)
├── pong.kix          ← Pong game written in KIX
├── examples/
│   ├── hello.kix
│   ├── arrays.kix
│   └── classes.kix
└── README.md
```

---

## Examples

**`examples/hello.kix`**
```kix
str name = "Khalid";
print(f"Hello {name}, welcome to KIX MK IV!");
```

**`examples/arrays.kix`**
```kix
arr scores = [95, 82, 76, 100, 88];
int total = 0;
for s in scores:
    total += s;
end
float avg = total / scores.len();
print(f"Average: {avg}");
```

**`examples/classes.kix`**
```kix
class Vector:
    x: float;
    y: float;

    fn init(px: float, py: float):
        self.x = px;
        self.y = py;
    end

    fn length() -> float:
        return sqrt(self.x * self.x + self.y * self.y);
    end

    fn print_info():
        print(f"Vector({self.x}, {self.y}) |len|={self.length()}");
    end
end

Vector v = new Vector(3, 4);
v.print_info();   // Vector(3, 4) |len|=5.0
```

---

## VS Code Extension

The `kix-language` VS Code extension provides full editor support:

- Syntax highlighting for all KIX MK IV tokens
- File icon next to `.kix` files in the explorer and tabs
- Auto-close brackets `()` `[]` and quotes `""`
- Comment toggling with `Ctrl+/`
- Auto-indent on `:` blocks, dedent on `end`
- F-string interpolation highlighting (`f"Hello {name}"`)

**Install from VSIX:**
```bash
code --install-extension kix-language-1.0.0.vsix
```

**Build the VSIX yourself:**
```bash
npm install -g @vscode/vsce
vsce package
```

---

## Roadmap — MK V

- [ ] Compile to bytecode (`.kixc`)
- [ ] Standard library (`io.kix`, `math.kix`, `net.kix`)
- [x] VSCode syntax highlighting extension
- [ ] First-class functions / closures
- [ ] Error stack traces
- [ ] PyInstaller binary release

---

## License

MIT — build whatever you want with it.

---

*Built as Side Quest #2 of the PHANTOM ZERO protocol.*  
*"If Tony Stark built a language, it would be KIX."*
