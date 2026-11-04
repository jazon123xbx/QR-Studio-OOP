# QR Studio — OOP School Project

**Topic:** Object-Oriented Programming (OOP) in JavaScript  
**Project:** Offline QR Code Generator for links, Wi-Fi, and class sign-up forms

This is the same QR Studio website, reorganized into a simple OOP project. Its design and user features remain the same as V1.

## Run the website

1. Unzip the entire project folder.
2. Double-click `index.html` to open it in Chrome or Edge. **Keep its `styles.css` and `js` folder beside it.**
3. Or open `QR_Studio_OOP_Standalone.html` if you want a single file that works by itself.
4. Choose **Link**, **Wi-Fi**, or **Class sign-up**.
5. Add an optional logo, choose colors, and download PNG/SVG.

Everything is generated in your browser. The website does not upload your input, logo, or Wi-Fi password.
A class sign-up QR code opens a form that you already created elsewhere, such as Google Forms.

## Project files

| File | What it is |
|---|---|
| `index.html` | Website structure, buttons, inputs, preview |
| `styles.css` | Original website colors, spacing, and layout |
| `js/app.js` | Our **three main OOP classes**, with student-friendly comments |
| `js/qr-core.js` | Unchanged third-party QR algorithm (MIT license) |
| `QR_Studio_OOP_Standalone.html` | One-file version to open immediately |
| `TEACHER_EXPLANATION.md` | Simple explanation and short defense script |
| `OPENCODE_HANDOFF.md` | How to load the project into OpenCode |
| `AGENTS.md` | Safe editing instructions for OpenCode |
| `tests/` | Source comparison test, sample logo, output and test results |
| `docs/` | Desktop/mobile preview images |
| `QR_ENGINE_LICENSE.txt` | QR library's MIT license |

## What makes this OOP?

The project uses three classes:

1. **QRDataBuilder** validates input and creates the QR content.
2. **QRImageRenderer** draws the squares and optional logo onto the image.
3. **QRStudioApp** handles the screen, buttons, and user actions.

A `class` is a blueprint for objects. `new QRDataBuilder()` creates one object.
Each object has **methods** (actions it can do). The app object also has **properties** like its current mode and logo.

## Requirements

No server, account, build tool, Node.js, or internet is needed to use the website.
For regression tests, Python + Playwright/Chromium are optional. For simple code syntax checking, Node.js is optional.

## Safety notes

- Never scan untrusted QR codes without checking where they lead.
- Scan-test the result before printing, especially if a logo is included.
- High contrast (dark squares on a light background) makes scanning easier.
- Wi-Fi password and link are encoded **inside** the QR image. Anyone who scans it can read or access the encoded information.
- There is no database or login system; class forms are externally hosted links.
