import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from datetime import datetime
import logging
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# DATABASE CONFIGURATION

DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'ecomarket',
    'user': 'postgres',
    'password': 'postgres'
}

DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
BRONZE_SCHEMA = "bronze"
SILVER_SCHEMA = "silver"

# DATA QUALITY FUNCTIONS

def validate_and_fix_date(date_str):
    """
    Validate and fix date strings.
    
    Rules:
    - Try multiple date formats (YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY)
    - Replace invalid dates with 1900-01-01
    - Handle NULL values
    
    Parameters:
    date_str: Date string to validate
    
    Returns:
    datetime.date or None: Validated date or Technical Default (1900-01-01)
    """
    if pd.isna(date_str) or date_str == '':
        return pd.NaT  # Keep as NaT for now (we'll handle in the ETL)
    
    date_str = str(date_str).strip()
    
    # Try multiple date formats
    date_formats = [
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%d/%m/%Y',
        '%m/%d/%Y',
        '%d-%m-%Y',
        '%m-%d-%Y',
        '%Y%m%d'
    ]
    
    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            # Check if date is reasonable (between 1900 and 2100)
            if 1900 <= parsed_date.year <= 2100:
                return parsed_date.date()
            else:
                # Unreasonable year, return default
                return datetime(1900, 1, 1).date()
        except (ValueError, TypeError):
            continue
    
    # If all formats fail, return Technical Default
    return datetime(1900, 1, 1).date()


def fix_sales_timestamp(timestamp_str):
    """
    Fix sales timestamps by adding default time if missing.
    
    Rules:
    - If date is missing, remove the row (None)
    - If time is missing, set to 00:00:00
    - If invalid date, remove the row
    
    Parameters:
    timestamp_str: Timestamp string
    
    Returns:
    datetime or None: Fixed timestamp or None
    """
    if pd.isna(timestamp_str) or timestamp_str == '':
        return None
    
    timestamp_str = str(timestamp_str).strip()
    
    # Try to parse timestamp
    try:
        # Try standard timestamp format
        parsed = pd.to_datetime(timestamp_str)
        return parsed.to_pydatetime()
    except (ValueError, TypeError):
        # Try date-only format
        try:
            # Try to parse as date
            parsed = pd.to_datetime(timestamp_str, format='%Y-%m-%d')
            # Set time to 00:00:00
            return parsed.replace(hour=0, minute=0, second=0).to_pydatetime()
        except (ValueError, TypeError):
            try:
                # Try with slashes
                parsed = pd.to_datetime(timestamp_str, format='%d/%m/%Y')
                return parsed.replace(hour=0, minute=0, second=0).to_pydatetime()
            except (ValueError, TypeError):
                # Invalid date - return None to indicate row should be removed
                return None


def convert_to_boolean(value):
    """Convert string to boolean with proper handling."""
    if pd.isna(value):
        return False
    
    if isinstance(value, bool):
        return value
    
    if isinstance(value, str):
        value_lower = value.lower().strip()
        if value_lower in ['true', 't', 'yes', 'y', '1']:
            return True
        elif value_lower in ['false', 'f', 'no', 'n', '0']:
            return False
        else:
            return False
    
    return bool(value)

# LOAD DATA FROM BRONZE LAYER

def load_from_bronze(engine, table_name):
    """Load data from bronze layer into pandas DataFrame."""
    try:
        query = f"SELECT * FROM {BRONZE_SCHEMA}.{table_name}"
        df = pd.read_sql(query, engine)
        logger.info(f"Loaded {len(df)} rows from {table_name}")
        return df
    except Exception as e:
        logger.error(f"Failed to load {table_name}: {e}")
        return pd.DataFrame()

# TRANSFORM FUNCTIONS

def transform_countries(df):
    """Transform countries data."""
    if df.empty:
        return df
    df = df.copy()
    df['loaded_at'] = datetime.now()
    return df


def transform_cities(df):
    """Transform cities data."""
    if df.empty:
        return df
    df = df.copy()
    df['loaded_at'] = datetime.now()
    return df


def transform_categories(df):
    """Transform categories data."""
    if df.empty:
        return df
    df = df.copy()
    df['loaded_at'] = datetime.now()
    return df


