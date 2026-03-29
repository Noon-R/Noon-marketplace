#!/bin/bash
# game-studio-workflow Plugin Installer
# Copies agents, hooks, rules, docs, and settings to .claude/ directory
# Usage: bash plugins/game-studio-workflow/setup.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CLAUDE_DIR="$PROJECT_ROOT/.claude"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "=== Game Studio Workflow Plugin Installer ==="
echo "Plugin: $SCRIPT_DIR"
echo "Target: $PROJECT_ROOT"
echo ""

# --- Backup existing .claude/ if it exists ---
if [ -d "$CLAUDE_DIR" ]; then
    BACKUP_DIR="$CLAUDE_DIR/backup_$TIMESTAMP"
    echo "Backing up existing .claude/ to $BACKUP_DIR ..."
    mkdir -p "$BACKUP_DIR"
    # Backup only files that will be overwritten
    for dir in agents hooks rules docs; do
        if [ -d "$CLAUDE_DIR/$dir" ]; then
            cp -r "$CLAUDE_DIR/$dir" "$BACKUP_DIR/$dir"
        fi
    done
    if [ -f "$CLAUDE_DIR/settings.json" ]; then
        cp "$CLAUDE_DIR/settings.json" "$BACKUP_DIR/settings.json"
    fi
    if [ -f "$CLAUDE_DIR/statusline.sh" ]; then
        cp "$CLAUDE_DIR/statusline.sh" "$BACKUP_DIR/statusline.sh"
    fi
    echo "  Backup complete: $BACKUP_DIR"
fi

# --- Create .claude/ structure ---
mkdir -p "$CLAUDE_DIR/agents"
mkdir -p "$CLAUDE_DIR/hooks"
mkdir -p "$CLAUDE_DIR/rules"
mkdir -p "$CLAUDE_DIR/docs"

# --- Copy agents ---
echo "Copying 48 agents..."
cp -r "$SCRIPT_DIR/agents/"* "$CLAUDE_DIR/agents/"

# --- Copy hooks ---
echo "Copying 8 hooks..."
cp -r "$SCRIPT_DIR/hooks/"* "$CLAUDE_DIR/hooks/"

# --- Copy rules ---
echo "Copying 11 rules..."
cp -r "$SCRIPT_DIR/rules/"* "$CLAUDE_DIR/rules/"

# --- Copy docs (including templates) ---
echo "Copying docs and templates..."
cp -r "$SCRIPT_DIR/docs/"* "$CLAUDE_DIR/docs/"

# --- Copy statusline ---
if [ -f "$SCRIPT_DIR/statusline.sh" ]; then
    echo "Copying statusline.sh..."
    cp "$SCRIPT_DIR/statusline.sh" "$CLAUDE_DIR/statusline.sh"
fi

# --- Copy settings.json ---
if [ -f "$CLAUDE_DIR/settings.json" ]; then
    echo ""
    echo "WARNING: .claude/settings.json already exists."
    echo "  Plugin settings: $SCRIPT_DIR/settings/settings.json"
    echo "  Existing settings: $CLAUDE_DIR/settings.json"
    echo ""
    read -p "Overwrite with plugin settings? (y/N): " OVERWRITE
    if [ "$OVERWRITE" = "y" ] || [ "$OVERWRITE" = "Y" ]; then
        cp "$SCRIPT_DIR/settings/settings.json" "$CLAUDE_DIR/settings.json"
        echo "  Settings overwritten."
    else
        echo "  Keeping existing settings. You may need to manually merge hook definitions."
        echo "  See: $SCRIPT_DIR/settings/settings.json"
    fi
else
    cp "$SCRIPT_DIR/settings/settings.json" "$CLAUDE_DIR/settings.json"
    echo "Copied settings.json"
fi

# --- Copy CLAUDE.md to project root ---
if [ -f "$SCRIPT_DIR/CLAUDE.md" ]; then
    if [ -f "$PROJECT_ROOT/CLAUDE.md" ]; then
        echo ""
        echo "WARNING: CLAUDE.md already exists at project root."
        read -p "Overwrite? (y/N): " OVERWRITE_CLAUDE
        if [ "$OVERWRITE_CLAUDE" = "y" ] || [ "$OVERWRITE_CLAUDE" = "Y" ]; then
            cp "$SCRIPT_DIR/CLAUDE.md" "$PROJECT_ROOT/CLAUDE.md"
            echo "  CLAUDE.md overwritten."
        else
            echo "  Keeping existing CLAUDE.md."
        fi
    else
        cp "$SCRIPT_DIR/CLAUDE.md" "$PROJECT_ROOT/CLAUDE.md"
        echo "Copied CLAUDE.md to project root"
    fi
fi

# --- Copy engine reference docs ---
if [ -d "$SCRIPT_DIR/engine-reference" ]; then
    mkdir -p "$PROJECT_ROOT/docs/engine-reference"
    echo "Copying engine reference docs..."
    cp -r "$SCRIPT_DIR/engine-reference/"* "$PROJECT_ROOT/docs/engine-reference/"
fi

# --- Create production directory ---
mkdir -p "$PROJECT_ROOT/production/session-state"
if [ ! -f "$PROJECT_ROOT/production/session-state/.gitkeep" ]; then
    touch "$PROJECT_ROOT/production/session-state/.gitkeep"
fi

echo ""
echo "=== Installation Complete ==="
echo ""
echo "Installed:"
echo "  - 48 agents → .claude/agents/"
echo "  - 8 hooks → .claude/hooks/"
echo "  - 11 rules → .claude/rules/"
echo "  - Docs & templates → .claude/docs/"
echo "  - Settings → .claude/settings.json"
echo "  - Engine reference → docs/engine-reference/"
echo ""
echo "Plugin skills (41) are served directly from:"
echo "  plugins/game-studio-workflow/skills/"
echo ""
echo "Next steps:"
echo "  1. Run /start for guided onboarding"
echo "  2. Run /setup-engine to configure your game engine"
echo "  3. Run /brainstorm to start ideation"
echo ""
echo "For more info: cat plugins/game-studio-workflow/README.md"
