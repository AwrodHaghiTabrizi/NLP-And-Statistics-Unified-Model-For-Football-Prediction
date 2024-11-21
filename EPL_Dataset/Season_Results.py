import pandas as pd

_cached_df = None

def get_cached_data(filepath='Winning_Percentage.csv'):

    global _cached_df
    if _cached_df is None:
        _cached_df = pd.read_csv(filepath)
    
    return _cached_df

def get_last_season_result(season, team):
    
    winning_percentage_df = get_cached_data()

    start_year, end_year = map(int, season.split('-'))
    previous_season = f"{start_year - 1}-{end_year - 1}"

    try:
        # Locate the row corresponding to the previous season
        previous_season_data = winning_percentage_df.loc[winning_percentage_df['Season'] == previous_season]
        if not previous_season_data.empty:
            result = previous_season_data[team].values[0]
            return result
        else:
            raise KeyError
    except KeyError:
        return f"Data for season {previous_season} or team {team} is not available."
    