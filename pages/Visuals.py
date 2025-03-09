import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# Set custom page configuration
st.set_page_config(
    page_title='Cricket Match Predictor',
    page_icon='🏏',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Set custom background style using CSS
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

# Load datasets (replace with actual paths or upload method)
df1 = pd.read_csv('datasets/mod_deliveries.csv')  # Deliveries data
df2 = pd.read_csv('datasets/mod_matches.csv')    # Matches data
df3 = pd.read_csv('datasets/ipl_final_data.csv')  # Final extracted data
data = df1.merge(df2[['match_id','season']],on = 'match_id')

# Main title with cricket emoji
st.markdown(
    """
    <div style="text-align: center; background-color: #FFD700; padding: 10px; border-radius: 10px;">
        <h2 style="color: #000080;">🏏 IPL Analysis Visualization</h2>
    </div>
    """,
    unsafe_allow_html=True
)


# teams Over seasons
st.title('teams over season')
#creating filter for sidebar
team_name = st.selectbox('Select the team',data['batting_team'].unique())
# Filter and group data
teams_runs = data[data['batting_team'] == team_name].groupby('season')['total_runs'].sum()
teams_wicket = data[data['bowling_team'] == team_name].groupby('season')['is_wicket'].sum()

# Unique seasons
seasons = teams_runs.index

# Create subplots with shared x-axis
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Runs by Season", "Wickets by Season"))

# Add runs plot
fig.add_trace(
    go.Scatter(
        x=seasons,
        y=teams_runs,
        mode='lines+markers',
        name='Total Runs',
        line=dict(color='blue')
    ),
    row=1, col=1
)

# Add wickets plot
fig.add_trace(
    go.Scatter(
        x=seasons,
        y=teams_wicket,
        mode='lines+markers',
        name='Total Wickets',
        line=dict(color='green')
    ),
    row=2, col=1
)

# Update layout
fig.update_layout(
    title=f"{team_name} Performance Over Seasons",
    xaxis=dict(title="Season"),
    yaxis=dict(title="Runs"),
    yaxis2=dict(title="Wickets"),
    height=600,
    width=800,
    showlegend=True
)

# Display the selected graph
st.plotly_chart(fig, use_container_width=True)


# players performance

# Set up the Streamlit app
st.title("Player Runs Across Seasons")

# Player dropdown filter
player_names = data['batter'].unique()
selected_player = st.selectbox("Select a Player", player_names)

# Filter data for the selected player
player_data = data[data['batter'] == selected_player]
runs_per_season = player_data.groupby('season')['batsman_runs'].sum().reset_index()

# Create the bar graph
fig = px.bar(
    runs_per_season,
    x='season',
    y='batsman_runs',
    title=f"Runs by {selected_player} Across Seasons",
    labels={'season': 'Season', 'batsman_runs': 'Runs'},
    text='batsman_runs',
    template='plotly_white'
)

# Enhance the graph
fig.update_traces(textposition='outside', marker_color='orange')
fig.update_layout(xaxis=dict(type='category'), yaxis_title="Total Runs")

# Display the graph
st.plotly_chart(fig, use_container_width=True)

# losses and wins over seasons
# Set up the Streamlit app
st.title("Team Wins and Losses Across Seasons")

# Team dropdown filter
teams = sorted(df2['team1'].unique())
selected_team = st.selectbox("Select a Team", teams)

# Filter data for the selected team
team_data = df2[(df2['team1'] == selected_team) | (df2['team2'] == selected_team)]

# Calculate wins and losses per season
team_wins = team_data[team_data['winner'] == selected_team].groupby('season').size().reset_index(name='wins')
team_losses = (
    team_data[((team_data['team1'] == selected_team) & (team_data['winner'] != selected_team)) |
              ((team_data['team2'] == selected_team) & (team_data['winner'] != selected_team))]
    .groupby('season').size().reset_index(name='losses')
)

# Merge wins and losses data
season_performance = pd.merge(team_wins, team_losses, on='season', how='outer').fillna(0)
season_performance['wins'] = season_performance['wins'].astype(int)
season_performance['losses'] = season_performance['losses'].astype(int)

# Create the grouped bar graph
fig = px.bar(
    season_performance,
    x='season',
    y=['wins', 'losses'],
    barmode='group',
    title=f"{selected_team} Wins and Losses Across Seasons",
    labels={'season': 'Season', 'value': 'Count', 'variable': 'Result'},
    template='plotly_white'
)

# Enhance the graph
fig.update_layout(
    yaxis_title="Count",
    xaxis_title="Season",
    legend_title="Result",
    xaxis=dict(type='category'),
    bargap=0.15
)

# Display the graph
st.plotly_chart(fig, use_container_width=True)

# Winners pie chart

# Set up the Streamlit app
st.title("IPL Final Winners Distribution")

# Filter data for finals only
final_matches = df2[df2['match_type'] == 'Final']

# Calculate the number of wins for each team
final_winners = final_matches['winner'].value_counts().reset_index()
final_winners.columns = ['Team', 'Wins']

# Create the pie chart
fig = px.pie(
    final_winners,
    names='Team',
    values='Wins',
    title="Distribution of IPL Final Winners",
    color_discrete_sequence=px.colors.qualitative.Set2,
    template='plotly_white'
)

# Enhance the chart
fig.update_traces(textinfo='percent+label', pull=[0.1 if i == 0 else 0 for i in range(len(final_winners))])

# Display the chart
st.plotly_chart(fig, use_container_width=True)

# venue vs wins and losses

# Set up the Streamlit app
st.title("Grouped Bar Chart: Wins and Losses by Venue")

# Calculate wins and losses by venue
wins_by_venue = df3[df3['result'] == 1].groupby('venue').size().reset_index(name='wins')
losses_by_venue = df3[df3['result'] == 0].groupby('venue').size().reset_index(name='losses')

# Merge the wins and losses into a single dataframe
venue_data = pd.merge(wins_by_venue, losses_by_venue, on='venue', how='outer').fillna(0)

# Create the grouped bar chart
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=venue_data['venue'],
        y=venue_data['wins'],
        name='Wins',
        marker_color='green'
    )
)

fig.add_trace(
    go.Bar(
        x=venue_data['venue'],
        y=venue_data['losses'],
        name='Losses',
        marker_color='red'
    )
)

# Customize layout
fig.update_layout(
    title="Wins and Losses by Venue",
    xaxis_title="Venue",
    yaxis_title="Number of Matches",
    barmode='group',
    xaxis=dict(tickangle=45),
    template='plotly_white',
    height=700
)

# Display the chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<center><p style='color: #FFEB3B;'>© 2025 IPL Analysis & Prediction App | Made with 💜 for Cricket Fans by DataTinker</p></center>",
    unsafe_allow_html=True
)