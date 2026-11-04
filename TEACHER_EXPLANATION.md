# QR Studio — Simple OOP Explanation for Our Teacher

## 1. What is our project?

Our project is **QR Studio**, a QR code generator website. It helps users make QR codes for website links, Wi-Fi access, and class registration forms. A user can add a logo, choose colors, and save the result as PNG or SVG. It works offline because the QR code is created in the browser.

## 2. Why did we use OOP?

OOP means **Object-Oriented Programming**. We use classes so that each part of the website has a clear job. This is easier to read, explain, fix, and improve than putting everything in one long group of functions.

## 3. Our three classes

| Class | Job | Important methods |
|---|---|---|
| `QRDataBuilder` | Checks the input and prepares the QR text | `build()`, `buildLink()`, `buildWifi()`, `buildClass()`, `safeUrl()`, `escapeWifi()` |
| `QRImageRenderer` | Draws QR code squares, logo, PNG/SVG content | `draw()`, `toSVG()`, `showPlaceholder()`, `contrast()` |
| `QRStudioApp` | Controls the page and reacts to users | `update()`, `selectMode()`, `loadLogo()`, `clearLogo()`, `setPasswordVisible()`, `reset()`, `downloadPNG()`, `downloadSVG()`, `copyDestination()` |

All three classes are in `js/app.js`. The QR math in `js/qr-core.js` is a separate, unchanged library used for encoding. We did not claim to have invented the QR algorithm.

## 4. Basic OOP concepts in our project

- **Class:** The blueprint, like `class QRDataBuilder`.
- **Object:** A real instance, like `new QRDataBuilder()`.
- **Property:** A value belonging to an object, like `this.mode`, `this.logo`, or `this.qr`.
- **Method:** A function belonging to a class, like `build()` or `draw()`.
- **Encapsulation (basic):** Each class keeps related tasks together. For example, the data builder handles input rules while the renderer handles pictures.
- **Composition:** `QRStudioApp` creates and uses the builder and renderer objects. We do **not** use inheritance because it is unnecessary for this small project.
- **Small methods:** A big job is split into methods with clear names, such as `buildLink()`, `showDetails()`, and `clearPreview()`. This makes each step easier to read and test.

## 5. How it works, step by step

1. The user chooses Link, Wi-Fi, or Class sign-up.
2. `QRStudioApp` reads the values from the input boxes.
3. `QRDataBuilder.build()` chooses `buildLink()`, `buildWifi()`, or `buildClass()`.
4. The chosen method checks the values and makes the correct QR text.
5. The QR library converts that text into a square pattern.
6. `QRStudioApp.update()` draws the preview and updates the screen.
7. The user can download a PNG or SVG image.

### Important methods in plain English

