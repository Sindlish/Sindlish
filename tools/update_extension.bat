@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0.."

echo ==============================================
echo Sindlish VS Code Extension - Build & Publish
echo ==============================================
echo.

rem ---- 1. Read version from the interpreter (single source of truth) ----
for /f "delims=" %%v in ('uv run python -c "import interpreter; print(interpreter.__version__)" 2^>nul') do set "EXT_VERSION=%%v"
if "%EXT_VERSION%"=="" (
    echo [ERROR] Could not read __version__ from interpreter\__init__.py.
    echo         Run this script from the repo root with uv installed.
    pause
    exit /b 1
)

echo [1/4] Mirroring bundled Python interpreter (removes stale files)...
if exist vscode-extension\server\interpreter rmdir /s /q vscode-extension\server\interpreter
xcopy /E /I /Y interpreter vscode-extension\server\interpreter >nul
if errorlevel 1 (
    echo [ERROR] Mirroring interpreter failed.
    pause
    exit /b 1
)

echo [2/4] Regenerating grammar and definitions from the vocab registries...
call uv run python tools\generate_grammar.py
if errorlevel 1 (
    echo [ERROR] Grammar generation failed.
    pause
    exit /b 1
)

echo [3/4] Syncing extension version to %EXT_VERSION%...
cd /d vscode-extension
call npm version %EXT_VERSION% --allow-same-version --no-git-tag-version >nul
if errorlevel 1 (
    echo [ERROR] Version bump failed.
    pause
    exit /b 1
)

echo [4/4] Packaging VSIX...
call vsce package
if errorlevel 1 (
    echo [ERROR] vsce package failed - is @vscode/vsce installed? Try: npm i -g @vscode/vsce
    pause
    exit /b 1
)

echo.
echo ==============================================
echo Extension built: vscode-extension\sindlish-%EXT_VERSION%.vsix
echo ==============================================
echo.

set /p PUBLISH="Publish to the VS Code Marketplace now? (y/n): "
if /i "%PUBLISH%"=="y" (
    call vsce publish --packagePath sindlish-%EXT_VERSION%.vsix
    if errorlevel 1 (
        echo [WARN] vsce publish failed - authenticate with your Azure PAT first:
        echo        npx vsce login AmanatAliPanhwer
    ) else (
        echo Published sindlish-%EXT_VERSION%.vsix to the Marketplace.
    )
)

echo.
pause