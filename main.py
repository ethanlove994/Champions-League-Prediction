import numpy as np
# Note can only import these if they're in the same directory, otherwise I'll need to provide a path
from Get_Ratings import ratings, exp_scores
import time

# Keep consistent with other script
K = 100

# The fixtures for the round of 16 already decided and the teams playing
teams_16 = ['Paris Saint-Germain','Real Madrid','Sporting CP','Manchester City','Inter','Liverpool','Red Bull Salzburg','Bayern Munchen','Villarreal',
            'Juventus','Chelsea','Lille OSC','Atletico Madrid','Manchester United','SL Benfica','Ajax']

fixtures = [['Paris Saint-Germain','Real Madrid'],['Sporting CP','Manchester City'],['Inter','Liverpool'],['Red Bull Salzburg','Bayern Munchen'],
            ['Villarreal','Juventus'],['Chelsea','Lille OSC'],['Atletico Madrid','Manchester United'],['SL Benfica','Ajax']]

# Functions that will be useful in running a simulation of games
def generate_fixtures(teams):
    """Generates a new set of game fixtures based on the remaining teams in the tournament"""
    new_fixtures = []
    new_teams = teams.copy()
    if len(new_teams)<2:
        return None
    while len(new_teams)>0:
        new_fixtures.append([new_teams[0], new_teams[1]])
        del new_teams[:2]
    return new_fixtures

def play_match(fixture, ratings):
    """Simulates the playing of a match between two teams returning the loser, winner and the winner's new rating"""
    p = np.random.random()

    R_H = ratings[fixture[0]]
    R_A = ratings[fixture[1]]

    E_H,E_A = exp_scores(R_H,R_A)

    if p < E_H:
        return fixture[1], fixture[0], R_H + K*(1 - E_H)
    else:
        return fixture[0], fixture[1], R_A + K*(1 - E_A)

# Chose to update the ratings mid-tournament for this as its consistent with what I did previously
def simulate_UCL(fixtures,teams,ratings):
    """Runs a simulation of the champions league from the round of 16, returns the winning team"""
    # Generate copies of each so as they are contained only in this function
    new_fixtures = fixtures.copy()
    new_teams = teams.copy()
    new_ratings = ratings.copy()

    while len(new_teams)>1:
        for fixture in new_fixtures:
            loser, winner, new_rating = play_match(fixture, new_ratings)
            new_ratings[winner] = new_rating
            new_teams.remove(loser)
        new_fixtures = generate_fixtures(new_teams)
    return new_teams[0]

# Timer to see how horrible and unoptimized my code is
start = time.time()

# Running simulations
n = 1000000
count = 0
for i in range(n):
    winner = simulate_UCL(fixtures,teams_16,ratings)
    if winner == 'Chelsea':
        count += 1

# Finally print out the estimated probability of Chelsea winning
print('Probability of Chelsea winning the Champions League is {:.3f}'.format(count/n))
end = time.time()
print('\n {}'.format(end-start))