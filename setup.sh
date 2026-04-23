#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="$SCRIPT_DIR/brain.config.yaml"
VAULT="$SCRIPT_DIR/2ndbrain-vault"

echo ""
echo "2nd Brain Setup"
echo "==============="
echo ""

# ── Checks ────────────────────────────────────────────────────────────────────

warnings=0

# Claude Code
if ! command -v claude &>/dev/null; then
  echo "  ⚠  Claude Code is not installed."
  echo "     Your vault will still be set up, but you need Claude Code to use it."
  echo "     Install: https://claude.ai/code"
  echo ""
  ((warnings++)) || true
fi

# Config file exists
if [[ ! -f "$CONFIG" ]]; then
  echo "Error: brain.config.yaml not found at $SCRIPT_DIR"
  exit 1
fi

# Detect re-run: if no {{USER_NAME}} exists anywhere in the vault, setup was already run
if ! grep -rqF "{{USER_NAME}}" "$VAULT" --include="*.md" 2>/dev/null; then
  echo "  ⚠  No {{USER_NAME}} tags found in the vault — setup may have already been run."
  echo "     If you're re-configuring, restore the vault from git first:"
  echo "     git checkout -- 2ndbrain-vault/"
  echo ""
  ((warnings++)) || true
fi

# Detect unfilled config defaults
defaults=("Your Name" "Your Role" "Your Company" "@yourhandle")
for default in "${defaults[@]}"; do
  if grep -qF "\"$default\"" "$CONFIG" 2>/dev/null; then
    echo "  ⚠  brain.config.yaml still has default values (e.g. \"$default\")."
    echo "     Fill in your details before running setup, or the vault will have placeholder text."
    echo ""
    ((warnings++)) || true
    break
  fi
done

if [[ $warnings -eq 0 ]]; then
  echo "  ✓  All checks passed."
  echo ""
fi

# ── Replace tags ───────────────────────────────────────────────────────────────

echo "Applying config..."
echo ""

while IFS= read -r line; do
  [[ "$line" =~ ^[[:space:]]*# ]] && continue
  [[ -z "${line// }" ]] && continue
  [[ "$line" != *:* ]] && continue

  key="${line%%:*}"
  value="${line#*: }"
  key="${key// /}"
  value="${value# }"
  value="${value#\"}"
  value="${value%\"}"
  value="${value#\'}"
  value="${value%\'}"

  [[ -z "$key" || -z "$value" ]] && continue

  placeholder="{{${key}}}"
  count=0

  while IFS= read -r -d '' file; do
    if grep -qF "$placeholder" "$file" 2>/dev/null; then
      sed -i "s|${placeholder}|${value}|g" "$file"
      ((count++)) || true
    fi
  done < <(find "$VAULT" -name "*.md" -print0)

  printf "  %-20s → %s  (%d file(s))\n" "{{${key}}}" "$value" "$count"
done < "$CONFIG"

echo ""

# ── Verify ─────────────────────────────────────────────────────────────────────

missed=()
while IFS= read -r line; do
  [[ "$line" =~ ^[[:space:]]*# ]] && continue
  [[ -z "${line// }" ]] && continue
  [[ "$line" != *:* ]] && continue
  key="${line%%:*}"
  key="${key// /}"
  [[ -z "$key" ]] && continue
  if grep -rqF "{{${key}}}" "$VAULT" --include="*.md" 2>/dev/null; then
    missed+=("{{${key}}}")
  fi
done < "$CONFIG"

if [[ ${#missed[@]} -gt 0 ]]; then
  echo "⚠  These tags were not replaced (check brain.config.yaml for empty values):"
  for tag in "${missed[@]}"; do
    echo "   $tag"
  done
else
  echo "✓  All config tags replaced."
fi

# ── Next steps ─────────────────────────────────────────────────────────────────

echo ""
echo "Next steps:"
echo ""
echo "  1. Copy and rename the example directories as needed:"
echo "       cp -r 2ndbrain-vault/user/relationships/_example-person 2ndbrain-vault/user/relationships/<name>"
echo "       cp -r 2ndbrain-vault/projects/_example-project 2ndbrain-vault/projects/<project-name>"
echo ""
echo "  2. Open 2ndbrain-vault/ in a markdown editor."
echo "     Obsidian (https://obsidian.md) works great — but any editor does."
echo ""
if command -v claude &>/dev/null; then
  echo "  3. Spawn Claude Code inside the vault:"
  echo "       cd 2ndbrain-vault && claude"
else
  echo "  3. Install Claude Code (https://claude.ai/code), then:"
  echo "       cd 2ndbrain-vault && claude"
fi
echo ""
echo "  4. Start."
echo ""