def transform_products(df):
    """Transform products data with type conversions."""
    if df.empty:
        return df
    
    df = df.copy()
    
    # Convert price to numeric with 2 decimal places
    df['price'] = pd.to_numeric(df['price'], errors='coerce').round(2)
    df['price'] = df['price'].fillna(0)
    
    # Convert to boolean
    df['resistant'] = df['resistant'].apply(convert_to_boolean)
    df['is_allergic'] = df['is_allergic'].apply(convert_to_boolean)
    
    # Convert modify_timestamp to proper timestamp
    df['modify_timestamp'] = df['modify_timestamp'].apply(
        lambda x: fix_sales_timestamp(x) if not pd.isna(x) else None
    )
    
    # Convert vitality_days to integer
    df['vitality_days'] = pd.to_numeric(df['vitality_days'], errors='coerce').fillna(0).astype(int)
    
    df['loaded_at'] = datetime.now()
    return df


def transform_employees(df):
    """Transform employees data with date validation."""
    if df.empty:
        return df
    
    df = df.copy()
    
    # Validate and fix birth_date
    df['birth_date'] = df['birth_date'].apply(validate_and_fix_date)
    
    # Validate and fix hire_date
    df['hire_date'] = df['hire_date'].apply(validate_and_fix_date)
    
    # Replace NaT with 1900-01-01 for birth_date
    df['birth_date'] = df['birth_date'].fillna(pd.Timestamp('1900-01-01'))
    
    # Replace NaT with 1900-01-01 for hire_date
    df['hire_date'] = df['hire_date'].fillna(pd.Timestamp('1900-01-01'))
    
    df['loaded_at'] = datetime.now()
    return df


def transform_customers(df):
    """Transform customers data."""
    if df.empty:
        return df
    df = df.copy()
    df['loaded_at'] = datetime.now()
    return df


def transform_shops(df):
    """Transform shops data."""
    if df.empty:
        return df
    df = df.copy()
    df['loaded_at'] = datetime.now()
    return df


def transform_sales(df, employees_df):
    """
    Transform sales data with enrichment.
    
    Adds shop_id and city_id from employee data.
    Validates and fixes sales_timestamp.
    """
    if df.empty:
        return df
    
    df = df.copy()
    
    # Convert numeric columns
    numeric_cols = ['quantity', 'discount', 'total_price']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).round(2)
    
    # Fix sales_timestamp - remove rows with invalid dates
    df['sales_timestamp'] = df['sales_timestamp'].apply(fix_sales_timestamp)
    
    # Remove rows with invalid timestamps
    initial_count = len(df)
    df = df.dropna(subset=['sales_timestamp'])
    logger.info(f"Removed {initial_count - len(df)} rows with invalid sales_timestamps")
    
    # Enrich with shop_id and city_id from employees
    if not employees_df.empty:
        # Create mapping from employee_id to shop_id and city_id
        employee_mapping = employees_df[['employee_id', 'shop_id', 'city_id']].drop_duplicates()
        
        # Merge to add shop_id and city_id
        df = df.merge(
            employee_mapping,
            on='employee_id',
            how='left',
            suffixes=('', '_emp')
        )
        
        # If shop_id or city_id is missing, set to 0
        df['shop_id'] = df['shop_id'].fillna(0).astype(int)
        df['city_id'] = df['city_id'].fillna(0).astype(int)
    
    # Convert sales_timestamp to datetime
    df['sales_timestamp'] = pd.to_datetime(df['sales_timestamp'])
    
    df['loaded_at'] = datetime.now()
    return df

# LOAD TO SILVER LAYER

def load_to_silver(engine, df, table_name):
    """Load transformed data to silver layer."""
    if df.empty:
        logger.warning(f"DataFrame for {table_name} is empty, skipping load")
        return False, 0
    
    try:
        # Replace empty strings with None for integer columns
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].replace('', None)
        
        df.to_sql(
            name=table_name,
            con=engine,
            schema=SILVER_SCHEMA,
            if_exists='append',
            index=False,
            method='multi'
        )
        logger.info(f"Loaded {len(df)} rows to silver.silver_{table_name}")
        return True, len(df)
    except Exception as e:
        logger.error(f"Failed to load silver_{table_name}: {e}")
        return False, 0

# MAIN ETL PIPELINE

