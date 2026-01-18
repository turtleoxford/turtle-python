@echo off
REM Quick build script for Turtle Python PDF documentation

echo ========================================
echo Turtle Python Documentation Builder
echo ========================================
echo.

REM Check if Sphinx is installed
python -c "import sphinx" 2>NUL
if errorlevel 1 (
    echo ERROR: Sphinx is not installed.
    echo Please install it with: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo Building PDF documentation...
echo.

REM Build the PDF
make.bat latexpdf

if errorlevel 1 (
    echo.
    echo ========================================
    echo BUILD FAILED
    echo ========================================
    echo.
    echo Possible issues:
    echo   1. LaTeX not installed - Install MiKTeX from https://miktex.org/
    echo   2. Missing LaTeX packages - MiKTeX will prompt to install them
    echo   3. Missing Python packages - Run: pip install -r requirements.txt
    echo.
    echo Try building HTML instead: make.bat html
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ========================================
    echo BUILD SUCCESSFUL
    echo ========================================
    echo.
    echo PDF created at: build\latex\TurtleOxford.pdf
    echo.
    
    REM Try to open the PDF
    if exist build\latex\TurtleOxford.pdf (
        echo Opening PDF...
        start build\latex\TurtleOxford.pdf
    )
    
    pause
)
