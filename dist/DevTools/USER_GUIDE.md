# DevTools Desktop — User Guide

Welcome to DevTools Desktop, your everyday developer toolkit.

## Getting Started

DevTools Desktop is organized with a navigation sidebar on the left and a primary workspace in the center. Click any tool in the sidebar to switch to it.

### Command Palette

Press **Ctrl+K** at any time to open the Command Palette. Type to search for tools by name or actions like "Toggle Theme".

### Sidebar Search

Press **Ctrl+L** to focus the sidebar search field and quickly filter the tool list.

---

## Tools

### 1. JSON Formatter

Format, minify, and validate JSON data.

- Paste or type JSON into the input panel.
- Click **Format** (or press `Ctrl+Enter`) to pretty-print.
- Click **Minify** to compress the JSON to a single line.
- Click **Validate** to check structural correctness.
- Use **Load File** to import a `.json` file from disk.
- Use **Save File** to export the formatted result.
- Invalid JSON will display a clear error message with the location of the problem.

### 2. JWT Decoder

Decode and inspect JSON Web Tokens locally.

- Paste a JWT string into the input field.
- The Header and Payload sections are decoded and displayed immediately.
- Expiration timestamps are converted to human-readable dates.
- **Note:** This tool inspects token contents only. It does not verify cryptographic signatures.

### 3. Base64 Encoder/Decoder

Encode and decode text or files using Base64.

- Type or paste text, then click **Encode** or **Decode**.
- Use the file input to encode a file's contents to Base64.
- Results can be copied to the clipboard.

### 4. URL Encoder/Decoder

Encode and decode URL strings and query parameters.

- Paste a URL or string, then click **Encode** or **Decode**.
- Useful for handling query parameters, special characters, and encoded URIs.

### 5. UUID Generator

Generate universally unique identifiers (v4) in bulk.

- Set the quantity of UUIDs to generate.
- Click **Generate** to create the batch.
- Toggle uppercase formatting if needed.
- Export the list to TXT or CSV using the export buttons.

### 6. Hash Generator

Generate cryptographic hashes for text or files.

- Type or paste text into the input field.
- Select one or more hash algorithms: MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512.
- Results update in real time.
- Use the file input to compute a hash of any file on disk.
- Click any result to copy it to the clipboard.

### 7. Timestamp Converter

Convert between Unix timestamps and human-readable date strings.

- Enter a Unix timestamp (seconds or milliseconds) to see the corresponding date.
- Enter a date string to see the corresponding Unix timestamp.
- Timezone conversion is supported.

### 8. Regex Tester

Test and debug regular expressions with live feedback.

- Enter your regex pattern in the pattern input.
- Enter test text in the text area below.
- Toggle flags: **Ignore Case** (`i`), **Multiline** (`m`), **DotAll** (`s`).
- Matches are highlighted in real time.
- Captured groups are listed in the results tree.

### 9. SQL Formatter

Format and minify SQL queries.

- Paste or type a SQL query into the input area.
- Click **Format** to produce a clean, indented version.
- Click **Minify** to compress the query to a single line.

### 10. HTTP Client

Send API requests directly from your desktop.

- Select the HTTP method: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS.
- Enter the target URL.
- Add custom headers via the Headers tab.
- Add a request body for POST/PUT/PATCH requests.
- Click **Send** to execute the request asynchronously.
- The response status, headers, and body are displayed in the response panel.
- This is the only tool that requires an internet connection.

---

## Settings

Access Settings from the bottom of the sidebar.

- **Theme**: Toggle between Dark and Light themes. Your preference is saved automatically.
- **Clear History**: Remove your recently-used tool history.
- **Startup Tool**: Choose which tool opens when the application starts.

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+K` | Open Command Palette |
| `Ctrl+L` | Focus Sidebar Search |
| `Ctrl+Enter` | Execute / Format |
| `Ctrl+Shift+C` | Copy output to clipboard |
| `Ctrl+Shift+X` | Clear current workspace |

---

## Troubleshooting

**The application won't start:**
Make sure you have fully extracted the ZIP file before running `DevTools.exe`. Running the EXE directly from inside the compressed archive will not work.

**Missing DLL errors:**
Ensure all files from the ZIP are extracted together. The `_internal` folder must remain alongside `DevTools.exe`.

**HTTP Client not working:**
The HTTP Client requires an active internet connection. Other tools work fully offline.

---

## Support

For help, feature requests, or bug reports:
**https://buymeacoffee.com/shakeelahamedofficial**

---

Copyright © 2026 shakeelahamedofficial. All rights reserved.
