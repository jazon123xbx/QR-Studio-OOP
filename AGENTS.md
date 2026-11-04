# OpenCode Project Instructions — QR Studio OOP

You are editing an existing, working offline QR code generator used as a student OOP project.

## Important rules

- Keep the website's current design, text labels, colors, and layout unchanged unless the user asks.
- Preserve all three QR modes: Link, Wi-Fi, Class sign-up.
- Preserve validation, Wi-Fi escaping, logo upload/removal, color contrast warning, reset, copy, PNG and SVG exports, and offline use.
- DO NOT rewrite `js/qr-core.js`; it is MIT-licensed third-party QR encoding code, tested and stable.
- Prefer beginner-friendly JavaScript classes over frameworks, build pipelines, databases, APIs, TypeScript, or excessive design patterns.
- Keep classes understandable: QRDataBuilder, QRImageRenderer, QRStudioApp.
- Do not send Wi-Fi passwords or uploaded logos to servers.
- Do not claim a form/database feature that is not implemented.
- Before editing, read README.md and TEACHER_EXPLANATION.md.
- Keep tests passing. Compare output with `tests/reference_v1.html` after changing QR behavior.
- When modifying files, list changes and explain how each change helps the student present the project.

## Common commands

```powershell
# From inside the unzipped project folder:
node --check .\js\app.js
opencode
```

Run `index.html` to test in Chrome or Edge. If a terminal web server is preferred, `python -m http.server 8000` is optional.
