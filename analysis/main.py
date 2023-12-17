
import streamlit as st
from telecom_analysis.telecom_analysis import TelecomAnalysis, timing_decorator
from Teloader.loader import load_data
from reports.report_functions import user_engagement_report, application_engagement_report, k_means_clustering_report
from telecom_analysis import TelecomAnalysis

def main():
    db_params = {
        'dbname': 'week1',
        'user': 'postgres',
        'password': 'habte',
        'host': 'localhost',
        'port': '5432'
    }

    telecom_analysis = TelecomAnalysis(db_params)
    mydata = load_data(db_params)

    # Example usage of the new methods
    user_engagement_data = telecom_analysis.aggregate_engagement_metrics_per_customer(mydata)
    normalized_user_engagement = telecom_analysis.normalize_engagement_metrics(user_engagement_data)
    clustered_user_engagement = telecom_analysis.k_means_clustering(normalized_user_engagement, k=3)
    cluster_metrics = telecom_analysis.analyze_clusters_metrics(clustered_user_engagement)
    user_traffic_per_app = telecom_analysis.aggregate_user_traffic_per_application(mydata)

    # Display the top 10 handsets
    top_10_handsets = telecom_analysis.get_top_handsets(mydata, n=10)
    print("Top 10 Handsets Used by Customers:")
    print(top_10_handsets)

    # Display the top 3 manufacturers
    top_3_manufacturers = telecom_analysis.get_top_manufacturers(mydata, n=3)
    print("\nTop 3 Handset Manufacturers:")
    print(top_3_manufacturers)

    # Display the top 5 handsets per top 3 manufacturers
    for manufacturer in top_3_manufacturers:
        top_5_handsets_per_manufacturer = telecom_analysis.get_top_handsets_by_manufacturer(mydata, manufacturer, n=5)
        print(f"\nTop 5 Handsets for {manufacturer}:")
        print(top_5_handsets_per_manufacturer)

    # Plot the top 3 most used applications
    telecom_analysis.plot_top_applications(user_traffic_per_app, top_n=3)

    # Find optimal k for k-means clustering using elbow method
    optimal_k = telecom_analysis.elbow_method_optimal_k(normalized_user_engagement)
    print(f"\nOptimal K for k-means clustering: {optimal_k}")

if __name__ == "__main__":
    main()
