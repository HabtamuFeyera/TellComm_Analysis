from dashboard.create_dashboard import create_dashboard
from analysis.data_preparation import load_data_from_postgres

def main():
    # Database connection parameters
    db_params = {
        'dbname': 'week1',
        'user': 'postgres',
        'password': 'habte',
        'host': 'localhost',
        'port': '5432'
    }

    # Load data from PostgreSQL
    mydata = load_data_from_postgres(db_params)

    # Create Streamlit dashboard
    create_dashboard(mydata)

if __name__ == "__main__":
    main()

