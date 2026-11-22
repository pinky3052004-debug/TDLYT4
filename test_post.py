"""စစ်ဆေးမှုများ:  python3 -m unittest -v test_post"""
import os, re, sys, glob, shutil, subprocess, unittest
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import live, make_post

POSTS = os.path.join(BASE, "posts")

def run_post(slot, date=None, *flags):
    env = dict(os.environ)
    if date:
        env["POST_DATE"] = date
    return subprocess.run([sys.executable, os.path.join(BASE, "make_post.py"), slot, "--html-only", *flags],
                          capture_output=True, text=True, env=env)

class TestGenerate(unittest.TestCase):
    def test_values_follow_rules(self):
        for _ in range(500):
            d1, d2, d3, p1, p2, p3 = make_post.generate()
            self.assertEqual(len({d1, d2, d3}), 3)                  # ဂဏန်း ၃ လုံး မတူ
            self.assertTrue(all(0 <= d <= 9 for d in (d1, d2, d3)))
            self.assertEqual(p1, f"{d1}{d2}")
            self.assertEqual(p2, f"{d1}{d3}")
            self.assertEqual(p3, p2[::-1])                          # ပြောင်းပြန်လှန်

class TestPostOutput(unittest.TestCase):
    def setUp(self):  shutil.rmtree(POSTS, ignore_errors=True)
    def tearDown(self): shutil.rmtree(POSTS, ignore_errors=True)

    def test_open_day_makes_html_with_disclaimer(self):
        r = run_post("12:01", "2026-10-14")                         # ဗုဒ္ဓဟူး၊ ဖွင့်ရက်
        self.assertEqual(r.returncode, 0, r.stderr)
        html = open(glob.glob(f"{POSTS}/2026-10-14_1201.html")[0], encoding="utf-8").read()
        self.assertNotIn("{{", html)                                # placeholder အကုန်ဖြည့်ပြီး
        self.assertIn("14.10.2026 (12:01)", html)
        self.assertIn("Auto generate", html)                        # disclaimer ပါရမယ်
        self.assertIn("ခန့်မှန်းချက် မဟုတ်ပါ", html)
        for banned in ("ဒဲ့ထိုး", "အထိကီး", "ငွေဝင်ပါစေ"):          # တိုက်တွန်းစာ မပါရ
            self.assertNotIn(banned, html)

    def test_evening_label(self):
        run_post("16:30", "2026-10-14")
        html = open(glob.glob(f"{POSTS}/2026-10-14_1630.html")[0], encoding="utf-8").read()
        self.assertIn("(4:30)", html)

    def test_holiday_is_skipped(self):
        r = run_post("12:01", "2026-10-13")                         # ထိုင်းပိတ်ရက်
        self.assertIn("ပိတ်ရက်", r.stdout)
        self.assertEqual(glob.glob(f"{POSTS}/*"), [])

    def test_weekend_is_skipped(self):
        r = run_post("12:01", "2026-10-24")                         # စနေ
        self.assertIn("ပိတ်ရက်", r.stdout)
        self.assertEqual(glob.glob(f"{POSTS}/*"), [])

    def test_force_overrides_holiday(self):
        run_post("12:01", "2026-10-13", "--force")
        self.assertTrue(glob.glob(f"{POSTS}/2026-10-13_1201.html"))

class TestPostTitle(unittest.TestCase):
    def test_dynamic_title(self):
        d = datetime(2026, 10, 26)
        self.assertEqual(make_post.build_title(d, "12:01"), "26.10.2026(12:01) Auto generate တန်ဖိုးများ")
        self.assertEqual(make_post.build_title(d, "4:30"), "26.10.2026(4:30) Auto generate တန်ဖိုးများ")

class TestWeek(unittest.TestCase):
    def tearDown(self): shutil.rmtree(os.path.join(BASE, "week"), ignore_errors=True)
    def test_week_skips_holidays_and_weekends(self):
        r = subprocess.run([sys.executable, os.path.join(BASE, "make_week.py"), "14", "--html-only"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        files = glob.glob(os.path.join(BASE, "week", "*.html"))
        self.assertTrue(files)
        for f in files:                                   # စနေ/တနင်္ဂနွေ/ပိတ်ရက် မပါရ
            d = datetime.strptime(os.path.basename(f)[:10], "%Y-%m-%d")
            self.assertLess(d.weekday(), 5)
            self.assertNotIn(d.date(), live.load_holidays())
        self.assertEqual(len(files) % 2, 0)               # တစ်ရက်ကို ၂ ခု
        self.assertIn("Auto generate", open(os.path.join(BASE, "week", "captions.txt"), encoding="utf-8").read())

class TestShorts(unittest.TestCase):
    def tearDown(self): shutil.rmtree(POSTS, ignore_errors=True)
    def test_shorts_title_and_template(self):
        d = datetime(2026, 10, 26)
        self.assertEqual(make_post.build_title(d, "12:01", shorts=True),
                         "26.10.2026(12:01) Auto generate တန်ဖိုးများ #Shorts")
        r = run_post("12:01", "2026-10-14", "--shorts")
        self.assertEqual(r.returncode, 0, r.stderr)
        html = open(glob.glob(f"{POSTS}/2026-10-14_1201.html")[0], encoding="utf-8").read()
        self.assertNotIn("{{", html)
        self.assertIn("1920px", html)                       # ဒေါင်လိုက်
        self.assertIn("Auto generate", html)

class TestHolidays(unittest.TestCase):
    def test_file_parses(self):
        h = live.load_holidays()
        self.assertGreater(len(h), 0)
        self.assertIn(datetime(2026, 10, 13).date(), h)

    def test_weekday_labels_match_dates(self):
        names = {"တနင်္လာ": 0, "အင်္ဂါ": 1, "ဗုဒ္ဓဟူး": 2, "ကြာသပတေး": 3, "သောကြာ": 4}
        for ln in open(os.path.join(BASE, "holidays.txt"), encoding="utf-8"):
            m = re.match(r"(\d\d)/(\d\d)/(\d{4}) \((\S+)\)", ln)
            if m:
                d = datetime(int(m[3]), int(m[2]), int(m[1]))
                self.assertEqual(names[m[4]], d.weekday(), ln.strip())

    def test_no_holiday_falls_on_weekend(self):
        for d in live.load_holidays():
            self.assertLess(d.weekday(), 5, f"{d} က စနေ/တနင်္ဂနွေ")

    def test_reason_function(self):
        mk = lambda s: datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=live.MMT)
        self.assertIsNone(live.holiday_reason(mk("2026-10-14")))
        self.assertTrue(live.holiday_reason(mk("2026-10-13")))
        self.assertTrue(live.holiday_reason(mk("2026-10-17")))

class TestLiveTitle(unittest.TestCase):
    def test_title_format(self):
        d = datetime(2026, 10, 6)
        self.assertEqual(live.make_title(d, live.SESSIONS[1], ""),
                         "(6.10.2026) ညနေ (04:30 PM) 2D3D Live တိုက်ရိုက်")
        self.assertEqual(live.make_title(d, live.SESSIONS[0], ""),
                         "(6.10.2026) မနက် (12:01 PM) 2D3D Live တိုက်ရိုက်")

if __name__ == "__main__":
    unittest.main(verbosity=2)
