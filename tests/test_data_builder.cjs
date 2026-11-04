// Simple built-in Node.js test for the OOP data class (no extra packages).
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const assert = require('assert');

const source = fs.readFileSync(path.join(__dirname, '../js/app.js'), 'utf8');
const fakeWindow = {};
vm.runInNewContext(source, {
  window: fakeWindow,
  document: { addEventListener() {} },
  URL
});

const builder = new fakeWindow.QRStudioClasses.QRDataBuilder();
const base = {
  linkUrl: 'https://example.com', linkTitle: '',
  classUrl: '', classTitle: '',
  wifiSsid: '', wifiSecurity: 'WPA', wifiPassword: '', wifiHidden: false
};
const link = builder.build('link', base);
assert.equal(link.payload, 'https://example.com/');
assert.equal(link.title, 'Your website');
assert.ok(builder.build('link', {...base, linkUrl: 'bad url'}).error);
assert.ok(builder.build('link', {...base, linkUrl: 'javascript:alert(1)'}).error);
const school = builder.build('class', {...base, classUrl: 'https://forms.gle/example', classTitle: 'Club'});
assert.equal(school.title, 'Club');
assert.equal(school.payload, 'https://forms.gle/example');
const wifi = builder.build('wifi', {...base, wifiSsid: 'Room;2', wifiPassword: 'hello:world'});
assert.equal(wifi.payload, 'WIFI:T:WPA;S:Room\\;2;P:hello\\:world;H:false;;');
const openWifi = builder.build('wifi', {...base, wifiSsid: 'Room A', wifiSecurity: 'nopass'});
assert.equal(openWifi.payload, 'WIFI:T:nopass;S:Room A;P:;H:false;;');
assert.ok(builder.build('wifi', {...base, wifiSsid: 'Room A'}).error);
console.log('PASS: 7 simple QRDataBuilder OOP checks');
