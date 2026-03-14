# Part 1: Michael Jordan, LeBron James, Kareem Abdul-Jabbar, Tim Duncan, Nikola Jokic
# All data sourced from Basketball Reference (basketball-reference.com)
# Pre-1974 steals/blocks estimated (marked with # EST)

MICHAEL_JORDAN = {
    "name": "Michael Jordan",
    "seasons": {"start_year": 1985, "end_year": 2003},
    "games_played": 1072,
    "career_span": 15,  # actual seasons played (skipped 93-94, 94-95 partial, 01-02, 02-03)
    "position": "SG",
    "active": False,

    # Career regular-season stats (Basketball Reference)
    "ppg": 30.1,
    "rpg": 6.2,
    "apg": 5.3,
    "spg": 2.35,
    "bpg": 0.83,
    "fg_pct": 0.497,
    "ft_pct": 0.835,
    "ts_pct": 0.570,
    "usage_rate": 33.3,

    # Advanced metrics (Basketball Reference)
    "per": 27.91,
    "bpm": 9.22,
    "vorp": 64.2,
    "ws": 214.0,
    "ws_48": 0.250,
    "dbpm": 3.03,
    "dws": 54.9,

    # Peak stats — best 7 consecutive seasons (1988–1993 + 1996 approximation)
    "peak_bpm": 11.4,
    "peak_per": 31.2,
    "peak_ws48": 0.312,
    "peak_window": "1988-1993, 1996",

    # Playoff career stats
    "po_ppg": 33.4,
    "po_per": 28.6,
    "po_bpm": 9.4,
    "po_vorp": 24.6,
    "po_games": 179,

    # Accolades
    "mvps": 5,
    "finals_mvps": 6,
    "championships": 6,
    "finals_record": (6, 0),
    "all_nba": 11,       # All-NBA First Team selections
    "all_defensive": 9,  # All-Defensive First Team
    "all_star": 14,
    "dpoy": 1,

    # Team context
    "on_off_diff": 10.5,   # estimated net rating differential on vs off
    "delta_w": 18.0,       # estimated team win delta

    # Era context
    "league_teams_avg": 27.0,
    "era_avg_ts": 0.531,
    "era_avg_pace": 91.8,

    # Season-by-season
    "seasons_data": [
        {"year": 1985, "age": 21, "games": 82, "mpg": 38.3, "ppg": 28.2, "bpm": 7.9,  "per": 22.7, "ws": 9.7,  "ts_pct": 0.531, "league_avg_ts": 0.524, "league_teams": 23, "team_wins": 38, "made_playoffs": True,  "playoff_round_reached": 1},
        {"year": 1986, "age": 22, "games": 18, "mpg": 25.1, "ppg": 22.7, "bpm": 7.5,  "per": 22.9, "ws": 2.6,  "ts_pct": 0.515, "league_avg_ts": 0.521, "league_teams": 23, "team_wins": 30, "made_playoffs": True,  "playoff_round_reached": 1},
        {"year": 1987, "age": 23, "games": 82, "mpg": 40.0, "ppg": 37.1, "bpm": 10.6, "per": 29.8, "ws": 17.4, "ts_pct": 0.557, "league_avg_ts": 0.524, "league_teams": 23, "team_wins": 40, "made_playoffs": True,  "playoff_round_reached": 1},
        {"year": 1988, "age": 24, "games": 82, "mpg": 40.4, "ppg": 35.0, "bpm": 10.3, "per": 31.7, "ws": 21.2, "ts_pct": 0.567, "league_avg_ts": 0.527, "league_teams": 23, "team_wins": 50, "made_playoffs": True,  "playoff_round_reached": 2},
        {"year": 1989, "age": 25, "games": 81, "mpg": 40.2, "ppg": 32.5, "bpm": 9.8,  "per": 30.1, "ws": 19.0, "ts_pct": 0.556, "league_avg_ts": 0.532, "league_teams": 25, "team_wins": 47, "made_playoffs": True,  "playoff_round_reached": 3},
        {"year": 1990, "age": 26, "games": 82, "mpg": 39.0, "ppg": 33.6, "bpm": 10.4, "per": 31.2, "ws": 20.4, "ts_pct": 0.560, "league_avg_ts": 0.532, "league_teams": 27, "team_wins": 55, "made_playoffs": True,  "playoff_round_reached": 3},
        {"year": 1991, "age": 27, "games": 82, "mpg": 37.0, "ppg": 31.5, "bpm": 10.1, "per": 29.2, "ws": 18.4, "ts_pct": 0.563, "league_avg_ts": 0.534, "league_teams": 27, "team_wins": 61, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 1992, "age": 28, "games": 80, "mpg": 38.8, "ppg": 30.1, "bpm": 9.9,  "per": 27.8, "ws": 17.3, "ts_pct": 0.554, "league_avg_ts": 0.534, "league_teams": 27, "team_wins": 67, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 1993, "age": 29, "games": 78, "mpg": 39.3, "ppg": 32.6, "bpm": 10.2, "per": 29.7, "ws": 17.4, "ts_pct": 0.565, "league_avg_ts": 0.534, "league_teams": 27, "team_wins": 57, "made_playoffs": True,  "playoff_round_reached": 4},
        # 1994: retired (baseball)
        {"year": 1995, "age": 31, "games": 17, "mpg": 39.3, "ppg": 26.9, "bpm": 6.5,  "per": 23.0, "ws": 2.8,  "ts_pct": 0.511, "league_avg_ts": 0.531, "league_teams": 29, "team_wins": 47, "made_playoffs": True,  "playoff_round_reached": 2},
        {"year": 1996, "age": 32, "games": 82, "mpg": 37.7, "ppg": 30.4, "bpm": 9.8,  "per": 27.8, "ws": 16.9, "ts_pct": 0.564, "league_avg_ts": 0.534, "league_teams": 29, "team_wins": 72, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 1997, "age": 33, "games": 82, "mpg": 37.9, "ppg": 29.6, "bpm": 9.1,  "per": 27.5, "ws": 15.9, "ts_pct": 0.566, "league_avg_ts": 0.536, "league_teams": 29, "team_wins": 69, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 1998, "age": 34, "games": 82, "mpg": 38.8, "ppg": 28.7, "bpm": 8.8,  "per": 27.2, "ws": 14.7, "ts_pct": 0.540, "league_avg_ts": 0.534, "league_teams": 29, "team_wins": 62, "made_playoffs": True,  "playoff_round_reached": 4},
        # 1999-2001: retired/Wizards front office
        {"year": 2002, "age": 38, "games": 60, "mpg": 34.9, "ppg": 22.9, "bpm": 1.7,  "per": 17.4, "ws": 3.2,  "ts_pct": 0.490, "league_avg_ts": 0.528, "league_teams": 29, "team_wins": 37, "made_playoffs": False, "playoff_round_reached": 0},
        {"year": 2003, "age": 39, "games": 82, "mpg": 37.0, "ppg": 20.0, "bpm": 0.5,  "per": 15.1, "ws": 4.6,  "ts_pct": 0.474, "league_avg_ts": 0.528, "league_teams": 29, "team_wins": 37, "made_playoffs": False, "playoff_round_reached": 0},
    ],
}