| Method | What it does | Why we use it |
|---|---|---|
| `build()` | Chooses the correct builder method | Keeps one small decision in one place |
| `buildLink()` | Checks a website link and prepares its QR text | Link mode has its own clear job |
| `buildWifi()` | Builds the special `WIFI:` text and escapes symbols | Phones need this exact format |
| `buildClass()` | Checks a sign-up form link | Class mode stays separate from link mode |
| `safeUrl()` | Allows only `http://` and `https://` links | Blocks unsafe link types |
| `escapeWifi()` | Adds `\` before special Wi-Fi characters | Prevents broken Wi-Fi QR data |
| `update()` | Runs the main read → check → generate → draw flow | One place controls the preview |
| `currentColors()` | Reads the two color values | Avoids repeating the same code |
| `refreshColorLabels()` | Shows the uppercase color codes | Keeps the labels correct |
| `showDetails()` | Shows the title and subtitle | Keeps screen text separate from QR logic |
| `setExportButtons()` | Enables or disables download/copy buttons | Users cannot download an old QR code |
| `clearPreview()` | Shows the empty box and an error message | Every error looks the same |
| `showContrastStatus()` | Warns when colors are hard to scan | Keeps the warning in one method |
| `loadLogo()` | Loads and checks the uploaded image | Protects the page from bad files |
| `clearLogo()` | Removes the logo and ignores old image loads | Fixes the logo race condition |
| `setPasswordVisible()` | Shows or hides the Wi-Fi password | One method handles both Show and Reset |
| `draw()` | Draws the QR squares and logo on the canvas | Makes the PNG preview |
| `toSVG()` | Builds the SVG text version | Makes a sharp printable file |
| `contrast()` | Measures light and dark color difference | Helps users make a scannable code |

### Example: Wi-Fi

If the user chooses WPA Wi-Fi and enters a network name and password, the data builder creates a special Wi-Fi text format, such as `WIFI:T:WPA;S:MyClass;P:sample123;H:false;;`. The QR library encodes that text. When a compatible phone scans the QR, it may offer to join the network.

### Example: Class Sign-up

The user pastes an existing Google Form URL. The QR code stores that URL. When someone scans it, they are taken to the form. **Our website does not create the form or store responses.**

### Improvements we made

- We split the long `build()` method into `buildLink()`, `buildWifi()`, and `buildClass()`. Each method now has one clear job.
- We split `update()` into smaller methods such as `showDetails()`, `setExportButtons()`, `clearPreview()`, and `showContrastStatus()`.
- If the QR text is too long, the app now clears the old preview and disables the download buttons.
- Reset now makes the Wi-Fi password hidden again and changes the button text back to “Show”.
- `logoLoadId` is a simple number that stops an older, slower logo upload from replacing a newer choice.
- We kept the same three classes and the same website design.

## 6. Short explanation to say in class

> Our project is a QR code generator that works for links, Wi-Fi, and class sign-ups. We used JavaScript OOP to make the code easier to understand. We made three classes: one checks the data, one draws the QR code, and one controls the website. The data class has separate methods for link, Wi-Fi, and class sign-up. The app class uses small methods to update the screen, handle errors, and enable downloads only when a QR code is ready. Users can also add a logo and download the code. We kept the original design and functions while making the code easier to read.

## 7. Questions your teacher might ask

**Q: Why are there only three main classes?**  
A: We wanted simple code that is easy to maintain. We did not want to add unnecessary classes.

**Q: Why did you split `build()` into several methods?**<br>
A: Each method now handles one QR mode. This follows the idea of one clear job per method, so the code is easier to read, test, and explain.

**Q: What does `this` mean?**  
A: It refers to the current object. For example, `this.mode` stores the mode selected in our app object, and `this.logo` stores the current logo.

**Q: How does the logo race fix work?**<br>
A: Every logo upload gets a number. When an image finishes loading, the app checks whether its number is still the newest one. An old image is ignored, so it cannot replace a newer logo or come back after Reset.

**Q: What happens if the QR data is too long?**<br>
A: The app catches the error, clears the old preview, shows a helpful message, and disables PNG, SVG, and copy buttons until the input is valid again.

**Q: What does Reset do now?**<br>
A: It restores the sample link, clears the logo, hides the Wi-Fi password again, and returns the Show/Hide button to its original label.

**Q: Is a QR code password private?**  
A: The website doesn't send the password to a server, but the password is stored in the QR code itself. Anyone with the QR code may access that information.

**Q: Do you use inheritance or polymorphism?**  
A: No. We mainly demonstrate classes, objects, properties, methods, encapsulation, and composition. Inheritance is not needed in this version.

**Q: Is this your own QR algorithm?**  
A: No. We use an MIT-licensed QR engine and wrote our own code for validation, image drawing, user interaction, and downloads.

## 8. Quick demo to present

1. Open `index.html`.
2. Enter a website link and show its QR code.
3. Change to Wi-Fi and enter sample test details (not your real password). Click Show, then Reset, and show that the password is hidden again.
4. Change to Class sign-up and paste a sample form link.
5. Upload a logo, replace it with another logo, then remove it.
6. Paste a very long link and show that the preview clears and the download buttons turn off.
7. Export a PNG and an SVG from a valid QR code.
8. Point out the three classes and the small methods in `js/app.js`.

**Reminder:** Teacher-friendly does not mean fake simplicity. Always explain what the code really does.
