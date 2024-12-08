import pandas as pd

df = pd.read_csv('Original_Dataset.csv', encoding='latin1')

df.iloc[:, 1] = pd.to_datetime(df.iloc[:, 1], errors='coerce')

filtered_df = df[(df.iloc[:, 1] >= '2013-08-01') & (df.iloc[:, 1] <= '2018-06-01')]
filtered_df = filtered_df.reset_index(drop=True)
filtered_df.to_csv('Season_Selected_Dataset.csv', index=False)

with open('Winning_Percentage.py') as file:
    exec(file.read())

#####

from Season_Results import get_last_season_result

filename = 'Season_Selected_Dataset.csv'
df = pd.read_csv(filename, encoding='latin1')

new_df = pd.concat([df.iloc[:, :4], df[['FTR']]], axis=1)

new_df['HomeTeam_WinPercentage'] = 0.0
new_df['HomeTeam_DrawPercentage'] = 0.0
new_df['AwayTeam_WinPercentage'] = 0.0
new_df['AwayTeam_DrawPercentage'] = 0.0

new_df['HomeTeam_Streak'] = 0
new_df['AwayTeam_Streak'] = 0

new_df['HomeTeam_AvgGoal'] = 0.0
new_df['AwayTeam_AvgGoal'] = 0.0

new_df['HomeTeam_AvgGoalDiff'] = 0.0
new_df['AwayTeam_AvgGoalDiff'] = 0.0

new_df['HomeTeam_AvgShotOnTarget'] = 0.0
new_df['AwayTeam_AvgShotOnTarget'] = 0.0

new_df['HomeTeam_AvgShotBlock'] = 0.0
new_df['AwayTeam_AvgShotBlock'] = 0.0

new_df['HomeTeam_AvgCorners'] = 0.0
new_df['AwayTeam_AvgCorners'] = 0.0

new_df['HomeTeam_AvgRedCards'] = 0.0
new_df['AwayTeam_AvgRedCards'] = 0.0

new_df['HomeTeam_AvgYellowCards'] = 0.0
new_df['AwayTeam_AvgYellowCards'] = 0.0

new_df['HomeTeam_H2H_Wins'] = 0.0
new_df['AwayTeam_H2H_Wins'] = 0.0

new_df['HomeTeam_Last_Season'] = 0.0
new_df['AwayTeam_Last_Season'] = 0.0

