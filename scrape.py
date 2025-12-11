from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd

# ============================================================
# ✅ PART 1 — SCRAPE PLAYER POSITIONS
# ============================================================

print("Scraping player positions...")

position_url = "https://www.pro-football-reference.com/years/2025/fantasy.htm"
web_page = urlopen(position_url).read().decode("UTF-8")
soup = BeautifulSoup(web_page, "html.parser")

table = soup.find("tbody")
trlist = table.find_all("tr", {"class": None})

position_data = []

for tr in trlist:
    tdlist = tr.find_all("td")
    name = tdlist[0].text.strip()
    position = tdlist[2].text.strip()

    position_data.append({
        "Player": name,
        "Position": position
    })

df_positions = pd.DataFrame(position_data)


# ============================================================
# ✅ PART 2 — SCRAPE WEEKLY POINTS
# ============================================================

print("Scraping weekly fantasy points...")

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
header = {"User-Agent": user_agent}

all_data = []
week = 13

while week >= 1:

    url = f"https://www.footballdb.com/fantasy-football/index.html?yr=2025&pos=OFF&wk={week}&key=48ca46aa7d721af4d58dccc0c249a1c4"
    print(f"Week {week}")

    req = Request(url, headers=header)
    html_doc = urlopen(req).read().decode("UTF-8")
    soup = BeautifulSoup(html_doc, "html.parser")

    table = soup.find("tbody")
    trlist = table.find_all("tr")

    for tr in trlist:
        tdlist = tr.find_all("td")
        a = tr.find("a")

        if a is None:
            continue

        name = a.text.strip()
        points = float(tdlist[2].text.strip())

        all_data.append({
            "Player": name,
            "Week": week,
            "Points": points
        })

    week -= 1


# ============================================================
# ✅ PART 3 — CREATE WEEKLY TABLE + TOTALS
# ============================================================

df_points = pd.DataFrame(all_data)

df_pivot = df_points.pivot_table(
    index="Player",
    columns="Week",
    values="Points"
)

# Sort Week columns left → right
df_pivot = df_pivot.reindex(sorted(df_pivot.columns), axis=1)

# ✅ ADD TOTAL COLUMN
df_pivot["Total Points"] = df_pivot.sum(axis=1)

df_pivot.reset_index(inplace=True)


# ============================================================
# ✅ PART 4 — MERGE POSITIONS + WEEKLY DATA
# ============================================================

df_final = pd.merge(
    df_pivot,
    df_positions,
    on="Player",
    how="left"
)

# Move Position to 2nd column
cols = df_final.columns.tolist()
cols.insert(1, cols.pop(cols.index("Position")))
df_final = df_final[cols]


# ============================================================
# ✅ PART 5 — SAVE FINAL CSV
# ============================================================

df_final.to_csv("fantasy_2025_full_weekly_with_positions.csv", index=False)

print("✅ CSV created: fantasy_2025_full_weekly_with_positions.csv")