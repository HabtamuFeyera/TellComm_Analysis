import pandas as pd
import seaborn as sns
import numpy as np
import psycopg2
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sklearn.cluster import KMeans

class UserExperienceAnalysis:
    def __init__(self, db_params):
        self.db_params = db_params
        self.mydata = self.load_data_from_database()

    def load_data_from_database(self):
        # Create a SQLAlchemy engine
        engine = create_engine(f'postgresql+psycopg2://{self.db_params["user"]}:{self.db_params["password"]}@{self.db_params["host"]}:{self.db_params["port"]}/{self.db_params["dbname"]}')

        # SQL query to retrieve data
        sql_query = "SELECT * FROM xdr_data;"

        # Read data from PostgreSQL into a DataFrame
        mydata = pd.read_sql_query(sql_query, engine)
        return mydata
    def clean_and_preprocess(self):
        # Use .loc to avoid SettingWithCopyWarning
        cleaned_data = self.mydata.dropna()
        cleaned_data['Start'] = pd.to_datetime(cleaned_data['Start'], errors='coerce')
        cleaned_data['End'] = pd.to_datetime(cleaned_data['End'], errors='coerce')
        numeric_columns = cleaned_data.select_dtypes(include='number').columns
        cleaned_data.loc[:, numeric_columns] = cleaned_data.loc[:, numeric_columns].fillna(cleaned_data[numeric_columns].mean())
        return cleaned_data

    def perform_user_experience_analysis(self):
        user_experience_metrics = pd.DataFrame({'MSISDN/Number': self.mydata['MSISDN/Number'].unique()})
        user_experience_metrics['AvgTCPRetransmission'] = self.aggregate_average_tcp_retransmission()['TCP DL Retrans. Vol (Bytes)']
        user_experience_metrics['AvgRTT'] = self.aggregate_average_rtt()['Avg RTT DL (ms)']
        user_experience_metrics['HandsetType'] = self.get_handset_type()['Handset Type']
        user_experience_metrics['SimpleTCPThroughput'] = self.calculate_simple_tcp_throughput()['SimpleTCPThroughput']

        return user_experience_metrics

    def aggregate_average_tcp_retransmission(self):
        return self.mydata.groupby('MSISDN/Number')['TCP DL Retrans. Vol (Bytes)'].mean().reset_index()

    def aggregate_average_rtt(self):
        return self.mydata.groupby('MSISDN/Number')['Avg RTT DL (ms)'].mean().reset_index()

    def get_handset_type(self):
        return self.mydata.groupby('MSISDN/Number')['Handset Type'].first().reset_index()

    def calculate_simple_tcp_throughput(self):
        # Example: Assuming columns 'TCP DL Retrans. Vol (Bytes)' and 'Avg Bearer TP DL (kbps)' for simplicity
        throughput = self.mydata['Avg Bearer TP DL (kbps)'] / (self.mydata['TCP DL Retrans. Vol (Bytes)'] + 1)
        return pd.DataFrame({'MSISDN/Number': self.mydata['MSISDN/Number'], 'SimpleTCPThroughput': throughput})

# Database connection parameters
db_params = {
    'dbname': 'week1',
    'user': 'postgres',
    'password': 'habte',
    'host': 'localhost',
    'port': '5432'
}

#user_experience_analysis = UserExperienceAnalysis(mydata)

# Perform user experience analysis
#user_experience_metrics = user_experience_analysis.perform_user_experience_analysis()

# Display the aggregated metrics
#print(user_experience_metrics)





