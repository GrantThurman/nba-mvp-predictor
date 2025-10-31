import nba_api
import pandas as pd
import time
import nba_api.stats.endpoints.leaguedashplayerstats as playerstats
import nba_api.stats.endpoints.leaguedashteamstats as teamstats


data = []
for year in range(2004, 2025):
    season = f"{year}-{str(year+1)[2:]}"

    # Players
    player_df = playerstats.LeagueDashPlayerStats(season=season, per_mode_detailed="PerGame", league_id_nullable="00").get_data_frames()[0]
    time.sleep(2)
    player_df["SEASON"] = season

    # Teams
    team_df = teamstats.LeagueDashTeamStats(season=season, league_id_nullable="00").get_data_frames()[0]
    team_df = team_df[["TEAM_ID", "TEAM_NAME", "W_PCT"]]
    team_df["SEASON"] = season

    # Merge dataframes
    season_df = pd.merge(player_df, team_df, on=["SEASON", "TEAM_ID"], how="left")
    data.append(season_df)

all_seasons_df = pd.concat(data)

# Merge MVP winners
mvp_winners_df = pd.read_csv("mvp_winners.csv")
mvp_winners_df["IS_MVP"] = 1
all_df = pd.merge(all_seasons_df, mvp_winners_df, on=["SEASON", "PLAYER_NAME"], how="left")
all_df["IS_MVP"].fillna(0)

# Create CSV file
all_seasons_df.to_csv("nba_player_stats.csv", index=False)