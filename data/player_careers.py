"""
data/player_careers.py
======================
Career statistics for 10 GOAT candidates, sourced from Basketball Reference.
All statistics are career regular-season unless noted.  Playoff figures are
stored separately under the 'playoffs' key.

Stat glossary
-------------
seasons       : number of NBA seasons played
games         : career regular-season games
ppg           : points per game
rpg           : rebounds per game
apg           : assists per game
spg           : steals per game  (0.0 = pre-tracking era, marked est.)
bpg           : blocks per game  (0.0 = pre-tracking era, marked est.)
fg_pct        : field-goal %
ts_pct        : true-shooting %  (estimated for pre-1984 players)
per           : Player Efficiency Rating
bpm           : Box Plus-Minus   (backfilled pre-1974 via B-Ref regression)
vorp          : Value Over Replacement Player (career)
win_shares    : career Win Shares
ws_per_48     : Win Shares per 48 minutes
peak_bpm_7yr  : best 7-season consecutive BPM average (prime window)
mvp_count     : regular-season MVP awards
finals_mvp    : Finals MVP awards
championships : rings
all_nba_1st   : 1st-team All-NBA selections
all_def_1st   : 1st-team All-Defensive selections
scoring_titles : scoring titles
all_star       : All-Star selections
era           : approximate era midpoint (for era-adjustment reference)

Playoff-specific keys (under 'playoffs'):
  games, ppg, rpg, apg, bpm, win_shares
"""

