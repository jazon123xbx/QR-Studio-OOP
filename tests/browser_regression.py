"""Run: python tests/browser_regression.py (requires playwright + chromium)."""
from pathlib import Path
import asyncio
from playwright.async_api import async_playwright

PROJECT = Path(__file__).resolve().parents[1]
OLD = PROJECT/'tests'/'reference_v1.html'
NEW = PROJECT/'index.html'

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
        browser = await p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        old = await browser.new_page(accept_downloads=True)
        new = await browser.new_page(accept_downloads=True)
        errors=[]
        for page in (old,new):
            page.on('pageerror', lambda err: errors.append(str(err)))
        # Playwright's container policy blocks local URL navigation, so inject
        # the same local source into blank pages. No network is used.
        await old.set_content(OLD.read_text())
        new_html = NEW.read_text()
        new_html = new_html.replace('<link rel="stylesheet" href="styles.css">',
                                    '<style>' + (PROJECT/'styles.css').read_text() + '</style>')
        new_html = new_html.replace('<script defer src="js/qr-core.js"></script>',
                                    '<script>' + (PROJECT/'js'/'qr-core.js').read_text() + '</script>')
        new_html = new_html.replace('<script defer src="js/app.js"></script>',
                                    '<script>' + (PROJECT/'js'/'app.js').read_text() + '</script>')
        await new.set_content(new_html)
        await new.evaluate('if (!window.qrStudio) document.dispatchEvent(new Event("DOMContentLoaded"))')
        await new.wait_for_function('window.qrStudio !== undefined')
        results=[]
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
        assert '<svg' in svg_path.read_text()
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
        await new.screenshot(path=str(PROJECT/'docs'/'desktop_preview.png'),full_page=True)
        await new.set_viewport_size({'width':390,'height':844})
        await new.screenshot(path=str(PROJECT/'docs'/'mobile_preview.png'),full_page=True)
        assert not errors, errors
        results.append('PASS JavaScript: no page errors')
        (PROJECT/'tests'/'test_results.txt').write_text('\n'.join(results)+'\n')
        await browser.close()
        print('\n'.join(results))

if __name__=='__main__':
    asyncio.run(main())
