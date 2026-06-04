#!/bin/bash
# Cut a new release: stamp .roadmap-version, commit, tag, and push.
#
# Usage: bash .kernel/release.sh [vX.Y.Z]
#        bash .kernel/release.sh          # interactive bump prompt

set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VERSION_FILE="$REPO_DIR/.roadmap-version"

# ── Current version ───────────────────────────────────────────────────────────

CURRENT_TAG=$(git -C "$REPO_DIR" describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")

# ── Determine next version ────────────────────────────────────────────────────

if [ -n "$1" ]; then
    NEXT_TAG="$1"
else
    VERSION="${CURRENT_TAG#v}"
    MAJOR=$(echo "$VERSION" | cut -d. -f1)
    MINOR=$(echo "$VERSION" | cut -d. -f2)
    PATCH=$(echo "$VERSION" | cut -d. -f3)

    echo "Current version: $CURRENT_TAG"
    echo ""
    echo "Bump:"
    echo "  1) patch → v$MAJOR.$MINOR.$((PATCH + 1))"
    echo "  2) minor → v$MAJOR.$((MINOR + 1)).0"
    echo "  3) major → v$((MAJOR + 1)).0.0"
    echo ""
    printf "Choice [1/2/3]: "
    read -r CHOICE

    case "$CHOICE" in
        1) NEXT_TAG="v$MAJOR.$MINOR.$((PATCH + 1))" ;;
        2) NEXT_TAG="v$MAJOR.$((MINOR + 1)).0" ;;
        3) NEXT_TAG="v$((MAJOR + 1)).0.0" ;;
        *) echo "Invalid choice. Aborting."; exit 1 ;;
    esac
fi

# ── Validate format ───────────────────────────────────────────────────────────

if ! echo "$NEXT_TAG" | grep -qE '^v[0-9]+\.[0-9]+\.[0-9]+$'; then
    echo "Error: '$NEXT_TAG' is not a valid semver tag (expected vX.Y.Z)."
    exit 1
fi

# ── Validate working tree is clean ────────────────────────────────────────────

if ! git -C "$REPO_DIR" diff --quiet || ! git -C "$REPO_DIR" diff --cached --quiet; then
    echo "Error: uncommitted changes detected — commit or stash before releasing."
    exit 1
fi

# ── Validate tag doesn't already exist ───────────────────────────────────────

if git -C "$REPO_DIR" tag | grep -qx "$NEXT_TAG"; then
    echo "Error: tag '$NEXT_TAG' already exists."
    exit 1
fi

# ── Confirm ───────────────────────────────────────────────────────────────────

echo ""
echo "Releasing $CURRENT_TAG → $NEXT_TAG"
printf "Proceed? [y/N]: "
read -r CONFIRM
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "Aborted."
    exit 0
fi

# ── Stamp .roadmap-version ────────────────────────────────────────────────────

echo "$NEXT_TAG" > "$VERSION_FILE"
echo "✓ .roadmap-version → $NEXT_TAG"

# ── Commit ────────────────────────────────────────────────────────────────────

git -C "$REPO_DIR" add .roadmap-version
git -C "$REPO_DIR" commit -m "chore: release $NEXT_TAG"
echo "✓ Committed"

# ── Tag ───────────────────────────────────────────────────────────────────────

git -C "$REPO_DIR" tag "$NEXT_TAG"
echo "✓ Tagged $NEXT_TAG"

# ── Push ─────────────────────────────────────────────────────────────────────

git -C "$REPO_DIR" push origin main
git -C "$REPO_DIR" push origin "$NEXT_TAG"
echo "✓ Pushed"

echo ""
echo "Released $NEXT_TAG"
