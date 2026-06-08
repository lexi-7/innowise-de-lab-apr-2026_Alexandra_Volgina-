
import pandas as pd
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'ecomarket',
    'user': 'postgres',
    'password': 'postgres'
}

DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
CSV_PATH = "/Users/denisvolgin/Documents/source"
BRONZE_SCHEMA = "bronze"

# Drop tables in reverse order
DROP_TABLES_ORDER = [
    'bronze_sales', 'bronze_employees', 'bronze_customers',
    'bronze_shops', 'bronze_products', 'bronze_cities',
    'bronze_categories', 'bronze_countries'
]

# Create table statements with correct schema
CREATE_TABLE_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS bronze.bronze_countries (
        country_id INTEGER PRIMARY KEY,
        country_name VARCHAR(100),
        country_code VARCHAR(10)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS bronze.bronze_categories (
        category_id INTEGER PRIMARY KEY,
        category_name VARCHAR(200)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS bronze.bronze_cities (
        city_id INTEGER PRIMARY KEY,
        city_name VARCHAR(100),
        zipcode VARCHAR(20),
        country_id INTEGER REFERENCES bronze.bronze_countries(country_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS bronze.bronze_products (
        product_id INTEGER PRIMARY KEY,
        product_name VARCHAR(200),
        price FLOAT,
        category_id INTEGER REFERENCES bronze.bronze_categories(category_id),
        class VARCHAR(50),
        modify_timestamp VARCHAR(50),
        resistant VARCHAR(10),
        is_allergic VARCHAR(10),
        vitality_days INTEGER
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS bronze.bronze_shops (
        shop_id INTEGER PRIMARY KEY,
        city_id INTEGER REFERENCES bronze.bronze_cities(city_id),
        address VARCHAR(500)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS bronze.bronze_employees (
        employee_id INTEGER PRIMARY KEY,
        first_name VARCHAR(100),
        middle_initial VARCHAR(10),
        last_name VARCHAR(100),
        birth_date VARCHAR(50),
        gender VARCHAR(10),
        city_id INTEGER REFERENCES bronze.bronze_cities(city_id),
        shop_id INTEGER REFERENCES bronze.bronze_shops(shop_id),
        hire_date VARCHAR(50)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS bronze.bronze_customers (
        customer_id INTEGER PRIMARY KEY,
        first_name VARCHAR(100),
        middle_initial VARCHAR(10),
        last_name VARCHAR(100),
        city_id INTEGER REFERENCES bronze.bronze_cities(city_id),
        address VARCHAR(500)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS bronze.bronze_sales (
        sales_id INTEGER PRIMARY KEY,
        employee_id INTEGER REFERENCES bronze.bronze_employees(employee_id),
        customer_id INTEGER REFERENCES bronze.bronze_customers(customer_id),
        product_id INTEGER REFERENCES bronze.bronze_products(product_id),
        quantity FLOAT,
        discount FLOAT,
        total_price FLOAT,
        sales_timestamp VARCHAR(50),
        transaction_number VARCHAR(100)
    )
    """
]

CSV_TO_TABLE = {
    'countries.csv': 'bronze_countries',
    'categories.csv': 'bronze_categories',
    'cities.csv': 'bronze_cities',
    'products.csv': 'bronze_products',
    'shops.csv': 'bronze_shops',
    'employees.csv': 'bronze_employees',
    'customers.csv': 'bronze_customers',
    'sales.csv': 'bronze_sales'
}

LOAD_ORDER = [
    'countries.csv', 'categories.csv', 'cities.csv',
    'products.csv', 'shops.csv', 'employees.csv',
    'customers.csv', 'sales.csv'
]

def create_schema(engine):
    with engine.connect() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {BRONZE_SCHEMA}"))
        conn.commit()
    logger.info(f"Schema '{BRONZE_SCHEMA}' ready")

def drop_tables(engine):
    with engine.connect() as conn:
        for table_name in DROP_TABLES_ORDER:
            conn.execute(text(f"DROP TABLE IF EXISTS {BRONZE_SCHEMA}.{table_name} CASCADE"))
            conn.commit()
    logger.info("Tables dropped")

def create_tables(engine):
    with engine.connect() as conn:
        for stmt in CREATE_TABLE_STATEMENTS:
            conn.execute(text(stmt))
            conn.commit()
    logger.info("Tables created")

def load_csv_to_table(engine, csv_path, table_name, delimiter=';'):
    """Load CSV with semicolon delimiter"""
    try:
        logger.info(f"Loading {os.path.basename(csv_path)} -> {table_name}")
        
        # Read CSV with semicolon delimiter
        df = pd.read_csv(csv_path, delimiter=delimiter)
        
        # Clean column names (remove spaces)
        df.columns = df.columns.str.strip()
        
        logger.info(f"  Columns: {list(df.columns)}")
        logger.info(f"  Rows: {len(df)}")
        
        # Load to database
        df.to_sql(
            name=table_name,
            con=engine,
            schema=BRONZE_SCHEMA,
            if_exists='append',
            index=False,
            method='multi'
        )
        
        logger.info(f"  ✓ Loaded {len(df)} rows")
        return True, len(df)
        
    except Exception as e:
        logger.error(f"  ✗ Failed: {e}")
        return False, 0

def verify_data(engine):
    logger.info("\n" + "="*60)
    logger.info("VERIFICATION")
    logger.info("="*60)
    
    for table_name in CSV_TO_TABLE.values():
        try:
            with engine.connect() as conn:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {BRONZE_SCHEMA}.{table_name}"))
                count = result.scalar()
                logger.info(f"  {table_name}: {count:,} rows")
        except Exception as e:
            logger.error(f"  {table_name}: Error - {e}")

def main():
    logger.info("="*60)
    logger.info("ECO MARKET ETL PIPELINE - BRONZE LAYER")
    logger.info("="*60)
    
    engine = None
    
    try:
        # Connect
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connected")
        
        # Setup
        create_schema(engine)
        drop_tables(engine)
        create_tables(engine)
        
        # Load data in correct order
        logger.info("\n" + "="*60)
        logger.info("LOADING DATA (semicolon delimiter)")
        logger.info("="*60)
        
        results = {}
        for csv_file in LOAD_ORDER:
            file_path = os.path.join(CSV_PATH, csv_file)
            table_name = CSV_TO_TABLE[csv_file]
            
            if os.path.exists(file_path):
                success, rows = load_csv_to_table(engine, file_path, table_name, delimiter=';')
                results[table_name] = (success, rows)
            else:
                logger.error(f"File not found: {csv_file}")
                results[table_name] = (False, 0)
        
        # Summary
        logger.info("\n" + "="*60)
        logger.info("LOAD SUMMARY")
        logger.info("="*60)
        
        success_count = 0
        for table_name, (success, rows) in results.items():
            if success:
                logger.info(f"✓ {table_name}: {rows:,} rows")
                success_count += 1
            else:
                logger.error(f"✗ {table_name}: FAILED")
        
        logger.info(f"\nSuccess: {success_count}/{len(results)} tables")
        
        # Verify
        verify_data(engine)
        
        logger.info("\n" + "="*60)
        logger.info("ETL PIPELINE COMPLETE")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise
    finally:
        if engine:
            engine.dispose()

if __name__ == "__main__":
    main()