PLAYERS = {
    "Michael Jordan": {
        "seasons": 15,
        "games": 1072,
        "ppg": 30.1,
        "rpg": 6.2,
        "apg": 5.3,
        "spg": 2.35,
        "bpg": 0.83,
        "fg_pct": 0.497,
        "ts_pct": 0.569,
        "per": 27.9,
        "bpm": 9.2,          # career BPM
        "vorp": 116.1,
        "win_shares": 214.0,
        "ws_per_48": 0.2505,
        "peak_bpm_7yr": 9.2,  # 1987-88 through 1993-94 avg
        "mvp_count": 5,
        "finals_mvp": 6,
        "championships": 6,
        "all_nba_1st": 10,
        "all_def_1st": 9,
        "scoring_titles": 10,
        "all_star": 14,
        "era": 1992,
        "playoffs": {
            "games": 179,
            "ppg": 33.4,
            "rpg": 6.4,
            "apg": 5.7,
            "bpm": 10.8,
            "win_shares": 42.0,
        },
    },
    "LeBron James": {
        "seasons": 21,
        "games": 1487,
        "ppg": 27.1,
        "rpg": 7.5,
        "apg": 7.4,
        "spg": 1.55,
        "bpg": 0.75,
        "fg_pct": 0.504,
        "ts_pct": 0.580,
        "per": 27.1,
        "bpm": 8.9,
        "vorp": 151.4,
        "win_shares": 262.7,
        "ws_per_48": 0.2328,
        "peak_bpm_7yr": 9.3,  # 2008-09 through 2014-15
        "mvp_count": 4,
        "finals_mvp": 4,
        "championships": 4,
        "all_nba_1st": 13,
        "all_def_1st": 5,
        "scoring_titles": 1,
        "all_star": 20,
        "era": 2013,
        "playoffs": {
            "games": 287,
            "ppg": 28.8,
            "rpg": 9.0,
            "apg": 7.2,
            "bpm": 9.8,
            "win_shares": 58.9,
        },
    },
    "Kareem Abdul-Jabbar": {
        "seasons": 20,
        "games": 1560,
        "ppg": 24.6,
        "rpg": 11.2,
        "apg": 3.6,
        "spg": 0.85,   # estimated; tracking began mid-career
        "bpg": 2.60,
        "fg_pct": 0.559,
        "ts_pct": 0.577,
        "per": 24.6,
        "bpm": 9.0,
        "vorp": 150.7,
        "win_shares": 273.4,
        "ws_per_48": 0.2274,
        "peak_bpm_7yr": 9.8,  # 1970-71 through 1976-77
        "mvp_count": 6,
        "finals_mvp": 2,
        "championships": 6,
        "all_nba_1st": 10,
        "all_def_1st": 5,
        "scoring_titles": 2,
        "all_star": 19,
        "era": 1978,
        "playoffs": {
            "games": 237,
            "ppg": 24.3,
            "rpg": 10.5,
            "apg": 3.1,
            "bpm": 8.4,
            "win_shares": 44.2,
        },
    },
    "Bill Russell": {
        "seasons": 13,
        "games": 963,
        "ppg": 15.1,
        "rpg": 22.5,
        "apg": 4.3,
        "spg": 0.0,   # not tracked; est. ~2.5
        "bpg": 0.0,   # not tracked; est. ~6.0+
        "fg_pct": 0.440,
        "ts_pct": 0.488,
        "per": 21.1,
        "bpm": 10.4,   # B-Ref backfill estimate
        "vorp": 95.0,
        "win_shares": 163.0,
        "ws_per_48": 0.2126,
        "peak_bpm_7yr": 11.2,  # 1958-59 through 1964-65
        "mvp_count": 5,
        "finals_mvp": 0,  # award didn't exist until 1969
        "championships": 11,
        "all_nba_1st": 3,
        "all_def_1st": 0,  # All-Defensive team started 1969
        "scoring_titles": 0,
        "all_star": 12,
        "era": 1962,
        "playoffs": {
            "games": 165,
            "ppg": 16.2,
            "rpg": 24.9,
            "apg": 4.7,
            "bpm": 11.6,
            "win_shares": 30.8,
        },
    },
    "Wilt Chamberlain": {
        "seasons": 14,
        "games": 1045,
        "ppg": 30.1,
        "rpg": 22.9,
        "apg": 4.4,
        "spg": 0.0,
        "bpg": 0.0,
        "fg_pct": 0.540,
        "ts_pct": 0.575,
        "per": 26.1,
        "bpm": 10.0,   # B-Ref backfill
        "vorp": 96.6,
        "win_shares": 247.2,
        "ws_per_48": 0.2977,
        "peak_bpm_7yr": 12.1,  # 1960-61 through 1966-67
        "mvp_count": 4,
        "finals_mvp": 0,  # none awarded to him
        "championships": 2,
        "all_nba_1st": 7,
        "all_def_1st": 0,
        "scoring_titles": 7,
        "all_star": 13,
        "era": 1965,
        "playoffs": {
            "games": 160,
            "ppg": 22.5,
            "rpg": 24.5,
            "apg": 4.2,
            "bpm": 9.8,
            "win_shares": 41.4,
        },
    },
    "Magic Johnson": {
        "seasons": 13,
        "games": 906,
        "ppg": 19.5,
        "rpg": 7.2,
        "apg": 11.2,
        "spg": 1.90,
        "bpg": 0.37,
        "fg_pct": 0.520,
        "ts_pct": 0.584,
        "per": 24.1,
        "bpm": 7.6,
        "vorp": 89.5,
        "win_shares": 196.1,
        "ws_per_48": 0.2279,
        "peak_bpm_7yr": 8.6,  # 1982-83 through 1988-89
        "mvp_count": 3,
        "finals_mvp": 3,
        "championships": 5,
        "all_nba_1st": 9,
        "all_def_1st": 0,
        "scoring_titles": 0,
        "all_star": 12,
        "era": 1987,
        "playoffs": {
            "games": 190,
            "ppg": 19.5,
            "rpg": 7.7,
            "apg": 12.3,
            "bpm": 8.5,
            "win_shares": 38.5,
        },
    },
    "Tim Duncan": {
        "seasons": 19,
        "games": 1392,
        "ppg": 19.0,
        "rpg": 10.8,
        "apg": 3.0,
        "spg": 0.70,
        "bpg": 2.17,
        "fg_pct": 0.506,
        "ts_pct": 0.543,
        "per": 24.2,
        "bpm": 8.2,
        "vorp": 126.7,
        "win_shares": 206.4,
        "ws_per_48": 0.1949,
        "peak_bpm_7yr": 9.4,  # 1998-99 through 2004-05
        "mvp_count": 2,
        "finals_mvp": 3,
        "championships": 5,
        "all_nba_1st": 10,
        "all_def_1st": 8,
        "scoring_titles": 0,
        "all_star": 15,
        "era": 2005,
        "playoffs": {
            "games": 251,
            "ppg": 20.6,
            "rpg": 11.4,
            "apg": 3.2,
            "bpm": 9.0,
            "win_shares": 45.8,
        },
    },
    "Larry Bird": {
        "seasons": 13,
        "games": 897,
        "ppg": 24.3,
        "rpg": 10.0,
        "apg": 6.3,
        "spg": 1.79,
        "bpg": 0.84,
        "fg_pct": 0.496,
        "ts_pct": 0.567,
        "per": 23.5,
        "bpm": 9.2,
        "vorp": 90.0,
        "win_shares": 196.8,
        "ws_per_48": 0.2339,
        "peak_bpm_7yr": 9.8,  # 1983-84 through 1989-90
        "mvp_count": 3,
        "finals_mvp": 2,
        "championships": 3,
        "all_nba_1st": 9,
        "all_def_1st": 0,
        "scoring_titles": 0,
        "all_star": 12,
        "era": 1986,
        "playoffs": {
            "games": 164,
            "ppg": 23.8,
            "rpg": 10.3,
            "apg": 6.5,
            "bpm": 9.3,
            "win_shares": 35.2,
        },
    },
    "Shaquille O'Neal": {
        "seasons": 19,
        "games": 1207,
        "ppg": 23.7,
        "rpg": 10.9,
        "apg": 2.5,
        "spg": 0.59,
        "bpg": 2.26,
        "fg_pct": 0.582,
        "ts_pct": 0.584,
        "per": 26.4,
        "bpm": 6.8,
        "vorp": 87.8,
        "win_shares": 181.7,
        "ws_per_48": 0.2270,
        "peak_bpm_7yr": 8.9,  # 1997-98 through 2003-04
        "mvp_count": 1,
        "finals_mvp": 3,
        "championships": 4,
        "all_nba_1st": 8,
        "all_def_1st": 0,
        "scoring_titles": 1,
        "all_star": 15,
        "era": 2001,
        "playoffs": {
            "games": 216,
            "ppg": 24.3,
            "rpg": 11.6,
            "apg": 2.8,
            "bpm": 7.2,
            "win_shares": 42.0,
        },
    },
    "Hakeem Olajuwon": {
        "seasons": 18,
        "games": 1238,
        "ppg": 21.8,
        "rpg": 11.1,
        "apg": 2.5,
        "spg": 1.71,
        "bpg": 3.09,
        "fg_pct": 0.512,
        "ts_pct": 0.546,
        "per": 23.6,
        "bpm": 7.2,
        "vorp": 101.1,
        "win_shares": 178.5,
        "ws_per_48": 0.2068,
        "peak_bpm_7yr": 8.5,  # 1987-88 through 1993-94
        "mvp_count": 1,
        "finals_mvp": 2,
        "championships": 2,
        "all_nba_1st": 6,
        "all_def_1st": 5,
        "scoring_titles": 0,
        "all_star": 12,
        "era": 1994,
        "playoffs": {
            "games": 145,
            "ppg": 25.9,
            "rpg": 11.0,
            "apg": 2.7,
            "bpm": 9.2,
            "win_shares": 27.5,
        },
    },
}

