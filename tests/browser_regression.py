"""Run: python tests/browser_regression.py (requires playwright + a browser).

Set QR_BROWSER to a Chrome/Edge/Chromium path if automatic detection fails.
"""
from pathlib import Path
import asyncio
import os
import shutil
import tempfile
from playwright.async_api import async_playwright

PROJECT = Path(__file__).resolve().parents[1]
OLD = PROJECT/'tests'/'reference_v1.html'
NEW = PROJECT/'index.html'

def find_browser():
    """Find Windows Chrome/Edge, Linux Chromium, or a QR_BROWSER override."""
    override = os.environ.get('QR_BROWSER')
    if override and Path(override).is_file():
        return override
    candidates = [
        shutil.which('chrome'),
        shutil.which('chromium'),
        shutil.which('chromium-browser'),
        shutil.which('google-chrome'),
        shutil.which('msedge'),
        shutil.which('microsoft-edge'),
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
    ]
    for path in candidates:
        if path and Path(path).is_file():
            return path
    return None

async def snapshot(page):
    return await page.evaluate('''() => ({
      data: document.getElementById('qrCanvas').toDataURL('image/png'),
      payload: window.__qrStudioTest.state.payload,
      valid: window.__qrStudioTest.state.valid,
      title: document.getElementById('previewTitle').textContent,
      subtitle: document.getElementById('previewKind').textContent,
      status: document.getElementById('status').textContent,
      pngDisabled: document.getElementById('downloadPNG').disabled
    })''')

async def apply(page, case):
    kind = case['mode']
    await page.locator(f'[data-mode="{kind}"]').click()
    if kind=='link':
        await page.locator('#linkUrl').fill(case['url'])
        await page.locator('#linkTitle').fill(case.get('title',''))
    elif kind=='class':
        await page.locator('#classUrl').fill(case['url'])
        await page.locator('#classTitle').fill(case.get('title',''))
    else:
        await page.locator('#wifiSsid').fill(case['ssid'])
        await page.locator('#wifiSecurity').select_option(case['security'])
        if case['security']!='nopass':
            await page.locator('#wifiPassword').fill(case['password'])
        await page.locator('#wifiHidden').set_checked(case.get('hidden',False))
    if case.get('foreground'):
        await page.locator('#foreground').fill(case['foreground'])
    if case.get('background'):
        await page.locator('#background').fill(case['background'])

