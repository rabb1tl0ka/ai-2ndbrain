#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="$SCRIPT_DIR/brain.config.yaml"
VAULT_TEMPLATE="$SCRIPT_DIR/2ndbrain-vault"

echo ""
echo "2nd Brain Setup"
echo "==============="
echo ""

# ── Checks ────────────────────────────────────────────────────────────────────

warnings=0

# Claude Code
if ! command -v claude &>/dev/null; then
  echo "  ⚠  Claude Code is not installed."
  echo "     It's required to use your vault."
  echo ""
  read -rp "     Install it now? [y/N]: " install_claude
  if [[ "$install_claude" =~ ^[Yy]$ ]]; then
    echo ""
    echo "     Running: curl -fsSL https://claude.ai/install.sh | bash"
    echo ""
    curl -fsSL https://claude.ai/install.sh | bash
    echo ""
    if command -v claude &>/dev/null; then
      echo "  ✓  Claude Code installed."
    else
      echo "  ⚠  Installation may have failed. Check the output above."
      echo "     You can install manually: https://claude.ai/code"
    fi
  else
    echo "     Skipping. Install manually when ready: https://claude.ai/code"
  fi
  echo ""
  ((warnings++)) || true
fi

# Config file exists
if [[ ! -f "$CONFIG" ]]; then
  echo "  Error: brain.config.yaml not found at $SCRIPT_DIR"
  exit 1
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

# ── Install location ───────────────────────────────────────────────────────────

DEFAULT_DEST="$HOME/2ndbrain"
echo "Where do you want to install your vault?"
echo "  Default: $DEFAULT_DEST"
read -rp "  Path [press Enter for default]: " install_path
install_path="${install_path:-$DEFAULT_DEST}"
install_path="${install_path/#\~/$HOME}"   # expand ~
# Resolve to absolute path (works even if path doesn't exist yet)
install_path="$(cd "$(dirname "$install_path")" 2>/dev/null && pwd)/$(basename "$install_path")" || install_path="$(pwd)/$install_path"
echo ""

# Block install inside the repo
if [[ "$install_path" == "$SCRIPT_DIR" || "$install_path" == "$SCRIPT_DIR/"* ]]; then
  echo "  ✗  Cannot install inside the repo directory."
  echo "     Your vault must live outside this repo so your personal notes"
  echo "     don't get mixed up with the template files."
  echo "     Choose a path outside of: $SCRIPT_DIR"
  echo ""
  exit 1
fi

if [[ -d "$install_path" ]]; then
  echo "  ⚠  $install_path already exists."
  read -rp "     Overwrite? [y/N]: " confirm
  [[ "$confirm" =~ ^[Yy]$ ]] || { echo "  Aborted."; exit 0; }
  rm -rf "$install_path"
  echo ""
fi

cp -r "$VAULT_TEMPLATE" "$install_path"
VAULT="$install_path"

echo "  ✓  Vault copied to $VAULT"
echo ""

# ── Apply config ───────────────────────────────────────────────────────────────

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
echo "       cp -r $VAULT/user/relationships/_example-person $VAULT/user/relationships/<name>"
echo "       cp -r $VAULT/projects/_example-project $VAULT/projects/<project-name>"
echo ""
echo "  2. Open $VAULT in a markdown editor."
echo "     Obsidian (https://obsidian.md) works great — but any editor does."
echo ""
if command -v claude &>/dev/null; then
  echo "  3. Spawn Claude Code inside the vault:"
  echo "       cd \"$VAULT\" && claude"
else
  echo "  3. Install Claude Code (https://claude.ai/code), then:"
  echo "       cd \"$VAULT\" && claude"
fi
echo ""
echo "  4. Start."
echo ""
