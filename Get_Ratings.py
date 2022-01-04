import pandas as pd

def exp_scores(R_H,R_A):
    """Computes the expected scores of the home and away teams based on their ratings"""
    Q_H = 10**(R_H/400)
    Q_A = 10**(R_A/400)

    E_H = Q_H/(Q_H + Q_A)
    E_A = Q_A/(Q_H + Q_A)

    return E_H,E_A

def ELO(R_H,R_A,Outcome,K):
    """Compute the new ELO ratings of each team based on their previous ratings and performance"""
    E_H,E_A = exp_scores(R_H,R_A)

    R_H = R_H + K*(Outcome - E_H)
    R_A = R_A + K*((1-Outcome)-E_A)

    return R_H,R_A

def score(gd):
    """Function for computing the score from each game based on goal difference"""
    if gd > 0:
        return 1
    elif gd < 0:
        return 0
    else:
        return 0.5

# Defining the path and file we need for our model
path = "/home/ethan/Documents/ChampionsLeagueData/"
file = "UEFA Champions League 2004-2021.csv"
file_22 = "UCL 2022.csv"

df = pd.read_csv(path+file,index_col=0)
df_22 = pd.read_csv(path+file_22,index_col=0)

# Remove columns we don't use and combine with 2021/2022 dataset
df.drop(['round','group'], axis=1, inplace=True)
df = pd.concat([df,df_22])

# Let's also remove accents and other non-standard characters
df[['homeTeam','awayteam']] = df[['homeTeam','awayteam']].apply(lambda x: x.str.normalize('NFKD').str.encode('ascii',errors='ignore').str.decode('utf-8'))


# Sort the data by the date so we can loop through chronologically
df['datetime'] = pd.to_datetime(df['date'])
df.sort_values(by='datetime',axis=0,inplace=True)

# Isolate the rows in which scores contain parentheses, these represent penalties in a penalty shootout
df_brackets = df[(df.homeScore.str.contains('(',regex=False)) & (df.awayscore.str.contains('(',regex=False))].copy()

# Isolate the penalties and replace the scores
df_brackets['homeScore'] = df_brackets['homeScore'].str.strip().str[-2]
df_brackets['awayscore'] = df_brackets['awayscore'].str.strip().str[-2]

df.loc[df_brackets.index,['homeScore','awayscore']] = df_brackets.loc[df_brackets.index,['homeScore','awayscore']]

# Change the score columns to integers
df[['homeScore','awayscore']] = df[['homeScore','awayscore']].astype(int)

# Calculate the outcome of each match, 1 for home win, 0 for away win, 0.5 for draw
df['Outcome'] = (df['homeScore'] - df['awayscore']).apply(score)

# Generate a full list of teams
home_teams = df.homeTeam.unique().tolist()
away_teams = df.awayteam.unique().tolist()
teams = list(set(home_teams + away_teams))

# Initialise ratings for each team
ratings = {}
for team in teams:
    ratings[team] = 1200
df['homeRating'] = 1200
df['awayRating'] = 1200


# reset the index so we can iterate through chronologically
df.reset_index(inplace=True, drop=True)
T = df.shape[0]
k = 100

# iterate through each game and update their ELO ratings
for t in range(T):
    R_H = ratings[df.loc[t,'homeTeam']]
    R_A = ratings[df.loc[t,'awayteam']]

    Outcome = df.loc[t,'Outcome']

    R_H,R_A = ELO(R_H,R_A,Outcome,k)

    ratings[df.loc[t,'homeTeam']] = R_H
    ratings[df.loc[t,'awayteam']] = R_A

    df.loc[t,'homeRating'] = R_H
    df.loc[t,'awayRating'] = R_A

