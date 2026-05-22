import pandas as pd
import numpy as np
import io
import warnings
warnings.filterwarnings('ignore')

def clean_redbull_data(df_raw):
    """
    Performs a series of data cleaning steps on the Red Bull sales dataset.
    """
    df = df_raw.copy()

    # --- 1. Handle Duplicate Data ---
    initial_rows = len(df)
    df = df.drop_duplicates()
    if len(df_raw) - len(df) > 0:
        print(f"✅ Removed {initial_rows - len(df)} exact duplicate rows.")
    else:
        print("✅ No exact duplicate rows found.")

    # --- 2. Handle Inconsistent Data ---
    # Region Column
    df['Region'] = df['Region'].str.strip().str.lower()
    region_mapping = {
        'th-central': 'TH-Central', 'th central': 'TH-Central',
        'thailand central': 'TH-Central', 'thailand-central': 'TH-Central',
        'thailand': 'TH-Central',
        'usa-east': 'USA-East', 'us east': 'USA-East',
        'united states east': 'USA-East', 'u.s.a.': 'USA-East',
        'europe-eu': 'Europe-EU', 'eu': 'Europe-EU',
        'europe': 'Europe-EU', 'european union': 'Europe-EU',
        'asia-pacific': 'Asia-Pacific', 'asia-pac': 'Asia-Pacific',
        'apac': 'Asia-Pacific', 'asia pacific': 'Asia-Pacific'
    }
    df['Region'] = df['Region'].replace(region_mapping)
    df['Region'] = df['Region'].str.upper()

    # Product_Variant Column
    df['Product_Variant'] = df['Product_Variant'].str.strip().str.lower()
    product_variant_mapping = {
        'original blue': 'Original Blue', 'original  blue': 'Original Blue',
        'krating daeng 250': 'Krating Daeng 250',
        'red edition': 'Red Edition',
        'sugarfree': 'Sugarfree', 'sugar free': 'Sugarfree',
        'sugarfree ': 'Sugarfree', 'sugar-free': 'Sugarfree',
        'tropical edition': 'Tropical Edition', 'tropical  edition': 'Tropical Edition',
        'tropical': 'Tropical Edition',
    }
    df['Product_Variant'] = df['Product_Variant'].replace(product_variant_mapping)

    # Channel Column
    df['Channel'] = df['Channel'].str.strip().str.lower()
    channel_mapping = {
        'social media': 'Social Media', 'social_media': 'Social Media',
        'tv ad': 'TV Ad', 'tv ads': 'TV Ad',
        'tv advertisement': 'TV Ad', 'television ad': 'TV Ad',
        'in-store promo': 'In-store Promo',
        'f1 sponsorship': 'F1 Sponsorship',
        'extreme sports': 'Extreme Sports'
    }
    df['Channel'] = df['Channel'].replace(channel_mapping)
    df['Channel'] = df['Channel'].apply(lambda x: x.title() if isinstance(x, str) else x)

    # Date Column
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')
    print("✅ Handled inconsistent data in 'Region', 'Product_Variant', 'Channel', and 'Date' columns.")

    # --- 3. Handle Missing Data ---
    missing_before_fill = df.isnull().sum().sum()
    if missing_before_fill > 0:
        median_marketing = df['Marketing_Spend'].median()
        df['Marketing_Spend'] = df['Marketing_Spend'].fillna(median_marketing)
        median_score = df['Customer_Score'].median()
        df['Customer_Score'] = df['Customer_Score'].fillna(median_score)
        print(f"✅ Filled missing values in 'Marketing_Spend' (median={median_marketing:,.2f}) and 'Customer_Score' (median={median_score}).")
    else:
        print("✅ No missing values to fill.")

    # --- 4. Handle Noisy Data ---
    initial_rows_noisy = len(df)
    df = df[df['Unit_Price'] > 0]
    df = df[df['Units_Sold'] > 0]
    df = df[df['Marketing_Spend'] >= 0]
    df = df[(df['Customer_Score'] >= 1) & (df['Customer_Score'] <= 10)]
    if initial_rows_noisy - len(df) > 0:
        print(f"✅ Removed {initial_rows_noisy - len(df)} rows containing noisy data based on business logic.")
    else:
        print("✅ No noisy data found based on business logic.")

    # --- 5. Outlier Detection (for review, not modification as per notebook) ---
    print("\n--- Outlier Detection Summary (no modification applied) ---")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    if 'Customer_Score' in numeric_cols:
        numeric_cols.remove('Customer_Score') # Handled in noisy data stage

    if numeric_cols:
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outlier_count = df[(df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))].shape[0]
            if outlier_count > 0:
                print(f"  - '{col}': {outlier_count} potential outliers detected.")
            else:
                print(f"  - '{col}': No significant outliers detected by IQR method.")
    else:
        print("  No numeric columns for outlier detection.")
    print("----------------------------------------------------------------")

    return df

# --- Main execution block ---
print("Loading redbull_workshop_dirty.csv...")

# Assuming the file 'redbull_workshop_dirty.csv' is available in the current directory
# If it's uploaded via files.upload(), you might need to adjust this to use 'filename'
try:
    df_raw_loaded = pd.read_csv('redbull_workshop_dirty.csv')
    print(f"Raw data loaded: {df_raw_loaded.shape[0]:,} rows, {df_raw_loaded.shape[1]} columns.")
except FileNotFoundError:
    print("Error: 'redbull_workshop_dirty.csv' not found. Please ensure it's uploaded.")
    # Fallback if the file was uploaded with a (1) suffix
    try:
        df_raw_loaded = pd.read_csv('redbull_workshop_dirty (1).csv')
        print(f"Raw data loaded from 'redbull_workshop_dirty (1).csv': {df_raw_loaded.shape[0]:,} rows, {df_raw_loaded.shape[1]} columns.")
    except FileNotFoundError:
        print("Fatal Error: Neither 'redbull_workshop_dirty.csv' nor 'redbull_workshop_dirty (1).csv' found.")
        df_raw_loaded = pd.DataFrame() # Create an empty DataFrame to avoid errors further down


if not df_raw_loaded.empty:
    print("\nStarting data cleaning process...")
    df_cleaned = clean_redbull_data(df_raw_loaded)

    print("\n--- Cleaning Summary ---")
    print(f"Original shape: {df_raw_loaded.shape}")
    print(f"Cleaned shape: {df_cleaned.shape}")
    print("------------------------")

    # Display first few rows of cleaned data
    print("\nFirst 5 rows of cleaned data:")
    display(df_cleaned.head())

    # Save the cleaned data
    output_filename = 'redbull_cleaned_standalone.csv'
    df_cleaned.to_csv(output_filename, index=False)
    print(f"\n✅ Cleaned data saved to '{output_filename}'")

    # Offer to download the file (Colab specific)
    from google.colab import files
    try:
        files.download(output_filename)
        print(f"Successfully downloaded '{output_filename}'.")
    except Exception as e:
        print(f"Could not initiate download for '{output_filename}': {e}")

print("\nData cleaning script finished.")