# Ordered list of player names (for consistent indexing)
PLAYER_NAMES = list(PLAYERS.keys())

# League history context — used by EARD talent-pool depth multiplier
LEAGUE_HISTORY = {
    # season_year: (n_teams, integration_factor, international_factor, pipeline_factor)
    # integration: reflects racial integration of NBA talent pool
    # international: fraction of international-born players (normalized 0-1 relative to 2020)
    # pipeline: college/youth pipeline development (normalized 0-1)
    1955: (8,  0.50, 0.05, 0.35),
    1960: (8,  0.62, 0.06, 0.40),
    1965: (10, 0.78, 0.07, 0.45),
    1970: (14, 0.90, 0.08, 0.55),
    1975: (18, 0.96, 0.10, 0.62),
    1980: (22, 0.98, 0.12, 0.70),
    1985: (23, 0.99, 0.15, 0.76),
    1990: (27, 0.99, 0.22, 0.82),
    1995: (29, 1.00, 0.32, 0.87),
    2000: (29, 1.00, 0.45, 0.91),
    2005: (30, 1.00, 0.60, 0.93),
    2010: (30, 1.00, 0.72, 0.95),
    2015: (30, 1.00, 0.80, 0.97),
    2020: (30, 1.00, 1.00, 1.00),
}


def get_player(name: str) -> dict:
    """Return career data dict for a player by name. Raises KeyError if not found."""
    return PLAYERS[name]


def get_league_tpd(era_year: int) -> float:
    """
    Return the Talent Pool Depth (TPD) multiplier for a given era year.
    Linearly interpolated between the anchor years in LEAGUE_HISTORY.
    TPD = log2(n_teams / 8) * integration * international * pipeline,
    normalised so TPD_2020 = 1.0.
    """
    import math

    years = sorted(LEAGUE_HISTORY.keys())

    # Clamp to known range
    if era_year <= years[0]:
        row = LEAGUE_HISTORY[years[0]]
    elif era_year >= years[-1]:
        row = LEAGUE_HISTORY[years[-1]]
    else:
        # Linear interpolation between bracketing years
        for i in range(len(years) - 1):
            y0, y1 = years[i], years[i + 1]
            if y0 <= era_year <= y1:
                t = (era_year - y0) / (y1 - y0)
                r0, r1 = LEAGUE_HISTORY[y0], LEAGUE_HISTORY[y1]
                row = tuple(r0[k] + t * (r1[k] - r0[k]) for k in range(4))
                break
        else:
            row = LEAGUE_HISTORY[years[-1]]

    n_teams, integ, intl, pipe = row
    raw = math.log2(max(n_teams, 8) / 8) * integ * intl * pipe

    # Normalise against 2020 baseline
    ref = LEAGUE_HISTORY[2020]
    ref_raw = math.log2(ref[0] / 8) * ref[1] * ref[2] * ref[3]

    if ref_raw == 0:
        return 1.0
    return raw / ref_raw


if __name__ == "__main__":
    print("=== Player Career Data ===")
    for name, data in PLAYERS.items():
        print(
            f"{name:25s}  PPG={data['ppg']:.1f}  BPM={data['bpm']:.1f}  "
            f"VORP={data['vorp']:.1f}  WS={data['win_shares']:.1f}  "
            f"Rings={data['championships']}"
        )

    print("\n=== League TPD by Era ===")
    for yr in [1960, 1970, 1980, 1990, 2000, 2010, 2020]:
        print(f"  {yr}: TPD = {get_league_tpd(yr):.4f}")
