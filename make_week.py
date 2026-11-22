#!/usr/bin/env python3
"""နောက်ရက် N ရက်စာ (12:01 နဲ့ 4:30) post ပုံတွေကို တစ်ခါတည်းထုတ် -> YouTube Studio မှာ Schedule လုပ်ဖို့
usage: python3 make_week.py [ရက်အရေအတွက်=7] [--html-only]"""
import os, sys, shutil
from datetime import datetime, timedelta

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import live, make_post

SLOTS = [("12:01", "12:01"), ("16:30", "4:30")]
OUT = os.path.join(BASE, "week")

def main():
    n = next((int(a) for a in sys.argv[1:] if a.isdigit()), 7)
    html_only = "--html-only" in sys.argv
    shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
    start = datetime.now(live.MMT).replace(hour=11, minute=0, second=0, microsecond=0) + timedelta(days=1)
    lines, count = [], 0
    for i in range(n):
        day = start + timedelta(days=i)
        reason = live.holiday_reason(day)
        if reason:
            print(f"{day:%d.%m.%Y} ကျော် - {reason}")
            continue
        for slot, shown in SLOTS:
            vals = make_post.generate()
            stem = os.path.join(OUT, f"{day:%Y-%m-%d}_{slot.replace(':', '')}")
            open(stem + ".html", "w", encoding="utf-8").write(make_post.build_html(day, shown, vals))
            if not html_only:
                make_post.screenshot(stem + ".html", stem + ".png")
                os.remove(stem + ".html")
            open(stem + ".txt", "w", encoding="utf-8").write(
                make_post.build_title(day, shown) + "\n" + make_post.POST_DESCRIPTION + "\n")   # phone က ဒီဖိုင်ကို ယူသုံးမယ်
            lines.append(f"[{os.path.basename(stem)}]  Schedule: {day:%d.%m.%Y} ({'ညနေ' if slot == '16:30' else 'မနက်'}ပိုင်း)\n"
                         f"{make_post.build_title(day, shown)}\n{make_post.POST_DESCRIPTION}\n")
            count += 1
    open(os.path.join(OUT, "captions.txt"), "w", encoding="utf-8").write("\n".join(lines))
    print(f"post {count} ခု ထုတ်ပြီး -> {OUT}")

if __name__ == "__main__":
    main()
