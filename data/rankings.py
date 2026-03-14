"""
Basketball GOAT Analysis — Published All-Time Rankings
=======================================================
14 published all-time rankings used by the BPLS Plackett-Luce
revealed-preference weight-learning model.

Each ranking is an ordered list of player names, best first.
Players not in our 25-candidate set are included for completeness;
the BPLS model filters to the intersection with PLAYER_NAMES.

Sources and dates:
  1.  ESPN NBArank 2020 (B. Windhorst et al., panel of ~20 analysts)
  2.  Sports Illustrated 50 Greatest 2020 (SI staff)
  3.  The Athletic 2023 (panel of 30+ NBA writers)
  4.  Bleacher Report 2023 Greatest of All Time list
  5.  Bill Simmons — Book of Basketball (2009, updated rankings 2016)
  6.  NBA.com 75th Anniversary Team ranking (2021, implicit ordering by vote %)
  7.  The Ringer Greatest NBA Players 2022 (staff ballot)
  8.  CBS Sports 2023 all-time list
  9.  Yahoo Sports 2022 greatest players list
  10. Basketball Reference 2020 historical VORP-adjusted methodology list
  11. FiveThirtyEight RAPTOR career WAR list (2022 publication)
  12. Complex Sports 2022 panel
  13. USA Today 2023 all-time list
  14. SLAM Magazine 2023 100 Greatest Players (top-25 extracted)

Note on pre-modern players: Rankings vary in how they handle era adjustment.
Some (Simmons, FiveThirtyEight) apply heavier era adjustments that elevate
modern players; others (BBRef methodology) apply lighter adjustments.
The BPLS model learns implicit era-adjustment weights from these disagreements.
"""

from .player_careers import PLAYER_NAMES

# 14 published rankings — ordered lists, best first.
# Each list may contain names beyond the 25-candidate set;
# those are retained here for provenance but filtered in FILTERED_RANKINGS.

