#!/bin/bash
set -e

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

# Generate documentation for each repository
for REPO in "${REPOS[@]}"; do
    echo "Processing $REPO..."
    
    # Clone the repository
    if [ -d "$TEMP_DIR/$REPO" ]; then
        echo "  Repository already cloned, pulling latest changes..."
        cd "$TEMP_DIR/$REPO"
        git pull -q || true
        cd ../..
    else
        echo "  Cloning repository..."
        git clone -q --depth 1 "https://github.com/$GITHUB_USER/$REPO.git" "$TEMP_DIR/$REPO" 2>&1 | grep -v "^Cloning" || true
    fi
    
    # Generate Doxyfile from template
    echo "  Generating documentation..."
    sed "s/@REPO_NAME@/$REPO/g" Doxyfile.template > "$TEMP_DIR/Doxyfile.$REPO"
    
    # Run doxygen
    doxygen "$TEMP_DIR/Doxyfile.$REPO" 2>&1 | grep -E "(error|Error)" || true
    rm "$TEMP_DIR/Doxyfile.$REPO"
    
    echo "  ✓ Documentation generated for $REPO"
done

echo ""
echo "✓ All documentation generated successfully!"
