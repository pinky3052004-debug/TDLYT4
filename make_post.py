#!/usr/bin/env python3
"""make_week.py အတွက် HTML တည်ဆောက်ခြင်း၊ ပုံရိုက်ထုတ်ခြင်း (PNG) နှင့် Title/Caption ထုတ်ပေးခြင်း"""
import os
import random
import shutil
import subprocess
from pathlib import Path

DAYS_EN = [
    "MONDAY", "TUESDAY", "WEDNESDAY",
    "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"
]

POST_DESCRIPTION = (
    "နေ့စဉ် အထူးဂဏန်းများ အမြဲမြင်ရအောင် Subscribe (SUB) နှိပ်ထားပေးပါနော် 🍀\n"
    "#2D #2DMyanmar #UWaiOfficial"
)


def generate():
    """0 မှ 9 အတွင်း မထပ်သော ဂဏန်း 3 လုံး ထုတ်ပေးသည်"""
    return random.sample(range(10), 3)


def build_title(day, shown):
    """YouTube Community Post Title ထုတ်ပေးသည် (ဥပမာ - 23.11.2026 (MONDAY) 12:01 Top)"""
    day_name = DAYS_EN[day.weekday()]
    return f"{day:%d.%m.%Y} ({day_name}) {shown} Top"


def build_html(day, shown, vals):
    """ပုံစံခွက်အတိုင်း 1080x1080 HTML code ထုတ်ပေးသည်"""
    day_name = DAYS_EN[day.weekday()]
    d0, d1, d2 = vals

    star_svg = (
        '<svg class="star" viewBox="0 0 24 24">'
        '<path fill="#ffc400" stroke="#5c2800" stroke-width="1.2" '
        'd="M12 2l2.9 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l7.1-1.01L12 2z"/>'
        '</svg>'
    )
    stars_html = "\n      ".join([star_svg] * 11)

    return f"""<!DOCTYPE html>
<html lang="my">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=1080, initial-scale=1.0" />
  <title>{day:%d.%m.%Y} ({day_name})</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@700&family=Padauk:wght@700&display=swap" rel="stylesheet" />
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html, body {{
      width: 1080px;
      height: 1080px;
      overflow: hidden;
      background: #140202;
      font-family: "Fredoka", "Padauk", sans-serif;
    }}

    .card {{
      position: relative;
      width: 1080px;
      height: 1080px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      padding: 54px 36px 50px;
      background:
        repeating-linear-gradient(
          90deg,
          rgba(255, 90, 60, 0.045) 0px,
          rgba(255, 90, 60, 0.045) 4px,
          rgba(0, 0, 0, 0.16) 4px,
          rgba(0, 0, 0, 0.16) 10px,
          rgba(255, 120, 80, 0.03) 10px,
          rgba(255, 120, 80, 0.03) 18px
        ),
        radial-gradient(circle at 50% 42%, #c91308 0%, #8e0602 58%, #520200 100%);
    }}

    .card::after {{
      content: "";
      position: absolute;
      inset: 0;
      pointer-events: none;
      box-shadow: inset 0 0 140px rgba(0, 0, 0, 0.65);
    }}

    .card > * {{
      position: relative;
      z-index: 1;
    }}

    .lime-outline {{
      color: #a8ff1a;
      -webkit-text-stroke: 4.5px #141a04;
      paint-order: stroke fill;
      text-shadow:
        0 6px 0 #141a04,
        0 10px 16px rgba(0, 0, 0, 0.65);
    }}

    .date-header {{
      font-size: 68px;
      font-weight: 700;
      letter-spacing: 1px;
      text-align: center;
      line-height: 1.15;
      white-space: nowrap;
    }}

    .top-wrap {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 24px;
      margin-top: -10px;
    }}

    .top-title {{
      font-size: 138px;
      font-weight: 700;
      line-height: 1;
      letter-spacing: 2px;
    }}

    .slot-badge {{
      font-size: 56px;
      font-weight: 700;
      color: #ffc400;
      background: rgba(0, 0, 0, 0.45);
      border: 3px solid #ffc400;
      border-radius: 22px;
      padding: 6px 24px;
      -webkit-text-stroke: 3px #141a04;
      paint-order: stroke fill;
      box-shadow: 0 6px 14px rgba(0, 0, 0, 0.55);
    }}

    .stars {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 14px;
      margin-top: -8px;
    }}

    .star {{
      width: 56px;
      height: 56px;
      filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.65));
    }}

    .circles {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 58px;
      width: 100%;
      margin: 8px 0;
    }}

    .circle-btn {{
      width: 284px;
      height: 284px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      background: radial-gradient(
        circle at 50% 45%,
        #d6180c 0%,
        #9e0903 68%,
        #680300 100%
      );
      border: 5px solid rgba(255, 215, 195, 0.85);
      box-shadow:
        0 0 28px 6px rgba(255, 190, 160, 0.55),
        0 0 56px 12px rgba(255, 90, 50, 0.35),
        inset 0 0 36px rgba(0, 0, 0, 0.55);
    }}

    .circle-num {{
      font-size: 154px;
      font-weight: 700;
      line-height: 1;
      -webkit-text-stroke: 6px #141a04;
      transform: translateY(-4px);
    }}

    .burmese-cta {{
      font-family: "Padauk", "Fredoka", sans-serif;
      font-size: 62px;
      font-weight: 700;
      text-align: center;
      line-height: 1.35;
      white-space: nowrap;
    }}

    .burmese-cta .sub-eng {{
      font-family: "Fredoka", sans-serif;
      letter-spacing: 1px;
    }}

    .footer {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 26px;
      white-space: nowrap;
    }}

    .clover {{
      font-size: 62px;
      line-height: 1;
      filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.7));
    }}

    .brand-name {{
      font-size: 66px;
      font-weight: 700;
      letter-spacing: 1.2px;
    }}
  </style>
</head>
<body>
  <main class="card">
    <div class="date-header lime-outline">{day:%d.%m.%Y}( {day_name} )</div>

    <div class="top-wrap">
      <div class="top-title lime-outline">Top</div>
      <div class="slot-badge">{shown}</div>
    </div>

    <div class="stars">
      {stars_html}
    </div>

    <div class="circles">
      <div class="circle-btn"><span class="circle-num lime-outline">{d0}</span></div>
      <div class="circle-btn"><span class="circle-num lime-outline">{d1}</span></div>
      <div class="circle-btn"><span class="circle-num lime-outline">{d2}</span></div>
    </div>

    <div class="burmese-cta lime-outline">
      အမြဲမြင်ရအောင် <span class="sub-eng">SUB</span> နှိပ်ထားပါ
    </div>

    <footer class="footer">
      <span class="clover">🍀</span>
      <span class="brand-name lime-outline">U WAI OFFICIAL</span>
      <span class="clover">🍀</span>
    </footer>
  </main>
</body>
</html>
"""