LEBRON_JAMES = {
    "name": "LeBron James",
    "seasons": {"start_year": 2004, "end_year": 2024},
    "games_played": 1492,
    "career_span": 21,
    "position": "SF/PF",
    "active": True,  # still active as of 2024-25

    "ppg": 27.1,
    "rpg": 7.5,
    "apg": 7.4,
    "spg": 1.58,
    "bpg": 0.77,
    "fg_pct": 0.504,
    "ft_pct": 0.735,
    "ts_pct": 0.581,
    "usage_rate": 31.5,

    "per": 27.34,
    "bpm": 8.90,
    "vorp": 152.3,   # all-time record
    "ws": 266.4,     # all-time record
    "ws_48": 0.233,
    "dbpm": 1.80,
    "dws": 52.6,

    "peak_bpm": 10.6,
    "peak_per": 30.8,
    "peak_ws48": 0.290,
    "peak_window": "2009-2013, 2016-2018",

    "po_ppg": 28.6,
    "po_per": 28.5,
    "po_bpm": 8.1,
    "po_vorp": 38.9,
    "po_games": 287,

    "mvps": 4,
    "finals_mvps": 4,
    "championships": 4,
    "finals_record": (4, 6),
    "all_nba": 13,
    "all_defensive": 6,
    "all_star": 20,
    "dpoy": 0,

    "on_off_diff": 8.2,
    "delta_w": 15.5,

    "league_teams_avg": 29.8,
    "era_avg_ts": 0.545,
    "era_avg_pace": 96.4,

    "seasons_data": [
        {"year": 2004, "age": 19, "games": 79, "mpg": 39.5, "ppg": 20.9, "bpm": 3.0,  "per": 16.6, "ws": 6.1,  "ts_pct": 0.501, "league_avg_ts": 0.527, "league_teams": 29, "team_wins": 35, "made_playoffs": False, "playoff_round_reached": 0},
        {"year": 2005, "age": 20, "games": 80, "mpg": 42.4, "ppg": 27.2, "bpm": 5.7,  "per": 22.5, "ws": 11.4, "ts_pct": 0.546, "league_avg_ts": 0.529, "league_teams": 29, "team_wins": 42, "made_playoffs": True,  "playoff_round_reached": 1},
        {"year": 2006, "age": 21, "games": 79, "mpg": 42.5, "ppg": 31.4, "bpm": 7.7,  "per": 25.7, "ws": 14.8, "ts_pct": 0.567, "league_avg_ts": 0.530, "league_teams": 30, "team_wins": 50, "made_playoffs": True,  "playoff_round_reached": 2},
        {"year": 2007, "age": 22, "games": 78, "mpg": 40.9, "ppg": 27.3, "bpm": 7.2,  "per": 25.5, "ws": 13.4, "ts_pct": 0.553, "league_avg_ts": 0.530, "league_teams": 30, "team_wins": 50, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 2008, "age": 23, "games": 75, "mpg": 40.4, "ppg": 30.0, "bpm": 9.0,  "per": 27.9, "ws": 15.7, "ts_pct": 0.578, "league_avg_ts": 0.532, "league_teams": 30, "team_wins": 45, "made_playoffs": True,  "playoff_round_reached": 2},
        {"year": 2009, "age": 24, "games": 81, "mpg": 37.7, "ppg": 28.4, "bpm": 10.5, "per": 31.7, "ws": 20.3, "ts_pct": 0.591, "league_avg_ts": 0.534, "league_teams": 30, "team_wins": 66, "made_playoffs": True,  "playoff_round_reached": 3},
        {"year": 2010, "age": 25, "games": 76, "mpg": 39.0, "ppg": 29.7, "bpm": 10.4, "per": 31.1, "ws": 18.1, "ts_pct": 0.602, "league_avg_ts": 0.535, "league_teams": 30, "team_wins": 61, "made_playoffs": True,  "playoff_round_reached": 3},
        {"year": 2011, "age": 26, "games": 79, "mpg": 38.8, "ppg": 26.7, "bpm": 8.7,  "per": 27.3, "ws": 14.7, "ts_pct": 0.602, "league_avg_ts": 0.535, "league_teams": 30, "team_wins": 58, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 2012, "age": 27, "games": 62, "mpg": 37.5, "ppg": 27.1, "bpm": 9.5,  "per": 30.7, "ws": 14.0, "ts_pct": 0.605, "league_avg_ts": 0.533, "league_teams": 30, "team_wins": 46, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 2013, "age": 28, "games": 76, "mpg": 37.9, "ppg": 26.8, "bpm": 9.5,  "per": 30.0, "ws": 17.1, "ts_pct": 0.603, "league_avg_ts": 0.534, "league_teams": 30, "team_wins": 66, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 2014, "age": 29, "games": 77, "mpg": 37.9, "ppg": 27.1, "bpm": 8.4,  "per": 27.6, "ws": 15.5, "ts_pct": 0.598, "league_avg_ts": 0.534, "league_teams": 30, "team_wins": 54, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 2015, "age": 30, "games": 69, "mpg": 36.1, "ppg": 25.3, "bpm": 7.1,  "per": 24.9, "ws": 10.8, "ts_pct": 0.580, "league_avg_ts": 0.535, "league_teams": 30, "team_wins": 53, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 2016, "age": 31, "games": 76, "mpg": 35.6, "ppg": 25.3, "bpm": 8.9,  "per": 26.2, "ws": 14.3, "ts_pct": 0.575, "league_avg_ts": 0.536, "league_teams": 30, "team_wins": 57, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 2017, "age": 32, "games": 74, "mpg": 37.8, "ppg": 26.4, "bpm": 8.2,  "per": 25.9, "ws": 12.6, "ts_pct": 0.619, "league_avg_ts": 0.543, "league_teams": 30, "team_wins": 51, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 2018, "age": 33, "games": 82, "mpg": 36.9, "ppg": 27.5, "bpm": 8.6,  "per": 28.0, "ws": 15.3, "ts_pct": 0.618, "league_avg_ts": 0.547, "league_teams": 30, "team_wins": 50, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 2019, "age": 34, "games": 55, "mpg": 35.2, "ppg": 27.4, "bpm": 6.3,  "per": 25.6, "ws": 7.3,  "ts_pct": 0.591, "league_avg_ts": 0.551, "league_teams": 30, "team_wins": 37, "made_playoffs": False, "playoff_round_reached": 0},
        {"year": 2020, "age": 35, "games": 67, "mpg": 34.6, "ppg": 25.3, "bpm": 6.7,  "per": 25.0, "ws": 10.4, "ts_pct": 0.582, "league_avg_ts": 0.556, "league_teams": 30, "team_wins": 52, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 2021, "age": 36, "games": 45, "mpg": 33.4, "ppg": 25.0, "bpm": 5.9,  "per": 24.3, "ws": 5.6,  "ts_pct": 0.588, "league_avg_ts": 0.561, "league_teams": 30, "team_wins": 42, "made_playoffs": True,  "playoff_round_reached": 1},
        {"year": 2022, "age": 37, "games": 56, "mpg": 37.2, "ppg": 30.3, "bpm": 7.4,  "per": 26.6, "ws": 8.4,  "ts_pct": 0.589, "league_avg_ts": 0.563, "league_teams": 30, "team_wins": 33, "made_playoffs": False, "playoff_round_reached": 0},
        {"year": 2023, "age": 38, "games": 55, "mpg": 35.5, "ppg": 28.9, "bpm": 6.6,  "per": 24.4, "ws": 6.7,  "ts_pct": 0.599, "league_avg_ts": 0.563, "league_teams": 30, "team_wins": 43, "made_playoffs": True,  "playoff_round_reached": 2},
        {"year": 2024, "age": 39, "games": 71, "mpg": 35.3, "ppg": 25.7, "bpm": 5.2,  "per": 22.8, "ws": 7.2,  "ts_pct": 0.594, "league_avg_ts": 0.574, "league_teams": 30, "team_wins": 47, "made_playoffs": True,  "playoff_round_reached": 2},
    ],
}

