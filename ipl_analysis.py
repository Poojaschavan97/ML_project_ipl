import pandas as pd
import numpy as np
import json

ipl1 = pd.read_csv('datasets/mod_deliveries.csv')
ipl2 = pd.read_csv('datasets/mod_matches.csv')
data = ipl1.merge(ipl2[['match_id','season']],on = 'match_id')
# 1) Basic information

# Teams participated till now
def team_name():
    a=set(list(ipl2['team1'])+list(ipl2['team2']))
    dict1={'Team_Name':list(a)}
    return dict1

# players participated till now all
def players():
    a=set(list(ipl1['batter'])+list(ipl1['bowler']))
    players={'Players':list(a)}
    return players

#2) Information of matches

# match Summary
def match_summary(team1, team2, date):
    # fetching match details with respective data
    data = ipl2[(ipl2['team1'] == team1) & (ipl2['team2'] == team2) & (ipl2['date'] == date)]

    if not data.empty:  # Check if data is not empty to avoid errors
        match = {
            'match_id': data['match_id'].iloc[0],
            'team1': data['team1'].iloc[0],
            'team2': data['team2'].iloc[0],
            'season': data['season'].iloc[0],
            'date': str(data['date'].iloc[0]),
            'city': data['city'].iloc[0],
            'venue': data['venue'].iloc[0],
            'toss_winner': data['toss_winner'].iloc[0],
            'toss_decision': data['toss_decision'].iloc[0],
            'winner': data['winner'].iloc[0],
            'result_margin': data['result_margin'].iloc[0],
            'target_runs': data['target_runs'].iloc[0]
        } # iloc is used to avoid index number
        return (match)
    else:
        return {"error": "No match found with the given details."}

#match_details ball-by ball
def match_details(team1,team2,date):
    """to get respective match details we compare find the date in second dataset for match id
    and search the data in 1st dataset cause ipl1 does not have date column"""
    id=ipl2[(ipl2['team1'] == team1) & (ipl2['team2'] == team2) & (ipl2['date'] == date)]['match_id']
    if not id.empty:
        id=id.iloc[0]
        match_detail=ipl1[ipl1['match_id']==id] # searched respective match in ipl1
        return json.loads(match_detail.to_json(orient='records',index=False)) # else return result, orientation removes index
    else:
        return {'error':'please check whether the details are correct'} #if data not matches

# every match from respective season
"""
        this function firstly checks whether we have data of respective season or not if yes then return the records else return error
    """

def season_record(season):
    seasons_played = ipl2['season'].unique()
    if season in seasons_played:
        records = ipl2[ipl2['season'] == season]
        # json.loads is used to convert inner string value to json
        response = json.loads(records.to_json(orient='records', index=False))
        return response
    else:
        return {'error': "Sorry we don't have data of this season"}

#3) Team Performance
# a) Overall team performance
def team_performance(team):
    if team in team_name()['Team_Name']:
        # To find sum of runs in respective seasons by the team
        team_runs_season = data.groupby(['batting_team', 'season'])['total_runs'].sum()
        team_runs_season = team_runs_season[team].to_dict() if team in team_runs_season.index.get_level_values(0) else {}

        # List of batters for the team across all seasons
        batters = list(data[data['batting_team'] == team]['batter'].unique())

        # List of bowlers for the team across all seasons
        bowlers = list(data[data['bowling_team'] == team]['bowler'].unique())

        # Total matches played by the team
        total_matches = ipl2[(ipl2['team1'] == team) | (ipl2['team2'] == team)]['match_id'].nunique()

        # Number of matches played as qualifiers
        qualifier = ipl2[ipl2['match_type'] != 'League']
        qualifier_team = qualifier[(qualifier['team1'] == team) | (qualifier['team2'] == team)]
        if not qualifier_team.empty:
            qualifier_team_season = list(qualifier_team['season'].unique())
        else:
            qualifier_team_season = f"{team} never qualified"

        # Number of matches played in finals
        finals = ipl2[ipl2['match_type'] == 'Final']
        final_team = finals[(finals['team1'] == team) | (finals['team2'] == team)]
        finalized = final_team.shape[0]

        # Number of finals won
        if not final_team.empty:
            final_win_count = final_team[final_team['winner'] == team].shape[0]
            if final_win_count == 0:
                winned_matches = f"{team} never won the finals"
            else:
                winned_matches = final_win_count
        else:
            winned_matches = f"{team} never went to finals"

        # Number of finals lost
        if isinstance(winned_matches, int):
            lossed_matches = finalized - winned_matches
        else:
            lossed_matches = f"{team} never reached the finals"

        # Winning percentage across all matches
        matches_played = ipl2[(ipl2['team1'] == team) | (ipl2['team2'] == team)]
        winned_matches_overall = matches_played[matches_played['winner'] == team]
        if matches_played.shape[0] > 0:
            winning_percentage = (winned_matches_overall.shape[0] / matches_played.shape[0]) * 100
        else:
            winning_percentage = 0

        # Prepare the final response dictionary
        final_response = {
            'seasonwise_runs': team_runs_season,
            'batters': batters,
            'bowlers': bowlers,
            'total_matches': total_matches,
            'qualified_matches_season': qualifier_team_season,
            'finals_played': finalized,
            'wins': winned_matches,
            'losses': lossed_matches,
            'winning_percentage_overall': f"{round(winning_percentage, 2)}%"
        }

        return final_response
    else:
        return {"error": f"Team '{team}' not found in the dataset"}

