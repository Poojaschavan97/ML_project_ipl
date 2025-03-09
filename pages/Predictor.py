import streamlit as st
import pickle
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

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

# App title with emoji
st.title('🏏 Cricket Match Predictor')

# Decorative header
st.markdown(
    """
    <div style="text-align: center; background-color: #FFD700; padding: 10px; border-radius: 10px;">
        <h2 style="color: #000080;">🏆 Predict Your Favorite Team's Victory with Real-Time Stats! 🏆</h2>
    </div>
    """,
    unsafe_allow_html=True
)

# Load data and pipeline
with open('ipl_predictor_dataset.pkl', 'rb') as file:
    df = pickle.load(file)

with open('pipeline2.pkl', 'rb') as file:
    pipe = pickle.load(file)

# Column Transformer
trf = ColumnTransformer(
    transformers=[('trf1', OneHotEncoder(sparse_output=False, drop='first'), ['batting_team', 'bowling_team', 'venue'])],
    remainder='passthrough'
)

# Sidebar for team selection
st.sidebar.header("Match Details 🏟️")
batting_team = st.sidebar.selectbox('Select Batting Team', sorted(df['batting_team'].unique().tolist()))
bowling_team = st.sidebar.selectbox('Select Bowling Team', sorted(df['bowling_team'].unique().tolist()))

# Validation for different teams
if batting_team == bowling_team:
    st.sidebar.error("Batting team and Bowling team must be different.")
else:
    # Sidebar inputs
    venue = st.sidebar.selectbox('Venue (where the match is held)', sorted(df['venue'].unique().tolist()))
    target = st.sidebar.number_input('Target Score', min_value=1, step=1)
    runs = st.sidebar.number_input('Runs Scored', min_value=0, step=1)
    overs = st.sidebar.number_input('Overs Completed', min_value=0.0, max_value=20.0, step=0.1)
    wickets = st.sidebar.number_input('Wickets Lost', min_value=0, max_value=10, step=1)

    # Main content area
    st.markdown("### Match Summary 📋")
    st.markdown(
        f"""
        **Batting Team**: {batting_team}  
        **Bowling Team**: {bowling_team}  
        **Venue**: {venue}  
        **Target Score**: {target}  
        **Runs Scored**: {runs}  
        **Overs Completed**: {overs}  
        **Wickets Lost**: {wickets}
        """
    )

    # Prediction Button
    if st.button('🏏 Predict Outcome'):
        # Calculate derived features
        runs_left = target - runs
        balls_left = 120 - int(overs * 6)
        wickets_left = 10 - wickets
        crr = runs / overs if overs > 0 else 0  # Avoid division by zero
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0  # Avoid division by zero

        # Prepare DataFrame for Prediction
        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'venue': [venue],
            'runs_left': [runs_left],
            'ball_left': [balls_left],
            'wicket_left': [wickets_left],
            'crr': [crr],
            'rrr': [rrr]
        })

        # Predict and Display Results
        result = pipe.predict_proba(input_df)[0]  # Get probabilities
        win_prob = result[1] * 100  # Probability of winning

        # Display result with styled container
        st.markdown(
            f"""
            <div style="text-align: center; background-color: #32CD32; padding: 20px; border-radius: 10px; color: white;">
                <h2>Winning Probability: {win_prob:.2f}%</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

# Footer
st.markdown("---")
st.markdown(
    "<center><p style='color: #FFEB3B;'>© 2025 IPL Analysis & Prediction App | Made with 💜 for Cricket Fans by DataTinker</p></center>",
    unsafe_allow_html=True
)
