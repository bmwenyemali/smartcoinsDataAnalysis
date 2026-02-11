# Power BI Dashboard Guide - SmartCoins Analysis

## Instructions for Creating an Interactive Dashboard

---

## Overview

This document provides step-by-step instructions for creating a comprehensive Power BI dashboard for the SmartCoins cryptocurrency analysis project. The dashboard will showcase data visualization and business intelligence skills.

---

## Data Source Setup

### Option 1: Connect to CSV File

1. Open Power BI Desktop
2. Click "Get Data" > "Text/CSV"
3. Navigate to: `output/data/smartcoins_analyzed.csv`
4. Click "Load"

### Option 2: Connect to SQLite Database

1. Click "Get Data" > "Database" > "ODBC"
2. Use SQLite ODBC driver to connect to: `output/data/smartcoins.db`
3. Select the "coins" table

### Option 3: Web API (Real-time)

1. Click "Get Data" > "Web"
2. Enter URL: `https://smartcoinsapp.com/api/coins`
3. Transform JSON data in Power Query

---

## Data Model Preparation

### Step 1: Transform Data in Power Query

```
1. Open Power Query Editor (Transform Data)
2. Create the following calculated columns:
```

### Calculated Columns to Add:

```DAX
// Price Category
Price_Category =
IF([price_usd] >= 100, "High (>$100)",
IF([price_usd] >= 1, "Medium ($1-$100)",
IF([price_usd] >= 0.001, "Low ($0.001-$1)", "Micro (<$0.001)")))

// Risk Category
Risk_Category =
IF([risk_score] <= 30, "Low Risk",
IF([risk_score] <= 60, "Medium Risk", "High Risk"))

// Signal Color
Signal_Color =
SWITCH([primary_signal],
    "STRONG_BUY", "#00AA00",
    "BUY", "#66CC66",
    "HOLD", "#FFCC00",
    "SELL", "#FF6666",
    "STRONG_SELL", "#CC0000",
    "#808080")
```

---

## Dashboard Pages Design

### Page 1: Executive Overview

#### Header Section:

- **Title**: "SmartCoins Investment Analysis Dashboard"
- **Subtitle**: "Real-time Cryptocurrency Market Intelligence"
- **Date filter**: Slicer for date range

#### KPI Cards (Top Row):

Create 6 card visuals showing:

1. Total Coins Analyzed - COUNT(coins)
2. STRONG_BUY Count - CALCULATE(COUNT(coins), primary_signal = "STRONG_BUY")
3. Average Investment Score - AVERAGE(investment_score)
4. Average Risk Score - AVERAGE(risk_score)
5. CRYPTO Count - CALCULATE(COUNT(coins), coin_type = "crypto")
6. MEME Count - CALCULATE(COUNT(coins), coin_type = "meme")

#### Main Visualizations:

1. **Pie Chart** - Distribution by Coin Type
   - Values: Count of coins
   - Legend: coin_type

2. **Bar Chart** - Top 10 Coins by Investment Score
   - Y-axis: coin_name
   - X-axis: investment_score
   - Sort: Descending
   - Data labels: ON

3. **Donut Chart** - Signal Distribution
   - Values: Count
   - Legend: primary_signal
   - Colors: Use Signal_Color column

4. **Clustered Bar Chart** - Avg Scores by Coin Type
   - Categories: coin_type
   - Values: AVG(investment_score), AVG(risk_score)

---

### Page 2: Top N Analysis

#### Slicers (Left Panel):

1. Top N Slider (5-50)
2. Coin Type filter (crypto/meme)
3. Signal filter (multi-select)

#### Visualizations:

1. **Table** - Top N Coins Detail
   - Columns: Rank, coin_name, symbol, investment_score, risk_score, primary_signal, price_usd
   - Conditional formatting: Green for STRONG_BUY
   - Sort by investment_score DESC

2. **Horizontal Bar Chart** - Top N by Momentum Score
3. **Horizontal Bar Chart** - Top N Lowest Risk

4. **Scatter Chart** - Investment Score vs Risk Score
   - X-axis: investment_score
   - Y-axis: risk_score
   - Size: overall_score
   - Color: coin_type
   - Tooltips: coin_name, symbol, primary_signal

---

### Page 3: Risk Analysis

#### Visualizations:

1. **Matrix** - Risk Profile by Coin Type
   - Rows: coin_type
   - Columns: risk_level
   - Values: Count, AVG(investment_score)

2. **Gauge Charts**:
   - Average Volatility Risk
   - Average Liquidity Risk
   - Average Concentration Risk

3. **Scatter Plot** - Volatility vs Momentum
   - X-axis: price_volatility
   - Y-axis: change_momentum
   - Color: primary_signal

4. **Table** - Lowest Risk Opportunities
   - Filters: risk_level = "Low Risk"
   - Columns: coin_name, risk_score, volatility_risk, investment_score

---

