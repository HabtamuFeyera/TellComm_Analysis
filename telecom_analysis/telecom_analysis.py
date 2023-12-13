import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from timing_decorator import timing_decorator
import streamlit as st
from sqlalchemy import create_engine
from Teloader.loader import load_data


class TelecomAnalysis:
    def __init__(self, db_params):
        self.db_params = db_params
        self.mydata = self.load_data()  # Load data in the constructor

    def load_data(self):
        engine = create_engine(f'postgresql+psycopg2://{self.db_params["user"]}:{self.db_params["password"]}@{self.db_params["host"]}:{self.db_params["port"]}/{self.db_params["dbname"]}')
        sql_query = "SELECT * FROM xdr_data;"
        mydata = pd.read_sql_query(sql_query, engine)
        return mydata

    @timing_decorator
    def aggregate_engagement_metrics_per_customer(self):
        mydata = self.load_data()
        # Group by customer (MSISDN) and aggregate engagement metrics
        user_engagement = mydata.groupby('MSISDN/Number').agg({
            'Bearer Id': 'count',                  # Session frequency
            'Dur. (ms)': 'sum',                    # Total session duration
            'Total UL (Bytes)': 'sum',             # Total upload data
            'Total DL (Bytes)': 'sum'              # Total download data
        }).reset_index()

        # Rename columns for clarity
        user_engagement.rename(columns={
            'Bearer Id': 'Sessions_Frequency',
            'Dur. (ms)': 'Sessions_Duration',
            'Total UL (Bytes)': 'Total_UL_Traffic',
            'Total DL (Bytes)': 'Total_DL_Traffic'
        }, inplace=True)

        return user_engagement

    @timing_decorator
    def normalize_engagement_metrics(self):
        # Normalize engagement metrics using z-score normalization
        scaler = StandardScaler()
        normalized_data = scaler.fit_transform(self.mydata.iloc[:, 1:])  # Exclude 'MSISDN/Number' for normalization
        normalized_df = pd.DataFrame(normalized_data, columns=self.mydata.columns[1:])
        normalized_df['MSISDN/Number'] = self.mydata['MSISDN/Number']  # Add 'MSISDN/Number' back to the DataFrame

        return normalized_df

    @timing_decorator
    def k_means_clustering(self, k=3):
        # Perform k-means clustering
        kmeans = KMeans(n_clusters=k, random_state=42)
        self.mydata['Cluster'] = kmeans.fit_predict(self.mydata.iloc[:, 1:])  # Exclude 'MSISDN/Number' and 'Cluster' for clustering
        self.mydata['Cluster'] = self.mydata['Cluster'].astype(str)  # Convert cluster to string for easier plotting

    @timing_decorator
    def analyze_clusters_metrics(self):
        # Compute minimum, maximum, average, and total non-normalized metrics for each cluster
        cluster_metrics = self.mydata.groupby('Cluster').agg({
            'Sessions_Frequency': ['min', 'max', 'mean', 'sum'],
            'Sessions_Duration': ['min', 'max', 'mean', 'sum'],
            'Total_UL_Traffic': ['min', 'max', 'mean', 'sum'],
            'Total_DL_Traffic': ['min', 'max', 'mean', 'sum']
        }).reset_index()

        return cluster_metrics

    @timing_decorator
    def aggregate_user_traffic_per_application(self):
        # Aggregate user total traffic per application
        user_traffic_per_app = self.mydata.groupby('MSISDN/Number').agg({
            'Social Media DL (Bytes)': 'sum',
            'Google DL (Bytes)': 'sum',
            'Email DL (Bytes)': 'sum',
            'Youtube DL (Bytes)': 'sum',
            'Netflix DL (Bytes)': 'sum',
            'Gaming DL (Bytes)': 'sum',
            'Other DL (Bytes)': 'sum',
            'Social Media UL (Bytes)': 'sum',
            'Google UL (Bytes)': 'sum',
            'Email UL (Bytes)': 'sum',
            'Youtube UL (Bytes)': 'sum',
            'Netflix UL (Bytes)': 'sum',
            'Gaming UL (Bytes)': 'sum',
            'Other UL (Bytes)': 'sum'
        }).reset_index()

        return user_traffic_per_app

    @timing_decorator
    def plot_top_applications(self, top_n=3):
        # Plot the top N most used applications
        top_apps = self.mydata.iloc[:, 1:].sum().nlargest(top_n)
        plt.figure(figsize=(10, 6))
        top_apps.plot(kind='bar', color='skyblue')
        plt.title(f'Top {top_n} Most Used Applications')
        plt.xlabel('Application')
        plt.ylabel('Total Traffic (Bytes)')
        plt.show()
        st.pyplot()

    @timing_decorator
    def elbow_method_optimal_k(self, max_k=10):
        # Elbow method to find optimal k for k-means clustering
        distortions = []
        for k in range(1, max_k + 1):
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(self.mydata.iloc[:, 1:])
            distortions.append(kmeans.inertia_)

        # Plot the elbow curve
        plt.figure(figsize=(8, 6))
        plt.plot(range(1, max_k + 1), distortions, marker='o', linestyle='-', color='b')
        plt.title('Elbow Method for Optimal K')
        plt.xlabel('Number of Clusters (K)')
        plt.ylabel('Distortion')
        plt.show()
        st.pyplot()

        # Find optimal k using the silhouette score
        silhouette_scores = [silhouette_score(self.mydata.iloc[:, 1:], KMeans(n_clusters=k, random_state=42).fit_predict(self.mydata.iloc[:, 1:])) for k in range(2, max_k + 1)]
        optimal_k = silhouette_scores.index(max(silhouette_scores)) + 2  # Add 2 to align with the range

        return optimal_k

    def get_top_handsets(self, n=10):
        # Assuming 'Handset Type' column contains handset information
        top_handsets = self.mydata['Handset Type'].value_counts().head(n).index.tolist()
        return top_handsets

    def get_top_manufacturers(self, n=3):
        # Assuming 'Handset Manufacturer' column contains manufacturer information
        top_manufacturers = self.mydata['Handset Manufacturer'].value_counts().head(n).index.tolist()
        return top_manufacturers

    def get_top_handsets_by_manufacturer(self, manufacturer, n=5):
        # Assuming 'Handset Type' column contains handset information
        # Filter data for the specified manufacturer
        manufacturer_data = self.mydata[self.mydata['Handset Manufacturer'] == manufacturer]
        # Get the top N handsets for the specified manufacturer
        top_handsets = manufacturer_data['Handset Type'].value_counts().head(n).index.tolist()
        return top_handsets

    def main(self):
        # Example usage of the new methods
        user_engagement_data = self.aggregate_engagement_metrics_per_customer()
        normalized_user_engagement = self.normalize_engagement_metrics()
        self.k_means_clustering(k=3)
        cluster_metrics = self.analyze_clusters_metrics()
        user_traffic_per_app = self.aggregate_user_traffic_per_application()

        # Display the top 10 handsets
        top_10_handsets = self.get_top_handsets(n=10)
        print("Top 10 Handsets Used by Customers:")
        print(top_10_handsets)

        # Display the top 3 manufacturers
        top_3_manufacturers = self.get_top_manufacturers(n=3)
        print("\nTop 3 Handset Manufacturers:")
        print(top_3_manufacturers)

        # Display the top 5 handsets per top 3 manufacturers
        for manufacturer in top_3_manufacturers:
            top_5_handsets_per_manufacturer = self.get_top_handsets_by_manufacturer(manufacturer, n=5)
            print(f"\nTop 5 Handsets for {manufacturer}:")
            print(top_5_handsets_per_manufacturer)

        # Plot the top 3 most used applications
        self.plot_top_applications(top_n=3)

        # Find optimal k for k-means clustering using elbow method
        optimal_k = self.elbow_method_optimal_k(max_k=10)
        print(f"\nOptimal K for k-means clustering: {optimal_k}")

# Example usage
if __name__ == "__main__":
    db_params = {
        'dbname': 'week1',
        'user': 'postgres',
        'password': 'habte',
        'host': 'localhost',
        'port': '5432'
    }

    telecom_analysis = TelecomAnalysis(db_params)
    telecom_analysis.main()
