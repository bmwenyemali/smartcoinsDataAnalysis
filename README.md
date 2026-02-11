# SmartCoins Data Analysis Project

A comprehensive data analytics portfolio project demonstrating Python, SQL, and Power BI skills through cryptocurrency market analysis.

## Project Overview

This project analyzes cryptocurrency data from the SmartCoins App API to provide investment insights, risk assessments, and market intelligence. It showcases end-to-end data analytics capabilities including data extraction, cleaning, statistical analysis, custom scoring algorithms, and interactive visualizations.

## Data Source

- **API:** https://smartcoinsapp.com/api/coins
- **Application:** SmartCoins App
- **Data:** Real-time cryptocurrency market data including prices, volumes, signals, and investment metrics

## Features

### Python Analysis (smartcoins_analysis.py)

- REST API data extraction using `requests`
- Data cleaning and preprocessing with `pandas`
- Statistical analysis using `scipy.stats`
- Custom scoring algorithms (Investment Score, Risk Score, Momentum Score)
- Signal prediction (STRONG_BUY, BUY, HOLD, SELL, STRONG_SELL)
- Outlier detection (Z-score and IQR methods)
- Data visualization with `matplotlib` and `seaborn`
- Export to CSV and SQLite database

### SQL Analysis (smartcoins_sql_analysis.sql)

- 50+ analytical queries
- Basic and advanced aggregations
- Window functions (RANK, ROW_NUMBER, NTILE)
- Common Table Expressions (CTEs)
- Cross-tabulations and pivot-style queries
- Data quality validation
- Business intelligence reporting

### Power BI Dashboard

- 5-page interactive dashboard
- KPI cards and distribution charts
- Top N analysis with dynamic slicers
- Risk analysis visualizations
- Cross-filtering and drill-through capabilities
- Custom DAX measures

## Project Structure

```
SmartCoinsDA/
├── smartcoins_analysis.py      # Main Python analysis script
├── smartcoins_sql_analysis.sql # SQL queries for data analysis
├── PowerBI_Dashboard_Guide.md  # Power BI creation instructions
├── Project_Report.md           # Comprehensive project report
├── Presentation_Outline.md     # PowerPoint presentation outline
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
└── output/                     # Generated outputs
    ├── data/
    │   ├── smartcoins_analyzed.csv
    │   ├── smartcoins.db
    │   ├── top_coins.csv
    │   ├── summary_statistics.csv
    │   └── correlation_matrix.csv
    ├── charts/
    │   ├── 01_score_distributions.png
    │   ├── 02_scatter_outliers.png
    │   ├── 03_category_analysis.png
    │   ├── 04_top_coins.png
    │   ├── 05_correlation_heatmap.png
    │   ├── 06_boxplots.png
    │   └── 07_momentum_comparison.png
    └── reports/
        └── analysis_report.txt
```

## Installation

### Prerequisites

- Python 3.8+
- Power BI Desktop (for dashboard)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/bmwenyemali/smartcoinsDataAnalysis.git
cd smartcoinsDataAnalysis
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Run the analysis:

```bash
python smartcoins_analysis.py
```

## Usage

### Running Python Analysis

```bash
python smartcoins_analysis.py
```

This will:

- Extract data from the SmartCoins API
- Clean and preprocess the data
- Perform statistical analysis
- Calculate custom scores
- Generate visualizations
- Export results to CSV and SQLite

### Running SQL Queries

1. Open the generated SQLite database: `output/data/smartcoins.db`
2. Execute queries from `smartcoins_sql_analysis.sql`

### Creating Power BI Dashboard

1. Follow instructions in `PowerBI_Dashboard_Guide.md`
2. Connect to `output/data/smartcoins_analyzed.csv` or `smartcoins.db`
3. Create visualizations as specified

## Key Metrics and Scores

### Investment Score

Composite score combining multiple factors to assess investment attractiveness:

- Overall Score (30%)
- Momentum Score (25%)
- Efficiency Score (20%)
- Inverted Risk Score (15%)
- MVRV Score (10%)

### Risk Score

Assessment of coin risk based on:

- Volatility Risk (35%)
- Liquidity Risk (25%)
- Concentration Risk (20%)
- Price Volatility (20%)

### Momentum Score

Measures trend strength:

- Change Momentum (40%)
- Momentum Consistency (30%)
- Momentum Acceleration (20%)
- Risk-Adjusted Momentum (10%)

## Visualizations Generated

1. **Score Distributions** - Histograms of key metrics
2. **Scatter Plots** - Relationship analysis with outlier detection
3. **Category Charts** - Distribution by coin type and signals
4. **Top Coins Rankings** - Bar charts of highest-scoring coins
5. **Correlation Heatmap** - Inter-metric relationships
6. **Box Plots** - Score comparisons across categories
7. **Momentum Comparison** - Multi-timeframe price changes

## Skills Demonstrated

| Category                  | Technologies/Skills                   |
| ------------------------- | ------------------------------------- |
| **Programming**           | Python, SQL                           |
| **Data Processing**       | pandas, numpy                         |
| **Visualization**         | matplotlib, seaborn, Power BI         |
| **Statistics**            | scipy, descriptive stats, correlation |
| **Database**              | SQLite, SQL queries                   |
| **Business Intelligence** | DAX, dashboards, reporting            |

## Results

- Analyzed 100+ cryptocurrency coins
- Identified top investment opportunities
- Detected market outliers
- Generated actionable trading signals
- Created interactive business intelligence dashboard

## Author

[Your Name]

- GitHub: https://github.com/bmwenyemali
- LinkedIn: [Your LinkedIn]
- Email: [Your Email]

## License

This project is for educational and portfolio demonstration purposes.

## Acknowledgments

- SmartCoins App for providing the API data
- Open-source communities for Python libraries

---

_Created as a Data Analytics Portfolio Project - February 2026_