# Head to Head performance
# SeasonWise
def HTH_season(team1, team2, season):
    # Fetch matches where the teams played against each other in the specified season
    possiblity1 = ipl2[(ipl2['team1'] == team1) & (ipl2['team2'] == team2) & (ipl2['season'] == season)]
    possiblity2 = ipl2[(ipl2['team1'] == team2) & (ipl2['team2'] == team1) & (ipl2['season'] == season)]

    # Combine the possibilities (matches found in either case)
    matches = pd.concat([possiblity1, possiblity2])

    # Check if there are any matches
    if not matches.empty:
        # Select relevant columns for the response
        records = matches[['match_id', 'season', 'date', 'match_type', 'city', 'venue',
                           'toss_winner', 'toss_decision', 'winner', 'target_runs', 'player_of_match']]
        response = json.loads(records.to_json(index=False, orient='records'))
        return response
    else:
        # Return an error if no matches are found
        return {'error': 'No records found regarding the provided data.'}


# for all seasons
def HTH_Overall(team1, team2):
    # Extracting data with respect to teams
    matches = ipl2[((ipl2['team1'] == team1) & (ipl2['team2'] == team2)) |
                   ((ipl2['team2'] == team1) & (ipl2['team1'] == team2))]

    # Checking if there are any matches
    if not matches.empty:
        # Fetching the required columns to return
        records = matches[['match_id', 'season', 'date', 'match_type', 'city', 'venue',
                           'toss_winner', 'toss_decision', 'winner', 'target_runs', 'player_of_match']]

        # Number of matches they played against
        total_matches = records.shape[0]

        # Number of wins for each team
        team1_win = records[records['winner'] == team1].shape[0]
        team2_win = records[records['winner'] == team2].shape[0]

        # Winning percentages
        winning_rate_team1 = (team1_win / total_matches) * 100
        winning_rate_team2 = (team2_win / total_matches) * 100

        # Creating the result dictionary
        result = {
            'match_records': json.loads(records.to_json(orient='records')),
            'summary': {
                'total_matches': total_matches,
                'wins_of_team1': team1_win,
                'wins_of_team2': team2_win,
                'winning_rate_team1': round(winning_rate_team1, 2),
                'winning_rate_team2': round(winning_rate_team2, 2)
            }
        }
        return result
    else:
        return {'error': 'Data not available'}


# Toss Analysis
def toss_analysis():
    """
    Analyzes toss decisions in IPL matches and computes statistics.
    Returns:
        dict: A dictionary containing percentages of toss decisions and their outcomes.
    """

    # Fetching details
    toss_bat = ipl2[ipl2['toss_decision'] == 'bat']
    toss_field = ipl2[ipl2['toss_decision'] == 'field']
    win_toss_match = ipl2[ipl2['toss_winner'] == ipl2['winner']].shape[0]
    win_bat_match = toss_bat[toss_bat['winner'] == toss_bat['toss_winner']].shape[0]
    win_field_match = toss_field[toss_field['winner'] == toss_field['toss_winner']].shape[0]

    # Converting to percentages
    rate_toss_bat = (toss_bat.shape[0] / ipl2.shape[0]) * 100
    rate_toss_field = (toss_field.shape[0] / ipl2.shape[0]) * 100
    rate_win_toss_match = (win_toss_match / ipl2.shape[0]) * 100
    rate_win_bat_match = (win_bat_match / toss_bat.shape[0] * 100) if toss_bat.shape[0] > 0 else 0
    rate_win_field_match = (win_field_match / toss_field.shape[0] * 100) if toss_field.shape[0] > 0 else 0

    # Preparing the response
    response = {
        'toss_bat_percentage': round(rate_toss_bat, 2),
        'toss_field_percentage': round(rate_toss_field, 2),
        'win_toss_match_percentage': round(rate_win_toss_match, 2),
        'bat_after_toss_win_percentage': round(rate_win_bat_match, 2),
        'field_after_toss_win_percentage': round(rate_win_field_match, 2),
    }

    return response


