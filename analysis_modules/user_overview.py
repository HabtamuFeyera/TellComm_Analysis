import pandas as pd
import seaborn as sns
import numpy as np
import psycopg2
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

class UserOverviewAnalysis:
    def __init__(self, mydata):
        self.mydata = mydata

    def clean_and_preprocess(self):
        # Use .loc to avoid SettingWithCopyWarning
        cleaned_data = self.mydata.dropna()
        cleaned_data['Start'] = pd.to_datetime(cleaned_data['Start'], errors='coerce')
        cleaned_data['End'] = pd.to_datetime(cleaned_data['End'], errors='coerce')
        numeric_columns = cleaned_data.select_dtypes(include='number').columns
        cleaned_data.loc[:, numeric_columns] = cleaned_data.loc[:, numeric_columns].fillna(cleaned_data[numeric_columns].mean())
        return cleaned_data

    #def visualize_results(self):
        #sns.set_theme(style="whitegrid")
        #plt.figure(figsize=(10, 6))
        #plt.show()

    def aggregate_user_behaviour(self):
        # Assuming ''Bearer Id'' is the correct identifier for aggregation
        aggregated_data = self.mydata.groupby('Bearer Id').sum()  
        return aggregated_data
    def user_device_mapping(self):
        # Group by user identifiers and aggregate to get associated devices
        user_mapping = mydata.groupby(['IMSI', 'MSISDN/Number'])['IMEI'].unique()
        return user_mapping
    def top_10_user(self):
        # Assuming 'Total UL (Bytes)' is the column representing total upload data
        top_users = mydata.nlargest(10, 'Total UL (Bytes)')
        return top_users
    
    def application_columns(self):
        # Assuming columns like 'Social Media DL (Bytes)', 'Gaming UL (Bytes)' represent application data
        app_columns = ['Social Media DL (Bytes)', 'Gaming UL (Bytes)']
        app_usage = mydata[app_columns].sum()
        return app_usage
    
    def network_tech_distribution(self):
        # Assuming 'Bearer Id' represents network technology
        network_distribution = mydata['Bearer Id'].value_counts()
        return network_distribution

    def top_10_handsets(self):
        top_10_handsets = self.mydata['IMEI'].value_counts().nlargest(10)
        return top_10_handsets

    def top_3_manufacturers(self):
       # Convert 'IMEI' column to strings
       mydata['IMEI'] = mydata['IMEI'].astype(str)
       # Extract the manufacturer information (e.g., first 8 characters of IMEI)
       mydata['Manufacturer'] = mydata['IMEI'].str[:8]
       # Identify the top 3 handset manufacturers
       top_manufacturer = mydata['Manufacturer'].value_counts().nlargest(3)
       return top_manufacturer

    def top_5_handsets_per_manufacturer(self):
        cleaned_data = self.clean_and_preprocess()  
        cleaned_data.loc[:, 'Start'] = pd.to_datetime(cleaned_data['Start'], errors='coerce')
        cleaned_data.loc[:, 'End'] = pd.to_datetime(cleaned_data['End'], errors='coerce')
        cleaned_data.loc[:, 'IMEI'] = cleaned_data['IMEI'].astype(str)
        cleaned_data.loc[:, 'Manufacturer'] = cleaned_data['IMEI'].str[:8]
        top_manufacturers = cleaned_data.loc[:, 'Manufacturer'].value_counts().nlargest(3).index


        combined_top_handsets = pd.DataFrame()

        for manufacturer in top_manufacturers:
            manufacturer_data = cleaned_data[cleaned_data['Manufacturer'] == manufacturer]
            top_handsets = manufacturer_data['IMEI'].value_counts().nlargest(5).reset_index()
            top_handsets.columns = ['IMEI', f'Top 5 Handsets for {manufacturer}']
            combined_top_handsets = pd.concat([combined_top_handsets, top_handsets], axis=1)

        return combined_top_handsets

    #def perform_analysis(self):
        # Select numeric variables for analysis
        #numeric_variables = mydata.select_dtypes(include='number')
        # Plot histograms for each numeric variable
        #for col in numeric_variables.columns:
           # plt.figure(figsize=(8, 5))
            #sns.histplot(mydata[col], bins=20, kde=True, color='skyblue')
            #plt.title(f'Histogram of {col}')
            #plt.xlabel(col)
            #plt.ylabel('Frequency')
            #plt.show()

# Database connection parameters
db_params = {
    'dbname': 'week1',
    'user': 'postgres',
    'password': 'habte',
    'host': 'localhost',
    'port': '5432'
}

engine = create_engine(f'postgresql+psycopg2://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["dbname"]}')

sql_query = "SELECT * FROM xdr_data;"
mydata = pd.read_sql_query(sql_query, engine)


user_analysis = UserOverviewAnalysis(mydata)
#user_analysis.perform_analysis()