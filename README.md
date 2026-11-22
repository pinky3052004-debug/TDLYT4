# 2D3D Live - Channel 1 (အဝါ/အနီ (မူလ))

ဒီ repo က channel 1 တစ်ခုတည်းအတွက်ပါ။ 11:59-12:02 clip video နဲ့ post ပုံ video ကို တင်။

## Setup
1. GitHub မှာ repo အသစ်ဆောက်ပြီး ဒီ folder ထဲက ဖိုင်အားလုံးကို အတိုင်း တင်ပါ။
   - `.github/workflows/` ထဲက ဖိုင်တွေ မတင်ဖြစ်ရင် **Add file -> Create new file** နဲ့ လမ်းကြောင်းအတိုင်း ကိုယ်တိုင် ဆောက်ပါ။
2. **Settings -> Secrets and variables -> Actions** မှာ ထည့်ပါ:
   - `YT_CLIENT_ID`, `YT_CLIENT_SECRET`
   - `YT_REFRESH_TOKEN`  (**channel 1** ရဲ့ token)
   - (ရွေးချယ်) `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` - error သတင်းပို့ရန်
3. **Actions -> YouTube Live 2D** -> Run workflow -> `test` နဲ့ အရင်စမ်းပါ။
4. cron-job.org မှာ ဒီ repo ရဲ့ URL နဲ့ job ဆောက်ပါ (မနက် 10:28 / ညနေ 14:28):
   `https://api.github.com/repos/USER/REPO/actions/workflows/live-stream.yml/dispatches`
   body: `{"ref":"main","inputs":{"session":"morning"}}` (ညနေဆို evening)
5. Post: `post.yml` (12:01 / 16:30)  ·  ပိတ်ရက်ပြင်: `holidays.txt`  ·  ကိုယ့်သီချင်း: `audio/` ထဲတင်
