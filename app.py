import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from mynote.user_overview import UserOverviewAnalysis
from mynote.user_engagement import UserEngagementAnalysis
from mynote.user_experience import UserExperienceAnalysis
from mynote.user_satisfaction import UserSatisfactionAnalysis

# Database connection parameters
db_params = {
    'dbname': 'week1',
    'user': 'postgres',
    'password': 'habte',
    'host': 'localhost',
    'port': '5432'
}

# Create an SQLAlchemy engine
engine = create_engine(f'postgresql+psycopg2://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["dbname"]}')

# SQL query to retrieve data
sql_query = "SELECT * FROM xdr_data;"

# Load data into a DataFrame
mydata = pd.read_sql_query(sql_query, engine)

# Sidebar for user input
selected_analysis = st.sidebar.selectbox("Select Analysis", ["User Overview", "User Engagement", "User Experience", "User Satisfaction"])

# Perform the selected analysis
if selected_analysis == "User Overview":
    # Assuming your analysis class accepts a DataFrame as an argument
    analysis = UserOverviewAnalysis(mydata)
elif selected_analysis == "User Engagement":
    analysis = UserEngagementAnalysis(mydata)
elif selected_analysis == "User Experience":
    analysis = UserExperienceAnalysis(mydata)
elif selected_analysis == "User Satisfaction":
    analysis = UserSatisfactionAnalysis(mydata)

# Display the analysis result
st.title(f"{selected_analysis} Analysis")
result = analysis.perform_analysis()
st.write(result)
