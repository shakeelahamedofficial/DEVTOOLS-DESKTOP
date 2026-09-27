# DevTools Desktop v1.0.0 — Release Checklist

## Build

- [ ] Production build completed successfully
- [ ] All 97 tests passed
- [ ] PyInstaller packaging succeeded
- [ ] No build warnings or errors

## EXE Verification

- [ ] `DevTools.exe` launches from the `dist/DevTools/` directory
- [ ] Application window renders correctly
- [ ] Application icon is displayed in the title bar
- [ ] Application icon is displayed in the Windows taskbar
- [ ] Application exits cleanly without errors

## Tool Smoke Tests

- [ ] JSON Formatter — format, minify, validate, empty input, invalid input
- [ ] JWT Decoder — valid token, invalid token, empty input
- [ ] Base64 — encode, decode, empty input, invalid decode input
- [ ] URL Encoder — encode, decode, empty input
- [ ] UUID Generator — generate single, generate bulk, export
- [ ] Hash Generator — text hash, file hash, empty input
- [ ] Timestamp Converter — Unix to date, date to Unix, invalid input
- [ ] Regex Tester — valid pattern, invalid pattern, matches, groups
- [ ] SQL Formatter — format, minify, empty input
- [ ] HTTP Client — successful request, invalid URL, timeout handling

## Features

- [ ] Command Palette opens with Ctrl+K
- [ ] Sidebar search filters tools
- [ ] Tool switching works for all 10 tools
- [ ] Dark theme renders correctly
- [ ] Light theme renders correctly
- [ ] Theme toggle persists across restarts
- [ ] Settings persist across restarts
- [ ] Clipboard copy operations work
- [ ] File import/export operations work

## Clean Environment

- [ ] EXE runs without Python installed on the machine
- [ ] No missing DLL errors
- [ ] No missing module errors
- [ ] No hardcoded development paths in logs or UI

## Source Code Exclusion

- [ ] No `.py` files in the release ZIP
- [ ] No `.pyc` or `.pyo` files outside `_internal/`
- [ ] No `.spec` files in the release ZIP
- [ ] No `tests/` directory in the release ZIP
- [ ] No `build.py` or development scripts in the release ZIP
- [ ] No `.git/` directory in the release ZIP
- [ ] No `__pycache__/` directories in the release ZIP (outside `_internal/`)
- [ ] No IDE configuration files in the release ZIP

## Documentation

- [ ] README.md is customer-facing (no development instructions)
- [ ] USER_GUIDE.md covers all 10 tools
- [ ] LICENSE.txt has no placeholder text
- [ ] PRIVACY.md is accurate
- [ ] CHANGELOG.md is up to date

## Branding

- [ ] Application title shows "DevTools Desktop"
- [ ] EXE metadata shows correct product name
- [ ] Icon is embedded in the EXE
- [ ] All documentation uses "DevTools Desktop" consistently
- [ ] Copyright shows correct year and holder
- [ ] No AI/ChatGPT/OpenAI branding present
- [ ] No placeholder names present

## Security & Privacy

- [ ] No telemetry code present
- [ ] No analytics code present
- [ ] No unexpected network requests
- [ ] No credentials or API keys in the package
- [ ] No debug logging with sensitive information
- [ ] HTTP networking only through the HTTP Client tool

## Marketing & Launch Materials

- [ ] STORE_LISTING.md prepared
- [ ] MARKETING.md prepared
- [ ] SCREENSHOTS.md prepared
- [ ] Source-code exclusion clearly stated in store listing

## Final Package

- [ ] ZIP created at `release/DevTools-Desktop-v1.0.0-Windows.zip`
- [ ] ZIP contains only customer-required files
- [ ] ZIP extracts cleanly
- [ ] EXE launches from extracted ZIP directory
- [ ] ZIP is ready for manual upload to Buy Me a Coffee