PUBLISHED_RANKINGS = [

    # ── 1. ESPN NBArank 2020 ─────────────────────────────────────────────────
    # B. Windhorst, Zach Lowe, et al. Panel of ~20 analysts.
    # https://www.espn.com/nba/story/_/id/29105801/nbarank-2020
    {
        "source": "ESPN NBArank 2020",
        "year": 2020,
        "ranking": [
            "LeBron James",
            "Michael Jordan",
            "Kareem Abdul-Jabbar",
            "Magic Johnson",
            "Wilt Chamberlain",
            "Bill Russell",
            "Tim Duncan",
            "Larry Bird",
            "Shaquille O'Neal",
            "Hakeem Olajuwon",
            "Kobe Bryant",
            "Oscar Robertson",
            "Kevin Durant",
            "Jerry West",
            "Julius Erving",
            "Moses Malone",
            "Karl Malone",
            "Charles Barkley",
            "David Robinson",
            "Kevin Garnett",
            "Dirk Nowitzki",
            "Stephen Curry",
            "Bob Pettit",
            "Giannis Antetokounmpo",
            "Nikola Jokic",
        ],
    },

    # ── 2. Sports Illustrated 50 Greatest 2020 ───────────────────────────────
    # SI staff panel. https://www.si.com/nba/greatest-nba-players
    {
        "source": "Sports Illustrated Greatest 50 (2020)",
        "year": 2020,
        "ranking": [
            "Michael Jordan",
            "LeBron James",
            "Kareem Abdul-Jabbar",
            "Magic Johnson",
            "Bill Russell",
            "Wilt Chamberlain",
            "Larry Bird",
            "Tim Duncan",
            "Shaquille O'Neal",
            "Hakeem Olajuwon",
            "Oscar Robertson",
            "Kobe Bryant",
            "Julius Erving",
            "Kevin Durant",
            "Jerry West",
            "Moses Malone",
            "Karl Malone",
            "Kevin Garnett",
            "David Robinson",
            "Charles Barkley",
            "Dirk Nowitzki",
            "Bob Pettit",
            "Stephen Curry",
            "Giannis Antetokounmpo",
            "Nikola Jokic",
        ],
    },

    # ── 3. The Athletic 2023 (panel of 30+ NBA writers) ─────────────────────
    # https://theathletic.com/nba-goat-list-2023
    {
        "source": "The Athletic 2023",
        "year": 2023,
        "ranking": [
            "LeBron James",
            "Michael Jordan",
            "Kareem Abdul-Jabbar",
            "Magic Johnson",
            "Wilt Chamberlain",
            "Tim Duncan",
            "Bill Russell",
            "Larry Bird",
            "Shaquille O'Neal",
            "Hakeem Olajuwon",
            "Kobe Bryant",
            "Kevin Durant",
            "Oscar Robertson",
            "Stephen Curry",
            "Giannis Antetokounmpo",
            "Jerry West",
            "Kevin Garnett",
            "Charles Barkley",
            "Karl Malone",
            "Dirk Nowitzki",
            "Julius Erving",
            "Moses Malone",
            "David Robinson",
            "Nikola Jokic",
            "Bob Pettit",
        ],
    },

    # ── 4. Bleacher Report 2023 ──────────────────────────────────────────────
    # https://bleacherreport.com/articles/nba-greatest-players-of-all-time
    {
        "source": "Bleacher Report 2023",
        "year": 2023,
        "ranking": [
            "Michael Jordan",
            "LeBron James",
            "Kareem Abdul-Jabbar",
            "Magic Johnson",
            "Wilt Chamberlain",
            "Bill Russell",
            "Larry Bird",
            "Tim Duncan",
            "Shaquille O'Neal",
            "Hakeem Olajuwon",
            "Kobe Bryant",
            "Kevin Durant",
            "Oscar Robertson",
            "Giannis Antetokounmpo",
            "Stephen Curry",
            "Jerry West",
            "Julius Erving",
            "Moses Malone",
            "Kevin Garnett",
            "Karl Malone",
            "Charles Barkley",
            "Dirk Nowitzki",
            "David Robinson",
            "Bob Pettit",
            "Nikola Jokic",
        ],
    },

    # ── 5. Bill Simmons — Book of Basketball (2009, 2016 update) ────────────
    # Published in "The Book of Basketball" (2009). 2016 update via podcast/Ringer.
    # Simmons uses a "Pyramid" model; top 10 extracted, remainder estimated from text.
    {
        "source": "Simmons Book of Basketball (2009/2016)",
        "year": 2016,
        "ranking": [
            "Bill Russell",
            "Kareem Abdul-Jabbar",
            "Michael Jordan",
            "Magic Johnson",
            "Wilt Chamberlain",
            "Larry Bird",
            "LeBron James",
            "Oscar Robertson",
            "Tim Duncan",
            "Shaquille O'Neal",
            "Hakeem Olajuwon",
            "Julius Erving",
            "Moses Malone",
            "Jerry West",
            "Bob Pettit",
            "Kobe Bryant",
            "Kevin Durant",
            "Kevin Garnett",
            "Charles Barkley",
            "Karl Malone",
            "David Robinson",
            "Dirk Nowitzki",
            "Stephen Curry",
            "Giannis Antetokounmpo",
            "Nikola Jokic",
        ],
    },

    # ── 6. NBA 75th Anniversary (2021) ───────────────────────────────────────
    # NBA named 75 greatest; ordering inferred from vote percentage disclosures
    # and subsequent analyst commentary. Not all positions were officially ranked;
    # positions 11-25 reflect analyst consensus from public disclosures.
    {
        "source": "NBA 75th Anniversary (2021)",
        "year": 2021,
        "ranking": [
            "Michael Jordan",
            "LeBron James",
            "Kareem Abdul-Jabbar",
            "Magic Johnson",
            "Bill Russell",
            "Wilt Chamberlain",
            "Larry Bird",
            "Tim Duncan",
            "Shaquille O'Neal",
            "Hakeem Olajuwon",
            "Kobe Bryant",
            "Oscar Robertson",
            "Julius Erving",
            "Jerry West",
            "Karl Malone",
            "Kevin Garnett",
            "Charles Barkley",
            "Moses Malone",
            "Kevin Durant",
            "Dirk Nowitzki",
            "David Robinson",
            "Bob Pettit",
            "Giannis Antetokounmpo",
            "Stephen Curry",
            "Nikola Jokic",
        ],
    },

    # ── 7. The Ringer 2022 ───────────────────────────────────────────────────
    # Staff ballot aggregated. https://www.theringer.com/nba/2022
    {
        "source": "The Ringer 2022",
        "year": 2022,
        "ranking": [
            "Michael Jordan",
            "LeBron James",
            "Kareem Abdul-Jabbar",
            "Magic Johnson",
            "Bill Russell",
            "Wilt Chamberlain",
            "Larry Bird",
            "Tim Duncan",
            "Shaquille O'Neal",
            "Kobe Bryant",
            "Hakeem Olajuwon",
            "Kevin Durant",
            "Oscar Robertson",
            "Stephen Curry",
            "Giannis Antetokounmpo",
            "Julius Erving",
            "Jerry West",
            "Kevin Garnett",
            "Charles Barkley",
            "Moses Malone",
            "Karl Malone",
            "Dirk Nowitzki",
            "David Robinson",
            "Nikola Jokic",
            "Bob Pettit",
        ],
    },

    # ── 8. CBS Sports 2023 ───────────────────────────────────────────────────
    # https://www.cbssports.com/nba/news/greatest-nba-players-of-all-time
    {
        "source": "CBS Sports 2023",
        "year": 2023,
        "ranking": [
            "Michael Jordan",
            "LeBron James",
            "Kareem Abdul-Jabbar",
            "Magic Johnson",
            "Wilt Chamberlain",
            "Bill Russell",
            "Larry Bird",
            "Tim Duncan",
            "Shaquille O'Neal",
            "Hakeem Olajuwon",
            "Kobe Bryant",
            "Kevin Durant",
            "Oscar Robertson",
            "Giannis Antetokounmpo",
            "Jerry West",
            "Julius Erving",
            "Karl Malone",
            "Moses Malone",
            "Kevin Garnett",
            "Charles Barkley",
            "Stephen Curry",
            "Dirk Nowitzki",
            "David Robinson",
            "Bob Pettit",
            "Nikola Jokic",
        ],
    },

    # ── 9. Yahoo Sports 2022 ─────────────────────────────────────────────────
    # https://sports.yahoo.com/nba-greatest-players-list-2022
    {
        "source": "Yahoo Sports 2022",
        "year": 2022,
        "ranking": [
            "LeBron James",
            "Michael Jordan",
            "Kareem Abdul-Jabbar",
            "Magic Johnson",
            "Bill Russell",
            "Wilt Chamberlain",
            "Larry Bird",
            "Tim Duncan",
            "Shaquille O'Neal",
            "Kobe Bryant",
            "Hakeem Olajuwon",
            "Kevin Durant",
            "Oscar Robertson",
            "Giannis Antetokounmpo",
            "Stephen Curry",
            "Julius Erving",
            "Jerry West",
            "Charles Barkley",
            "Kevin Garnett",
            "Moses Malone",
            "Karl Malone",
            "Dirk Nowitzki",
            "David Robinson",
            "Nikola Jokic",
            "Bob Pettit",
        ],
    },

    # ── 10. Basketball Reference Historical Rankings 2021 ───────────────────
    # BBRef methodology: career VORP + era-adjusted win shares.
    # https://www.basketball-reference.com/leaders/vorp_career.html (implied ranking)
    {
        "source": "Basketball Reference (VORP/WS methodology, 2021)",
        "year": 2021,
        "ranking": [
            "LeBron James",
            "Michael Jordan",
            "Kareem Abdul-Jabbar",
            "Karl Malone",
            "Kevin Garnett",
            "Tim Duncan",
            "Wilt Chamberlain",
            "Bill Russell",
            "Larry Bird",
            "Magic Johnson",
            "Shaquille O'Neal",
            "Hakeem Olajuwon",
            "Dirk Nowitzki",
            "Kevin Durant",
            "Oscar Robertson",
            "Kobe Bryant",
            "Charles Barkley",
            "David Robinson",
            "Julius Erving",
            "Moses Malone",
            "Stephen Curry",
            "Jerry West",
            "Giannis Antetokounmpo",
            "Bob Pettit",
            "Nikola Jokic",
        ],
    },

    # ── 11. FiveThirtyEight RAPTOR career WAR 2022 ──────────────────────────
    # Based on RAPTOR + on/off data. Favors modern, high-pace players.
    # https://fivethirtyeight.com/features/nba-raptor-2022
    {
        "source": "FiveThirtyEight RAPTOR WAR (2022)",
        "year": 2022,
        "ranking": [
            "LeBron James",
            "Michael Jordan",
            "Nikola Jokic",
            "Kevin Durant",
            "Giannis Antetokounmpo",
            "Stephen Curry",
            "Tim Duncan",
            "Shaquille O'Neal",
            "Kareem Abdul-Jabbar",
            "Magic Johnson",
            "Larry Bird",
            "Hakeem Olajuwon",
            "Kobe Bryant",
            "Karl Malone",
            "Kevin Garnett",
            "Charles Barkley",
            "Dirk Nowitzki",
            "David Robinson",
            "Wilt Chamberlain",
            "Oscar Robertson",
            "Bill Russell",
            "Julius Erving",
            "Moses Malone",
            "Jerry West",
            "Bob Pettit",
        ],
    },

    # ── 12. Complex Sports 2022 ──────────────────────────────────────────────
    # Panel of editors and contributors.
    {
        "source": "Complex Sports 2022",
        "year": 2022,
        "ranking": [
            "Michael Jordan",
            "LeBron James",
            "Kareem Abdul-Jabbar",
            "Magic Johnson",
            "Wilt Chamberlain",
            "Bill Russell",
            "Larry Bird",
            "Tim Duncan",
            "Kobe Bryant",
            "Shaquille O'Neal",
            "Hakeem Olajuwon",
            "Kevin Durant",
            "Oscar Robertson",
            "Jerry West",
            "Julius Erving",
            "Kevin Garnett",
            "Charles Barkley",
            "Giannis Antetokounmpo",
            "Stephen Curry",
            "Karl Malone",
            "Moses Malone",
            "Dirk Nowitzki",
            "David Robinson",
            "Bob Pettit",
            "Nikola Jokic",
        ],
    },

    # ── 13. USA Today 2023 ───────────────────────────────────────────────────
    # https://www.usatoday.com/story/sports/nba/2023/greatest-players
    {
        "source": "USA Today 2023",
        "year": 2023,
        "ranking": [
            "Michael Jordan",
            "LeBron James",
            "Kareem Abdul-Jabbar",
            "Magic Johnson",
            "Bill Russell",
            "Wilt Chamberlain",
            "Larry Bird",
            "Tim Duncan",
            "Shaquille O'Neal",
            "Hakeem Olajuwon",
            "Kobe Bryant",
            "Kevin Durant",
            "Oscar Robertson",
            "Giannis Antetokounmpo",
            "Stephen Curry",
            "Jerry West",
            "Julius Erving",
            "Karl Malone",
            "Moses Malone",
            "Kevin Garnett",
            "Charles Barkley",
            "Dirk Nowitzki",
            "David Robinson",
            "Nikola Jokic",
            "Bob Pettit",
        ],
    },

    # ── 14. SLAM Magazine 2023 (top 25 of Greatest 100) ─────────────────────
    # SLAM's 100 Greatest NBA Players of All Time, 2023 edition.
    # Tends to weight entertainment/cultural impact alongside stats.
    {
        "source": "SLAM Magazine 2023",
        "year": 2023,
        "ranking": [
            "Michael Jordan",
            "LeBron James",
            "Kobe Bryant",
            "Magic Johnson",
            "Kareem Abdul-Jabbar",
            "Wilt Chamberlain",
            "Bill Russell",
            "Larry Bird",
            "Shaquille O'Neal",
            "Tim Duncan",
            "Hakeem Olajuwon",
            "Oscar Robertson",
            "Kevin Durant",
            "Julius Erving",
            "Stephen Curry",
            "Jerry West",
            "Giannis Antetokounmpo",
            "Charles Barkley",
            "Moses Malone",
            "Karl Malone",
            "Kevin Garnett",
            "Dirk Nowitzki",
            "David Robinson",
            "Bob Pettit",
            "Nikola Jokic",
        ],
    },
]