KAREEM_ABDUL_JABBAR = {
    "name": "Kareem Abdul-Jabbar",
    "seasons": {"start_year": 1970, "end_year": 1989},
    "games_played": 1560,
    "career_span": 20,
    "position": "C",
    "active": False,

    "ppg": 24.6,
    "rpg": 11.2,
    "apg": 3.6,
    "spg": 0.89,   # EST: steals not tracked pre-1974
    "bpg": 2.60,
    "fg_pct": 0.559,
    "ft_pct": 0.721,
    "ts_pct": 0.579,
    "usage_rate": 26.5,

    "per": 24.58,
    "bpm": 9.07,
    "vorp": 98.3,
    "ws": 273.4,   # all-time record before LeBron surpassed
    "ws_48": 0.227,
    "dbpm": 3.10,
    "dws": 66.4,

    "peak_bpm": 12.0,
    "peak_per": 31.6,
    "peak_ws48": 0.310,
    "peak_window": "1972-1977",

    "po_ppg": 24.3,
    "po_per": 24.5,
    "po_bpm": 8.3,
    "po_vorp": 22.7,
    "po_games": 237,

    "mvps": 6,
    "finals_mvps": 2,
    "championships": 6,
    "finals_record": (6, 2),
    "all_nba": 10,
    "all_defensive": 11,
    "all_star": 19,
    "dpoy": 0,  # DPOY award started 1983; won it 0 times

    "on_off_diff": 7.9,
    "delta_w": 14.0,

    "league_teams_avg": 21.5,
    "era_avg_ts": 0.507,
    "era_avg_pace": 103.5,

    "seasons_data": [
        {"year": 1970, "age": 22, "games": 82, "mpg": 43.2, "ppg": 28.8, "bpm": 10.5, "per": 28.4, "ws": 18.0, "ts_pct": 0.549, "league_avg_ts": 0.494, "league_teams": 14, "team_wins": 56, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 1971, "age": 23, "games": 82, "mpg": 45.5, "ppg": 31.7, "bpm": 12.3, "per": 31.8, "ws": 22.0, "ts_pct": 0.580, "league_avg_ts": 0.496, "league_teams": 17, "team_wins": 66, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 1972, "age": 24, "games": 81, "mpg": 44.3, "ppg": 34.8, "bpm": 12.0, "per": 31.5, "ws": 23.3, "ts_pct": 0.598, "league_avg_ts": 0.498, "league_teams": 17, "team_wins": 63, "made_playoffs": True,  "playoff_round_reached": 3},
        {"year": 1973, "age": 25, "games": 76, "mpg": 40.0, "ppg": 30.2, "bpm": 11.8, "per": 31.5, "ws": 19.0, "ts_pct": 0.583, "league_avg_ts": 0.498, "league_teams": 17, "team_wins": 60, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 1974, "age": 26, "games": 81, "mpg": 43.1, "ppg": 27.0, "bpm": 11.0, "per": 29.5, "ws": 20.3, "ts_pct": 0.572, "league_avg_ts": 0.501, "league_teams": 17, "team_wins": 59, "made_playoffs": True,  "playoff_round_reached": 3},
        {"year": 1975, "age": 27, "games": 65, "mpg": 36.8, "ppg": 30.0, "bpm": 11.5, "per": 31.8, "ws": 14.1, "ts_pct": 0.587, "league_avg_ts": 0.497, "league_teams": 18, "team_wins": 30, "made_playoffs": False, "playoff_round_reached": 0},
        {"year": 1976, "age": 28, "games": 82, "mpg": 43.3, "ppg": 27.7, "bpm": 10.2, "per": 29.4, "ws": 20.4, "ts_pct": 0.575, "league_avg_ts": 0.499, "league_teams": 18, "team_wins": 40, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 1977, "age": 29, "games": 82, "mpg": 39.3, "ppg": 26.2, "bpm": 9.3,  "per": 27.7, "ws": 17.0, "ts_pct": 0.558, "league_avg_ts": 0.499, "league_teams": 22, "team_wins": 53, "made_playoffs": True,  "playoff_round_reached": 3},
        {"year": 1978, "age": 30, "games": 62, "mpg": 36.7, "ppg": 25.8, "bpm": 8.8,  "per": 26.4, "ws": 11.5, "ts_pct": 0.554, "league_avg_ts": 0.505, "league_teams": 22, "team_wins": 45, "made_playoffs": True,  "playoff_round_reached": 2},
        {"year": 1979, "age": 31, "games": 80, "mpg": 38.8, "ppg": 23.8, "bpm": 8.5,  "per": 25.0, "ws": 15.3, "ts_pct": 0.553, "league_avg_ts": 0.509, "league_teams": 22, "team_wins": 47, "made_playoffs": True,  "playoff_round_reached": 2},
        {"year": 1980, "age": 32, "games": 82, "mpg": 36.3, "ppg": 24.8, "bpm": 8.0,  "per": 24.6, "ws": 14.5, "ts_pct": 0.556, "league_avg_ts": 0.511, "league_teams": 22, "team_wins": 60, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 1981, "age": 33, "games": 80, "mpg": 36.0, "ppg": 26.2, "bpm": 8.2,  "per": 24.7, "ws": 14.4, "ts_pct": 0.560, "league_avg_ts": 0.511, "league_teams": 23, "team_wins": 54, "made_playoffs": True,  "playoff_round_reached": 3},
        {"year": 1982, "age": 34, "games": 76, "mpg": 35.4, "ppg": 23.9, "bpm": 7.8,  "per": 23.6, "ws": 12.6, "ts_pct": 0.558, "league_avg_ts": 0.516, "league_teams": 23, "team_wins": 57, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 1983, "age": 35, "games": 79, "mpg": 34.8, "ppg": 21.8, "bpm": 7.0,  "per": 22.3, "ws": 12.9, "ts_pct": 0.556, "league_avg_ts": 0.520, "league_teams": 23, "team_wins": 58, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 1984, "age": 36, "games": 80, "mpg": 33.8, "ppg": 17.5, "bpm": 5.4,  "per": 18.9, "ws": 9.3,  "ts_pct": 0.542, "league_avg_ts": 0.524, "league_teams": 23, "team_wins": 54, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 1985, "age": 37, "games": 79, "mpg": 32.9, "ppg": 22.0, "bpm": 6.2,  "per": 21.2, "ws": 11.0, "ts_pct": 0.566, "league_avg_ts": 0.524, "league_teams": 23, "team_wins": 62, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 1986, "age": 38, "games": 79, "mpg": 31.7, "ppg": 23.4, "bpm": 5.8,  "per": 20.6, "ws": 9.9,  "ts_pct": 0.571, "league_avg_ts": 0.521, "league_teams": 23, "team_wins": 65, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 1987, "age": 39, "games": 78, "mpg": 30.8, "ppg": 17.5, "bpm": 3.9,  "per": 17.8, "ws": 8.2,  "ts_pct": 0.540, "league_avg_ts": 0.524, "league_teams": 23, "team_wins": 65, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 1988, "age": 40, "games": 80, "mpg": 29.6, "ppg": 14.6, "bpm": 2.8,  "per": 15.8, "ws": 6.4,  "ts_pct": 0.529, "league_avg_ts": 0.527, "league_teams": 23, "team_wins": 62, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 1989, "age": 41, "games": 74, "mpg": 22.8, "ppg": 10.1, "bpm": -0.1, "per": 12.6, "ws": 3.1,  "ts_pct": 0.506, "league_avg_ts": 0.532, "league_teams": 25, "team_wins": 57, "made_playoffs": True,  "playoff_round_reached": 4},
    ],
}

