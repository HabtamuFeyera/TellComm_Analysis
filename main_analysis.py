
from analysis.data_preparation import load_data_from_postgres
from analysis.business_and_customer_overview import analyze_business_and_customer
from analysis.revenue_analysis import analyze_revenue
from analysis.profitability_analysis import analyze_profitability
from analysis.growth_opportunities import identify_growth_opportunities
from analysis.recommendations import generate_recommendations

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

    # Analyze data
    analyze_business_and_customer(mydata)
    analyze_revenue(mydata)
    analyze_profitability(mydata)
    identify_growth_opportunities(mydata)
    generate_recommendations(mydata)

if __name__ == "__main__":
    main()

