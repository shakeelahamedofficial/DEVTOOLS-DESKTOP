# DevTools Desktop — User Guide

Welcome to DevTools Desktop, your everyday developer toolkit.

## Getting Started
The application is organized into a primary workspace (the center pane) and a navigation sidebar on the left.

### Navigation
You can switch tools by clicking them in the sidebar, or by using the global **Command Palette** which can be triggered at any time by pressing `Ctrl+K`. In the command palette, you can type the name of the tool (e.g. "JSON") or search for actions like "Toggle Theme".

## Tool Workspaces

### JSON Formatter
- Paste your minified or messy JSON into the left panel.
- Click **Format** to pretty-print.
- Click **Validate** to ensure your payload is structurally sound.
- Use `Ctrl+Enter` to quickly format while focused in the input pane.

### JWT Decoder
- Paste a JSON Web Token. The application will decode the Header and Payload safely on your local machine.
- Note: This tool does not verify cryptographic signatures. It only inspects the contents.

### Regex Tester
- Write your pattern in the top input. Toggle flags like Ignore Case (`i`), Multiline (`m`), or DotAll (`s`).
- Matches are highlighted in real-time in the text input, and captured groups are listed in the tree below.

### HTTP Client
- Send asynchronous API requests directly from your desktop.
- Add required headers via the Headers tab.
- Supports all standard methods: GET, POST, PUT, PATCH, DELETE, etc.

## Settings
Access Settings from the bottom of the sidebar to:
- Toggle between Dark and Light themes.
- Clear your local usage history.
- Change startup behavior.
