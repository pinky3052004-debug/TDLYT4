#!/usr/bin/env python3
"""12:01 / 16:30 post ပုံထုတ် (Auto generate တန်ဖိုး - ကျပန်းဂဏန်း ၃ လုံး + တွဲဂဏန်း)
usage: python3 make_post.py 12:01     |   python3 make_post.py 16:30 [--html-only]"""
import os, sys, random, subprocess
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import live                                   # holiday_reason(), MMT ကို ပြန်သုံး

POST_TITLE = "{date}({slot}) Auto generate တန်ဖိုးများ"      # YouTube title (ရက်စွဲ/အချိန် အလိုအလျောက်ပြောင်း)
POST_DESCRIPTION = ("ဤဂဏန်းများသည် Auto generate လုပ်ထားသော တန်ဖိုးများသာ ဖြစ်ပါသည်။\n"
                    "ခန့်မှန်းချက် မဟုတ်ပါ၊ ထိုးရန် အကြံပြုခြင်း မဟုတ်ပါ။ ပညာပေး၊ ဖျော်ဖြေရေးအတွက်သာ။")

def build_title(day, shown, shorts=False):
    t = POST_TITLE.format(date=f"{day:%d.%m.%Y}", slot=shown)
    return t + " #Shorts" if shorts else t

def make_video(png, mp4, seconds=8, vertical=False):
    """ပုံကို အသံတိတ် video လေးအဖြစ်ပြောင်း (YouTube က ပုံကို တိုက်ရိုက်မလက်ခံ)"""
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-loop", "1", "-framerate", "5", "-i", png,
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        *(["-vf", "scale=1080:1920"] if vertical else []),
        "-t", str(seconds), "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "64k", "-shortest", "-movflags", "+faststart", mp4], check=True)

def build_html(day, shown, vals, template="post-template.html"):
    d1, d2, d3, p1, p2, p3 = vals
    html = open(os.path.join(BASE, template), encoding="utf-8").read()
    for k, v in {"DATE": f"{day:%d.%m.%Y}", "SLOT": shown, "D1": d1, "D2": d2, "D3": d3,
                 "P1": p1, "P2": p2, "P3": p3}.items():
        html = html.replace("{{" + k + "}}", str(v))
    return html

def screenshot(html_path, png, size="1024,1024"):
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={size}", f"--screenshot={png}", "file://" + html_path], check=True)

def generate():
    d1, d2, d3 = random.sample(range(10), 3)          # မတူတဲ့ ဂဏန်း ၃ လုံး (ကျပန်း)
    p1, p2 = f"{d1}{d2}", f"{d1}{d3}"                 # တွဲ: 53, 58
    p3 = p2[::-1]                                     # 58 ကို ပြောင်းပြန် -> 85
    return d1, d2, d3, p1, p2, p3

def main():
    slot = sys.argv[1] if len(sys.argv) > 1 else "12:01"
    shown = {"12:01": "12:01", "16:30": "4:30"}.get(slot, slot)
    day = datetime.now(live.MMT)
    if os.environ.get("POST_DATE"):                    # စမ်းသပ်ရန် ရက်စွဲအတု (YYYY-MM-DD)
        day = datetime.strptime(os.environ["POST_DATE"], "%Y-%m-%d").replace(hour=11, tzinfo=live.MMT)
    reason = live.holiday_reason(day)
    if reason and "--force" not in sys.argv:
        print(f"{day:%d.%m.%Y} ပိတ်ရက် ({reason}) -> post မထုတ်ပါ"); return
    shorts = "--shorts" in sys.argv                    # Shorts (ဒေါင်လိုက် 1080x1920) ပုံစံ
    vals = generate()
    d1, d2, d3, p1, p2, p3 = vals
    html = build_html(day, shown, vals, "post-template-shorts.html" if shorts else "post-template.html")
    os.makedirs(os.path.join(BASE, "posts"), exist_ok=True)
    stem = os.path.join(BASE, "posts", f"{day:%Y-%m-%d}_{slot.replace(':', '')}")
    open(stem + ".html", "w", encoding="utf-8").write(html)
    with open(stem + ".txt", "w", encoding="utf-8") as f:
        f.write(f"{day:%d.%m.%Y} ({shown}) - {d1}.{d2}.{d3} | {p1}*{p2}.{p3}\n"
                "ဤဂဏန်းများသည် Auto generate လုပ်ထားသော တန်ဖိုးများသာ ဖြစ်ပါသည်။ "
                "ခန့်မှန်းချက် မဟုတ်ပါ၊ ထိုးရန် အကြံပြုခြင်း မဟုတ်ပါ။ ပညာပေး၊ ဖျော်ဖြေရေးအတွက်သာ။\n")
    print("values:", d1, d2, d3, p1, p2, p3)
    if "--html-only" in sys.argv:
        print("html:", stem + ".html"); return
    screenshot(stem + ".html", stem + ".png", "1080,1920" if shorts else "1024,1024")
    print("image:", stem + ".png")
    if "--upload" in sys.argv:                          # YouTube သို့ တင်
        make_video(stem + ".png", stem + ".mp4", seconds=10 if shorts else 8, vertical=shorts)
        test = "--force" in sys.argv                    # force = စမ်းသပ်မှု -> private
        title = ("TEST " if test else "") + build_title(day, shown, shorts)
        desc = POST_DESCRIPTION + ("\n\n#Shorts" if shorts else "")
        vid = live.upload_video(stem + ".mp4", title, desc, "private" if test else "public")
        if not vid:
            sys.exit(1)

if __name__ == "__main__":
    main()
