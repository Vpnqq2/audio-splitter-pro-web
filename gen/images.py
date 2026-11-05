"""Makes the PNG icons and the social image (needs playwright + chromium). Run: python3 gen/images.py"""
import asyncio, os, base64
from playwright.async_api import async_playwright
W = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "web")
svg = open(os.path.join(W, "icon.svg")).read()
MIC = "data:image/webp;base64," + base64.b64encode(open(os.path.join(W, "img", "hero-mic.webp"), "rb").read()).decode()
OG = f'''<html><body style="margin:0;width:1200px;height:630px;background:radial-gradient(900px 500px at 50% -80px,#12392a,#090D0B 70%);font-family:system-ui,Segoe UI,Roboto,sans-serif;color:#F4F8F5;display:flex;flex-direction:column;justify-content:center;padding:0 90px;box-sizing:border-box;position:relative;overflow:hidden"><img src="{MIC}" style="position:absolute;right:-90px;bottom:0;height:400px;opacity:.95">
<div style="display:flex;align-items:center;gap:22px"><div style="width:96px;height:96px">{svg}</div><div style="font-size:54px;font-weight:700">Audio<span style="color:#00C78A;font-weight:800">Split</span>AI</div></div>
<div style="font-size:70px;font-weight:800;line-height:1.08;margin-top:34px;letter-spacing:-2px;max-width:680px;position:relative">Split Music Into Vocals, Drums, Bass &amp; More</div>
<div style="font-size:30px;color:#A0AEA6;margin-top:22px;max-width:560px">Free online AI stem splitter, right in your browser.</div>
<div style="display:flex;gap:14px;margin-top:38px">{"".join(f'<div style="padding:12px 26px;border-radius:999px;border:2px solid {c};color:{c};font-size:28px;font-weight:700">{n}</div>' for n,c in [("Vocals","#00C78A"),("Drums","#2BB5FF"),("Bass","#FF9F1C"),("Other","#C04CFF")])}</div></body></html>'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1200, "height": 630})
        await pg.set_content(OG); await pg.screenshot(path=os.path.join(W, "og-image.png"))
        for size, name in [(192, "icon-192.png"), (512, "icon-512.png"), (180, "apple-touch-icon.png")]:
            pg = await b.new_page(viewport={"width": size, "height": size})
            await pg.set_content(f'<html><body style="margin:0;background:transparent">{svg.replace("<svg ", f"<svg width=%d height=%d " % (size, size), 1)}</body></html>')
            await pg.screenshot(path=os.path.join(W, name), omit_background=True)
        await b.close()
asyncio.run(main())