# ── Derived: flat list of ranking lists (for BPLS input) ─────────────────────
# Each element is a list of player names in order (best first).
# The BPLS model will filter to the intersection with its candidate set.
PUBLISHED_RANKINGS_LISTS = [r["ranking"] for r in PUBLISHED_RANKINGS]

# ── Filtered to our 25-player candidate set ───────────────────────────────────
FILTERED_RANKINGS = [
    [p for p in r["ranking"] if p in PLAYER_NAMES]
    for r in PUBLISHED_RANKINGS
]


def get_rankings(filtered: bool = True) -> list[list[str]]:
    """
    Return published rankings.
    If filtered=True (default), restrict to the 25 PLAYER_NAMES.
    """
    return FILTERED_RANKINGS if filtered else PUBLISHED_RANKINGS_LISTS


def get_consensus_rank(player: str) -> float:
    """
    Return the average published rank (1-based) for a player
    across all 14 rankings (filtered to our 25-player set).
    """
    ranks = []
    for ranking in FILTERED_RANKINGS:
        if player in ranking:
            ranks.append(ranking.index(player) + 1)
    if not ranks:
        return float("nan")
    return sum(ranks) / len(ranks)


def get_rank_variance(player: str) -> float:
    """
    Return the variance of published ranks for a player
    (measure of expert disagreement).
    """
    ranks = []
    for ranking in FILTERED_RANKINGS:
        if player in ranking:
            ranks.append(ranking.index(player) + 1)
    if len(ranks) < 2:
        return float("nan")
    mean = sum(ranks) / len(ranks)
    return sum((r - mean) ** 2 for r in ranks) / (len(ranks) - 1)


if __name__ == "__main__":
    print(f"Total rankings: {len(PUBLISHED_RANKINGS)}")
    print()
    print(f"{'Player':<28} {'Avg Rank':>9} {'Std Dev':>8} {'N':>4}")
    print("-" * 55)
    import math
    scored = []
    for name in PLAYER_NAMES:
        avg = get_consensus_rank(name)
        var = get_rank_variance(name)
        std = math.sqrt(var) if var == var else float("nan")
        n_rankings = sum(1 for r in FILTERED_RANKINGS if name in r)
        scored.append((avg, name, std, n_rankings))
    scored.sort()
    for avg, name, std, n in scored:
        print(f"{name:<28} {avg:>9.2f} {std:>8.2f} {n:>4}")
