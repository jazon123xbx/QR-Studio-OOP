# How to move QR Studio OOP into OpenCode

The ZIP is a complete local project. OpenCode runs on **your laptop**, not in this chat. I did not connect to your laptop or push the files into your local OpenCode session.

## Windows / PowerShell instructions

1. Download `QR_Studio_OOP_Project.zip` and extract it.
2. Open the extracted `QR_Studio_OOP_Project` folder in File Explorer.
3. Click the address bar, type `powershell`, and press Enter.
4. Run:

```powershell
opencode
```

5. In OpenCode, you can run `/init` to let it read the project and understand its files. Our `AGENTS.md` already documents important rules.
6. Paste the instruction below. Make sure you are in the project folder first.

## Paste this prompt into OpenCode

```text
Read README.md, TEACHER_EXPLANATION.md, and AGENTS.md first.

This project is QR Studio, a working offline QR code generator written in HTML, CSS, and object-oriented JavaScript. The main OOP code is js/app.js, with three classes: QRDataBuilder, QRImageRenderer, and QRStudioApp.

Your task is to REVIEW and IMPROVE EXPLAINABILITY ONLY. Keep the website's exact visual design and all working features. Do not change js/qr-core.js (MIT library), redesign the UI, add frameworks, add unnecessary classes, or add network calls.

1. Explain the real OOP ideas using Grade 9-level English: class, object, property, method, simple encapsulation, and composition.
2. Point to the actual methods that do each job.
3. Add short useful comments only where they help a beginner. Do not fill every line with comments.
4. Check QR link, Wi-Fi, class form, errors, logos, colors, copy, reset, PNG and SVG downloads.
5. Compare behavior to tests/reference_v1.html; prevent any regression.
6. If there are issues, fix them one at a time, then retest.
7. Produce a simple final summary of the project for a teacher presentation and mention anything not implemented.

Before touching code: give a brief list of planned changes. Do not say testing passed unless you actually ran the tests.
```

## How to send it for a school project

You can submit the project ZIP or the extracted files as your teacher requests. Use TEACHER_EXPLANATION.md to prepare your oral explanation. Do not submit only the screenshot, because a screenshot does not show the code.
