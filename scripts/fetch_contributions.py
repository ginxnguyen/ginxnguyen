import json, os, re, sys
from collections import OrderedDict
from datetime import date, datetime, timezone

import requests
from bs4 import BeautifulSoup

USER = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_USERNAME", "ginxnguyen")
URL = f"https://github.com/users/{USER}/contributions"

resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

tips = {t.get("for"): t.get_text(" ", strip=True) for t in soup.find_all("tool-tip")}
today = date.today().isoformat()

days = []
for td in soup.select("td.ContributionCalendar-day"):
    d = td.get("data-date")
    if not d or d > today:
        continue
    m = re.match(r"(\d[\d,]*)", tips.get(td.get("id"), ""))
    days.append({
        "date": d,
        "level": int(td.get("data-level", 0)),
        "count": int(m.group(1).replace(",", "")) if m else 0,
    })
days.sort(key=lambda x: x["date"])
if not days:
    sys.exit("No contribution cells found - GitHub's HTML may have changed.")

longest = run = 0
for d in days:
    run = run + 1 if d["count"] > 0 else 0
    longest = max(longest, run)

current, i = 0, len(days) - 1
if days[i]["count"] == 0:      # today may not have contributions yet
    i -= 1
while i >= 0 and days[i]["count"] > 0:
    current += 1
    i -= 1

monthly = OrderedDict()
for d in days:
    monthly[d["date"][:7]] = monthly.get(d["date"][:7], 0) + d["count"]

best = max(days, key=lambda x: x["count"])
data = {
    "user": USER,
    "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "total": sum(d["count"] for d in days),
    "current_streak": current,
    "longest_streak": longest,
    "best_day": {"date": best["date"], "count": best["count"]},
    "monthly": monthly,
    "days": days,
}
with open("data/contributions.json", "w") as f:
    json.dump(data, f, indent=1)
print(f"{USER}: {data['total']} contributions, streak {current}d (longest {longest}d)")
