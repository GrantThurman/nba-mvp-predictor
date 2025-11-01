import nba_api
import pandas as pd
import time
import os
import nba_api.stats.endpoints.leaguedashplayerstats as playerstats
import nba_api.stats.endpoints.leaguedashteamstats as teamstats

player_seasons_filepath = "player_seasons.csv"

if not os.path.exists(player_seasons_filepath):
    print("Could not find player seasons CSV")
    data = []
    for year in range(2000, 2025):
        season = f"{year}-{str(year+1)[2:]}"

        # Players
        player_df = playerstats.LeagueDashPlayerStats(season=season, per_mode_detailed="PerGame", league_id_nullable="00").get_data_frames()[0]
        time.sleep(3)
        player_df["SEASON"] = season
        player_df = player_df.rename(columns={"W_PCT": "PLAYER_W_PCT"})

        # Teams
        team_df = teamstats.LeagueDashTeamStats(season=season, league_id_nullable="00").get_data_frames()[0]
        time.sleep(3)
        team_df = team_df[["TEAM_ID", "TEAM_NAME", "W_PCT"]]
        team_df["SEASON"] = season
        team_df = team_df.rename(columns={"W_PCT": "TEAM_W_PCT"})

        # Merge dataframes
        season_df = pd.merge(player_df, team_df, on=["SEASON", "TEAM_ID"], how="left")
        data.append(season_df)

    player_seasons_df = pd.concat(data)
    player_seasons_df.to_csv("player_seasons.csv", index=False)
else:
    player_seasons_df = pd.read_csv(player_seasons_filepath)


# Merge MVP voting and winners
mvp_voting_df = pd.read_csv("mvp_voting.csv")
mvp_voting_df = mvp_voting_df[["PLAYER_NAME", "SEASON", "MVP_PCT_SHARE"]]
mvp_winners_df = pd.read_csv("mvp_winners.csv")
mvp_winners_df["IS_MVP"] = 1
mvp_df = pd.merge(mvp_voting_df, mvp_winners_df, on=["SEASON", "PLAYER_NAME"], how="left")

# Merge player data and MVP data
all_df = pd.merge(player_seasons_df, mvp_df, on=["SEASON", "PLAYER_NAME"], how="left")
all_df["IS_MVP"] = all_df["IS_MVP"].fillna(value=0)
all_df["MVP_PCT_SHARE"] = all_df["MVP_PCT_SHARE"].fillna(value=0)

# Create per minute stats
all_df["PTS_PER_MIN"] = all_df["PTS"] / all_df["MIN"]
all_df["AST_PER_MIN"] = all_df["AST"] / all_df["MIN"]
all_df["REB_PER_MIN"] = all_df["REB"] / all_df["MIN"]

# Create efficiency stat
all_df["FG_MISS"] = all_df["FGA"] - all_df["FGA"] * all_df["FG_PCT"]
all_df["FT_MISS"] = all_df["FTA"] - all_df["FTA"] * all_df["FT_PCT"]
all_df["EFFICIENCY"] = all_df["PTS"] + all_df["AST"] + all_df["REB"] + all_df["STL"] + all_df["BLK"] - all_df["FG_MISS"] - all_df["FT_MISS"] - all_df["TOV"]

# Remove rank columns to avoid multicollinearity
all_df = all_df.loc[:, ~all_df.columns.str.contains("RANK")]
# Remove other columns that cause multicollinearity
all_df.drop(axis="columns", labels=["W", "L", "FGM", "FG3M", "FTM", "OREB", "DREB", "DD2", "TD3"], inplace=True)
# Remove unnecessary columns
all_df.drop(axis="columns", labels=["AGE", "PF", "PFD", "TOV", "BLKA", "NBA_FANTASY_PTS", "WNBA_FANTASY_PTS", "TEAM_COUNT", "TEAM_ABBREVIATION", "TEAM_ID", "PLAYER_ID", "NICKNAME"], inplace=True)

all_df.to_csv("all_data.csv", index=False)