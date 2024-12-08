import pandas as pd
from sklearn.discriminant_analysis import StandardScaler
from Standardized_Team_Names import standardized_team_names, get_standardize_team_name

import os

if os.getcwd() != '/Users/shannooooon/NLP-And-Statistics-Unified-Model-For-Football-Prediction/EPL_Dataset':
    os.chdir('./EPL_Dataset')

numeric_dataset = pd.read_csv('./Numeric_Dataset.csv')
guardian_dataset = pd.read_csv('./Guardian_Dataset.csv')

numeric_dataset = numeric_dataset.rename(columns={"HomeTeam": "Home", "AwayTeam": "Away"})
numeric_dataset['Home'] = numeric_dataset['Home'].apply(lambda x: get_standardize_team_name(x, standardized_team_names))
numeric_dataset['Away'] = numeric_dataset['Away'].apply(lambda x: get_standardize_team_name(x, standardized_team_names))

guardian_dataset['Home'] = guardian_dataset['Home'].apply(lambda x: get_standardize_team_name(x, standardized_team_names))
guardian_dataset['Away'] = guardian_dataset['Away'].apply(lambda x: get_standardize_team_name(x, standardized_team_names))


merged = pd.merge(numeric_dataset, guardian_dataset, left_on=['Home', 'Away', 'Season'], right_on=['Home', 'Away', 'Season'], how='inner', indicator=True)
match_ID = merged['MatchID']
merged = merged.drop(columns=['Date', 'MatchID', '_merge'])
# merged['DateTime'] = pd.to_datetime(merged['DateTime']).dt.date
merged = merged.rename(columns={"DateTime":"Date"})

numeric_columns = merged.select_dtypes(include=["number"]).columns


def standardize(df):
    scaler = StandardScaler()
    numeric_columns = []
    for col in df.columns:
        try:
            pd.to_numeric(df[col], errors='raise')
            numeric_columns.append(col)
        except Exception as e:
            pass
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns].astype(float))
    return df

merged = merged.dropna()
merged = standardize(merged)
merged.insert(0, 'MatchID', match_ID)

output_file_path = 'Final_Data.csv'
merged.to_csv(output_file_path, index=False)

# a = pd.read_csv('Final_Data.csv')
# a