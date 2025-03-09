import streamlit as st
import ipl_analysis
import pandas as pd
import datetime

from ipl_analysis import venue_stat

# Page Configuration
st.set_page_config(
    page_title='Cricket Match Predictor',
    page_icon='🏏',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Page Styling
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1552223303-58e96b6c89d4");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0);
}
[data-testid="stSidebar"] {
    background-color: #2C8A2E;
}
h1 {
    color: #FF4500;
    text-align: center;
    text-shadow: 2px 2px 4px #000000;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Page Header and Description
st.markdown(
    """
    <div style="text-align: center; background-color: #FFD700; padding: 10px; border-radius: 10px;">
        <h2 style="color: #000080;">🏏 IPL Analysis Dashboard</h2>
    </div>
    """,
    unsafe_allow_html=True
)


# Sidebar title with cricket emojis
st.sidebar.title("🏏 Cricket Dashboard 🏏")

# Sidebar navigation with cricket-themed options
option = st.sidebar.radio(
    "Choose a Section:",
    (
        "ℹ️ Basic Info",
        "🏏 Matches Info",
        "👥 Teams Info",
        "🪙 Toss Analysis",
        "🏃 Players Info",
        "🏟️ Venue",
        "🥇 Winners Chart"
    )
)


#importing data
ipl1 = pd.read_csv('datasets/mod_deliveries.csv')
ipl2 = pd.read_csv('datasets/mod_matches.csv')

# Section 1: Basic Info
if option == "ℹ️ Basic Info":
    st.header("📋 Basic Information")
    st.markdown("""
    Here you'll find an overview of the dataset and key details about the IPL.
    """)
    # Display team names using the `team_name` function
    info_about = st.selectbox('Basic information about:-',['select an option','teams','players'])
    if info_about == 'select an option':
        st.write('')
    elif info_about == 'teams':
        teams = ipl_analysis.team_name()
        st.subheader("Team Names:")
        for team in teams['Team_Name']:
            st.write(f"- {team}")
    elif info_about == 'players':
        players = ipl_analysis.players()
        st.subheader('All players ever played IPL')
        for player in sorted(players['Players']):
            st.write(f'- {player}')

# Section 2: Matches Info
elif option == "🏏 Matches Info":
    st.header("📊 Matches Information")
    st.markdown("""
    Analyze details about matches, including scores, outcomes, and performance trends.
    """)
    info_about = st.selectbox('Select what information about match do you need',['Select an option','Summary of a match','ball-by-ball details of a match',
                                                                                 'Details of matches corresponding to a season'])
    if info_about == 'Select an option':
        st.write('')

    elif info_about == 'Summary of a match':

        col1,col2,col3 = st.columns(3)

        with col1:
            team1 = st.selectbox(
                'Select the team name',
                ['Select a team'] + sorted((ipl_analysis.team_name())['Team_Name'])
            )

        with col2:
            team2 = st.selectbox(
                'Select another team',
                ['Select another team'] + sorted((ipl_analysis.team_name())['Team_Name'], reverse=True)
            )

        with col3:
            # Define a date range
            min_date = datetime.date(2008, 1, 1)
            max_date = datetime.date(2024, 12, 31)

            # Add a date input with restricted range
            date = str(st.date_input("Select a date", min_value=min_date, max_value=max_date))

        if team1=='select a team' or team2 == 'Select another team' or date == '2024-12-31':  # Check if any input is missing
            st.info('Please select both teams and a date to view the match summary.')
        elif team1 == team2:  # Check if the same team is selected for both inputs
            st.error('You have selected the same teams. Please select different teams.')
        else:
            # Fetch and display the match summary
            response = ipl_analysis.match_summary(team1, team2, date)
            st.subheader(f'Summary of match between {team1} and {team2} played on {date}')

            # Display the response details
            for key, value in response.items():
                st.write(f'{key}: {value}')

    elif info_about == 'ball-by-ball details of a match':
        col1, col2, col3 = st.columns(3)

        with col1:
            team1 = st.selectbox('Select the team name', ['Select a team']+sorted((ipl_analysis.team_name())['Team_Name']))

        with col2:
            team2 = st.selectbox('ball-by-ball details of a match',
                                 ['Select another team']+sorted((ipl_analysis.team_name())['Team_Name'], reverse=True))

        with col3:
            # Define a date range
            min_date = datetime.date(2008, 1, 1)
            max_date = datetime.date(2024, 12, 31)

            # Add a date input with restricted range
            date = str(st.date_input("Select a date", min_value=min_date, max_value=max_date))
        if team1 == 'Select a team' or team2 == 'Select another team' or date == '2024-12-31':
            st.info('select value to display result')
            st.write('')
        elif team1 == team2:
            st.error('You Have Selected Same Teams. Please Select Different Teams')
        else:
            response = ipl_analysis.match_details(team1,team2,date)
            if 'error' in response:
                st.error(response['error'])
            else:
                st.success("Match details retrieved successfully!")
                st.table(response)

    elif info_about == 'Details of matches corresponding to a season':
        season = st.selectbox('select a season from below',['Select an option']+sorted(ipl2['season'].unique()))

        records = ipl_analysis.season_record(season)
        if season == 'Select an option':
            st.info('Please Select details to display result')
            st.write('')
        elif 'error' in records:
            st.error(records['error'])
        else:
            count=0
            for record in records:
                count+=1
                # Display team1, team2, and date in bold
                col1,col2,col3=st.columns(3)
                team1 = f"**Team 1:** {record['team1']}"
                team2 = f"**Team 2:** {record['team2']}"
                date = f"**Date:** {record['date']}"
                with col1:
                    st.markdown(f'{count})   {team1}')
                with col2:
                    st.markdown(team2)
                with col3:
                    st.markdown(date)

                # Display other fields normally
                other_details = {k: v for k, v in record.items() if k not in ['team1', 'team2', 'date']}
                for key, value in other_details.items():
                    st.write(f"{key}: {value}")

                st.markdown('-----')




# Section 3: Teams Info
elif option == "👥 Teams Info":
    st.header("📈 Teams Information")
    st.markdown("""
    Dive into team performance metrics, season-wise statistics, and head-to-head analysis.
    """)

    # Dropdown for type of analysis
    info_about = st.selectbox(
        'Select what type of team analysis you want',
        ['Select an option for details', 'Team performance', 'Head-to-head team performance']
    )

    if info_about == 'Select an option for details':
        st.info('Please select an option for information')

    elif info_about == 'Team performance':
        # Dropdown for selecting the team
        team = st.selectbox(
            'Select a team',
            ['Select a team'] + sorted(ipl_analysis.team_name()['Team_Name'])
        )

        if team == 'Select a team':
            st.info('Please select a valid team to see performance details.')
        else:
            # Fetch and display the response
            data = ipl_analysis.team_performance(team)
            if 'error' in data:
                st.error(data['error'])
            else:
                st.subheader(f"Performance Details for {team}")
                # Display Season-wise Runs
                st.subheader("Season-wise Runs")
                seasonwise_df = pd.DataFrame(data['seasonwise_runs'].items(), columns=['Season', 'Runs'])
                st.table(seasonwise_df)

                # Display Batters
                st.subheader("Batters")
                if data['batters']:
                    st.write(", ".join(data['bowlers']))
                else:
                    st.write("No data available")

                # Display Bowlers
                st.subheader("Bowlers")
                if data['bowlers']:
                    st.write(", ".join(data['bowlers']))
                else:
                    st.write("No data available")

                # Display Overall Stats
                st.subheader("Overall Stats")
                st.markdown(f"""
                - **Total Matches Played**: {data['total_matches']}
                - **Qualified Seasons**: {', '.join(map(str, data['qualified_matches_season']))}
                - **Finals Played**: {data['finals_played']}
                - **Wins**: {data['wins']}
                - **Losses**: {data['losses']}
                - **Winning Percentage**: {data['winning_percentage_overall']}%
                """)

    elif info_about == 'Head-to-head team performance':
        team1 = st.selectbox('Select a team', ['Select a team'] + sorted(ipl_analysis.team_name()['Team_Name']))
        team2 = st.selectbox('Select another team',
                             ['select another team'] + sorted(ipl_analysis.team_name()['Team_Name']))
        if team1 == team2:
            st.error('You have selected same team name. Please select different team')

        option = st.selectbox('select whether you want head-to-head information of a season or allover',
                              ['select an option','head_to_head for season','head_to_head Overall'])
        if option == 'select an option':
            st.write('')
        elif option == 'head_to_head for season':

            season = st.selectbox('Select a year',['Select a year']+sorted(ipl2['season'].unique()))

            if team1 == 'Select a team' or team2 =='Select another team' or season == 'Select a year':
                st.write('')
            else:
                response = ipl_analysis.HTH_season(team1,team2,season)
                st.table(response)
        elif option == 'head_to_head Overall':
            response = ipl_analysis.HTH_Overall(team1,team2)
            st.table(response['match_records'])

            st.markdown("Overall summary of teams")
            st.write(f'- Total matches between {team1} and {team2} are {response['summary']['total_matches']}')
            st.write(f'- Total matches won by {team1} are {response['summary']['wins_of_team1']}')
            st.write(f'- Total matches won by {team2} are {response['summary']['wins_of_team2']}')
            st.write(f'- Winning rate if {team1} is {response['summary']['winning_rate_team1']}')
            st.write(f'- Winning rate of {team2} is {response['summary']['winning_rate_team2']}')



# Section 4: Toss Analysis
elif option == '🪙 Toss Analysis':
    st.header("🎯 Toss Analysis")
    st.markdown("""
        Explore how Toss decision Affected the matches.
        """)
    toss = ipl_analysis.toss_analysis()
    st.markdown(f'1) After Tossing there is   {toss['toss_bat_percentage']}%   chances that the team will choose batting')
    st.write('')
    st.markdown(f'2) After Tossing there is   {toss['toss_field_percentage']}%   chances that the team will choose bowling')
    st.write('')
    st.markdown(f'3) After winning the Toss there is   {toss['win_toss_match_percentage']}%   chances that the team will win the match too')
    st.write("")
    st.markdown(f"4) After choosing batting there is   {toss["bat_after_toss_win_percentage"]}%   chances that the team team will win the match")
    st.write("")
    st.markdown(f"5) After choosing bowling there is   {toss["field_after_toss_win_percentage"]}%   chances that the team team will win the match")


# Section 5: Players Info
elif option == "🏃 Players Info":
    st.header("🏃 Players Information")
    st.markdown("""
    Explore player statistics, including runs, wickets, and other key performance indicators.
    """)
    info_about = st.selectbox('Select an option to display details',['Select an option','Player Performance','Top Players'])
    if info_about == 'Select an option':
        st.info('Please select what information do you want')
    elif info_about == 'Player Performance':
        name = st.selectbox('Select a player',['select a player']+sorted(ipl_analysis.players()['Players']))
        if name == 'select a player':
            st.info('Please select a player')
        else:
            player = ipl_analysis.players_performance(name)
            count = 0
            for key, value in player.items():
                count+=1
                st.write(f"{count})  {key} --- {value}")
    elif info_about == 'Top Players':
        what = st.selectbox('Select whether you want top batters or bowlers',['select an option','batter','bowler'])
        if what == 'select an option':
            st.write("")
        elif what == 'batter':
            st.success('here players are listed according to their strike rates')
            top_player = ipl_analysis.top_players(what)
            for key, value in top_player.items():
                st.subheader(key)
                count=0
                for i,j in value.items():
                    count+=1
                    st.write(f'{count}) {i}--{j}')
        elif what == 'bowler':
            st.success('here players are listed according to wickets taken by them')
            top_player = ipl_analysis.top_players(what)
            for key, value in top_player.items():
                st.subheader(key)
                count=0
                for i,j in value.items():
                    count+=1
                    st.write(f'{count}) {i}--{j}')

# Section 6: Venue
elif option == "🏟️ Venue":
    st.header("🏟️ Venue Analysis")
    st.markdown("""
    Analyze match outcomes and trends based on venue locations.
    """)
    info_about = st.selectbox('Select an option',['select an option','Venue Statistics','Top Venues'])
    if info_about == 'select an option':
        st.write("")
    elif info_about == 'Venue Statistics':
        venue = st.selectbox('select a venue to get a stat',['select a venue']+sorted(ipl2['venue'].unique()))
        venue_stat = ipl_analysis.venue_stat(venue)
        if venue == 'select a venue':
            st.write("")
        else:
            #Displaying Stats

            st.markdown(f"""
            <div style='text-align: centre'><h2>{venue_stat['venue']}</h2></div>
            """,
            unsafe_allow_html=True)
            st.write(f'<h3> Seasons Played on the venue :</h3>',
                     unsafe_allow_html=True)
            for i in venue_stat['seasons_held']:
                st.markdown(f"""
                - {i}
                """)
            st.write(f'<h3>Teams Played On this Menu Till Now</h3>',
                     unsafe_allow_html=True)
            for i in venue_stat['teams_played']:
                st.markdown(f"""
                - {i}
            """)
            st.write(f"<h3>Preferred Toss Decision By Teams On This Field:-  <i>{venue_stat['prefered_toss_decision']}</i> </h3> ",
                     unsafe_allow_html=True)
            st.write(
                f"<h3>Number of Matches PLayed On This Field:-  <i>{venue_stat['number_matches']}</i> </h3> ",
                unsafe_allow_html=True)
            st.write(
                f"<h3>Average runs a team can achieve on this field:-  <i>{venue_stat['avg_score']}</i> </h3> ",
                unsafe_allow_html=True)
            st.write(f"<h3>Minimum score achieved till date on this field:- <i>{venue_stat['min_score']}</i></h3>",
                     unsafe_allow_html=True)
            st.write(f"<h3>Maximum score achieved on this field till date :- <i>{venue_stat['max_score']}</i></h3>",
                     unsafe_allow_html=True)
            st.write(f"<h3>Number of wickets Taken till now:- <i>{venue_stat['num_wickets']}</i></h3>",
                     unsafe_allow_html=True)
            st.write(f"<h3>Chances of a chasing team to win:- <i>{venue_stat['chasing_rate']}</i></h3>",
                     unsafe_allow_html=True)
            st.write(f"<h3>Chances of a defending team to win:- <i>{venue_stat['defending_rate']}</i></h3>",
                     unsafe_allow_html=True)
    elif info_about == 'Top Venues':
        top_venue = ipl_analysis.top_venues()
        for i in top_venue:
            st.markdown(f"<h3>{i}</h3>",
                        unsafe_allow_html=True)
            st.markdown(f"""
                - Number of matches Played on this Field :- {top_venue[i]['num_matches']}
                - Total Runs Scored Till Now :- {top_venue[i]['total_runs']}<br>
                - Total Wickets Taken Till Now:- {top_venue[i]['total_wickets']}<br>
                - Average Runs Scored On This Field:- {top_venue[i]['avg_runs']}<br>
                - Preferred Toss Decision :- {top_venue[i]['prefered_toss_decision']}
            """,
                        unsafe_allow_html=True)

#section 7 Season summary
elif option == '🥇 Winners Chart':
    st.header("🥇 Season Summary")
    st.markdown("""
        Winners over the seasons.
        """)
    winners = ipl_analysis.season_winners()
    for i in winners:
        st.markdown(f'''
        <h4>{i['season']}:- <i><u>{i['winner']}</u></i></h4>
''',
                    unsafe_allow_html=True)


# Footer
st.markdown("---")
st.markdown(
    "<center><p style='color: #FFEB3B;'>© 2025 IPL Analysis & Prediction App | Made with 💜 for Cricket Fans by DataTinker</p></center>",
    unsafe_allow_html=True
)
