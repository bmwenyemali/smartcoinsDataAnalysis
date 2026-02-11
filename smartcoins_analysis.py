"""
SmartCoins Data Analysis Project
================================
Author: [Your Name]
Date: February 2026
Data Source: SmartCoins App API (https://smartcoinsapp.com/api/coins)

This comprehensive analysis demonstrates Python skills for data extraction, 
exploration, cleaning, statistical analysis, and visualization of cryptocurrency data.
"""

# =============================================================================
# IMPORTS AND CONFIGURATION
# =============================================================================
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
import json
import sqlite3
from scipy import stats
from scipy.stats import zscore
import os

# Try to import seaborn, handle version compatibility
try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except (ImportError, AttributeError):
    SEABORN_AVAILABLE = False
    print("Note: Seaborn not available, using matplotlib only")

# Configuration
warnings.filterwarnings('ignore')
try:
    plt.style.use('seaborn-v0_8-whitegrid')
except:
    try:
        plt.style.use('seaborn-whitegrid')
    except:
        plt.style.use('ggplot')

if SEABORN_AVAILABLE:
    try:
        sns.set_palette("husl")
    except:
        pass

# Create output directories
os.makedirs('output/charts', exist_ok=True)
os.makedirs('output/data', exist_ok=True)
os.makedirs('output/reports', exist_ok=True)