async def main():
    cases = [
        {'mode':'link','url':'https://example.com'},
        {'mode':'link','url':'https://example.org/news?a=1&b=2','title':'My Webpage'},
        {'mode':'link','url':'javascript:alert(1)'},
        {'mode':'link','url':'not-a-website'},
        {'mode':'link','url':''},
        {'mode':'class','url':'https://forms.gle/example?x=2','title':'Grade 7'},
        {'mode':'class','url':''},
        {'mode':'wifi','ssid':'Room 101','security':'WPA','password':'Pass:word;5','hidden':True},
        {'mode':'wifi','ssid':'Public Classroom','security':'nopass'},
        {'mode':'wifi','ssid':'','security':'WPA','password':'missing'},
        {'mode':'wifi','ssid':'Room 102','security':'WPA','password':''},
        {'mode':'link','url':'https://example.com','foreground':'#ffffff','background':'#ffffff'}
    ]
    async with async_playwright() as p:
        launch_options = {'headless': True, 'args': ['--no-sandbox']}
        browser_path = find_browser()
        if browser_path:
            launch_options['executable_path'] = browser_path
        browser = await p.chromium.launch(**launch_options)
        old = await browser.new_page(accept_downloads=True)
        new = await browser.new_page(accept_downloads=True)
        errors=[]
        for page in (old,new):
            page.on('pageerror', lambda err: errors.append(str(err)))
        # Playwright's container policy blocks local URL navigation, so inject
        # the same local source into blank pages. No network is used.
        await old.set_content(OLD.read_text(encoding='utf-8'))
        new_html = NEW.read_text(encoding='utf-8')
        new_html = new_html.replace('<link rel="stylesheet" href="styles.css">',
                                    '<style>' + (PROJECT/'styles.css').read_text(encoding='utf-8') + '</style>')
        new_html = new_html.replace('<script defer src="js/qr-core.js"></script>',
                                    '<script>' + (PROJECT/'js'/'qr-core.js').read_text(encoding='utf-8') + '</script>')
        new_html = new_html.replace('<script defer src="js/app.js"></script>',
                                    '<script>' + (PROJECT/'js'/'app.js').read_text(encoding='utf-8') + '</script>')
        await new.set_content(new_html)
        await new.evaluate('if (!window.qrStudio) document.dispatchEvent(new Event("DOMContentLoaded"))')
        await new.wait_for_function('window.qrStudio !== undefined')
        results=[]
        # The one-file standalone must contain the same reviewed app classes.
        standalone = (PROJECT/'QR_Studio_OOP_Standalone.html').read_text(encoding='utf-8')
        app_source = (PROJECT/'js'/'app.js').read_text(encoding='utf-8')
        start = standalone.index('/*\n * QR STUDIO')
        end = standalone.index('</script>', start)
        assert standalone[start:end].rstrip() == app_source.rstrip()
        results.append('PASS standalone matches app.js')
        for i,case in enumerate(cases,1):
            await apply(old,case)
            await apply(new,case)
            before,after = await snapshot(old),await snapshot(new)
            for attr in ('payload','valid','title','subtitle','status','pngDisabled','data'):
                assert before[attr]==after[attr], f'Case {i} {case} differs in {attr}: {str(before[attr])[:100]} vs {str(after[attr])[:100]}'
            results.append(f'PASS {i}: {case["mode"]} {case.get("url",case.get("ssid"))!r}')
        await new.locator('#reset').click()
        assert (await new.locator('#linkUrl').input_value())=='https://example.com'
        assert (await new.locator('[data-mode="link"]').get_attribute('aria-selected'))=='true'
        results.append('PASS reset')
        async with new.expect_download() as event:
            await new.locator('#downloadPNG').click()
        png=await event.value
        assert png.suggested_filename.endswith('.png')
        png_path=PROJECT/'tests'/'downloaded.png'
        await png.save_as(png_path)
        results.append('PASS PNG download')
        async with new.expect_download() as event:
            await new.locator('#downloadSVG').click()
        svg=await event.value
        assert svg.suggested_filename.endswith('.svg')
        svg_path=PROJECT/'tests'/'downloaded.svg'
        await svg.save_as(svg_path)
        assert '<svg' in svg_path.read_text(encoding='utf-8')
        results.append('PASS SVG download')
        # Upload a logo and test download again.
        logo_file=PROJECT/'tests'/'test_logo.png'
        await new.locator('#logoFile').set_input_files(str(logo_file))
        await new.wait_for_function("document.getElementById('fileLabel').textContent.includes('test_logo')")
        async with new.expect_download() as event:
            await new.locator('#downloadPNG').click()
        logo_download=await event.value
        await logo_download.save_as(PROJECT/'tests'/'logo.png')
        results.append('PASS PNG with logo')
        await new.locator('#removeLogo').click()
        assert (await new.locator('#fileLabel').text_content()) == 'No logo selected'
        results.append('PASS remove logo')
        # Replace one logo with another, then remove it again.
        with tempfile.TemporaryDirectory() as temp_dir:
            replacement_logo = Path(temp_dir)/'replacement_logo.png'
            shutil.copyfile(logo_file, replacement_logo)
            await new.locator('#logoFile').set_input_files(str(logo_file))
            await new.wait_for_function("document.getElementById('fileLabel').textContent.includes('test_logo')")
            assert (await new.evaluate('Boolean(window.__qrStudioTest.state.logo)')) is True
            await new.locator('#logoFile').set_input_files(str(replacement_logo))
            await new.wait_for_function("document.getElementById('fileLabel').textContent.includes('replacement_logo')")
            assert (await new.evaluate('Boolean(window.__qrStudioTest.state.logo)')) is True
            await new.locator('#removeLogo').click()
            assert (await new.locator('#fileLabel').text_content()) == 'No logo selected'
            assert (await new.evaluate('window.__qrStudioTest.state.logo')) is None
        results.append('PASS logo replacement and removal')
        # A slow, outdated logo load must not restore a logo after removal.
        await new.evaluate('''() => {
          const original = FileReader.prototype.readAsDataURL;
          window.__restoreReader = () => { FileReader.prototype.readAsDataURL = original; };
          FileReader.prototype.readAsDataURL = function(file) {
            setTimeout(() => original.call(this, file), 200);
          };
        }''')
        await new.locator('#logoFile').set_input_files(str(logo_file))
        await new.evaluate('window.qrStudio.removeLogo()')
        await new.wait_for_timeout(700)
        assert (await new.evaluate('window.__qrStudioTest.state.logo')) is None
        await new.evaluate('window.__restoreReader()')
        results.append('PASS outdated logo load ignored')
        # Reset must hide a password that was shown.
        await new.locator('[data-mode="wifi"]').click()
        await new.locator('#showPassword').click()
        assert (await new.locator('#wifiPassword').get_attribute('type')) == 'text'
        await new.locator('#reset').click()
        assert (await new.locator('#wifiPassword').get_attribute('type')) == 'password'
        assert (await new.locator('#showPassword').text_content()) == 'Show'
        results.append('PASS password visibility after reset')
        # Too much data must clear the preview and disable every export button.
        await new.locator('#linkUrl').fill('https://example.com/valid')
        await new.wait_for_function('window.__qrStudioTest.state.valid === true')
        valid_canvas = await new.evaluate("document.getElementById('qrCanvas').toDataURL('image/png')")
        await new.locator('#linkUrl').fill('https://example.com/' + 'a' * 5000)
        assert (await new.evaluate('window.__qrStudioTest.state.valid')) is False
        assert await new.locator('#downloadPNG').is_disabled()
        assert await new.locator('#downloadSVG').is_disabled()
        assert await new.locator('#copyData').is_disabled()
        empty_canvas = await new.evaluate("document.getElementById('qrCanvas').toDataURL('image/png')")
        assert valid_canvas != empty_canvas
        assert 'too long' in (await new.locator('#status').text_content()).lower()
        results.append('PASS too-long QR clears preview and disables downloads')
        # A valid input must turn the buttons back on for the screenshots.
        await new.locator('#linkUrl').fill('https://example.com')
        await new.wait_for_function('window.__qrStudioTest.state.valid === true')
        assert not await new.locator('#downloadPNG').is_disabled()
        results.append('PASS valid input restores downloads')
        # The one-file standalone must load and generate its sample QR code.
        standalone_page = await browser.new_page()
        standalone_errors = []
        standalone_page.on('pageerror', lambda err: standalone_errors.append(str(err)))
        await standalone_page.set_content(
            (PROJECT/'QR_Studio_OOP_Standalone.html').read_text(encoding='utf-8'))
        await standalone_page.wait_for_function('window.qrStudio !== undefined')
        assert (await standalone_page.evaluate('window.__qrStudioTest.state.valid')) is True
        assert not standalone_errors, standalone_errors
        await standalone_page.close()
        results.append('PASS standalone smoke test')
        await new.screenshot(path=str(PROJECT/'docs'/'desktop_preview.png'),full_page=True)
        await new.set_viewport_size({'width':390,'height':844})
        await new.screenshot(path=str(PROJECT/'docs'/'mobile_preview.png'),full_page=True)
        assert not errors, errors
        results.append('PASS JavaScript: no page errors')
        (PROJECT/'tests'/'test_results.txt').write_text('\n'.join(results)+'\n', encoding='utf-8')
        await browser.close()
        print('\n'.join(results))

if __name__=='__main__':
    asyncio.run(main())
