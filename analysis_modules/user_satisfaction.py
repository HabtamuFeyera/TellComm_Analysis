import pandas as pd
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sqlalchemy import create_engine

class UserSatisfactionAnalysis:
    engagement_columns = [
        'Dur. (ms)',
        'TCP DL Retrans. Vol (Bytes)',
        'DL TP < 50 Kbps (%)',
        '50 Kbps < DL TP < 250 Kbps (%)',
        '250 Kbps < DL TP < 1 Mbps (%)',
        'DL TP > 1 Mbps (%)',
        'Activity Duration DL (ms)',
        'Activity Duration UL (ms)',
        'Social Media DL (Bytes)',
        'Google DL (Bytes)',
        'Email DL (Bytes)',
        'Youtube DL (Bytes)',
        'Netflix DL (Bytes)',
        'Gaming DL (Bytes)',
        'Other DL (Bytes)',
        'Total UL (Bytes)',
        'Total DL (Bytes)'
    ]

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

    def perform_user_satisfaction_analysis(self):
        """
        Perform user satisfaction analysis by calculating engagement and experience scores,
        deriving a satisfaction score, identifying the top 10 satisfied customers, and clustering users.
        """
        # Calculate engagement and experience scores
        engagement_score, experience_score = self.calculate_scores()

        # Derive satisfaction score as the average of engagement and experience scores
        satisfaction_score = (engagement_score + experience_score) / 2

        # Add satisfaction score to the DataFrame
        self.mydata['SatisfactionScore'] = satisfaction_score

        # Identify the top 10 satisfied customers
        top_satisfied_customers = self.mydata.nlargest(10, 'SatisfactionScore')

        # Run k-means clustering on engagement and experience scores
        kmeans_clusters = self.run_kmeans()

        # Aggregate average satisfaction and experience scores per cluster
        cluster_aggregates = self.aggregate_scores_by_cluster(kmeans_clusters)

        return top_satisfied_customers, cluster_aggregates

    def calculate_scores(self):
        """
        Calculate engagement and experience scores based on relevant columns in the dataset.
        """
        
        engagement_score = self.mydata[self.engagement_columns].mean(axis=1)

        # Placeholder for experience score calculation
        experience_score = 0

        return engagement_score, experience_score

    def run_kmeans(self):
        """
        Run k-means clustering on engagement and experience scores.
        """
        # Impute missing values
        imputer = SimpleImputer(strategy='mean')
        kmeans_data_imputed = imputer.fit_transform(self.mydata[self.engagement_columns])

        # logic to run k-means clustering (k=2) on engagement scores
        kmeans_model = KMeans(n_clusters=2, random_state=42)
        kmeans_clusters = kmeans_model.fit_predict(kmeans_data_imputed)

        return kmeans_clusters

    def aggregate_scores_by_cluster(self, kmeans_clusters):
        """
        Aggregate average satisfaction scores per cluster.
        """
        # logic to aggregate average scores per cluster
        cluster_data = self.mydata.copy()
        cluster_data['Cluster'] = kmeans_clusters
        cluster_aggregates = cluster_data.groupby('Cluster').agg({
            'SatisfactionScore': 'mean'
        }).reset_index()

        return cluster_aggregates

# Database connection parameters
db_params = {
    'dbname': 'week1',
    'user': 'postgres',
    'password': 'habte',
    'host': 'localhost',
    'port': '5432'
}

# Create an instance of UserSatisfactionAnalysis with the actual database parameters
#satisfaction_analysis = UserSatisfactionAnalysis(db_params)

# Execute the analysis
#top_satisfied, cluster_aggregates = satisfaction_analysis.perform_user_satisfaction_analysis()

# Display the results
#print("Top 10 Satisfied Customers:")
#print(top_satisfied)

#print("\nCluster Aggregates:")
#print(cluster_aggregates)