# 4) Players Performance

# overall player performance
def players_performance(name):
    records1 = ipl1[ipl1['batter'] == name]
    records2 = ipl1[ipl1['bowler'] == name]
    records3 = ipl1[ipl1['fielder'] == name]
    plays_as = []

    # Initialize variables
    total_runs = 0
    min_score = 0
    max_score = 0
    avg_score = 0
    num_ball = 0
    boundary_4 = 0
    boundary_6 = 0
    strike_rate = 0
    wickets_taken = 0

    if not records1.empty:
        plays_as.append('batter')
        total_runs = records1['batsman_runs'].sum()
        min_score = records1.groupby('match_id')['batsman_runs'].sum().min()
        max_score = records1.groupby('match_id')['batsman_runs'].sum().max()
        avg_score = records1.groupby('match_id')['batsman_runs'].sum().mean()
        num_ball = records1['ball'].count()
        boundary_4 = records1[records1['batsman_runs'] == 4].shape[0]
        boundary_6 = records1[records1['batsman_runs'] == 6].shape[0]
        strike_rate = round((total_runs / num_ball) * 100, 2) if num_ball > 0 else 0

    if not records2.empty:
        plays_as.append('bowler')
        wickets_taken = records2[records2['is_wicket'] == 1].shape[0]

    if not records3.empty:
        plays_as.append('fielder')

    # Combine records to get matches played
    all_records = pd.concat([records1, records2, records3])
    matches_played = all_records['match_id'].nunique()

    # Get unique teams played for
    teams_played = pd.concat([
        records1['batting_team'],
        records2['bowling_team'],
        records3['bowling_team']
    ]).unique().tolist()

    # Number of times player was "Player of the Match"
    num_man_of_match = ipl2[ipl2['player_of_match'] == name].shape[0]

    response = {
        'teams_played': teams_played,
        'played_as': plays_as,
        'number_matches': matches_played,
        'total_runs': total_runs,
        'num_ball': num_ball,
        'highest_score': max_score,
        'lowest_score': min_score,
        'average_score': round(avg_score, 2),
        'boundaries_4': boundary_4,
         'boundaries_6': boundary_6,
        'strike_rate': strike_rate,
        'wickets_taken': wickets_taken,
        'player_of_match': num_man_of_match
        }
    return response

#top players
def top_players(player):
    if player == 'batter':
        # Grouping by batter to calculate runs and balls faced
        runs = ipl1.groupby('batter')['batsman_runs'].sum()
        balls = ipl1.groupby('batter')['ball'].count()

        # Calculating strike rate
        strike_rate = round((runs / balls) * 100, 2)

        # Creating a DataFrame
        batter_stats = pd.DataFrame({'runs': runs, 'balls': balls, 'strike_rate': strike_rate})

        # Filtering players who faced more than 20 balls
        filtered_batters = batter_stats[batter_stats['balls'] > 20]

        # Sorting by strike rate in descending order
        sorted_batters = filtered_batters.sort_values(by='strike_rate', ascending=False)

        # Creating a dictionary with player names as keys
        response = sorted_batters.to_dict(orient='index')

        return {name: details for name, details in response.items()}

    elif player == 'bowler':
        # Grouping by bowler to calculate balls bowled
        balls = ipl1.groupby('bowler')['ball'].count()

        # Filtering only dismissals (is_wicket == 1) and grouping by bowler
        wickets = ipl1[ipl1['is_wicket'] == 1].groupby('bowler')['is_wicket'].count()

        # Creating a DataFrame for bowlers
        bowler_stats = pd.DataFrame({'balls': balls, 'wickets': wickets}).fillna(0)

        # Filtering bowlers who have taken at least 1 wicket
        filtered_bowlers = bowler_stats[bowler_stats['wickets'] > 0]

        # Sorting by wickets taken in descending order
        sorted_bowlers = filtered_bowlers.sort_values(by='wickets', ascending=False)

        # Creating a dictionary with player names as keys
        response = sorted_bowlers.to_dict(orient='index')

        return {name: details for name, details in response.items()}

    else:
        return {'error': 'Invalid player type. Please use "batter" or "bowler".'}