def main():
    """Main ETL pipeline execution."""
    logger.info("="*60)
    logger.info("SILVER LAYER ETL - DATA QUALITY & TRANSFORMATION")
    logger.info("="*60)
    
    engine = None
    
    try:
        # Connect to database
        logger.info("Connecting to PostgreSQL...")
        engine = create_engine(DATABASE_URL, echo=False)
        
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection successful")
        
        # Clear existing silver tables (optional - comment out if you want to preserve data)
        logger.info("Clearing existing silver tables...")
        with engine.connect() as conn:
            tables = [
                'silver_sales', 'silver_employees', 'silver_customers',
                'silver_products', 'silver_shops', 'silver_cities',
                'silver_countries', 'silver_categories'
            ]
            for table in tables:
                conn.execute(text(f"TRUNCATE TABLE {SILVER_SCHEMA}.{table} CASCADE"))
                conn.commit()
                logger.info(f"  Truncated {table}")
        
        # LOAD AND TRANSFORM DIMENSION TABLES
        
        logger.info("\n" + "="*60)
        logger.info("LOADING AND TRANSFORMING DIMENSION TABLES")
        logger.info("="*60)
        
        # Transform dimensions
        transform_functions = {
            'countries': transform_countries,
            'cities': transform_cities,
            'categories': transform_categories,
            'products': transform_products,
            'shops': transform_shops,
            'employees': transform_employees,
            'customers': transform_customers,
        }
        
        # First pass: load all dimensions
        dimension_dfs = {}
        for table_name, transform_func in transform_functions.items():
            logger.info(f"\nProcessing {table_name}...")
            
            # Load from bronze
            df = load_from_bronze(engine, f"bronze_{table_name}")
            
            if not df.empty:
                # Transform
                df_transformed = transform_func(df)
                
                # Load to silver
                success, rows = load_to_silver(engine, df_transformed, table_name)
                
                if success:
                    dimension_dfs[table_name] = df_transformed
                    logger.info(f"✓ {table_name}: {rows} rows loaded to silver")
                else:
                    logger.error(f"✗ {table_name}: Failed to load")
            else:
                logger.warning(f"✗ {table_name}: No data found in bronze")
        
        # LOAD AND TRANSFORM FACT TABLE (SALES)
        
        logger.info("\n" + "="*60)
        logger.info("LOADING AND TRANSFORMING FACT TABLE (SALES)")
        logger.info("="*60)
        
        # Load sales from bronze
        sales_df = load_from_bronze(engine, "bronze_sales")
        
        if not sales_df.empty:
            # Transform sales with enrichment
            employees_df = dimension_dfs.get('employees', pd.DataFrame())
            sales_transformed = transform_sales(sales_df, employees_df)
            
            # Load to silver
            success, rows = load_to_silver(engine, sales_transformed, 'sales')
            
            if success:
                logger.info(f"✓ sales: {rows} rows loaded to silver")
                
                # Show enrichment summary
                if 'shop_id' in sales_transformed.columns:
                    unique_shops = sales_transformed['shop_id'].nunique()
                    unique_cities = sales_transformed['city_id'].nunique()
                    logger.info(f"  Enrichment: {unique_shops} shops, {unique_cities} cities")
            else:
                logger.error("✗ sales: Failed to load")
        else:
            logger.warning("✗ sales: No data found in bronze")
        
        # SUMMARY
        
        logger.info("\n" + "="*60)
        logger.info("ETL PIPELINE SUMMARY")
        logger.info("="*60)
        
        # Count rows in silver tables
        with engine.connect() as conn:
            for table_name in ['silver_countries', 'silver_cities', 'silver_categories',
                              'silver_products', 'silver_shops', 'silver_employees',
                              'silver_customers', 'silver_sales']:
                try:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {SILVER_SCHEMA}.{table_name}"))
                    count = result.scalar()
                    logger.info(f"  {table_name}: {count:,} rows")
                except Exception as e:
                    logger.error(f"  {table_name}: Error - {e}")
        
        logger.info("\n" + "="*60)
        logger.info("SILVER LAYER ETL COMPLETED SUCCESSFULLY")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise
    finally:
        if engine:
            engine.dispose()
            logger.info("Database connection closed")


if __name__ == "__main__":
    main()
