/*
 * QR STUDIO — OBJECT-ORIENTED JAVASCRIPT (OOP)
 *
 * We use three simple classes:
 * 1. QRDataBuilder: checks inputs and prepares text for a QR code.
 * 2. QRImageRenderer: draws the QR image on canvas or in SVG.
 * 3. QRStudioApp: controls the buttons, fields, and screen.
 *
 * The QR math is kept unchanged in qr-core.js (MIT licensed).
 * The browser runs this file locally; data is never sent to a server.
 */

'use strict';

// CLASS 1: QRDataBuilder — prepare the content to be encoded.
class QRDataBuilder {
  // Accept only normal website links. Block other URL schemes.
  safeUrl(text) {
    try {
      const url = new URL(text);
      return url.protocol === 'http:' || url.protocol === 'https:'
        ? url.toString()
        : null;
    } catch {
      return null;
    }
  }

  // Special symbols in Wi-Fi names/passwords need an escape character.
  escapeWifi(text) {
    return text.replace(/([\\;,:"])|\n/g, character =>
      character === '\n' ? '\\n' : '\\' + character
    );
  }

  // One method supports all three QR types.
  build(mode, fields) {
    if (mode === 'link') {
      const urlText = fields.linkUrl.trim();
      if (!urlText) return { error: 'Enter a link to make a QR code.' };
      const url = this.safeUrl(urlText);
      if (!url) return { error: 'Use a complete http:// or https:// link.' };
      return {
        payload: url,
        title: fields.linkTitle.trim() || 'Your website',
        subtitle: url
      };
    }

    if (mode === 'class') {
      const urlText = fields.classUrl.trim();
      if (!urlText) return { error: 'Paste a class registration form link.' };
      const url = this.safeUrl(urlText);
      if (!url) return { error: 'Use a complete http:// or https:// form link.' };
      return {
        payload: url,
        title: fields.classTitle.trim() || 'Class sign-up',
        subtitle: 'Scan to open the registration form'
      };
    }

    if (mode === 'wifi') {
      if (!fields.wifiSsid) return { error: 'Enter a Wi-Fi network name.' };
      if (fields.wifiSecurity !== 'nopass' && !fields.wifiPassword) {
        return { error: 'Enter the Wi-Fi password.' };
      }

      const password = fields.wifiSecurity === 'nopass'
        ? '' : this.escapeWifi(fields.wifiPassword);
      const hidden = fields.wifiHidden ? 'true' : 'false';
      const payload = 'WIFI:T:' + fields.wifiSecurity
        + ';S:' + this.escapeWifi(fields.wifiSsid)
        + ';P:' + password + ';H:' + hidden + ';;';

      return {
        payload,
        title: fields.wifiSsid,
        subtitle: fields.wifiSecurity === 'nopass'
          ? 'Open Wi-Fi network' : 'Scan to join Wi-Fi'
      };
    }

    return { error: 'Select a QR code type.' };
  }
}

// CLASS 2: QRImageRenderer — turn QR data into a visible/downloadable image.
class QRImageRenderer {
  // Show a friendly blank area when a required field is missing.
  showPlaceholder(canvas, size) {
    canvas.width = size;
    canvas.height = size;
    const context = canvas.getContext('2d');
    context.fillStyle = '#f4f5f9';
    context.fillRect(0, 0, size, size);
    context.fillStyle = '#a9aabf';
    context.font = '600 16px system-ui';
    context.textAlign = 'center';
    context.fillText('Your QR will appear here', size / 2, size / 2);
  }

  // Draw the same QR squares as the original website.
  draw(canvas, size, qr, foreground, background, logo) {
    const count = qr.getModuleCount();
    const border = 4; // Quiet zone: 4 blank squares around the QR code.
    const total = count + border * 2;

    canvas.width = size;
    canvas.height = size;
    const context = canvas.getContext('2d');
    context.fillStyle = background;
    context.fillRect(0, 0, size, size);
    context.fillStyle = foreground;

    const location = index => Math.round(index * size / total);
    for (let row = 0; row < count; row++) {
      for (let column = 0; column < count; column++) {
        if (!qr.isDark(row, column)) continue;
        const x = location(column + border);
        const y = location(row + border);
        const width = location(column + border + 1) - x;
        const height = location(row + border + 1) - y;
        context.fillRect(x, y, width, height);
      }
    }

    if (logo) {
      // A small white badge behind the logo helps preserve readability.
      const side = Math.floor(size * 0.16);
      const middle = (size - side) / 2;
      const pad = Math.max(5, Math.round(size * 0.013));
      context.fillStyle = '#ffffff';
      context.beginPath();
      if (context.roundRect) {
        context.roundRect(middle - pad, middle - pad,
          side + pad * 2, side + pad * 2, Math.round(size * 0.02));
      } else {
        context.rect(middle - pad, middle - pad, side + pad * 2, side + pad * 2);
      }
      context.fill();

      const scale = Math.min(side / logo.width, side / logo.height);
      const imageWidth = logo.width * scale;
      const imageHeight = logo.height * scale;
      context.drawImage(logo,
        (size - imageWidth) / 2, (size - imageHeight) / 2,
        imageWidth, imageHeight);
    }
  }

  // Vector version for very large, sharp prints.
  toSVG(qr, foreground, background, logo) {
    const count = qr.getModuleCount();
    const border = 4;
    const total = count + border * 2;
    const safe = text => text.replaceAll('&', '&amp;')
      .replaceAll('"', '&quot;').replaceAll('<', '&lt;');

    let svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 ${total} ${total}"><rect width="${total}" height="${total}" fill="${safe(background)}"/>`;
    let squares = '';
    for (let row = 0; row < count; row++) {
      for (let column = 0; column < count; column++) {
        if (qr.isDark(row, column)) {
          squares += `M${column + border},${row + border}h1v1h-1z`;
        }
      }
    }
    svg += `<path fill="${safe(foreground)}" d="${squares}"/>`;

    if (logo) {
      const pad = count * 0.017;
      const side = count * 0.16;
      const center = (total - side) / 2;
      svg += `<rect x="${center - pad}" y="${center - pad}" width="${side + pad * 2}" height="${side + pad * 2}" rx="${pad}" fill="white"/>`;
      svg += `<image href="${safe(logo.src)}" x="${center}" y="${center}" width="${side}" height="${side}" preserveAspectRatio="xMidYMid meet"/>`;
    }
    return svg + '</svg>';
  }

  // Warn users if a QR code has weak foreground/background contrast.
  contrast(foreground, background) {
    const brightness = color => {
      const values = color.match(/[a-f0-9]{2}/ig).map(hex =>
        parseInt(hex, 16) / 255).map(value =>
        value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4);
      return 0.2126 * values[0] + 0.7152 * values[1] + 0.0722 * values[2];
    };
    const light1 = brightness(foreground);
    const light2 = brightness(background);
    return (Math.max(light1, light2) + 0.05) / (Math.min(light1, light2) + 0.05);
  }
}

// CLASS 3: QRStudioApp — connect user actions to the two classes above.
class QRStudioApp {
  constructor() {
    // OBJECT ATTRIBUTES: values belonging to this particular app object.
    this.mode = 'link';
    this.logo = null;
    this.qr = null;
    this.payload = '';
    this.valid = false;

    // OBJECTS: the app uses a data builder and an image renderer.
    this.builder = new QRDataBuilder();
    this.renderer = new QRImageRenderer();

    this.bindEvents();
    this.update();
  }

  element(id) {
    return document.getElementById(id);
  }

  status(message, error = false) {
    const area = this.element('status');
    area.textContent = message;
    area.classList.toggle('error', error);
  }

  // Read all user inputs so QRDataBuilder does not need to know the HTML.
  readInputs() {
    const value = id => this.element(id).value;
    return {
      linkUrl: value('linkUrl'), linkTitle: value('linkTitle'),
      wifiSsid: value('wifiSsid'), wifiSecurity: value('wifiSecurity'),
      wifiPassword: value('wifiPassword'), wifiHidden: this.element('wifiHidden').checked,
      classUrl: value('classUrl'), classTitle: value('classTitle')
    };
  }

  currentDetails() {
    return this.builder.build(this.mode, this.readInputs());
  }

  // Main flow: read → validate → generate → draw.
  update() {
    const foreground = this.element('foreground').value;
    const background = this.element('background').value;
    this.element('fgLabel').textContent = foreground.toUpperCase();
    this.element('bgLabel').textContent = background.toUpperCase();

    const details = this.currentDetails();
    this.qr = null;
    this.valid = false;
    for (const id of ['downloadPNG', 'downloadSVG', 'copyData']) {
      this.element(id).disabled = Boolean(details.error);
    }
    this.element('previewTitle').textContent = details.title || 'Almost ready';
    this.element('previewKind').textContent = details.subtitle || 'Fill in the required fields';

    const size = Number(this.element('qrSize').value);
    const canvas = this.element('qrCanvas');
    if (details.error) {
      this.renderer.showPlaceholder(canvas, size);
      this.status(details.error, true);
      return;
    }

    this.payload = details.payload;
    try {
      // QRCodeCore comes from the unchanged, locally bundled QR library.
      const qr = new QRCodeCore(-1, QRErrorCorrectLevel.H);
      qr.addData(this.payload);
      qr.make();
      this.qr = qr;
      this.valid = true;
      this.renderer.draw(canvas, size, qr, foreground, background, this.logo);

      const contrast = this.renderer.contrast(foreground, background);
      if (contrast < 4.5) {
        this.status('Low color contrast. Choose darker QR modules and a lighter background.', true);
      } else {
        this.status(`✓ QR code ready · ${qr.getModuleCount()} × ${qr.getModuleCount()} modules`);
      }
    } catch (error) {
      this.valid = false;
      this.status('This text is too long for a QR code. Try a shorter URL or network name.', true);
    }
  }

  selectMode(mode) {
    this.mode = mode;
    for (const tab of document.querySelectorAll('[data-mode]')) {
      const isActive = tab.dataset.mode === mode;
      tab.classList.toggle('active', isActive);
      tab.setAttribute('aria-selected', String(isActive));
    }
    for (const name of ['link', 'wifi', 'class']) {
      this.element(name + 'Fields').classList.toggle('hidden', name !== mode);
    }
    this.element('modeBadge').textContent = {
      link: 'LINK', wifi: 'WI-FI', class: 'CLASS SIGN-UP'
    }[mode];
    this.update();
  }

  async loadLogo(file) {
    if (!file) return;
    if (!['image/png', 'image/jpeg', 'image/webp'].includes(file.type)
        || file.size > 5 * 1024 * 1024) {
      this.status('Choose a PNG, JPG or WebP logo under 5 MB.', true);
      this.element('logoFile').value = '';
      return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      const image = new Image();
      image.onload = () => {
        this.logo = image;
        this.element('fileLabel').textContent = file.name;
        this.element('removeLogo').classList.remove('hidden');
        this.update();
      };
      image.onerror = () => this.status('Could not read that image.', true);
      image.src = reader.result;
    };
    reader.readAsDataURL(file);
  }

  removeLogo() {
    this.logo = null;
    this.element('logoFile').value = '';
    this.element('fileLabel').textContent = 'No logo selected';
    this.element('removeLogo').classList.add('hidden');
    this.update();
  }

  reset() {
    const defaults = {
      linkUrl: 'https://example.com', linkTitle: '', wifiSsid: '',
      wifiSecurity: 'WPA', wifiPassword: '', classTitle: '', classUrl: '',
      foreground: '#1a1a32', background: '#ffffff', qrSize: '512'
    };
    for (const [id, value] of Object.entries(defaults)) {
      this.element(id).value = value;
    }
    this.element('wifiHidden').checked = false;
    this.element('wifiPassword').disabled = false;
    this.logo = null;
    this.element('logoFile').value = '';
    this.element('fileLabel').textContent = 'No logo selected';
    this.element('removeLogo').classList.add('hidden');
    this.selectMode('link');
    this.status('Settings reset to sample link.');
  }

  filename() {
    const title = this.currentDetails().title || 'qr-code';
    const clean = title.toLowerCase().normalize('NFKD')
      .replace(/[^a-z0-9-_ ]/g, '').trim()
      .replace(/ +/g, '-').slice(0, 42);
    return 'qr-' + (clean || 'code');
  }

  download(data, name) {
    const link = document.createElement('a');
    link.href = data;
    link.download = name;
    document.body.append(link);
    link.click();
    link.remove();
  }

  downloadPNG() {
    if (!this.valid) return;
    const canvas = document.createElement('canvas');
    const size = Number(this.element('qrSize').value);
    this.renderer.draw(canvas, size, this.qr,
      this.element('foreground').value, this.element('background').value, this.logo);
    this.download(canvas.toDataURL('image/png'), this.filename() + '.png');
    this.status('✓ Downloaded PNG. Remember to scan-test it.');
  }

  downloadSVG() {
    if (!this.valid) return;
    const svg = this.renderer.toSVG(this.qr,
      this.element('foreground').value, this.element('background').value, this.logo);
    const blob = new Blob([svg], { type: 'image/svg+xml;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    this.download(url, this.filename() + '.svg');
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    this.status('✓ Downloaded SVG. Remember to scan-test it.');
  }

  async copyDestination() {
    if (!this.valid) return;
    try {
      await navigator.clipboard.writeText(this.payload);
      this.status('✓ QR destination copied.');
    } catch {
      const input = document.createElement('textarea');
      input.value = this.payload;
      document.body.append(input);
      input.select();
      try {
        document.execCommand('copy');
        this.status('✓ QR destination copied.');
      } catch {
        this.status('Copy is unavailable in this browser.', true);
      }
      input.remove();
    }
  }

  // Event listeners make the app react when a user clicks or types.
  bindEvents() {
    for (const tab of document.querySelectorAll('[data-mode]')) {
      tab.addEventListener('click', () => this.selectMode(tab.dataset.mode));
    }

    const fields = ['linkUrl', 'linkTitle', 'wifiSsid', 'wifiSecurity',
      'wifiPassword', 'wifiHidden', 'classTitle', 'classUrl',
      'foreground', 'background', 'qrSize'];
    for (const id of fields) {
      const event = id === 'wifiHidden' ? 'change' : 'input';
      this.element(id).addEventListener(event, () => this.update());
    }

    this.element('wifiSecurity').addEventListener('change', () => {
      this.element('wifiPassword').disabled =
        this.element('wifiSecurity').value === 'nopass';
      this.update();
    });

    this.element('showPassword').addEventListener('click', () => {
      const input = this.element('wifiPassword');
      input.type = input.type === 'password' ? 'text' : 'password';
      this.element('showPassword').textContent =
        input.type === 'password' ? 'Show' : 'Hide';
    });

    this.element('logoFile').addEventListener('change', event =>
      this.loadLogo(event.target.files?.[0]));
    this.element('removeLogo').addEventListener('click', () => this.removeLogo());
    this.element('reset').addEventListener('click', () => this.reset());
    this.element('downloadPNG').addEventListener('click', () => this.downloadPNG());
    this.element('downloadSVG').addEventListener('click', () => this.downloadSVG());
    this.element('copyData').addEventListener('click', () => this.copyDestination());
  }
}

// The classes can be inspected by a teacher or by our test script.
window.QRStudioClasses = { QRDataBuilder, QRImageRenderer, QRStudioApp };

document.addEventListener('DOMContentLoaded', () => {
  const app = new QRStudioApp();
  window.qrStudio = app;
  // Useful for automated checks; it does not change the normal interface.
  window.__qrStudioTest = {
    get state() { return { mode: app.mode, logo: app.logo,
      qr: app.qr, payload: app.payload, valid: app.valid }; },
    update: () => app.update(),
    getDetails: () => app.currentDetails()
  };
});
