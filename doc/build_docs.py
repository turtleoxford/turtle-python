#!/usr/bin/env python3
"""
Build script for Turtle Python documentation.
This script provides a convenient way to build the documentation in various formats.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_command(command, cwd=None):
    """Run a shell command and return success status."""
    print(f"Running: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(e.stderr)
        return False


def build_html(doc_dir):
    """Build HTML documentation."""
    print("Building HTML documentation...")
    if sys.platform == 'win32':
        cmd = ['make.bat', 'html']
    else:
        cmd = ['make', 'html']
    
    if run_command(cmd, cwd=doc_dir):
        print(f"\nHTML documentation built successfully!")
        print(f"Open: {doc_dir / 'build' / 'html' / 'index.html'}")
        return True
    return False


def build_latex(doc_dir):
    """Build LaTeX source files."""
    print("Building LaTeX source...")
    if sys.platform == 'win32':
        cmd = ['make.bat', 'latex']
    else:
        cmd = ['make', 'latex']
    
    if run_command(cmd, cwd=doc_dir):
        print(f"\nLaTeX source built successfully!")
        print(f"LaTeX files in: {doc_dir / 'build' / 'latex'}")
        return True
    return False


def build_pdf(doc_dir):
    """Build PDF documentation."""
    print("Building PDF documentation...")
    if sys.platform == 'win32':
        cmd = ['make.bat', 'latexpdf']
    else:
        cmd = ['make', 'latexpdf']
    
    if run_command(cmd, cwd=doc_dir):
        pdf_path = doc_dir / 'build' / 'latex' / 'TurtleOxford.pdf'
        print(f"\nPDF documentation built successfully!")
        print(f"PDF file: {pdf_path}")
        return True
    else:
        print("\nPDF build failed. Possible reasons:")
        print("  1. LaTeX not installed (install MiKTeX, TeX Live, or MacTeX)")
        print("  2. Missing LaTeX packages")
        print("  3. Try building LaTeX source first: python build_docs.py --latex")
        return False


def clean(doc_dir):
    """Clean build artifacts."""
    print("Cleaning build artifacts...")
    if sys.platform == 'win32':
        cmd = ['make.bat', 'clean']
    else:
        cmd = ['make', 'clean']
    
    if run_command(cmd, cwd=doc_dir):
        print("Build artifacts cleaned successfully!")
        return True
    return False


def main():
    parser = argparse.ArgumentParser(
        description='Build Turtle Python documentation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build_docs.py --html              Build HTML documentation
  python build_docs.py --pdf               Build PDF documentation
  python build_docs.py --latex             Build LaTeX source only
  python build_docs.py --all               Build all formats
  python build_docs.py --clean             Clean build artifacts
        """
    )
    
    parser.add_argument('--html', action='store_true',
                        help='Build HTML documentation')
    parser.add_argument('--pdf', action='store_true',
                        help='Build PDF documentation')
    parser.add_argument('--latex', action='store_true',
                        help='Build LaTeX source only')
    parser.add_argument('--all', action='store_true',
                        help='Build all formats')
    parser.add_argument('--clean', action='store_true',
                        help='Clean build artifacts')
    
    args = parser.parse_args()
    
    # Get doc directory
    doc_dir = Path(__file__).parent
    
    # If no arguments, show help
    if not any(vars(args).values()):
        parser.print_help()
        return 0
    
    success = True
    
    if args.clean:
        success = clean(doc_dir) and success
    
    if args.html or args.all:
        success = build_html(doc_dir) and success
    
    if args.latex:
        success = build_latex(doc_dir) and success
    
    if args.pdf or args.all:
        success = build_pdf(doc_dir) and success
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
