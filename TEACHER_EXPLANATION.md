# QR Studio — Simple OOP Explanation for Our Teacher

## 1. What is our project?

Our project is **QR Studio**, a QR code generator website. It helps users make QR codes for website links, Wi-Fi access, and class registration forms. A user can add a logo, choose colors, and save the result as PNG or SVG. It works offline because the QR code is created in the browser.

## 2. Why did we use OOP?

OOP means **Object-Oriented Programming**. We use classes so that each part of the website has a clear job. This is easier to read, explain, fix, and improve than putting everything in one long group of functions.

## 3. Our three classes

| Class | Job | Example methods |
|---|---|---|
| `QRDataBuilder` | Checks the input and prepares the QR text | `safeUrl()`, `escapeWifi()`, `build()` |
| `QRImageRenderer` | Draws QR code squares, logo, PNG/SVG content | `draw()`, `toSVG()`, `contrast()` |
| `QRStudioApp` | Controls the page and reacts to users | `update()`, `selectMode()`, `downloadPNG()`, `reset()` |

All three classes are in `js/app.js`. The QR math in `js/qr-core.js` is a separate, unchanged library used for encoding. We did not claim to have invented the QR algorithm.

## 4. Basic OOP concepts in our project

- **Class:** The blueprint, like `class QRDataBuilder`.
- **Object:** A real instance, like `new QRDataBuilder()`.
- **Property:** A value belonging to an object, like `this.mode`, `this.logo`, or `this.qr`.
- **Method:** A function belonging to a class, like `build()` or `draw()`.
- **Encapsulation (basic):** Each class keeps related tasks together. For example, the data builder handles input rules while the renderer handles pictures.
- **Composition:** `QRStudioApp` creates and uses the builder and renderer objects. We do **not** use inheritance because it is unnecessary for this small project.

## 5. How it works, step by step

1. The user chooses Link, Wi-Fi, or Class sign-up.
2. `QRStudioApp` reads the values from the input boxes.
3. `QRDataBuilder.build()` checks the values and makes the correct QR text.
4. The QR library converts that text into a square pattern.
5. `QRImageRenderer.draw()` displays the QR code and optional logo.
6. The user can download a PNG or SVG image.

### Example: Wi-Fi

If the user chooses WPA Wi-Fi and enters a network name and password, the data builder creates a special Wi-Fi text format, such as `WIFI:T:WPA;S:MyClass;P:sample123;H:false;;`. The QR library encodes that text. When a compatible phone scans the QR, it may offer to join the network.

### Example: Class Sign-up

The user pastes an existing Google Form URL. The QR code stores that URL. When someone scans it, they are taken to the form. **Our website does not create the form or store responses.**

## 6. Short explanation to say in class

> Our project is a QR code generator that works for links, Wi-Fi, and class sign-ups. We used JavaScript OOP to make the code easier to understand. We made three classes: one checks the data, one draws the QR code, and one controls the website. When someone enters information, the system checks it, makes a QR code, and shows it on the screen. Users can also add a logo and download the code. We kept the original design and functions while making the code easier to read.

## 7. Questions your teacher might ask

**Q: Why are there only three main classes?**  
A: We wanted simple code that is easy to maintain. We did not want to add unnecessary classes.

**Q: What does `this` mean?**  
A: It refers to the current object. For example, `this.mode` stores the mode selected in our app object.

**Q: Is a QR code password private?**  
A: The website doesn't send the password to a server, but the password is stored in the QR code itself. Anyone with the QR code may access that information.

**Q: Do you use inheritance or polymorphism?**  
A: No. We mainly demonstrate classes, objects, properties, methods, and composition. Inheritance is not needed in this version.

**Q: Is this your own QR algorithm?**  
A: No. We use an MIT-licensed QR engine and wrote our own code for validation, image drawing, user interaction, and downloads.

## 8. Quick demo to present

1. Open `index.html`.
2. Enter a website link and show its QR code.
3. Change to Wi-Fi and enter sample test details (not your real password).
4. Change to Class sign-up and paste a sample form link.
5. Upload a logo, then export PNG and SVG.
6. Point out the three classes in `js/app.js`.

**Reminder:** Teacher-friendly does not mean fake simplicity. Always explain what the code really does.
