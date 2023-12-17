import streamlit as st

def user_engagement_report(telecom_analysis):
    user_engagement_data = telecom_analysis.aggregate_engagement_metrics_per_customer()
    normalized_user_engagement = telecom_analysis.normalize_engagement_metrics(user_engagement_data)
    clustered_user_engagement = telecom_analysis.k_means_clustering(normalized_user_engagement, k=3)
    cluster_metrics = telecom_analysis.analyze_clusters_metrics(clustered_user_engagement)

    st.header("User Engagement Metrics")
    st.write("Aggregate engagement metrics per customer:")
    st.write(user_engagement_data.head(10))
    st.header("User Engagement Metrics")
    st.write("Aggregate engagement metrics per customer:")
    st.write(user_engagement_data.head(10))

    # ... (other sections of the user engagement report)

def application_engagement_report(telecom_analysis, data):
    user_traffic_per_app = telecom_analysis.aggregate_user_traffic_per_application(data)

    st.header("Application Engagement")
    st.write("User total traffic per application:")
    st.write(user_traffic_per_app.head(10))

    # ... (other sections of the application engagement report)

def k_means_clustering_report(telecom_analysis, data):
    normalized_user_engagement = telecom_analysis.normalize_engagement_metrics(data)
    optimal_k = telecom_analysis.elbow_method_optimal_k(normalized_user_engagement)

    st.header("K-means Clustering")
    st.write(f"Optimal K for K-means clustering using the elbow method: {optimal_k}")

    # ... (other sections of the k-means clustering report)

