import streamlit as st
import numpy as np
import pandas as pd
from sklearn import datasets
from sqlalchemy import create_engine

# Database connection parameters
db_params = {
    'dbname': 'week1',
    'user': 'postgres',
    'password': 'habte',
    'host': 'localhost',
    'port': '5432'
}

# Create a SQLAlchemy engine
engine = create_engine(f'postgresql+psycopg2://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["dbname"]}')

# SQL query to retrieve data
sql_query = "SELECT * FROM xdr_data;"

# Read data from PostgreSQL into a DataFrame
mydata = pd.read_sql_query(sql_query, engine)

st.title('Welcome to Streamlit')

st.write("""
         
# Explore MLOps
  Select the best one here
         
""")
my_dataset = st.sidebar.selectbox("Select Dataset", ("Iris", "Breast Cancer", "Wine Dataset", "Custom", "PostgreSQL Data"))

if my_dataset == "Custom":
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        x = data.iloc[:, :-1].values
        y = data.iloc[:, -1].values

        st.write("Custom Dataset:")
        st.write("First 5 rows of the dataset:")
        st.write(data.head())

    else:
        st.warning("Please upload a CSV file.")
        st.stop()

elif my_dataset == "PostgreSQL Data":
    st.write("PostgreSQL Dataset:")
    st.write("First 5 rows of the dataset:")
    st.write(mydata.head())

else:
    def get_dataset(my_dataset):
        if my_dataset == "Iris":
            data = datasets.load_iris()
        elif my_dataset == "Breast Cancer":
            data = datasets.load_breast_cancer()
        else:
            data = datasets.load_wine()

        x = data.data
        y = data.target
        return x, y

    x, y = get_dataset(my_dataset)

    st.write("Shape of dataset", x.shape)
    st.write("Number of classes", len(np.unique(y)))
