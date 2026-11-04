# QR Studio OOP — Test Report

The OOP website was compared with the original V1 source, using a real Chromium browser to generate canvas images on each page. The browser's administrator policy prevented direct navigation to local file URLs, so the same local HTML/CSS/JS sources were inserted into blank pages for the automated regression test.

## Passed checks

- Link QR: normal URL, URL with query parameters, custom caption
- Link QR: rejects unsafe/invalid/blank input
- Class Sign-up QR: valid link and empty link
- Wi-Fi QR: secured network, open network, special characters, missing input
- Foreground/background color and low-contrast warning
- Canvas image matches original V1 for all twelve data/visual test cases
- Reset settings and active mode
- PNG download, SVG download
- Logo upload and PNG export; logo removal
- No JavaScript page errors during test
- QR image decoded back to `https://example.com/` both without and with a logo using OpenCV QRCodeDetector
- Mobile-width layout screenshot generated for visual review

## Testing limits

Automated test simulates website loading with local sources in a browser. Opening `index.html` from a real student's Windows laptop and scanning with different phone cameras should still be checked before class submission. A logo may reduce scanning reliability if too large or if the colors are too light.