# 5) Venue

def venue_stat(venue):
    # Fetching data for the respective venue
    records = ipl2[ipl2['venue'] == venue][
        ['match_id', 'season', 'city', 'team1', 'team2', 'toss_winner', 'toss_decision', 'winner']]
    if not records.empty:
        # Seasons held at the venue
        seasons_played = sorted(records['season'].unique())

        # city
        city = records['city'].unique()[0]

        # Teams that played at the venue
        teams_played = list(set(list(records['team1'].unique()) + list(records['team2'].unique())))

        # Most preferred toss decision
        prefered_toss_decision = records['toss_decision'].value_counts().idxmax()

        # Fetch statistics from the related dataset
        new_records = ipl1[ipl1['match_id'].isin(records['match_id'])]
        grouped_data = new_records.groupby(['match_id', 'inning'])
        avg_runs = round(grouped_data['batsman_runs'].sum().mean(), 2)
        wickets_taken = new_records[new_records['is_wicket'] == 1]['is_wicket'].count()

        # number of matches played
        num_matches = records.shape[0]

        # Chasing and defending rates
        inning1_runs = new_records[new_records['inning'] == 1].groupby('match_id')['batsman_runs'].sum()
        inning2_runs = new_records[new_records['inning'] == 2].groupby('match_id')['batsman_runs'].sum()
        margin = inning1_runs - inning2_runs
        chased_match = (margin < 0).sum()
        defended_match = (margin >= 0).sum()

        chasing_rate = round((chased_match / margin.shape[0]) * 100, 2)
        defending_rate = round((defended_match / margin.shape[0]) * 100, 2)

        # min and max score of venue
        min_score = min(inning1_runs.min(), inning2_runs.min())
        max_score = max(inning1_runs.max(), inning2_runs.max())

        # Creating output dictionary
        venue_stats = {
            'venue': f'{venue}, {city}',
            'seasons_held': seasons_played,
            'teams_played': sorted(teams_played),
            'prefered_toss_decision': prefered_toss_decision,
            'number_matches': num_matches,
            'avg_score': avg_runs,
            'min_score': min_score,
            'max_score': max_score,
            'num_wickets': wickets_taken,
            'chasing_rate': chasing_rate,
            'defending_rate': defending_rate
        }
        return venue_stats
    else:
        return {'error': 'This venue is not represented in our data'}

#top venues
def top_venues():
    # Initialize a list to store venue statistics
    venue_stats = []

    for venue in ipl2['venue'].unique():
        # Extract records for the venue
        records = ipl2[ipl2['venue'] == venue][['match_id', 'toss_decision']]

        # Calculate matches played
        num_matches = records['match_id'].nunique()

        # Check if matches played are more than 10
        if num_matches > 10:
            # Fetch data from ipl1 for the venue
            venue_matches = ipl1[ipl1['match_id'].isin(records['match_id'])]
            grouped_data = venue_matches.groupby(['match_id', 'inning'])

            # Calculate total runs scored at the venue
            total_runs = grouped_data['batsman_runs'].sum().sum()

            # Count total wickets taken at the venue
            total_wickets = venue_matches[venue_matches['is_wicket'] == 1]['is_wicket'].count()

            # Apply remaining criteria
            if total_runs > 1000 and total_wickets > 20:
                # Calculate average runs per inning
                avg_runs = round(grouped_data['batsman_runs'].sum().mean(), 2)

                # Most preferred toss decision
                prefered_toss_decision = records['toss_decision'].value_counts().idxmax()

                # Append venue statistics
                venue_stats.append({
                    'venue': venue,
                    'num_matches': num_matches,
                    'total_runs': total_runs,
                    'total_wickets': total_wickets,
                    'avg_runs': avg_runs,
                    'prefered_toss_decision': prefered_toss_decision
                })

    # Convert to DataFrame for sorting
    venue_df = pd.DataFrame(venue_stats)

    # Sort by total_runs (descending) and total_wickets (descending)
    sorted_venues = venue_df.sort_values(by=['total_runs', 'total_wickets'], ascending=[False, False])

    #  Convert to a dictionary with venues as keys
    response = sorted_venues.set_index('venue').T.to_dict()
    return response

#6) season summary
def season_winners():
    winning_team=(ipl2[ipl2['match_type']=='Final'][['season','winner']].to_dict(orient='records'))
    return winning_team