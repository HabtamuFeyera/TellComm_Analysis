import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

class UserEngagementAnalysis:
    def __init__(self, db_params):
        self.db_params = db_params
        self.mydata = self.load_data_from_database()

    def load_data_from_database(self):
        """
        Load data from the PostgreSQL database into a Pandas DataFrame.
        """
        engine = create_engine(f'postgresql+psycopg2://{self.db_params["user"]}:{self.db_params["password"]}@{self.db_params["host"]}:{self.db_params["port"]}/{self.db_params["dbname"]}')
        sql_query = "SELECT * FROM xdr_data;"
        mydata = pd.read_sql_query(sql_query, engine)
        return mydata

    def perform_analysis(self):
        """
        Perform user engagement analysis by calling various analysis functions.
        """
        self.aggregate_per_user_session_duration()
        self.aggregate_per_user_data_usage()
        self.aggregate_per_user_social_media_usage()

    def aggregate_per_user_session_duration(self):
        """
        Aggregate per user the total session duration.
        """
        result = self.mydata.groupby('MSISDN/Number')['Dur. (ms)'].sum().reset_index()
        print("Per user total session duration:")
        print(result)

    def aggregate_per_user_data_usage(self):
        """
        Aggregate per user the total download (DL) and upload (UL) data.
        """
        data_columns = ['Total DL (Bytes)', 'Total UL (Bytes)']
        result = self.mydata.groupby('MSISDN/Number')[data_columns].sum().reset_index()
        print("Per user total download and upload data:")
        print(result)
        # Plot the distribution of data usage
        self.plot_data_usage_distribution(result, 'Data Usage Distribution')

    def aggregate_per_user_social_media_usage(self):
        """
        Aggregate per user the total data volume for Social Media.
        """
        social_media_columns = ['Social Media DL (Bytes)', 'Social Media UL (Bytes)']
        result = self.mydata.groupby('MSISDN/Number')[social_media_columns].sum().reset_index()
        print("Per user total social media usage:")
        print(result)

    def plot_data_usage_distribution(self, data, title):
        """
        Plot the distribution of data usage.
        """
        plt.figure(figsize=(10, 6))
        sns.histplot(data['Total DL (Bytes)'] + data['Total UL (Bytes)'], bins=30, kde=True, color='skyblue')
        plt.title(title)
        plt.xlabel('Total Data Usage (Bytes)')
        plt.ylabel('Frequency')
        plt.show()

# Database connection parameters
db_params = {
    'dbname': 'week1',
    'user': 'postgres',
    'password': 'habte',
    'host': 'localhost',
    'port': '5432'
}
# Create an instance of UserEngagementAnalysis with the actual database parameters
engagement_analysis = UserEngagementAnalysis(db_params)


engagement_analysis.perform_analysis()




