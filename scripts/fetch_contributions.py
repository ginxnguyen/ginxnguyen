import json, re, sys
import requests
from bs4 import BeautifulSoup

USER = sys.argv[1] if len(sys.argv) > 1 else "ginxnguyen"
html = requests.get(f"https://github.com/users/{USER}/contributions", timeout=30).text
soup = BeautifulSoup(html, "html.parser")

tips = {t["for"]: t.get_text() for t in soup.find_all("tool-tip")}
days = []
for td in soup.select("td.ContributionCalendar-day"):
    m = re.match(r"(\d+)", tips.get(td.get("id"), ""))
    days.append({
        "date": td["data-date"],
        "level": int(td["data-level"]),
        "count": int(m.group(1)) if m else 0,
    })
days.sort(key=lambda d: d["date"])

total = sum(d["count"] for d in days)
with open("data/contributions.json", "w") as f:
    json.dump({"user": USER, "total": total, "days": days}, f)
print("Total:", total)