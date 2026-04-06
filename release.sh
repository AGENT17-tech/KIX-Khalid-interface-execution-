#!/bin/bash
# ═══════════════════════════════════════════
#  KIX MK IV — GitHub Release Script
#  Run this after your recording is done
# ═══════════════════════════════════════════

echo "╔══════════════════════════════════════╗"
echo "║   KIX MK IV — GitHub Release         ║"
echo "╚══════════════════════════════════════╝"

# 1. Init repo
git init

# 2. Create .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
.env
dist/
build/
*.spec
.DS_Store
Thumbs.db
EOF

# 3. Stage everything
git add kix.py pong.kix README.md .gitignore examples/

# 4. First commit
git commit -m "🚀 KIX MK IV — initial release

- Full interpreter: Lexer → Parser → Interpreter
- Types: int float bool str arr
- Arrays with push/pop/len/join/reverse
- for..in loops + break/continue
- F-strings: f\"Hello {name}!\"
- Classes with init() and inheritance
- Compound assign: += -= *= /=
- import system
- 30+ built-in functions
- Built-in pygame graphics engine
- Pong game written entirely in KIX
- REPL + file runner + --check validator"

# 5. Add remote and push
echo ""
echo "Now run:"
echo "  git remote add origin https://github.com/AGENT17-tech/kix.git"
echo "  git branch -M main"
echo "  git push -u origin main"
echo ""
echo "Then create a GitHub Release tagged v4.0.0"