TIM_DUNCAN = {
    "name": "Tim Duncan",
    "seasons": {"start_year": 1998, "end_year": 2016},
    "games_played": 1392,
    "career_span": 19,
    "position": "PF/C",
    "active": False,

    "ppg": 19.0,
    "rpg": 10.8,
    "apg": 3.0,
    "spg": 0.71,
    "bpg": 2.22,
    "fg_pct": 0.506,
    "ft_pct": 0.696,
    "ts_pct": 0.540,
    "usage_rate": 24.6,

    "per": 24.22,
    "bpm": 8.19,
    "vorp": 101.4,
    "ws": 206.4,
    "ws_48": 0.249,
    "dbpm": 3.63,
    "dws": 73.1,

    "peak_bpm": 10.2,
    "peak_per": 27.9,
    "peak_ws48": 0.299,
    "peak_window": "1999-2005",

    "po_ppg": 20.6,
    "po_per": 24.5,
    "po_bpm": 8.3,
    "po_vorp": 27.1,
    "po_games": 251,

    "mvps": 2,
    "finals_mvps": 3,
    "championships": 5,
    "finals_record": (5, 1),
    "all_nba": 10,
    "all_defensive": 15,
    "all_star": 15,
    "dpoy": 0,

    "on_off_diff": 9.1,
    "delta_w": 16.0,

    "league_teams_avg": 29.2,
    "era_avg_ts": 0.540,
    "era_avg_pace": 92.5,

    "seasons_data": [
        {"year": 1998, "age": 21, "games": 82, "mpg": 39.4, "ppg": 21.1, "bpm": 7.9,  "per": 23.0, "ws": 14.0, "ts_pct": 0.531, "league_avg_ts": 0.518, "league_teams": 29, "team_wins": 56, "made_playoffs": True,  "playoff_round_reached": 2},
        {"year": 1999, "age": 22, "games": 50, "mpg": 38.9, "ppg": 23.2, "bpm": 9.0,  "per": 25.9, "ws": 11.0, "ts_pct": 0.543, "league_avg_ts": 0.513, "league_teams": 29, "team_wins": 37, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 2000, "age": 23, "games": 74, "mpg": 40.0, "ppg": 23.2, "bpm": 9.3,  "per": 26.4, "ws": 14.5, "ts_pct": 0.528, "league_avg_ts": 0.521, "league_teams": 29, "team_wins": 53, "made_playoffs": True,  "playoff_round_reached": 2},
        {"year": 2001, "age": 24, "games": 82, "mpg": 40.6, "ppg": 22.9, "bpm": 10.0, "per": 27.8, "ws": 18.0, "ts_pct": 0.524, "league_avg_ts": 0.521, "league_teams": 29, "team_wins": 58, "made_playoffs": True,  "playoff_round_reached": 3},
        {"year": 2002, "age": 25, "games": 82, "mpg": 40.6, "ppg": 25.5, "bpm": 10.2, "per": 27.9, "ws": 19.1, "ts_pct": 0.547, "league_avg_ts": 0.528, "league_teams": 29, "team_wins": 58, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 2003, "age": 26, "games": 81, "mpg": 39.3, "ppg": 23.3, "bpm": 9.8,  "per": 26.3, "ws": 16.7, "ts_pct": 0.533, "league_avg_ts": 0.528, "league_teams": 29, "team_wins": 60, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 2004, "age": 27, "games": 69, "mpg": 36.5, "ppg": 22.3, "bpm": 9.0,  "per": 24.9, "ws": 12.6, "ts_pct": 0.527, "league_avg_ts": 0.527, "league_teams": 29, "team_wins": 57, "made_playoffs": True,  "playoff_round_reached": 3},
        {"year": 2005, "age": 28, "games": 66, "mpg": 35.4, "ppg": 20.3, "bpm": 8.8,  "per": 24.2, "ws": 11.3, "ts_pct": 0.528, "league_avg_ts": 0.529, "league_teams": 29, "team_wins": 59, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 2006, "age": 29, "games": 80, "mpg": 36.0, "ppg": 18.6, "bpm": 8.0,  "per": 22.7, "ws": 13.1, "ts_pct": 0.527, "league_avg_ts": 0.530, "league_teams": 30, "team_wins": 63, "made_playoffs": True,  "playoff_round_reached": 2},
        {"year": 2007, "age": 30, "games": 80, "mpg": 34.9, "ppg": 20.0, "bpm": 7.6,  "per": 22.3, "ws": 12.6, "ts_pct": 0.519, "league_avg_ts": 0.530, "league_teams": 30, "team_wins": 58, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 2008, "age": 31, "games": 78, "mpg": 34.5, "ppg": 19.3, "bpm": 7.3,  "per": 22.8, "ws": 12.7, "ts_pct": 0.529, "league_avg_ts": 0.532, "league_teams": 30, "team_wins": 56, "made_playoffs": True,  "playoff_round_reached": 2},
        {"year": 2009, "age": 32, "games": 75, "mpg": 33.0, "ppg": 15.6, "bpm": 5.7,  "per": 19.4, "ws": 9.6,  "ts_pct": 0.517, "league_avg_ts": 0.534, "league_teams": 30, "team_wins": 54, "made_playoffs": True,  "playoff_round_reached": 2},
        {"year": 2010, "age": 33, "games": 78, "mpg": 31.7, "ppg": 13.6, "bpm": 5.0,  "per": 18.3, "ws": 9.3,  "ts_pct": 0.526, "league_avg_ts": 0.535, "league_teams": 30, "team_wins": 50, "made_playoffs": True,  "playoff_round_reached": 2},
        {"year": 2011, "age": 34, "games": 76, "mpg": 30.0, "ppg": 13.3, "bpm": 4.8,  "per": 18.1, "ws": 8.6,  "ts_pct": 0.514, "league_avg_ts": 0.535, "league_teams": 30, "team_wins": 61, "made_playoffs": True,  "playoff_round_reached": 2},
        {"year": 2012, "age": 35, "games": 58, "mpg": 30.0, "ppg": 15.6, "bpm": 5.4,  "per": 19.7, "ws": 7.1,  "ts_pct": 0.535, "league_avg_ts": 0.533, "league_teams": 30, "team_wins": 50, "made_playoffs": True,  "playoff_round_reached": 2},
        {"year": 2013, "age": 36, "games": 69, "mpg": 30.2, "ppg": 16.9, "bpm": 5.7,  "per": 20.3, "ws": 9.5,  "ts_pct": 0.549, "league_avg_ts": 0.534, "league_teams": 30, "team_wins": 58, "made_playoffs": True,  "playoff_round_reached": 3},
        {"year": 2014, "age": 37, "games": 77, "mpg": 30.9, "ppg": 15.1, "bpm": 4.6,  "per": 18.9, "ws": 8.5,  "ts_pct": 0.529, "league_avg_ts": 0.534, "league_teams": 30, "team_wins": 62, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 2015, "age": 38, "games": 77, "mpg": 28.0, "ppg": 13.9, "bpm": 3.6,  "per": 17.8, "ws": 7.5,  "ts_pct": 0.546, "league_avg_ts": 0.535, "league_teams": 30, "team_wins": 55, "made_playoffs": True,  "playoff_round_reached": 2},
        {"year": 2016, "age": 39, "games": 61, "mpg": 25.8, "ppg": 8.6,  "bpm": 1.2,  "per": 12.7, "ws": 2.6,  "ts_pct": 0.483, "league_avg_ts": 0.536, "league_teams": 30, "team_wins": 67, "made_playoffs": True,  "playoff_round_reached": 3},
    ],
}

