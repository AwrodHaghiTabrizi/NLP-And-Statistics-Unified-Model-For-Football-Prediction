import pandas as pd 

df = pd.read_csv('Original_Dataset.csv', encoding='latin1')

# Ensure the first column is treated as datetime
df.iloc[:, 1] = pd.to_datetime(df.iloc[:, 1], errors='coerce')

# Filter rows where the first column is before 2010-01-01
df_1218 = df[(df.iloc[:, 1] >= '2010-08-01') & (df.iloc[:, 1] <= '2020-06-01')]
df_1218 = df_1218.reset_index(drop=True)
# filtered_df.to_csv('12_19.csv', index=False)

# Extract all unique team names from both HomeTeam and AwayTeam columns
teams = pd.unique(df[['HomeTeam', 'AwayTeam']].values.ravel('K'))

# Create a dictionary to track wins and total matches for each team and season
team_stats = {}

# Iterate through the rows and count wins and total matches for each team
for _, row in df_1218.iterrows():
    season = row['Season']
    home_team = row['HomeTeam']
    away_team = row['AwayTeam']
    result = row['FTR']
    
    # Initialize season in team_stats if not already present
    if season not in team_stats:
        team_stats[season] = {team: {'Wins': 0, 'Matches': 0} for team in teams}
    
    # Increment matches played for both teams
    team_stats[season][home_team]['Matches'] += 1
    team_stats[season][away_team]['Matches'] += 1

    # Determine the winner and increment the win count
    if result == 'H':
        team_stats[season][home_team]['Wins'] += 1
    elif result == 'A':
        team_stats[season][away_team]['Wins'] += 1

# Create a DataFrame with seasons as rows and teams as columns with winning percentages
winning_percentage_data = {}

for season, teams_data in team_stats.items():
    winning_percentage_data[season] = {}
    for team, stats in teams_data.items():
        matches = stats['Matches']
        wins = stats['Wins']
        winning_percentage = wins / matches if matches > 0 else 0
        winning_percentage_data[season][team] = winning_percentage

# Convert the dictionary to a DataFrame
winning_percentage_df = pd.DataFrame(winning_percentage_data).T.reset_index().rename(columns={'index': 'Season'})


output_file_path = 'Winning_Percentage.csv'
winning_percentage_df.to_csv(output_file_path)