### Page 4: Momentum & Signals

#### Visualizations:

1. **Stacked Bar Chart** - Signal Distribution by Platform
   - X-axis: platform
   - Y-axis: Count
   - Legend: primary_signal

2. **Scatter Chart** - Momentum Analysis
   - X-axis: change_momentum
   - Y-axis: momentum_consistency
   - Size: investment_score
   - Color: momentum_category

3. **Gauge** - Average Signal Strength
   - Value: AVG(signal_strength)
   - Min: 0, Max: 100

4. **Waterfall Chart** - Price Change Analysis (Selected Coins)

---

### Page 5: Platform Analysis

#### Visualizations:

1. **Treemap** - Coins by Platform
   - Group: platform
   - Values: Count
   - Color: AVG(investment_score)

2. **Bar Chart** - Platform Performance
   - Y-axis: platform
   - X-axis: AVG(investment_score)
   - Sort: Descending

3. **Table** - Platform Summary Statistics
   - Columns: platform, coin_count, avg_investment_score, bullish_count, bullish_pct

---

## Navigation Menu Setup

### Create Bookmarks for each page:

1. Go to View > Bookmarks
2. Create bookmark for each page view
3. Add navigation buttons with Bookmark actions

### Button Setup:

1. Insert > Buttons > Blank
2. Set Action: Page Navigation or Bookmark
3. Style buttons to match theme

---

## Measures (DAX Formulas)

```DAX
// Total Coins
Total Coins = COUNT(coins[symbol])

// Strong Buy Percentage
Strong Buy % =
DIVIDE(
    CALCULATE(COUNT(coins[symbol]), coins[primary_signal] = "STRONG_BUY"),
    COUNT(coins[symbol]),
    0
) * 100

// Average Risk Adjusted Score
Avg Risk Adjusted Score =
DIVIDE(AVERAGE(coins[investment_score]), AVERAGE(coins[risk_score]), 0)

// Bullish Coins Count
Bullish Coins =
CALCULATE(
    COUNT(coins[symbol]),
    coins[primary_signal] IN {"STRONG_BUY", "BUY"}
)

// Top N Function
Top N Investment Score =
RANKX(ALL(coins), coins[investment_score], , DESC)

// Crypto vs Meme Comparison
Crypto Avg Score =
CALCULATE(AVERAGE(coins[investment_score]), coins[coin_type] = "crypto")

Meme Avg Score =
CALCULATE(AVERAGE(coins[investment_score]), coins[coin_type] = "meme")

// Dynamic Top N Filter
Selected Top N = SELECTEDVALUE('Top N Table'[Top N Value], 10)

// Conditional Signal Color
Signal Background =
SWITCH(
    SELECTEDVALUE(coins[primary_signal]),
    "STRONG_BUY", "#00AA00",
    "BUY", "#66CC66",
    "HOLD", "#FFCC00",
    "SELL", "#FF6666",
    "STRONG_SELL", "#CC0000",
    "#FFFFFF"
)
```

---

## Color Theme

### Recommended Color Palette:

- Primary: #1E3A5F (Dark Blue)
- Secondary: #3498DB (Light Blue)
- Success/Buy: #27AE60 (Green)
- Warning/Hold: #F1C40F (Yellow)
- Danger/Sell: #E74C3C (Red)
- Background: #F5F6FA (Light Gray)
- Text: #2C3E50 (Dark Gray)

### Apply Theme:

1. View > Themes > Customize current theme
2. Set background, text, and accent colors
3. Save as custom theme

---

## Interactivity Setup

### Cross-filtering:

- Enable cross-highlighting between visuals
- Set interactions for slicers to affect all visuals

### Drill-through:

1. Create "Coin Details" page
2. Add drill-through field: coin_name
3. Add detailed metrics for selected coin

### Tooltips:

1. Create custom tooltip pages
2. Include detailed metrics
3. Apply to charts

---

## Export and Sharing

### Publish to Power BI Service:

1. File > Publish > Publish to Power BI
2. Select workspace
3. Share dashboard link

### Export Options:

- Export to PDF
- Export to PowerPoint
- Export data to Excel

---

## Final Checklist

- [ ] All 5 pages created with navigation
- [ ] Slicers connected and working
- [ ] KPI cards displaying correctly
- [ ] Cross-filtering enabled
- [ ] Custom theme applied
- [ ] Mobile layout created
- [ ] Bookmarks for navigation
- [ ] Report published to service
- [ ] Dashboard sharing configured

---

## Screenshots to Capture

For the project portfolio, capture screenshots of:

1. Executive Overview page
2. Top N Analysis with filters applied
3. Scatter plot showing outliers
4. Risk Analysis dashboard
5. Mobile view layout

Save screenshots to: `powerbi_screenshots/` folder

---

_Created for SmartCoins Data Analysis Portfolio Project_
_Author: [Your Name]_
_Date: February 2026_
