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
- Reset hides a Wi-Fi password that was shown and restores the Show label
- Too-long QR data clears the old preview and disables PNG, SVG, and copy
- A valid input turns the download buttons back on
- PNG download, SVG download
- Logo upload and PNG export; logo replacement; logo removal
- An older, slower logo load is ignored after the logo is removed
- The single-file standalone contains the same app classes and passes a smoke test
- No JavaScript page errors during test
- Previous check, not re-run in this session: QR image decoded back to `https://example.com/` both without and with a logo using OpenCV QRCodeDetector
- Mobile-width layout screenshot generated for visual review

## Browser compatibility

`tests/browser_regression.py` now finds Windows Chrome/Edge or a Linux Chromium automatically. Set the `QR_BROWSER` environment variable to a browser path if detection fails. The full suite was run on Windows with both Google Chrome and Microsoft Edge.

## Testing limits

Automated test simulates website loading with local sources in a browser. Opening `index.html` from a real student's Windows laptop and scanning with different phone cameras should still be checked before class submission. A logo may reduce scanning reliability if too large or if the colors are too light.
