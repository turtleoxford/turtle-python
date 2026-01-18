#!/bin/bash
# Quick build script for Turtle Python PDF documentation (Linux/Mac)

set -e  # Exit on error

echo "========================================"
echo "Turtle Python Documentation Builder"
echo "========================================"
echo ""

# Check if Sphinx is installed
if ! python3 -c "import sphinx" 2>/dev/null; then
    echo "ERROR: Sphinx is not installed."
    echo "Please install it with: pip install -r requirements.txt"
    echo ""
    exit 1
fi

echo "Building PDF documentation..."
echo ""

# Build the PDF
make latexpdf

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "BUILD SUCCESSFUL"
    echo "========================================"
    echo ""
    echo "PDF created at: build/latex/TurtleOxford.pdf"
    echo ""
    
    # Try to open the PDF on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if [ -f build/latex/TurtleOxford.pdf ]; then
            echo "Opening PDF..."
            open build/latex/TurtleOxford.pdf
        fi
    fi
else
    echo ""
    echo "========================================"
    echo "BUILD FAILED"
    echo "========================================"
    echo ""
    echo "Possible issues:"
    echo "  1. LaTeX not installed - Install TeX Live"
    echo "  2. Missing LaTeX packages"
    echo "  3. Missing Python packages - Run: pip install -r requirements.txt"
    echo ""
    echo "Try building HTML instead: make html"
    echo ""
    exit 1
fi