NIKOLA_JOKIC = {
    "name": "Nikola Jokic",
    "seasons": {"start_year": 2016, "end_year": 2024},
    "games_played": 658,
    "career_span": 9,
    "position": "C",
    "active": True,

    "ppg": 22.0,
    "rpg": 11.1,
    "apg": 6.5,
    "spg": 1.32,
    "bpg": 0.71,
    "fg_pct": 0.573,
    "ft_pct": 0.826,
    "ts_pct": 0.641,
    "usage_rate": 28.3,

    "per": 31.48,  # highest ever per BBRef through 2024
    "bpm": 11.82,
    "vorp": 74.5,
    "ws": 122.1,
    "ws_48": 0.301,
    "dbpm": 1.42,
    "dws": 20.1,

    "peak_bpm": 13.7,
    "peak_per": 35.3,
    "peak_ws48": 0.351,
    "peak_window": "2021-2024",

    "po_ppg": 26.2,
    "po_per": 31.6,
    "po_bpm": 12.1,
    "po_vorp": 16.4,
    "po_games": 92,

    "mvps": 3,
    "finals_mvps": 1,
    "championships": 1,
    "finals_record": (1, 0),
    "all_nba": 7,
    "all_defensive": 0,
    "all_star": 7,
    "dpoy": 0,

    "on_off_diff": 13.5,
    "delta_w": 19.0,

    "league_teams_avg": 30.0,
    "era_avg_ts": 0.558,
    "era_avg_pace": 99.7,

    "seasons_data": [
        {"year": 2016, "age": 20, "games": 80, "mpg": 21.7, "ppg": 10.0, "bpm": 4.2,  "per": 17.6, "ws": 6.4,  "ts_pct": 0.567, "league_avg_ts": 0.536, "league_teams": 30, "team_wins": 33, "made_playoffs": False, "playoff_round_reached": 0},
        {"year": 2017, "age": 21, "games": 73, "mpg": 27.8, "ppg": 16.7, "bpm": 6.6,  "per": 21.2, "ws": 9.5,  "ts_pct": 0.593, "league_avg_ts": 0.543, "league_teams": 30, "team_wins": 40, "made_playoffs": True,  "playoff_round_reached": 1},
        {"year": 2018, "age": 22, "games": 75, "mpg": 32.0, "ppg": 18.5, "bpm": 7.8,  "per": 24.4, "ws": 12.8, "ts_pct": 0.611, "league_avg_ts": 0.547, "league_teams": 30, "team_wins": 46, "made_playoffs": True,  "playoff_round_reached": 1},
        {"year": 2019, "age": 23, "games": 80, "mpg": 31.9, "ppg": 20.2, "bpm": 9.0,  "per": 26.3, "ws": 15.0, "ts_pct": 0.610, "league_avg_ts": 0.551, "league_teams": 30, "team_wins": 54, "made_playoffs": True,  "playoff_round_reached": 2},
        {"year": 2020, "age": 24, "games": 73, "mpg": 32.0, "ppg": 20.2, "bpm": 8.5,  "per": 26.1, "ws": 12.7, "ts_pct": 0.616, "league_avg_ts": 0.556, "league_teams": 30, "team_wins": 46, "made_playoffs": True,  "playoff_round_reached": 1},
        {"year": 2021, "age": 25, "games": 72, "mpg": 34.0, "ppg": 26.4, "bpm": 12.5, "per": 32.4, "ws": 18.3, "ts_pct": 0.640, "league_avg_ts": 0.561, "league_teams": 30, "team_wins": 47, "made_playoffs": True,  "playoff_round_reached": 3},
        {"year": 2022, "age": 26, "games": 74, "mpg": 33.5, "ppg": 27.1, "bpm": 13.7, "per": 35.3, "ws": 19.5, "ts_pct": 0.661, "league_avg_ts": 0.563, "league_teams": 30, "team_wins": 48, "made_playoffs": True,  "playoff_round_reached": 2},
        {"year": 2023, "age": 27, "games": 69, "mpg": 33.7, "ppg": 24.5, "bpm": 12.0, "per": 30.3, "ws": 14.6, "ts_pct": 0.652, "league_avg_ts": 0.563, "league_teams": 30, "team_wins": 53, "made_playoffs": True,  "playoff_round_reached": 4},
        {"year": 2024, "age": 28, "games": 79, "mpg": 34.6, "ppg": 26.4, "bpm": 13.0, "per": 31.5, "ws": 17.5, "ts_pct": 0.640, "league_avg_ts": 0.574, "league_teams": 30, "team_wins": 57, "made_playoffs": True,  "playoff_round_reached": 2},
    ],
}
