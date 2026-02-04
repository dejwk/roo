#!/bin/bash
set -e

echo "======================================"
echo "Roo Libraries - Documentation Generator"
echo "======================================"
echo ""

# List of repositories to generate documentation for
REPOS=(
    "roo_display"
    "roo_io"
    "roo_windows"
    "roo_testing"
    "roo_transport"
    "roo_logging"
    "roo_windows_wifi"
    "roo_windows_transceivers"
    "roo_prefs"
    "roo_monitoring"
    "roo_time"
    "roo_quantity"
    "roo_transceivers"
    "roo_dashboard"
    "roo_wifi"
    "roo_onewire"
    "roo_backport"
    "roo_collections"
    "roo_scheduler"
    "roo_blink"
    "roo_flags"
    "roo_temperature"
    "roo_comms"
    "roo_locale"
    "roo_icons"
    "roo_threads"
    "roo_powersafefs"
    "roo_control"
    "roo_io_arduino"
    "roo_windows_onewire"
    "roo_time_ds3231"
)

GITHUB_USER="dejwk"
TEMP_DIR="temp_repos"
OUTPUT_DIR="docs"

mkdir -p "$TEMP_DIR"
mkdir -p "$OUTPUT_DIR"

echo "Generating documentation for ${#REPOS[@]} repositories..."
echo ""

# Track success/failure
SUCCESSFUL=()
FAILED=()

# Generate documentation for each repository
COUNT=0
for REPO in "${REPOS[@]}"; do
    COUNT=$((COUNT+1))
    echo "[$COUNT/${#REPOS[@]}] Processing $REPO..."
    
    # Clone the repository
    if [ -d "$TEMP_DIR/$REPO" ]; then
        echo "  ↻ Repository already cloned, pulling latest changes..."
        cd "$TEMP_DIR/$REPO"
        if ! git pull -q; then
            echo "  ⚠ Warning: Failed to pull latest changes, using existing version"
        fi
        cd ../..
    else
        echo "  ⬇ Cloning repository..."
        if git clone -q --depth 1 "https://github.com/$GITHUB_USER/$REPO.git" "$TEMP_DIR/$REPO"; then
            echo "  ✓ Cloned successfully"
        else
            echo "  ✗ Failed to clone $REPO, skipping..."
            FAILED+=("$REPO")
            echo ""
            continue
        fi
    fi
    
    # Generate Doxyfile from template
    echo "  📝 Generating documentation..."
    sed "s/@REPO_NAME@/$REPO/g" Doxyfile.template > "$TEMP_DIR/Doxyfile.$REPO"
    
    # Run doxygen and capture errors
    if ! doxygen "$TEMP_DIR/Doxyfile.$REPO" > /dev/null 2>&1; then
        echo "  ⚠ Warning: Doxygen reported errors for $REPO"
        FAILED+=("$REPO")
    else
        echo "  ✓ Documentation generated for $REPO"
        SUCCESSFUL+=("$REPO")
    fi
    
    rm "$TEMP_DIR/Doxyfile.$REPO"
    echo ""
done

echo "======================================"
echo "Documentation Generation Complete"
echo "======================================"
echo "Successful: ${#SUCCESSFUL[@]}"
echo "Failed: ${#FAILED[@]}"

if [ ${#FAILED[@]} -gt 0 ]; then
    echo ""
    echo "Failed repositories:"
    for REPO in "${FAILED[@]}"; do
        echo "  - $REPO"
    done
fi

echo "======================================"
