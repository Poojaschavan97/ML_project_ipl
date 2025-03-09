import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="IPL Data Visualizations",
    page_icon="🏏",
    layout="centered",
    initial_sidebar_state="expanded",
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

# Title of the home page
st.markdown(
    """
    <div style="text-align: center; background-color: #FFD700; padding: 10px; border-radius: 10px;">
        <h2 style="color: #000080;">Welcome to IPL Data Visualizations! 🏏</h2>
    </div><br><br>
    """,
    unsafe_allow_html=True
)

# Brief description of the project
st.write("""
Welcome to the IPL Data Visualizations project! This application provides comprehensive insights into the Indian Premier League (IPL) through various data visualizations and predictive analyses. Explore the different sections to gain a deeper understanding of the IPL's dynamics.
""")

# Overview of subpages
st.header("Explore the Sections")

# Insights section
st.subheader("📊 Insights")
st.write("""
Dive into detailed analyses of various aspects of the IPL:
- **Basic Info**: General information about the IPL.
- **Matches Info**: Statistics and outcomes of matches.
- **Teams Info**: Performance and details of the teams.
- **Toss Analysis**: Insights into toss decisions and their impacts.
- **Players Info**: Individual player statistics and achievements.
- **Venue**: Information about match venues and their significance.
- **Winners Chart**: Historical data on IPL winners over the years.
""")

# Prediction section
st.subheader("🔮 Prediction")
st.write("""
Utilize predictive models to forecast future match outcomes and player performances based on historical data.
""")

# Visualizations section
st.subheader("📈 Visualizations")
st.write("""
Explore various visual representations of IPL data:
- **Teams Performance**: Comparative analysis of team performances.
- **Players Performance**: Visual insights into player statistics.
- **Winners**: Winners of all seasons.
- **Venue**: Venues Stats.
""")

# Navigation instructions
st.write("""
Use the navigation sidebar to access each section and delve deeper into the IPL data.
""")

# Footer
st.markdown("---")
st.markdown(
    "<center><p style='color: #FFEB3B;'>© 2025 IPL Analysis & Prediction App | Made with 💜 for Cricket Fans by DataTinker</p></center>",
    unsafe_allow_html=True
)