print("=" * 80)
print("SMARTCOINS DATA ANALYSIS PROJECT")
print("Data Source: SmartCoins App (https://smartcoinsapp.com/api/coins)")
print("Analysis Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 80)


# =============================================================================
# SECTION 1: DATA EXTRACTION FROM API
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 1: DATA EXTRACTION FROM API")
print("=" * 80)

def extract_data_from_api(api_url):
    """
    Extract cryptocurrency data from SmartCoins API.
    
    Parameters:
    -----------
    api_url : str
        The API endpoint URL
    
    Returns:
    --------
    dict : Raw JSON response from API
    """
    try:
        print(f"Fetching data from: {api_url}")
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        data = response.json()
        print(f"Successfully extracted {len(data.get('data', []))} coins")
        return data
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Extract data
API_URL = "https://smartcoinsapp.com/api/coins"
raw_data = extract_data_from_api(API_URL)

if raw_data and 'data' in raw_data:
    coins_data = raw_data['data']
    print(f"\nTotal coins retrieved: {len(coins_data)}")
else:
    print("Failed to retrieve data. Exiting...")
    exit()


# =============================================================================
# SECTION 2: DATA TRANSFORMATION AND DATAFRAME CREATION
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 2: DATA TRANSFORMATION AND DATAFRAME CREATION")
print("=" * 80)

def flatten_investment_scores(coin_data):
    """Flatten nested investment scores into main dictionary."""
    flattened = coin_data.copy()
    if 'investmentScores' in flattened:
        scores = flattened.pop('investmentScores')
        for key, value in scores.items():
            flattened[f'score_{key}'] = value
    return flattened

# Flatten all coin data
flattened_data = [flatten_investment_scores(coin) for coin in coins_data]

# Create DataFrame
df = pd.DataFrame(flattened_data)

# Select and rename important columns
important_columns = {
    'name': 'coin_name',
    'symbol': 'symbol',
    'price': 'price_usd',
    'marketCap': 'market_cap',
    'volume24h': 'volume_24h',
    'volumeChange24h': 'volume_change_24h',
    'percentChange1h': 'pct_change_1h',
    'percentChange24h': 'pct_change_24h',
    'percentChange7d': 'pct_change_7d',
    'percentChange30d': 'pct_change_30d',
    'percentChange60d': 'pct_change_60d',
    'percentChange90d': 'pct_change_90d',
    'coinType': 'coin_type',
    'platform': 'platform',
    'category': 'category',
    'primarySignal': 'primary_signal',
    'signalStrength': 'signal_strength',
    'overallScore': 'overall_score',
    'compositeScore': 'composite_score',
    'changeMomentum': 'change_momentum',
    'momentumAcceleration': 'momentum_acceleration',
    'riskAdjustedMomentum': 'risk_adjusted_momentum',
    'priceVolatility': 'price_volatility',
    'volatilityRisk': 'volatility_risk',
    'liquidityRisk': 'liquidity_risk',
    'concentrationRisk': 'concentration_risk',
    'nvtScore': 'nvt_score',
    'mvrvScore': 'mvrv_score',
    'scarcityScore': 'scarcity_score',
    'efficiencyScore': 'efficiency_score',
    'momentumConsistency': 'momentum_consistency',
    'score_momentum': 'inv_momentum_score',
    'score_value': 'inv_value_score',
    'score_risk': 'inv_risk_score',
    'score_activity': 'inv_activity_score',
    'score_network': 'inv_network_score',
    'dateAdded': 'date_added',
    'lastUpdated': 'last_updated',
    'maxSupply': 'max_supply',
    'circulatingSupply': 'circulating_supply',
    'totalSupply': 'total_supply',
    'annualInflation': 'annual_inflation',
    'stockToFlow': 'stock_to_flow'
}

# Rename columns that exist
existing_cols = {k: v for k, v in important_columns.items() if k in df.columns}
df_clean = df[list(existing_cols.keys())].rename(columns=existing_cols)

print(f"\nDataFrame created with {len(df_clean)} rows and {len(df_clean.columns)} columns")
print("\nColumn names:")
print(df_clean.columns.tolist())


# =============================================================================
# SECTION 3: DATA EXPLORATION AND INITIAL ANALYSIS
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 3: DATA EXPLORATION AND INITIAL ANALYSIS")
print("=" * 80)

def explore_data(dataframe):
    """Comprehensive data exploration function."""
    print("\n--- DataFrame Shape ---")
    print(f"Rows: {dataframe.shape[0]}, Columns: {dataframe.shape[1]}")
    
    print("\n--- Data Types ---")
    print(dataframe.dtypes)
    
    print("\n--- First 5 Rows ---")
    print(dataframe.head())
    
    print("\n--- Basic Statistics ---")
    print(dataframe.describe())
    
    print("\n--- Missing Values ---")
    missing = dataframe.isnull().sum()
    missing_pct = (missing / len(dataframe)) * 100
    missing_df = pd.DataFrame({'Missing Count': missing, 'Missing %': missing_pct})
    print(missing_df[missing_df['Missing Count'] > 0])
    
    return missing_df

missing_report = explore_data(df_clean)


# =============================================================================
# SECTION 4: DATA CLEANING AND PREPROCESSING
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 4: DATA CLEANING AND PREPROCESSING")
print("=" * 80)

def clean_data(dataframe):
    """
    Clean and preprocess the cryptocurrency dataframe.
    
    Steps:
    1. Handle missing values
    2. Convert data types
    3. Remove duplicates
    4. Handle outliers
    5. Create derived features
    """
    df_cleaned = dataframe.copy()
    
    # 1. Handle missing values
    print("\n--- Handling Missing Values ---")
    
    # Fill numeric columns with 0 or median based on context
    numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        missing_count = df_cleaned[col].isnull().sum()
        if missing_count > 0:
            if 'score' in col.lower() or 'risk' in col.lower():
                df_cleaned[col].fillna(df_cleaned[col].median(), inplace=True)
                print(f"  {col}: Filled {missing_count} missing values with median")
            else:
                df_cleaned[col].fillna(0, inplace=True)
                print(f"  {col}: Filled {missing_count} missing values with 0")
    
    # Fill categorical columns
    categorical_cols = ['coin_type', 'platform', 'category', 'primary_signal']
    for col in categorical_cols:
        if col in df_cleaned.columns:
            df_cleaned[col].fillna('Unknown', inplace=True)
    
    # 2. Convert date columns
    print("\n--- Converting Date Columns ---")
    date_cols = ['date_added', 'last_updated']
    for col in date_cols:
        if col in df_cleaned.columns:
            df_cleaned[col] = pd.to_datetime(df_cleaned[col], errors='coerce')
            print(f"  Converted {col} to datetime")
    
    # 3. Remove duplicates
    print("\n--- Removing Duplicates ---")
    initial_len = len(df_cleaned)
    df_cleaned = df_cleaned.drop_duplicates(subset=['symbol'], keep='first')
    print(f"  Removed {initial_len - len(df_cleaned)} duplicate records")
    
    # 4. Create derived features
    print("\n--- Creating Derived Features ---")
    
    # Price tier classification
    def classify_price_tier(price):
        if pd.isna(price) or price == 0:
            return 'Micro'
        elif price < 0.001:
            return 'Micro'
        elif price < 1:
            return 'Low'
        elif price < 100:
            return 'Medium'
        else:
            return 'High'
    
    df_cleaned['price_tier'] = df_cleaned['price_usd'].apply(classify_price_tier)
    print("  Created price_tier classification")
    
    # Momentum category
    def classify_momentum(momentum):
        if pd.isna(momentum):
            return 'Neutral'
        elif momentum < 0.8:
            return 'Bearish'
        elif momentum < 1.2:
            return 'Neutral'
        elif momentum < 2:
            return 'Bullish'
        else:
            return 'Strong Bullish'
    
    df_cleaned['momentum_category'] = df_cleaned['change_momentum'].apply(classify_momentum)
    print("  Created momentum_category classification")
    
    # Risk level classification
    def classify_risk(volatility_risk):
        if pd.isna(volatility_risk):
            return 'Unknown'
        elif volatility_risk < 1:
            return 'Low Risk'
        elif volatility_risk < 3:
            return 'Medium Risk'
        else:
            return 'High Risk'
    
    df_cleaned['risk_level'] = df_cleaned['volatility_risk'].apply(classify_risk)
    print("  Created risk_level classification")
    
    # Days since added
    if 'date_added' in df_cleaned.columns:
        # Handle timezone-aware vs naive datetime comparison
        now = pd.Timestamp.now(tz='UTC')
        if df_cleaned['date_added'].dt.tz is None:
            df_cleaned['days_since_added'] = (datetime.now() - df_cleaned['date_added']).dt.days
        else:
            df_cleaned['days_since_added'] = (now - df_cleaned['date_added']).dt.days
        print("  Created days_since_added feature")
    
    return df_cleaned

df_clean = clean_data(df_clean)

print(f"\nCleaned DataFrame: {len(df_clean)} rows, {len(df_clean.columns)} columns")


# =============================================================================
# SECTION 5: STATISTICAL ANALYSIS
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 5: STATISTICAL ANALYSIS")
print("=" * 80)

def perform_statistical_analysis(dataframe):
    """Perform comprehensive statistical analysis."""
    
    # 1. Descriptive Statistics
    print("\n--- Descriptive Statistics for Key Metrics ---")
    key_metrics = ['price_usd', 'volume_24h', 'overall_score', 'composite_score', 
                   'change_momentum', 'price_volatility', 'volatility_risk']
    available_metrics = [m for m in key_metrics if m in dataframe.columns]
    
    stats_df = dataframe[available_metrics].describe()
    print(stats_df)
    
    # 2. Correlation Analysis
    print("\n--- Correlation Analysis ---")
    numeric_cols = dataframe.select_dtypes(include=[np.number]).columns
    correlation_matrix = dataframe[numeric_cols].corr()
    
    # Find top correlations
    corr_pairs = []
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            col1, col2 = correlation_matrix.columns[i], correlation_matrix.columns[j]
            corr_val = correlation_matrix.iloc[i, j]
            if not pd.isna(corr_val):
                corr_pairs.append((col1, col2, corr_val))
    
    corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    print("\nTop 10 Strongest Correlations:")
    for col1, col2, corr in corr_pairs[:10]:
        print(f"  {col1} <-> {col2}: {corr:.4f}")
    
    # 3. Distribution Analysis
    print("\n--- Distribution Analysis ---")
    for col in available_metrics:
        data = dataframe[col].dropna()
        if len(data) > 0:
            skewness = stats.skew(data)
            kurtosis = stats.kurtosis(data)
            print(f"\n  {col}:")
            print(f"    Mean: {data.mean():.4f}")
            print(f"    Median: {data.median():.4f}")
            print(f"    Std Dev: {data.std():.4f}")
            print(f"    Skewness: {skewness:.4f}")
            print(f"    Kurtosis: {kurtosis:.4f}")
    
    # 4. Group Statistics
    print("\n--- Group Statistics by Coin Type ---")
    if 'coin_type' in dataframe.columns:
        group_stats = dataframe.groupby('coin_type').agg({
            'price_usd': ['mean', 'median', 'count'],
            'overall_score': ['mean', 'median'],
            'change_momentum': ['mean', 'median']
        }).round(4)
        print(group_stats)
    
    print("\n--- Group Statistics by Signal ---")
    if 'primary_signal' in dataframe.columns:
        signal_stats = dataframe.groupby('primary_signal').agg({
            'overall_score': ['mean', 'count'],
            'change_momentum': 'mean',
            'volatility_risk': 'mean'
        }).round(4)
        print(signal_stats)
    
    return correlation_matrix

correlation_matrix = perform_statistical_analysis(df_clean)


# =============================================================================
# SECTION 6: CUSTOM SCORING FUNCTIONS
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 6: CUSTOM SCORING AND PREDICTION FUNCTIONS")
print("=" * 80)

def calculate_momentum_score(row):
    """
    Calculate a custom momentum score based on multiple factors.
    
    Formula considers:
    - Change momentum (40%)
    - Momentum consistency (30%)
    - Momentum acceleration (20%)
    - Risk-adjusted momentum (10%)
    """
    weights = {
        'change_momentum': 0.4,
        'momentum_consistency': 0.3,
        'momentum_acceleration': 0.2,
        'risk_adjusted_momentum': 0.1
    }
    
    score = 0
    for col, weight in weights.items():
        if col in row.index and pd.notna(row[col]):
            # Normalize the value
            if col == 'momentum_acceleration':
                # Can be negative, normalize around 0
                normalized = (row[col] + 100) / 200 * 100
            elif col == 'change_momentum':
                # Usually between 0 and 3
                normalized = min(row[col] * 33.33, 100)
            elif col == 'risk_adjusted_momentum':
                normalized = min(row[col] * 50, 100)
            else:
                normalized = min(row[col], 100)
            score += normalized * weight
    
    return round(score, 2)


def calculate_risk_score(row):
    """
    Calculate a comprehensive risk score.
    Lower score = lower risk = better.
    
    Components:
    - Volatility risk (35%)
    - Liquidity risk (25%)
    - Concentration risk (20%)
    - Price volatility (20%)
    """
    weights = {
        'volatility_risk': 0.35,
        'liquidity_risk': 0.25,
        'concentration_risk': 0.20,
        'price_volatility': 0.20
    }
    
    score = 0
    for col, weight in weights.items():
        if col in row.index and pd.notna(row[col]):
            # Normalize to 0-100
            if col == 'price_volatility':
                normalized = min(row[col] / 10, 100)
            elif col in ['volatility_risk', 'liquidity_risk', 'concentration_risk']:
                normalized = row[col]
            else:
                normalized = min(row[col], 100)
            score += normalized * weight
    
    return round(score, 2)


def calculate_investment_score(row):
    """
    Calculate an overall investment attractiveness score.
    Higher is better.
    
    Components:
    - Overall score (30%)
    - Momentum score (25%)
    - Efficiency score (20%)
    - Risk score inverted (15%)
    - MVRV score (10%)
    """
    score = 0
    
    # Overall score contribution (30%)
    if 'overall_score' in row.index and pd.notna(row['overall_score']):
        score += min(row['overall_score'] / 100, 100) * 0.3
    
    # Momentum contribution (25%)
    if 'momentum_score' in row.index and pd.notna(row['momentum_score']):
        score += row['momentum_score'] * 0.25
    
    # Efficiency score (20%)
    if 'efficiency_score' in row.index and pd.notna(row['efficiency_score']):
        score += row['efficiency_score'] * 0.2
    
    # Inverted risk (15%) - lower risk = higher score
    if 'risk_score' in row.index and pd.notna(row['risk_score']):
        score += (100 - row['risk_score']) * 0.15
    
    # MVRV score (10%)
    if 'mvrv_score' in row.index and pd.notna(row['mvrv_score']):
        score += row['mvrv_score'] * 0.1
    
    return round(score, 2)


def predict_signal(row):
    """
    Predict buy/sell signal based on custom scoring.
    
    Thresholds:
    - Strong Buy: Investment score > 70 and Momentum > 60
    - Buy: Investment score > 50 and Momentum > 40
    - Hold: Investment score > 30 or Momentum > 30
    - Sell: Investment score < 30 and high risk
    - Strong Sell: Investment score < 20 and very high risk
    """
    inv_score = row.get('investment_score', 0) or 0
    momentum = row.get('momentum_score', 0) or 0
    risk = row.get('risk_score', 100) or 100
    
    if inv_score > 70 and momentum > 60 and risk < 50:
        return 'STRONG_BUY'
    elif inv_score > 50 and momentum > 40 and risk < 70:
        return 'BUY'
    elif inv_score > 30 or momentum > 30:
        return 'HOLD'
    elif inv_score < 20 and risk > 80:
        return 'STRONG_SELL'
    else:
        return 'SELL'


def calculate_potential_return(row):
    """
    Estimate potential return based on historical patterns.
    """
    momentum = row.get('change_momentum', 1) or 1
    consistency = row.get('momentum_consistency', 50) or 50
    volatility = row.get('price_volatility', 50) or 50
    
    # Base potential from momentum
    base_potential = (momentum - 1) * 100
    
    # Adjust for consistency
    consistency_factor = consistency / 100
    
    # Risk adjustment
    risk_factor = max(0.1, 1 - (volatility / 500))
    
    potential = base_potential * consistency_factor * risk_factor
    
    return round(potential, 2)


# Apply scoring functions
print("\nCalculating custom scores...")
df_clean['momentum_score'] = df_clean.apply(calculate_momentum_score, axis=1)
print("  - Momentum Score calculated")

df_clean['risk_score'] = df_clean.apply(calculate_risk_score, axis=1)
print("  - Risk Score calculated")

df_clean['investment_score'] = df_clean.apply(calculate_investment_score, axis=1)
print("  - Investment Score calculated")

df_clean['predicted_signal'] = df_clean.apply(predict_signal, axis=1)
print("  - Predicted Signal calculated")

df_clean['potential_return'] = df_clean.apply(calculate_potential_return, axis=1)
print("  - Potential Return estimated")

# Show sample scores
print("\n--- Sample of Calculated Scores ---")
score_cols = ['coin_name', 'symbol', 'momentum_score', 'risk_score', 
              'investment_score', 'predicted_signal', 'potential_return']
print(df_clean[score_cols].head(10).to_string())


# =============================================================================
# SECTION 7: TOP N ANALYSIS
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 7: TOP N COINS ANALYSIS")
print("=" * 80)

def get_top_coins(dataframe, n=10, by='investment_score', ascending=False, 
                  coin_type=None):
    """
    Get top N coins based on specified criteria.
    
    Parameters:
    -----------
    dataframe : pd.DataFrame
    n : int - Number of coins to return
    by : str - Column to sort by
    ascending : bool - Sort order
    coin_type : str - Filter by coin type ('crypto', 'meme', or None for all)
    """
    df_filtered = dataframe.copy()
    
    if coin_type:
        df_filtered = df_filtered[df_filtered['coin_type'] == coin_type]
    
    df_sorted = df_filtered.sort_values(by=by, ascending=ascending)
    
    return df_sorted.head(n)


# Top 10 by Investment Score (All Coins)
print("\n--- Top 10 Coins by Investment Score (All) ---")
top_10_all = get_top_coins(df_clean, n=10, by='investment_score')
display_cols = ['coin_name', 'symbol', 'price_usd', 'investment_score', 
                'primary_signal', 'coin_type']
print(top_10_all[display_cols].to_string())

# Top 10 Crypto Coins
print("\n--- Top 10 Crypto Coins ---")
top_10_crypto = get_top_coins(df_clean, n=10, by='investment_score', coin_type='crypto')
print(top_10_crypto[display_cols].to_string())

# Top 10 Meme Coins
print("\n--- Top 10 Meme Coins ---")
top_10_meme = get_top_coins(df_clean, n=10, by='investment_score', coin_type='meme')
print(top_10_meme[display_cols].to_string())

# Top 10 by Momentum
print("\n--- Top 10 Coins by Momentum Score ---")
top_10_momentum = get_top_coins(df_clean, n=10, by='momentum_score')
print(top_10_momentum[['coin_name', 'symbol', 'momentum_score', 'change_momentum', 
                        'momentum_category']].to_string())

# Lowest Risk Coins
print("\n--- Top 10 Lowest Risk Coins ---")
top_10_low_risk = get_top_coins(df_clean, n=10, by='risk_score', ascending=True)
print(top_10_low_risk[['coin_name', 'symbol', 'risk_score', 'risk_level', 
                        'volatility_risk']].to_string())

# Strong Buy Signals
print("\n--- Coins with STRONG_BUY Signal ---")
strong_buy = df_clean[df_clean['primary_signal'] == 'STRONG_BUY']
print(f"Total coins with STRONG_BUY: {len(strong_buy)}")
print(strong_buy[display_cols].head(15).to_string())


# =============================================================================
# SECTION 8: DATA VISUALIZATION
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 8: DATA VISUALIZATION")
print("=" * 80)

# Set figure size
fig_size = (12, 8)

# 1. Distribution of Investment Scores
print("\n--- Creating Distribution Charts ---")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Investment Score Distribution
axes[0, 0].hist(df_clean['investment_score'].dropna(), bins=30, edgecolor='black', alpha=0.7)
axes[0, 0].set_title('Distribution of Investment Scores', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('Investment Score')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].axvline(df_clean['investment_score'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {df_clean["investment_score"].mean():.2f}')
axes[0, 0].legend()

# Risk Score Distribution
axes[0, 1].hist(df_clean['risk_score'].dropna(), bins=30, edgecolor='black', 
                alpha=0.7, color='orange')
axes[0, 1].set_title('Distribution of Risk Scores', fontsize=12, fontweight='bold')
axes[0, 1].set_xlabel('Risk Score')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].axvline(df_clean['risk_score'].mean(), color='red', linestyle='--',
                   label=f'Mean: {df_clean["risk_score"].mean():.2f}')
axes[0, 1].legend()

# Momentum Score Distribution
axes[1, 0].hist(df_clean['momentum_score'].dropna(), bins=30, edgecolor='black', 
                alpha=0.7, color='green')
axes[1, 0].set_title('Distribution of Momentum Scores', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('Momentum Score')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].axvline(df_clean['momentum_score'].mean(), color='red', linestyle='--',
                   label=f'Mean: {df_clean["momentum_score"].mean():.2f}')
axes[1, 0].legend()

# Price Distribution (log scale)
price_data = df_clean['price_usd'][df_clean['price_usd'] > 0].dropna()
axes[1, 1].hist(np.log10(price_data + 1e-10), bins=30, edgecolor='black', 
                alpha=0.7, color='purple')
axes[1, 1].set_title('Distribution of Prices (Log Scale)', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Log10(Price USD)')
axes[1, 1].set_ylabel('Frequency')

plt.tight_layout()
plt.savefig('output/charts/01_score_distributions.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: 01_score_distributions.png")


# 2. Scatter Plot - Investment Score vs Risk Score (Outlier Detection)
print("\n--- Creating Scatter Plots for Outlier Detection ---")
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# Investment vs Risk Score
axes[0, 0].scatter(df_clean['investment_score'], df_clean['risk_score'], 
                   alpha=0.6, c=df_clean['change_momentum'], cmap='RdYlGn', s=50)
axes[0, 0].set_xlabel('Investment Score', fontsize=10)
axes[0, 0].set_ylabel('Risk Score', fontsize=10)
axes[0, 0].set_title('Investment Score vs Risk Score\n(Color: Change Momentum)', 
                     fontsize=12, fontweight='bold')
cbar = plt.colorbar(axes[0, 0].collections[0], ax=axes[0, 0])
cbar.set_label('Change Momentum')

# Mark outliers (high investment, low risk - best coins)
best_coins = df_clean[(df_clean['investment_score'] > 50) & (df_clean['risk_score'] < 30)]
if len(best_coins) > 0:
    axes[0, 0].scatter(best_coins['investment_score'], best_coins['risk_score'], 
                       color='red', s=100, marker='*', label='Best Opportunities')
    axes[0, 0].legend()

# Momentum vs Volatility
axes[0, 1].scatter(df_clean['change_momentum'], df_clean['price_volatility'], 
                   alpha=0.6, s=50)
axes[0, 1].set_xlabel('Change Momentum', fontsize=10)
axes[0, 1].set_ylabel('Price Volatility', fontsize=10)
axes[0, 1].set_title('Change Momentum vs Price Volatility', 
                     fontsize=12, fontweight='bold')

# Identify outliers using IQR
Q1 = df_clean['price_volatility'].quantile(0.25)
Q3 = df_clean['price_volatility'].quantile(0.75)
IQR = Q3 - Q1
outliers = df_clean[(df_clean['price_volatility'] > Q3 + 1.5 * IQR)]
if len(outliers) > 0:
    axes[0, 1].scatter(outliers['change_momentum'], outliers['price_volatility'], 
                       color='red', s=100, marker='x', label='Volatility Outliers')
    axes[0, 1].legend()

# Overall Score vs Composite Score
axes[1, 0].scatter(df_clean['overall_score'], df_clean['composite_score'], 
                   alpha=0.6, s=50, color='green')
axes[1, 0].set_xlabel('Overall Score', fontsize=10)
axes[1, 0].set_ylabel('Composite Score', fontsize=10)
axes[1, 0].set_title('Overall Score vs Composite Score', 
                     fontsize=12, fontweight='bold')

# Add trend line
z = np.polyfit(df_clean['overall_score'].fillna(0), df_clean['composite_score'].fillna(0), 1)
p = np.poly1d(z)
x_line = np.linspace(df_clean['overall_score'].min(), df_clean['overall_score'].max(), 100)
axes[1, 0].plot(x_line, p(x_line), "r--", alpha=0.8, label='Trend Line')
axes[1, 0].legend()

# Volume vs Market Cap (for coins with data)
vol_cap = df_clean[(df_clean['volume_24h'] > 0) & (df_clean['market_cap'] > 0)]
if len(vol_cap) > 0:
    axes[1, 1].scatter(np.log10(vol_cap['volume_24h'] + 1), 
                       np.log10(vol_cap['market_cap'] + 1), 
                       alpha=0.6, s=50, color='orange')
    axes[1, 1].set_xlabel('Log10(Volume 24h)', fontsize=10)
    axes[1, 1].set_ylabel('Log10(Market Cap)', fontsize=10)
    axes[1, 1].set_title('Volume vs Market Cap (Log Scale)', 
                         fontsize=12, fontweight='bold')
else:
    axes[1, 1].text(0.5, 0.5, 'Insufficient data', ha='center', va='center')
    axes[1, 1].set_title('Volume vs Market Cap', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('output/charts/02_scatter_outliers.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: 02_scatter_outliers.png")


# 3. Category Analysis Charts
print("\n--- Creating Category Analysis Charts ---")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Coin Type Distribution
if 'coin_type' in df_clean.columns:
    coin_type_counts = df_clean['coin_type'].value_counts()
    axes[0, 0].pie(coin_type_counts.values, labels=coin_type_counts.index, 
                   autopct='%1.1f%%', startangle=90)
    axes[0, 0].set_title('Distribution by Coin Type', fontsize=12, fontweight='bold')

# Signal Distribution
if 'primary_signal' in df_clean.columns:
    signal_counts = df_clean['primary_signal'].value_counts()
    colors = ['green' if 'BUY' in s else 'red' if 'SELL' in s else 'gray' 
              for s in signal_counts.index]
    axes[0, 1].barh(signal_counts.index, signal_counts.values, color=colors)
    axes[0, 1].set_xlabel('Count')
    axes[0, 1].set_title('Distribution by Trading Signal', fontsize=12, fontweight='bold')

# Average Investment Score by Coin Type
if 'coin_type' in df_clean.columns:
    avg_score_by_type = df_clean.groupby('coin_type')['investment_score'].mean()
    axes[1, 0].bar(avg_score_by_type.index, avg_score_by_type.values, color=['blue', 'orange'])
    axes[1, 0].set_ylabel('Average Investment Score')
    axes[1, 0].set_title('Average Investment Score by Coin Type', 
                         fontsize=12, fontweight='bold')

# Risk Level Distribution
if 'risk_level' in df_clean.columns:
    risk_counts = df_clean['risk_level'].value_counts()
    colors = {'Low Risk': 'green', 'Medium Risk': 'yellow', 'High Risk': 'red', 'Unknown': 'gray'}
    bar_colors = [colors.get(r, 'blue') for r in risk_counts.index]
    axes[1, 1].bar(risk_counts.index, risk_counts.values, color=bar_colors)
    axes[1, 1].set_ylabel('Count')
    axes[1, 1].set_title('Distribution by Risk Level', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('output/charts/03_category_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: 03_category_analysis.png")


# 4. Top Coins Bar Chart
print("\n--- Creating Top Coins Charts ---")
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Top 15 by Investment Score
top_15 = df_clean.nlargest(15, 'investment_score')
colors = ['green' if t == 'crypto' else 'orange' for t in top_15['coin_type']]
bars = axes[0].barh(top_15['symbol'], top_15['investment_score'], color=colors)
axes[0].set_xlabel('Investment Score')
axes[0].set_title('Top 15 Coins by Investment Score', fontsize=12, fontweight='bold')
axes[0].invert_yaxis()

# Add value labels
for bar, score in zip(bars, top_15['investment_score']):
    axes[0].text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
                 f'{score:.1f}', va='center', fontsize=8)

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='green', label='Crypto'),
                   Patch(facecolor='orange', label='Meme')]
axes[0].legend(handles=legend_elements, loc='lower right')

# Top 15 by Momentum
top_15_mom = df_clean.nlargest(15, 'momentum_score')
bars = axes[1].barh(top_15_mom['symbol'], top_15_mom['momentum_score'], color='purple')
axes[1].set_xlabel('Momentum Score')
axes[1].set_title('Top 15 Coins by Momentum Score', fontsize=12, fontweight='bold')
axes[1].invert_yaxis()

plt.tight_layout()
plt.savefig('output/charts/04_top_coins.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: 04_top_coins.png")


# 5. Correlation Heatmap
print("\n--- Creating Correlation Heatmap ---")
score_columns = ['investment_score', 'momentum_score', 'risk_score', 'overall_score',
                 'composite_score', 'change_momentum', 'price_volatility', 
                 'efficiency_score', 'mvrv_score']
available_score_cols = [c for c in score_columns if c in df_clean.columns]

fig, ax = plt.subplots(figsize=(12, 10))
corr_matrix = df_clean[available_score_cols].corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

if SEABORN_AVAILABLE:
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdYlGn', 
                center=0, ax=ax, square=True, linewidths=0.5)
else:
    # Fallback to matplotlib imshow
    masked_corr = np.ma.masked_where(mask, corr_matrix)
    im = ax.imshow(masked_corr, cmap='RdYlGn', vmin=-1, vmax=1, aspect='auto')
    plt.colorbar(im, ax=ax)
    ax.set_xticks(range(len(available_score_cols)))
    ax.set_yticks(range(len(available_score_cols)))
    ax.set_xticklabels(available_score_cols, rotation=45, ha='right')
    ax.set_yticklabels(available_score_cols)
    # Add annotations
    for i in range(len(available_score_cols)):
        for j in range(len(available_score_cols)):
            if not mask[i, j]:
                ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}', ha='center', va='center', fontsize=8)

ax.set_title('Correlation Heatmap of Key Metrics', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('output/charts/05_correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: 05_correlation_heatmap.png")


# 6. Box Plot for Score Comparison
print("\n--- Creating Box Plots ---")
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Box plot by Coin Type
if 'coin_type' in df_clean.columns:
    df_clean.boxplot(column='investment_score', by='coin_type', ax=axes[0])
    axes[0].set_title('Investment Score by Coin Type', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('Coin Type')
    axes[0].set_ylabel('Investment Score')

# Box plot by Signal
if 'primary_signal' in df_clean.columns:
    signal_order = ['STRONG_BUY', 'BUY', 'HOLD', 'SELL', 'STRONG_SELL']
    existing_signals = [s for s in signal_order if s in df_clean['primary_signal'].values]
    df_signals = df_clean[df_clean['primary_signal'].isin(existing_signals)]
    df_signals.boxplot(column='investment_score', by='primary_signal', ax=axes[1])
    axes[1].set_title('Investment Score by Signal', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Trading Signal')
    axes[1].set_ylabel('Investment Score')

plt.suptitle('')  # Remove automatic title
plt.tight_layout()
plt.savefig('output/charts/06_boxplots.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: 06_boxplots.png")


# 7. Momentum Analysis for Selected Coins
print("\n--- Creating Momentum Comparison Chart ---")
# Select 3 representative coins for detailed momentum analysis
top_3_coins = df_clean.nlargest(3, 'overall_score')[['coin_name', 'symbol', 
    'pct_change_1h', 'pct_change_24h', 'pct_change_7d', 'pct_change_30d']]

fig, ax = plt.subplots(figsize=(12, 6))

x = np.arange(4)
width = 0.25

for i, (_, coin) in enumerate(top_3_coins.iterrows()):
    changes = [
        coin['pct_change_1h'] if pd.notna(coin['pct_change_1h']) else 0,
        coin['pct_change_24h'] if pd.notna(coin['pct_change_24h']) else 0,
        coin['pct_change_7d'] if pd.notna(coin['pct_change_7d']) else 0,
        coin['pct_change_30d'] if pd.notna(coin['pct_change_30d']) else 0
    ]
    # Cap extreme values for visualization
    changes = [min(max(c, -100), 500) for c in changes]
    bars = ax.bar(x + i*width, changes, width, label=coin['symbol'])

ax.set_ylabel('Percent Change (%)')
ax.set_title('Price Change Comparison - Top 3 Coins', fontsize=12, fontweight='bold')
ax.set_xticks(x + width)
ax.set_xticklabels(['1 Hour', '24 Hours', '7 Days', '30 Days'])
ax.legend()
ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

plt.tight_layout()
plt.savefig('output/charts/07_momentum_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print("  Saved: 07_momentum_comparison.png")


# =============================================================================
# SECTION 9: OUTLIER DETECTION AND ANALYSIS
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 9: OUTLIER DETECTION AND ANALYSIS")
print("=" * 80)

def detect_outliers(dataframe, columns, method='zscore', threshold=3):
    """
    Detect outliers using various methods.
    
    Methods:
    - zscore: Standard deviation based (default threshold: 3)
    - iqr: Interquartile range based
    - percentile: Extreme percentiles
    """
    outliers_report = {}
    
    for col in columns:
        if col not in dataframe.columns:
            continue
            
        data = dataframe[col].dropna()
        
        if method == 'zscore':
            z_scores = np.abs(stats.zscore(data))
            outlier_mask = z_scores > threshold
            outliers = dataframe.loc[data.index[outlier_mask]]
        
        elif method == 'iqr':
            Q1, Q3 = data.quantile([0.25, 0.75])
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            outlier_mask = (data < lower) | (data > upper)
            outliers = dataframe.loc[data.index[outlier_mask]]
        
        elif method == 'percentile':
            lower = data.quantile(0.01)
            upper = data.quantile(0.99)
            outlier_mask = (data < lower) | (data > upper)
            outliers = dataframe.loc[data.index[outlier_mask]]
        
        outliers_report[col] = {
            'count': len(outliers),
            'percentage': len(outliers) / len(data) * 100,
            'examples': outliers[['coin_name', 'symbol', col]].head(5) if len(outliers) > 0 else None
        }
    
    return outliers_report

# Detect outliers
outlier_columns = ['investment_score', 'risk_score', 'momentum_score', 
                   'change_momentum', 'price_volatility', 'overall_score']

print("\n--- Outlier Detection (Z-Score Method) ---")
outliers_zscore = detect_outliers(df_clean, outlier_columns, method='zscore')
for col, report in outliers_zscore.items():
    print(f"\n{col}:")
    print(f"  Outliers found: {report['count']} ({report['percentage']:.2f}%)")
    if report['examples'] is not None:
        print(f"  Examples:")
        print(report['examples'].to_string())

print("\n--- Outlier Detection (IQR Method) ---")
outliers_iqr = detect_outliers(df_clean, outlier_columns, method='iqr')
for col, report in outliers_iqr.items():
    print(f"\n{col}: {report['count']} outliers ({report['percentage']:.2f}%)")


# =============================================================================
# SECTION 10: EXPORT DATA
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 10: EXPORT DATA")
print("=" * 80)

# 1. Export to CSV
csv_path = 'output/data/smartcoins_analyzed.csv'
df_clean.to_csv(csv_path, index=False)
print(f"  Exported full dataset to: {csv_path}")

# 2. Export top coins to CSV
top_coins_path = 'output/data/top_coins.csv'
top_50 = df_clean.nlargest(50, 'investment_score')
top_50.to_csv(top_coins_path, index=False)
print(f"  Exported top 50 coins to: {top_coins_path}")

# 3. Export to SQLite database for SQL analysis
db_path = 'output/data/smartcoins.db'
conn = sqlite3.connect(db_path)
df_clean.to_sql('coins', conn, if_exists='replace', index=False)
conn.close()
print(f"  Exported to SQLite database: {db_path}")

# 4. Export summary statistics
summary_path = 'output/data/summary_statistics.csv'
summary_stats = df_clean.describe()
summary_stats.to_csv(summary_path)
print(f"  Exported summary statistics to: {summary_path}")

# 5. Export correlation matrix
corr_path = 'output/data/correlation_matrix.csv'
correlation_matrix.to_csv(corr_path)
print(f"  Exported correlation matrix to: {corr_path}")


# =============================================================================
# SECTION 11: GENERATE ANALYSIS REPORT
# =============================================================================
print("\n" + "=" * 80)
print("SECTION 11: ANALYSIS SUMMARY REPORT")
print("=" * 80)

report = f"""
================================================================================
                    SMARTCOINS DATA ANALYSIS REPORT
                    Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
================================================================================

1. DATA OVERVIEW
----------------
   Total Coins Analyzed: {len(df_clean)}
   Crypto Coins: {len(df_clean[df_clean['coin_type'] == 'crypto'])}
   Meme Coins: {len(df_clean[df_clean['coin_type'] == 'meme'])}
   
2. SIGNAL DISTRIBUTION
----------------------
{df_clean['primary_signal'].value_counts().to_string()}

3. KEY STATISTICS
-----------------
   Average Investment Score: {df_clean['investment_score'].mean():.2f}
   Median Investment Score: {df_clean['investment_score'].median():.2f}
   Average Risk Score: {df_clean['risk_score'].mean():.2f}
   Average Momentum Score: {df_clean['momentum_score'].mean():.2f}

4. TOP 5 INVESTMENT OPPORTUNITIES
---------------------------------
{df_clean.nlargest(5, 'investment_score')[['coin_name', 'symbol', 'investment_score', 'primary_signal']].to_string()}

5. TOP 5 MEME COINS
-------------------
{df_clean[df_clean['coin_type'] == 'meme'].nlargest(5, 'investment_score')[['coin_name', 'symbol', 'investment_score', 'primary_signal']].to_string()}

6. LOWEST RISK COINS (TOP 5)
----------------------------
{df_clean.nsmallest(5, 'risk_score')[['coin_name', 'symbol', 'risk_score', 'risk_level']].to_string()}

7. STRONGEST MOMENTUM (TOP 5)
-----------------------------
{df_clean.nlargest(5, 'momentum_score')[['coin_name', 'symbol', 'momentum_score', 'change_momentum']].to_string()}

8. PRICE TIER DISTRIBUTION
--------------------------
{df_clean['price_tier'].value_counts().to_string()}

9. RISK LEVEL DISTRIBUTION
--------------------------
{df_clean['risk_level'].value_counts().to_string()}

================================================================================
                              END OF REPORT
================================================================================
"""

print(report)

# Save report to file
report_path = 'output/reports/analysis_report.txt'
with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report)
print(f"\nReport saved to: {report_path}")


# =============================================================================
# SECTION 12: FINAL SUMMARY
# =============================================================================
print("\n" + "=" * 80)
print("ANALYSIS COMPLETE - FILES GENERATED")
print("=" * 80)
print("""
Output Files:
-------------
Data Files:
  - output/data/smartcoins_analyzed.csv (Full analyzed dataset)
  - output/data/top_coins.csv (Top 50 coins)
  - output/data/smartcoins.db (SQLite database for SQL analysis)
  - output/data/summary_statistics.csv
  - output/data/correlation_matrix.csv

Charts:
  - output/charts/01_score_distributions.png
  - output/charts/02_scatter_outliers.png
  - output/charts/03_category_analysis.png
  - output/charts/04_top_coins.png
  - output/charts/05_correlation_heatmap.png
  - output/charts/06_boxplots.png
  - output/charts/07_momentum_comparison.png

Reports:
  - output/reports/analysis_report.txt

Skills Demonstrated:
--------------------
- API Data Extraction (requests)
- Data Transformation (pandas)
- Data Cleaning and Preprocessing
- Statistical Analysis (scipy.stats)
- Custom Scoring Functions
- Outlier Detection
- Data Visualization (matplotlib, seaborn)
- SQL Database Export (sqlite3)
- Report Generation
""")

print("\nThank you for using SmartCoins Analysis!")
print("=" * 80)