for index, row in df.iterrows():
    home_team = row['HomeTeam']
    away_team = row['AwayTeam']
    
    # Get team's last season winning percentage
    home_team_last_season = get_last_season_result(row['Season'], home_team)
    away_team_last_season = get_last_season_result(row['Season'], away_team)
     
    # Filter matches involving the home team before the current match
    home_team_matches = df[((df['HomeTeam'] == home_team) | (df['AwayTeam'] == home_team)) & (df.index < index)]
    home_team_matches_len = len(home_team_matches)
    home_wins = 0
    home_draws = 0
    home_streak = 0
    home_goal_sum = 0
    home_goal_diff_sum = 0
    home_shot_on_target_sum = 0
    home_shot_block_sum = 0
    home_corners_sum = 0
    home_red_cards_sum = 0
    home_yellow_cards_sum = 0
        
    for _, match in home_team_matches.iterrows():
        if match['HomeTeam'] == home_team and match['FTR'] == 'H':
            home_wins += 1
            home_streak = home_streak + 1 if home_streak >= 0 else 1
        elif match['AwayTeam'] == home_team and match['FTR'] == 'A':
            home_wins += 1
            home_streak = home_streak + 1 if home_streak >= 0 else 1
        elif match['FTR'] == 'D':
            home_draws += 1
            home_streak = 0
        else:
            home_streak = home_streak - 1 if home_streak <= 0 else -1
        
        if match['HomeTeam'] == home_team:
            home_goal_sum += match['FTHG']
            home_goal_diff_sum += match['FTHG'] - match['FTAG']
            home_shot_on_target_sum += match['HST']
            home_shot_block_sum += match['AST'] - match['FTAG']
            home_corners_sum += match['HC']
            home_red_cards_sum += match['HR']
            home_yellow_cards_sum += match['HY']
        elif match['AwayTeam'] == home_team:
            home_goal_sum += match['FTAG']
            home_goal_diff_sum += match['FTAG'] - match['FTHG']
            home_shot_on_target_sum += match['AST']
            home_shot_block_sum += match['HST'] - match['FTHG']
            home_corners_sum += match['AC']
            home_red_cards_sum += match['AR']
            home_yellow_cards_sum += match['AY']
    
    # count avg
    if home_team_matches_len > 0:
        home_team_win_percentage = home_wins / home_team_matches_len
        home_team_draw_percentage = home_draws / home_team_matches_len
        home_team_avg_goal = home_goal_sum / home_team_matches_len
        home_team_avg_goal_diff = home_goal_diff_sum / home_team_matches_len
        home_team_avg_shot_on_target = home_shot_on_target_sum / home_team_matches_len
        home_team_avg_shot_block = home_shot_block_sum / home_team_matches_len
        home_team_avg_corners = home_corners_sum / home_team_matches_len
        home_team_avg_red_cards = home_red_cards_sum / home_team_matches_len
        home_team_avg_yellow_cards = home_yellow_cards_sum / home_team_matches_len
    else:
        home_team_win_percentage = 0.0
        home_team_draw_percentage = 0.0
        home_team_avg_goal = 0.0
        home_team_avg_goal_diff = 0.0
        home_team_avg_shot_on_target = 0.0
        home_team_avg_shot_block = 0.0
        home_team_avg_corners = 0.0
        home_team_avg_red_cards = 0.0
        home_team_avg_yellow_cards = 0.0

    new_df.at[index, 'HomeTeam_WinPercentage'] = home_team_win_percentage
    new_df.at[index, 'HomeTeam_DrawPercentage'] = home_team_draw_percentage
    new_df.at[index, 'HomeTeam_Streak'] = home_streak
    new_df.at[index, 'HomeTeam_AvgGoal'] = home_team_avg_goal
    new_df.at[index, 'HomeTeam_AvgGoalDiff'] = home_team_avg_goal_diff
    new_df.at[index, 'HomeTeam_AvgShotOnTarget'] = home_team_avg_shot_on_target
    new_df.at[index, 'HomeTeam_AvgShotBlock'] = home_team_avg_shot_block
    new_df.at[index, 'HomeTeam_AvgCorners'] = home_team_avg_corners
    new_df.at[index, 'HomeTeam_AvgRedCards'] = home_team_avg_red_cards
    new_df.at[index, 'HomeTeam_AvgYellowCards'] = home_team_avg_yellow_cards
    new_df.at[index, 'HomeTeam_Last_Season'] = home_team_last_season
    

    # Filter matches involving the away team before the current match
    away_team_matches = df[((df['HomeTeam'] == away_team) | (df['AwayTeam'] == away_team)) & (df.index < index)]
    away_team_matches_len = len(away_team_matches)
    away_wins = 0
    away_draws = 0
    away_streak = 0
    away_goal_sum = 0
    away_goal_diff_sum = 0
    away_shot_on_target_sum = 0
    away_shot_block_sum = 0
    away_corners_sum = 0
    away_red_cards_sum = 0
    away_yellow_cards_sum = 0
    
    for _, match in away_team_matches.iterrows():
        if match['HomeTeam'] == away_team and match['FTR'] == 'H':
            away_wins += 1
            away_streak = away_streak + 1 if away_streak >= 0 else 1
        elif match['AwayTeam'] == away_team and match['FTR'] == 'A':
            away_wins += 1
            away_streak = away_streak + 1 if away_streak >= 0 else 1
        elif match['FTR'] == 'D':
            away_draws += 1
            away_streak = 0
        else:
            away_streak = away_streak - 1 if away_streak <= 0 else -1
        
        if match['HomeTeam'] == away_team:
            away_goal_sum += match['FTHG']
            away_goal_diff_sum += match['FTHG'] - match['FTAG']
            away_shot_on_target_sum += match['HST']
            away_shot_block_sum += match['AST'] - match['FTAG']
            away_corners_sum += match['HC']
            away_red_cards_sum += match['HR']
            away_yellow_cards_sum += match['HY']
        elif match['AwayTeam'] == away_team:
            away_goal_sum += match['FTAG']
            away_goal_diff_sum += match['FTAG'] - match['FTHG']
            away_shot_on_target_sum += match['AST']
            away_shot_block_sum += match['HST'] - match['FTHG']
            away_corners_sum += match['AC']
            away_red_cards_sum += match['AR']
            away_yellow_cards_sum += match['AY']
    
    # calculate avg
    if away_team_matches_len > 0:
        away_team_win_percentage = away_wins / away_team_matches_len
        away_team_draw_percentage = away_draws / away_team_matches_len
        away_team_avg_goal = away_goal_sum / away_team_matches_len
        away_team_avg_goal_diff = away_goal_diff_sum / away_team_matches_len
        away_team_avg_shot_on_target = away_shot_on_target_sum / away_team_matches_len
        away_team_avg_shot_block = away_shot_block_sum / away_team_matches_len
        away_team_avg_corners = away_corners_sum / away_team_matches_len
        away_team_avg_red_cards = away_red_cards_sum / away_team_matches_len
        away_team_avg_yellow_cards = away_yellow_cards_sum / away_team_matches_len
    else:
        away_team_win_percentage = 0.0
        away_team_draw_percentage = 0.0
        away_team_avg_goal = 0.0
        away_team_avg_goal_diff = 0.0
        away_team_avg_shot_on_target = 0.0
        away_team_avg_shot_block = 0.0
        away_team_avg_corners = 0.0
        away_team_avg_red_cards = 0.0
        away_team_avg_yellow_cards = 0.0

    new_df.at[index, 'AwayTeam_WinPercentage'] = away_team_win_percentage
    new_df.at[index, 'AwayTeam_DrawPercentage'] = away_team_draw_percentage
    new_df.at[index, 'AwayTeam_Streak'] = away_streak
    new_df.at[index, 'AwayTeam_AvgGoal'] = away_team_avg_goal
    new_df.at[index, 'AwayTeam_AvgGoalDiff'] = away_team_avg_goal_diff
    new_df.at[index, 'AwayTeam_AvgShotOnTarget'] = away_team_avg_shot_on_target
    new_df.at[index, 'AwayTeam_AvgShotBlock'] = away_team_avg_shot_block
    new_df.at[index, 'AwayTeam_AvgCorners'] = away_team_avg_corners
    new_df.at[index, 'AwayTeam_AvgRedCards'] = away_team_avg_red_cards
    new_df.at[index, 'AwayTeam_AvgYellowCards'] = away_team_avg_yellow_cards
    new_df.at[index, 'AwayTeam_Last_Season'] = away_team_last_season

    # Filter h2h matches before the current match
    h2h_matches = df[((df['HomeTeam'] == home_team) & (df['AwayTeam'] == away_team)) | ((df['HomeTeam'] == away_team) & (df['AwayTeam'] == home_team)) & (df.index < index)]
    home_team_h2h_wins = 0.0
    away_team_h2h_wins = 0.0
    for _, match in h2h_matches.iterrows():
        if match['FTR'] == 'H' and match['HomeTeam'] == home_team:
            home_team_h2h_wins += 1
        elif match['FTR'] == 'A' and match['AwayTeam'] == home_team:
            home_team_h2h_wins += 1
        elif match['FTR'] == 'H' and match['HomeTeam'] == away_team:
            away_team_h2h_wins += 1
        elif match['FTR'] == 'A' and match['AwayTeam'] == away_team:
            away_team_h2h_wins += 1
        elif match['FTR'] == 'D':
            home_team_h2h_wins += 0.5
            away_team_h2h_wins += 0.5
    
    # Update h2h columns in the DataFrame
    new_df.at[index, 'HomeTeam_H2H_Wins'] = home_team_h2h_wins
    new_df.at[index, 'AwayTeam_H2H_Wins'] = away_team_h2h_wins
    
output_file_path = 'Numeric_Dataset.csv'
new_df.to_csv(output_file_path, index=False)

#####

with open('Combine_Datasets.py') as file:
    exec(file.read())