def screenshot(html_path, png_path):
    """HTML ဖိုင်ကို 1080x1080 PNG ပုံအဖြစ် ပြောင်းပေးသည် (Playwright သို့မဟုတ် Chrome/Chromium သုံးသည်)"""
    html_uri = Path(os.path.abspath(html_path)).as_uri()

    # 1. Playwright ရှိပါက အရင်သုံးမည် (Google Fonts + Emoji အတွက် အကောင်းဆုံး)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=1)
            page.goto(html_uri, wait_until="networkidle")
            page.wait_for_timeout(300)
            page.screenshot(path=png_path)
            browser.close()
        return
    except ImportError:
        pass

    # 2. Playwright မရှိပါက စက်ထဲရှိ Chrome / Chromium / Edge headless ဖြင့် ရိုက်ထုတ်မည်
    browsers = [
        "google-chrome", "google-chrome-stable", "chromium",
        "chromium-browser", "microsoft-edge", "msedge",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    browser_bin = next((b for b in browsers if shutil.which(b) or os.path.exists(b)), None)
    if not browser_bin:
        raise RuntimeError(
            "Screenshot ရိုက်ရန် Playwright သို့မဟုတ် Chrome/Chromium မတွေ့ပါ။ "
            "`pip install playwright && playwright install chromium` သွင်းပါ သို့မဟုတ် `--html-only` ဖြင့် run ပါ။"
        )

    cmd = [
        browser_bin,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--window-size=1080,1080",
        f"--screenshot={os.path.abspath(png_path)}",
        html_uri,
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
