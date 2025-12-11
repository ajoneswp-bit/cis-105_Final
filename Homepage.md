# home page
## Overview
I created a tool to help fantasy football players find people to pick up in free agency throughout the season.  By filtering out the top players that are likely on teams already, and sorting by average production over the last three weeks, you can find players that have recently had an uptick in scoring and are likely to do better than their overall ranking would suggest.
## Web Scraping

### Data Sources

This project uses two fantasy football data sources, scraped using Python:

- **Pro-Football-Reference**  
  Used to collect player names and positions for the 2025 fantasy season.

- **FootballDB**  
  Used to collect weekly fantasy points (Weeks 1–13) for offensive players.

FootballDB did not have the player positions in their table, so I used Pro-football-reference to collect those.

---

### Tools Used

The following Python libraries were used for web scraping and data processing:

- `urllib.request` – to send HTTP requests  
- `BeautifulSoup` (from `bs4`) – to parse HTML and extract table data  
- `pandas` – to clean, merge, and export the data to CSV  

---

### Example Scraping Code (Request + Parse)

The example below shows the core scraping pattern used throughout the project. This version demonstrates scraping weekly fantasy points from FootballDB.

``` python
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

user_agent = "Mozilla/5.0"
header = {"User-Agent": user_agent}

url = "https://www.footballdb.com/fantasy-football/index.html?yr=2025&pos=OFF&wk=13"

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

    print(name, points)
```

### AI Assistance Disclosure

An AI assistant was used to help:

Restructure weekly scraping logic

Add total points calculations

Merge position data with weekly data

Export a clean final CSV file

Example prompt used during development:

Write a Python function that uses requests and BeautifulSoup to scrape weekly fantasy football points from this FootballDB page. Store the data by player and week, then pivot it into a table with players as rows and weeks as columns. Add a total points column and export to a CSV file. Also merge player positions from Pro-Football-Reference.

For the whole AI conversation, click here: https://chatgpt.com/share/6931d54e-4bf0-8005-a30d-33f72470479e

## Database
For my database, I collected the players names, positions, points for each week from 1-13, and their total points.

### Format

The first column lists player names, the second is position, then the next thirteen columns are the weekly points, and finally the last column is total points.

### SQL

I initially had several different SQL queries I had to run in order to get my final csv file, but i was able to merge them all into this one query:

``` sql
SELECT 
    ranked.position_rank,
    ranked.player_name,
    ranked.position,
    ranked.total_points,
    ROUND((COALESCE(ranked.week_11, 0) + COALESCE(ranked.week_12, 0) + COALESCE(ranked.week_13, 0)) / 3.0, 2) as last_3_weeks_avg,
    ranked.week_11,
    ranked.week_12,
    ranked.week_13
FROM (
    SELECT 
        ROW_NUMBER() OVER (PARTITION BY position ORDER BY total_points DESC) as position_rank,
        player_name, 
        position, 
        total_points,
        week_11,
        week_12,
        week_13
    FROM player_stats
) ranked
ORDER BY last_3_weeks_avg DESC;
```
## Web Application
At the top of the application, there is a dropdown that allows you to filter by position. Next to it, there is an input box where you can enter a number and it will filter out any player whose position rank is above that number.  You can also sort by any of the columns in the table, ascending or descending, by clicking on the headers.  The main intended funcionality of the program is to find players that may not have a high ranking, but have been performing well recently.  While it is not perfect, the average points for the last three weeks can be used as an indicator for how a player may perform in the near future.  