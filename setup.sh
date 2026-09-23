#!/usr/bin/env bash
#
# One-time / repeatable environment setup for this Hugo site.
#
# Ensures:
#   1. The theme git submodule (themes/hugo-texify3) is checked out.
#   2. The standalone dart-sass binary is on PATH (required by the theme's
#      `transpiler: "dartsass"` SCSS pipeline on Hugo >= 0.114).
#   3. The theme's npm dependencies (postcss-cli, autoprefixer, ...) are
#      installed, since Hugo's postCSS resource step needs them on PATH.
#
# Idempotent: safe to re-run at any time.
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
THEME_DIR="$REPO_ROOT/themes/hugo-texify3"

DART_SASS_VERSION="${DART_SASS_VERSION:-1.104.0}"
BIN_DIR="${BIN_DIR:-$HOME/.local/bin}"
DART_SASS_DIR="$HOME/.local/share/dart-sass"

say()  { printf '\033[1;36m[setup]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[warn ]\033[0m %s\n' "$*" >&2; }

# ---------------------------------------------------------------------------
# 1. Theme submodule
# ---------------------------------------------------------------------------
say "Ensuring the theme submodule is initialized..."
git -C "$REPO_ROOT" submodule update --init --recursive

# ---------------------------------------------------------------------------
# 2. dart-sass (Hugo looks for a `dartsass` binary on PATH)
# ---------------------------------------------------------------------------
if command -v dartsass >/dev/null 2>&1; then
  say "dart-sass already available: $(dartsass --version)"
else
  asset=""
  case "$(uname -s)-$(uname -m)" in
    Linux-x86_64)   asset="linux-x64" ;;
    Linux-aarch64)  asset="linux-arm64" ;;
    Darwin-x86_64)  asset="macos-x64" ;;
    Darwin-arm64)   asset="macos-arm64" ;;
    *)
      warn "Unsupported platform $(uname -s)-$(uname -m)."
      warn "Install dart-sass manually, e.g. 'sudo snap install dart-sass' or 'brew install sass/sass/sass'."
      ;;
  esac

  if [ -n "$asset" ]; then
    say "Installing dart-sass $DART_SASS_VERSION (standalone) into $BIN_DIR ..."
    mkdir -p "$BIN_DIR" "$DART_SASS_DIR"
    url="https://github.com/sass/dart-sass/releases/download/$DART_SASS_VERSION/dart-sass-$DART_SASS_VERSION-$asset.tar.gz"
    tmp="$(mktemp -d)"
    trap 'rm -rf "$tmp"' EXIT
    curl -fsSL "$url" -o "$tmp/dart-sass.tar.gz"
    tar -xzf "$tmp/dart-sass.tar.gz" -C "$DART_SASS_DIR" --strip-components=1
    ln -sf "$DART_SASS_DIR/sass" "$BIN_DIR/dartsass"
    [ -e "$BIN_DIR/sass" ] || ln -s "$DART_SASS_DIR/sass" "$BIN_DIR/sass"
    say "dart-sass installed: $("$BIN_DIR/dartsass" --version)"
  fi
fi

# Make sure the user's shell will actually find it.
case ":$PATH:" in
  *":$BIN_DIR:"*) ;;
  *) warn "$BIN_DIR is not on your PATH. Add 'export PATH=\"$BIN_DIR:\$PATH\"' to your shell rc file." ;;
esac

# ---------------------------------------------------------------------------
# 3. Theme npm deps (for Hugo's postCSS step)
# ---------------------------------------------------------------------------
if [ -f "$THEME_DIR/package-lock.json" ] && [ ! -x "$THEME_DIR/node_modules/.bin/postcss" ]; then
  say "Installing theme npm dependencies in $THEME_DIR ..."
  (cd "$THEME_DIR" && npm ci --no-audit --no-fund)
else
  say "Theme npm dependencies already installed."
fi

# ---------------------------------------------------------------------------
# 4. Sanity checks
# ---------------------------------------------------------------------------
if ! command -v hugo >/dev/null 2>&1; then
  warn "hugo not found on PATH."
elif ! hugo version 2>/dev/null | grep -q extended; then
  warn "hugo is installed but not the extended build; the theme needs it for SCSS support."
fi

say "Done. Start the dev server with 'make serve' (Ctrl+C to stop) or build with 'make build'."