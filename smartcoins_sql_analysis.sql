-- =============================================================================
-- SMARTCOINS DATA ANALYSIS - SQL QUERIES
-- =============================================================================
-- Author: [Your Name]
-- Date: February 2026
-- Database: smartcoins.db (SQLite)
-- Description: Comprehensive SQL queries demonstrating data analysis skills
--              for cryptocurrency data from SmartCoins App
-- =============================================================================

-- This file contains SQL queries organized by analysis type to showcase
-- data engineering, data analysis, and business analysis skills.

-- =============================================================================
-- SECTION 1: BASIC DATA EXPLORATION
-- =============================================================================

-- 1.1 View table structure and sample data
SELECT * FROM coins LIMIT 10;

-- 1.2 Count total records
SELECT COUNT(*) AS total_coins FROM coins;

-- 1.3 Get column information (SQLite specific)
PRAGMA table_info(coins);

-- 1.4 Check for NULL values in key columns
SELECT 
    'coin_name' AS column_name, COUNT(*) - COUNT(coin_name) AS null_count FROM coins
UNION ALL
SELECT 'symbol', COUNT(*) - COUNT(symbol) FROM coins
UNION ALL
SELECT 'price_usd', COUNT(*) - COUNT(price_usd) FROM coins
UNION ALL
SELECT 'investment_score', COUNT(*) - COUNT(investment_score) FROM coins
UNION ALL
SELECT 'primary_signal', COUNT(*) - COUNT(primary_signal) FROM coins;

-- 1.5 Get distinct values for categorical columns
SELECT DISTINCT coin_type FROM coins;
SELECT DISTINCT primary_signal FROM coins;
SELECT DISTINCT category FROM coins;
SELECT DISTINCT platform FROM coins;
SELECT DISTINCT risk_level FROM coins;


-- =============================================================================
-- SECTION 2: AGGREGATION AND STATISTICAL ANALYSIS
-- =============================================================================

-- 2.1 Basic statistics for numeric columns
SELECT 
    'Investment Score' AS metric,
    MIN(investment_score) AS min_value,
    MAX(investment_score) AS max_value,
    AVG(investment_score) AS avg_value,
    COUNT(investment_score) AS count_value
FROM coins
UNION ALL
SELECT 'Risk Score', MIN(risk_score), MAX(risk_score), AVG(risk_score), COUNT(risk_score) FROM coins
UNION ALL
SELECT 'Momentum Score', MIN(momentum_score), MAX(momentum_score), AVG(momentum_score), COUNT(momentum_score) FROM coins
UNION ALL
SELECT 'Price USD', MIN(price_usd), MAX(price_usd), AVG(price_usd), COUNT(price_usd) FROM coins;

-- 2.2 Count and percentage by coin type
SELECT 
    coin_type,
    COUNT(*) AS coin_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM coins), 2) AS percentage
FROM coins
GROUP BY coin_type
ORDER BY coin_count DESC;

-- 2.3 Count and percentage by trading signal
SELECT 
    primary_signal,
    COUNT(*) AS signal_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM coins), 2) AS percentage
FROM coins
GROUP BY primary_signal
ORDER BY signal_count DESC;

-- 2.4 Average metrics by coin type
SELECT 
    coin_type,
    COUNT(*) AS total_coins,
    ROUND(AVG(investment_score), 2) AS avg_investment_score,
    ROUND(AVG(risk_score), 2) AS avg_risk_score,
    ROUND(AVG(momentum_score), 2) AS avg_momentum_score,
    ROUND(AVG(change_momentum), 2) AS avg_change_momentum,
    ROUND(AVG(price_volatility), 2) AS avg_volatility
FROM coins
GROUP BY coin_type;

-- 2.5 Average metrics by trading signal
SELECT 
    primary_signal,
    COUNT(*) AS total_coins,
    ROUND(AVG(investment_score), 2) AS avg_investment_score,
    ROUND(AVG(overall_score), 2) AS avg_overall_score,
    ROUND(AVG(risk_score), 2) AS avg_risk_score,
    ROUND(AVG(change_momentum), 2) AS avg_change_momentum
FROM coins
GROUP BY primary_signal
ORDER BY avg_investment_score DESC;

-- 2.6 Statistics by platform
SELECT 
    platform,
    COUNT(*) AS coin_count,
    ROUND(AVG(investment_score), 2) AS avg_investment_score,
    ROUND(AVG(price_usd), 6) AS avg_price,
    ROUND(SUM(volume_24h), 2) AS total_volume
FROM coins
WHERE platform IS NOT NULL AND platform != 'Unknown'
GROUP BY platform
HAVING COUNT(*) >= 3
ORDER BY avg_investment_score DESC
LIMIT 15;


-- =============================================================================
-- SECTION 3: RANKING AND TOP N ANALYSIS
-- =============================================================================

-- 3.1 Top 20 coins by investment score
SELECT 
    coin_name,
    symbol,
    coin_type,
    ROUND(investment_score, 2) AS investment_score,
    ROUND(risk_score, 2) AS risk_score,
    primary_signal,
    ROUND(price_usd, 8) AS price_usd
FROM coins
ORDER BY investment_score DESC
LIMIT 20;

-- 3.2 Top 10 crypto coins
SELECT 
    coin_name,
    symbol,
    ROUND(investment_score, 2) AS investment_score,
    ROUND(momentum_score, 2) AS momentum_score,
    primary_signal
FROM coins
WHERE coin_type = 'crypto'
ORDER BY investment_score DESC
LIMIT 10;

-- 3.3 Top 10 meme coins
SELECT 
    coin_name,
    symbol,
    ROUND(investment_score, 2) AS investment_score,
    ROUND(momentum_score, 2) AS momentum_score,
    primary_signal
FROM coins
WHERE coin_type = 'meme'
ORDER BY investment_score DESC
LIMIT 10;

-- 3.4 Top 10 by momentum score
SELECT 
    coin_name,
    symbol,
    coin_type,
    ROUND(momentum_score, 2) AS momentum_score,
    ROUND(change_momentum, 2) AS change_momentum,
    momentum_category
FROM coins
ORDER BY momentum_score DESC
LIMIT 10;

-- 3.5 Top 10 lowest risk coins
SELECT 
    coin_name,
    symbol,
    coin_type,
    ROUND(risk_score, 2) AS risk_score,
    risk_level,
    ROUND(volatility_risk, 2) AS volatility_risk
FROM coins
ORDER BY risk_score ASC
LIMIT 10;

-- 3.6 Top coins with highest 24h volume
SELECT 
    coin_name,
    symbol,
    coin_type,
    ROUND(volume_24h, 2) AS volume_24h,
    ROUND(volume_change_24h, 2) AS volume_change_pct,
    primary_signal
FROM coins
WHERE volume_24h > 0
ORDER BY volume_24h DESC
LIMIT 10;

-- 3.7 Ranking using window functions
SELECT 
    coin_name,
    symbol,
    coin_type,
    ROUND(investment_score, 2) AS investment_score,
    RANK() OVER (ORDER BY investment_score DESC) AS overall_rank,
    RANK() OVER (PARTITION BY coin_type ORDER BY investment_score DESC) AS type_rank
FROM coins
ORDER BY overall_rank
LIMIT 30;


-- =============================================================================
-- SECTION 4: FILTERING AND CONDITIONAL ANALYSIS
-- =============================================================================

-- 4.1 Coins with STRONG_BUY signal
SELECT 
    coin_name,
    symbol,
    coin_type,
    ROUND(investment_score, 2) AS investment_score,
    ROUND(overall_score, 2) AS overall_score,
    ROUND(change_momentum, 2) AS change_momentum
FROM coins
WHERE primary_signal = 'STRONG_BUY'
ORDER BY investment_score DESC;

-- 4.2 High potential, low risk opportunities
SELECT 
    coin_name,
    symbol,
    coin_type,
    ROUND(investment_score, 2) AS investment_score,
    ROUND(risk_score, 2) AS risk_score,
    primary_signal
FROM coins
WHERE investment_score > 40 
  AND risk_score < 50
  AND primary_signal IN ('STRONG_BUY', 'BUY')
ORDER BY investment_score DESC
LIMIT 15;

-- 4.3 Bullish momentum coins
SELECT 
    coin_name,
    symbol,
    coin_type,
    ROUND(change_momentum, 2) AS change_momentum,
    momentum_category,
    ROUND(momentum_consistency, 2) AS momentum_consistency
FROM coins
WHERE momentum_category IN ('Bullish', 'Strong Bullish')
ORDER BY change_momentum DESC
LIMIT 15;

-- 4.4 Coins by price tier analysis
SELECT 
    price_tier,
    COUNT(*) AS coin_count,
    ROUND(AVG(investment_score), 2) AS avg_investment_score,
    ROUND(AVG(risk_score), 2) AS avg_risk_score,
    ROUND(AVG(change_momentum), 2) AS avg_momentum
FROM coins
GROUP BY price_tier
ORDER BY 
    CASE price_tier 
        WHEN 'High' THEN 1 
        WHEN 'Medium' THEN 2 
        WHEN 'Low' THEN 3 
        ELSE 4 
    END;

-- 4.5 Coins with significant price changes
SELECT 
    coin_name,
    symbol,
    coin_type,
    ROUND(pct_change_24h, 2) AS pct_change_24h,
    ROUND(pct_change_7d, 2) AS pct_change_7d,
    ROUND(pct_change_30d, 2) AS pct_change_30d,
    primary_signal
FROM coins
WHERE ABS(pct_change_24h) > 100
ORDER BY pct_change_24h DESC
LIMIT 20;


-- =============================================================================
-- SECTION 5: ADVANCED AGGREGATIONS AND PIVOTING
-- =============================================================================

-- 5.1 Cross-tabulation: Coin type vs Signal
SELECT 
    coin_type,
    SUM(CASE WHEN primary_signal = 'STRONG_BUY' THEN 1 ELSE 0 END) AS strong_buy,
    SUM(CASE WHEN primary_signal = 'BUY' THEN 1 ELSE 0 END) AS buy,
    SUM(CASE WHEN primary_signal = 'HOLD' THEN 1 ELSE 0 END) AS hold,
    SUM(CASE WHEN primary_signal = 'SELL' THEN 1 ELSE 0 END) AS sell,
    SUM(CASE WHEN primary_signal = 'STRONG_SELL' THEN 1 ELSE 0 END) AS strong_sell,
    COUNT(*) AS total
FROM coins
GROUP BY coin_type;

-- 5.2 Cross-tabulation: Risk level vs Coin type
SELECT 
    risk_level,
    SUM(CASE WHEN coin_type = 'crypto' THEN 1 ELSE 0 END) AS crypto_count,
    SUM(CASE WHEN coin_type = 'meme' THEN 1 ELSE 0 END) AS meme_count,
    COUNT(*) AS total
FROM coins
GROUP BY risk_level
ORDER BY 
    CASE risk_level 
        WHEN 'Low Risk' THEN 1 
        WHEN 'Medium Risk' THEN 2 
        WHEN 'High Risk' THEN 3 
        ELSE 4 
    END;

-- 5.3 Score distribution buckets
SELECT 
    CASE 
        WHEN investment_score >= 80 THEN '80-100 (Excellent)'
        WHEN investment_score >= 60 THEN '60-79 (Good)'
        WHEN investment_score >= 40 THEN '40-59 (Average)'
        WHEN investment_score >= 20 THEN '20-39 (Below Average)'
        ELSE '0-19 (Poor)'
    END AS score_bucket,
    COUNT(*) AS coin_count,
    ROUND(AVG(risk_score), 2) AS avg_risk,
    ROUND(AVG(change_momentum), 2) AS avg_momentum
FROM coins
GROUP BY 
    CASE 
        WHEN investment_score >= 80 THEN '80-100 (Excellent)'
        WHEN investment_score >= 60 THEN '60-79 (Good)'
        WHEN investment_score >= 40 THEN '40-59 (Average)'
        WHEN investment_score >= 20 THEN '20-39 (Below Average)'
        ELSE '0-19 (Poor)'
    END
ORDER BY score_bucket DESC;

-- 5.4 Platform performance summary
SELECT 
    platform,
    COUNT(*) AS total_coins,
    SUM(CASE WHEN primary_signal IN ('STRONG_BUY', 'BUY') THEN 1 ELSE 0 END) AS bullish_coins,
    ROUND(SUM(CASE WHEN primary_signal IN ('STRONG_BUY', 'BUY') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS bullish_pct,
    ROUND(AVG(investment_score), 2) AS avg_investment_score
FROM coins
WHERE platform IS NOT NULL AND platform != 'Unknown'
GROUP BY platform
HAVING COUNT(*) >= 5
ORDER BY bullish_pct DESC;


-- =============================================================================
-- SECTION 6: TIME-BASED ANALYSIS
-- =============================================================================

-- 6.1 Coins by date added (year-month)
SELECT 
    strftime('%Y-%m', date_added) AS added_month,
    COUNT(*) AS coins_added,
    ROUND(AVG(investment_score), 2) AS avg_investment_score,
    ROUND(AVG(overall_score), 2) AS avg_overall_score
FROM coins
WHERE date_added IS NOT NULL
GROUP BY strftime('%Y-%m', date_added)
ORDER BY added_month DESC
LIMIT 12;

-- 6.2 Recently added coins (last 30 days)
SELECT 
    coin_name,
    symbol,
    coin_type,
    date_added,
    days_since_added,
    ROUND(investment_score, 2) AS investment_score,
    primary_signal
FROM coins
WHERE days_since_added <= 30
ORDER BY date_added DESC
LIMIT 20;

-- 6.3 New coins performance analysis
SELECT 
    CASE 
        WHEN days_since_added <= 7 THEN '0-7 days (Very New)'
        WHEN days_since_added <= 30 THEN '8-30 days (New)'
        WHEN days_since_added <= 90 THEN '31-90 days (Recent)'
        WHEN days_since_added <= 365 THEN '91-365 days (Established)'
        ELSE '365+ days (Mature)'
    END AS age_category,
    COUNT(*) AS coin_count,
    ROUND(AVG(investment_score), 2) AS avg_investment_score,
    ROUND(AVG(risk_score), 2) AS avg_risk_score,
    ROUND(AVG(change_momentum), 2) AS avg_momentum
FROM coins
GROUP BY 
    CASE 
        WHEN days_since_added <= 7 THEN '0-7 days (Very New)'
        WHEN days_since_added <= 30 THEN '8-30 days (New)'
        WHEN days_since_added <= 90 THEN '31-90 days (Recent)'
        WHEN days_since_added <= 365 THEN '91-365 days (Established)'
        ELSE '365+ days (Mature)'
    END
ORDER BY avg_investment_score DESC;


-- =============================================================================
-- SECTION 7: COMPARATIVE ANALYSIS
-- =============================================================================

-- 7.1 Compare crypto vs meme coins
SELECT 
    'Crypto' AS coin_type,
    COUNT(*) AS total_coins,
    ROUND(AVG(investment_score), 2) AS avg_investment_score,
    ROUND(AVG(risk_score), 2) AS avg_risk_score,
    ROUND(AVG(momentum_score), 2) AS avg_momentum_score,
    ROUND(AVG(price_volatility), 2) AS avg_volatility,
    ROUND(AVG(overall_score), 2) AS avg_overall_score
FROM coins WHERE coin_type = 'crypto'
UNION ALL
SELECT 
    'Meme',
    COUNT(*),
    ROUND(AVG(investment_score), 2),
    ROUND(AVG(risk_score), 2),
    ROUND(AVG(momentum_score), 2),
    ROUND(AVG(price_volatility), 2),
    ROUND(AVG(overall_score), 2)
FROM coins WHERE coin_type = 'meme';

-- 7.2 Compare STRONG_BUY coins: Crypto vs Meme
SELECT 
    coin_type,
    COUNT(*) AS strong_buy_count,
    ROUND(AVG(investment_score), 2) AS avg_investment_score,
    ROUND(AVG(risk_score), 2) AS avg_risk_score,
    ROUND(AVG(change_momentum), 2) AS avg_momentum
FROM coins
WHERE primary_signal = 'STRONG_BUY'
GROUP BY coin_type;

-- 7.3 High vs Low risk coin comparison
SELECT 
    risk_level,
    COUNT(*) AS coin_count,
    ROUND(AVG(investment_score), 2) AS avg_investment_score,
    ROUND(AVG(momentum_score), 2) AS avg_momentum_score,
    ROUND(AVG(pct_change_24h), 2) AS avg_24h_change,
    SUM(CASE WHEN primary_signal IN ('STRONG_BUY', 'BUY') THEN 1 ELSE 0 END) AS bullish_count
FROM coins
GROUP BY risk_level
ORDER BY 
    CASE risk_level 
        WHEN 'Low Risk' THEN 1 
        WHEN 'Medium Risk' THEN 2 
        WHEN 'High Risk' THEN 3 
        ELSE 4 
    END;


-- =============================================================================
-- SECTION 8: SUBQUERIES AND CTEs
-- =============================================================================

-- 8.1 Coins above average investment score
SELECT 
    coin_name,
    symbol,
    coin_type,
    ROUND(investment_score, 2) AS investment_score,
    primary_signal
FROM coins
WHERE investment_score > (SELECT AVG(investment_score) FROM coins)
ORDER BY investment_score DESC
LIMIT 20;

-- 8.2 Using CTE for rank analysis
WITH RankedCoins AS (
    SELECT 
        coin_name,
        symbol,
        coin_type,
        investment_score,
        risk_score,
        ROW_NUMBER() OVER (PARTITION BY coin_type ORDER BY investment_score DESC) AS rank_in_type
    FROM coins
)
SELECT 
    coin_name,
    symbol,
    coin_type,
    ROUND(investment_score, 2) AS investment_score,
    ROUND(risk_score, 2) AS risk_score,
    rank_in_type
FROM RankedCoins
WHERE rank_in_type <= 5
ORDER BY coin_type, rank_in_type;

-- 8.3 CTE for percentile calculation
WITH ScorePercentiles AS (
    SELECT 
        investment_score,
        NTILE(4) OVER (ORDER BY investment_score) AS quartile
    FROM coins
)
SELECT 
    quartile AS investment_quartile,
    MIN(investment_score) AS min_score,
    MAX(investment_score) AS max_score,
    COUNT(*) AS coin_count
FROM ScorePercentiles
GROUP BY quartile
ORDER BY quartile;

-- 8.4 CTE for outperformers by coin type
WITH TypeAverages AS (
    SELECT 
        coin_type,
        AVG(investment_score) AS avg_score
    FROM coins
    GROUP BY coin_type
)
SELECT 
    c.coin_name,
    c.symbol,
    c.coin_type,
    ROUND(c.investment_score, 2) AS investment_score,
    ROUND(ta.avg_score, 2) AS type_avg_score,
    ROUND(c.investment_score - ta.avg_score, 2) AS outperformance
FROM coins c
JOIN TypeAverages ta ON c.coin_type = ta.coin_type
WHERE c.investment_score > ta.avg_score
ORDER BY outperformance DESC
LIMIT 15;


-- =============================================================================
-- SECTION 9: BUSINESS INTELLIGENCE QUERIES
-- =============================================================================

-- 9.1 Investment opportunity summary dashboard
SELECT 
    'Total Coins' AS metric, CAST(COUNT(*) AS TEXT) AS value FROM coins
UNION ALL
SELECT 'STRONG_BUY Count', CAST(SUM(CASE WHEN primary_signal = 'STRONG_BUY' THEN 1 ELSE 0 END) AS TEXT) FROM coins
UNION ALL
SELECT 'Average Investment Score', CAST(ROUND(AVG(investment_score), 2) AS TEXT) FROM coins
UNION ALL
SELECT 'High Score Coins (>60)', CAST(SUM(CASE WHEN investment_score > 60 THEN 1 ELSE 0 END) AS TEXT) FROM coins
UNION ALL
SELECT 'Low Risk Count', CAST(SUM(CASE WHEN risk_level = 'Low Risk' THEN 1 ELSE 0 END) AS TEXT) FROM coins
UNION ALL
SELECT 'Strong Bullish Momentum', CAST(SUM(CASE WHEN momentum_category = 'Strong Bullish' THEN 1 ELSE 0 END) AS TEXT) FROM coins;

-- 9.2 Platform market share
SELECT 
    platform,
    COUNT(*) AS coin_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM coins WHERE platform IS NOT NULL), 2) AS market_share_pct,
    RANK() OVER (ORDER BY COUNT(*) DESC) AS platform_rank
FROM coins
WHERE platform IS NOT NULL AND platform != 'Unknown'
GROUP BY platform
ORDER BY coin_count DESC
LIMIT 10;

-- 9.3 Signal strength analysis
SELECT 
    primary_signal,
    ROUND(AVG(signal_strength), 2) AS avg_signal_strength,
    ROUND(AVG(investment_score), 2) AS avg_investment_score,
    ROUND(AVG(momentum_consistency), 2) AS avg_momentum_consistency,
    COUNT(*) AS total_coins
FROM coins
GROUP BY primary_signal
ORDER BY avg_investment_score DESC;

-- 9.4 Risk-adjusted return potential
SELECT 
    coin_name,
    symbol,
    coin_type,
    ROUND(investment_score, 2) AS investment_score,
    ROUND(risk_score, 2) AS risk_score,
    ROUND(potential_return, 2) AS potential_return,
    ROUND(investment_score / NULLIF(risk_score, 0), 2) AS risk_adjusted_score,
    primary_signal
FROM coins
WHERE risk_score > 0
ORDER BY risk_adjusted_score DESC
LIMIT 15;


-- =============================================================================
-- SECTION 10: DATA QUALITY AND VALIDATION
-- =============================================================================

-- 10.1 Check for data completeness
SELECT 
    COUNT(*) AS total_records,
    SUM(CASE WHEN coin_name IS NOT NULL THEN 1 ELSE 0 END) AS has_name,
    SUM(CASE WHEN symbol IS NOT NULL THEN 1 ELSE 0 END) AS has_symbol,
    SUM(CASE WHEN price_usd IS NOT NULL THEN 1 ELSE 0 END) AS has_price,
    SUM(CASE WHEN investment_score IS NOT NULL THEN 1 ELSE 0 END) AS has_inv_score,
    SUM(CASE WHEN primary_signal IS NOT NULL THEN 1 ELSE 0 END) AS has_signal
FROM coins;

-- 10.2 Check for duplicate symbols
SELECT 
    symbol,
    COUNT(*) AS occurrence_count
FROM coins
GROUP BY symbol
HAVING COUNT(*) > 1
ORDER BY occurrence_count DESC;

-- 10.3 Outlier detection for investment score
WITH QuartileStats AS (
    SELECT 
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY investment_score) OVER () AS Q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY investment_score) OVER () AS Q3
    FROM coins
    LIMIT 1
)
SELECT 
    coin_name,
    symbol,
    investment_score,
    'Potential Outlier' AS status
FROM coins
WHERE investment_score > (
    SELECT AVG(investment_score) + 3 * 
    (SELECT MAX(investment_score) - MIN(investment_score) FROM coins) / 4
    FROM coins
)
ORDER BY investment_score DESC
LIMIT 10;

-- 10.4 Data range validation
SELECT 
    'Investment Score' AS metric,
    MIN(investment_score) AS min_val,
    MAX(investment_score) AS max_val,
    CASE 
        WHEN MIN(investment_score) >= 0 AND MAX(investment_score) <= 100 THEN 'Valid'
        ELSE 'Check Required'
    END AS validation_status
FROM coins
UNION ALL
SELECT 
    'Risk Score',
    MIN(risk_score),
    MAX(risk_score),
    CASE 
        WHEN MIN(risk_score) >= 0 AND MAX(risk_score) <= 100 THEN 'Valid'
        ELSE 'Check Required'
    END
FROM coins
UNION ALL
SELECT 
    'Momentum Score',
    MIN(momentum_score),
    MAX(momentum_score),
    CASE 
        WHEN MIN(momentum_score) >= 0 AND MAX(momentum_score) <= 100 THEN 'Valid'
        ELSE 'Check Required'
    END
FROM coins;


-- =============================================================================
-- SECTION 11: REPORT GENERATION QUERIES
-- =============================================================================

-- 11.1 Executive Summary
SELECT 
    '=== EXECUTIVE SUMMARY ===' AS report_section,
    '' AS detail
UNION ALL
SELECT 'Total Cryptocurrency Assets Analyzed:', CAST(COUNT(*) AS TEXT) FROM coins
UNION ALL
SELECT 'Assets with Strong Buy Signal:', CAST(SUM(CASE WHEN primary_signal = 'STRONG_BUY' THEN 1 ELSE 0 END) AS TEXT) FROM coins
UNION ALL
SELECT 'Average Investment Score:', CAST(ROUND(AVG(investment_score), 2) AS TEXT) FROM coins
UNION ALL
SELECT 'Crypto Coins:', CAST(SUM(CASE WHEN coin_type = 'crypto' THEN 1 ELSE 0 END) AS TEXT) FROM coins
UNION ALL
SELECT 'Meme Coins:', CAST(SUM(CASE WHEN coin_type = 'meme' THEN 1 ELSE 0 END) AS TEXT) FROM coins;

-- 11.2 Top recommendations report
SELECT 
    'RANK' AS position,
    'COIN' AS coin_details,
    'SIGNAL' AS recommendation,
    'SCORE' AS inv_score
UNION ALL
SELECT 
    CAST(ROW_NUMBER() OVER (ORDER BY investment_score DESC) AS TEXT),
    coin_name || ' (' || symbol || ')',
    primary_signal,
    CAST(ROUND(investment_score, 2) AS TEXT)
FROM coins
ORDER BY 
    CASE WHEN position = 'RANK' THEN 0 ELSE 1 END,
    CAST(position AS INTEGER)
LIMIT 16;


-- =============================================================================
-- END OF SQL ANALYSIS QUERIES
-- =============================================================================

-- Skills Demonstrated in this SQL file:
-- 1. Basic SELECT queries with filtering and sorting
-- 2. Aggregation functions (COUNT, SUM, AVG, MIN, MAX)
-- 3. GROUP BY and HAVING clauses
-- 4. Window functions (RANK, ROW_NUMBER, NTILE, PERCENTILE)
-- 5. Common Table Expressions (CTEs)
-- 6. Subqueries (scalar, correlated)
-- 7. CASE statements for conditional logic
-- 8. UNION queries for combining results
-- 9. Date/time functions
-- 10. Pivot-style queries
-- 11. Data validation and quality checks
-- 12. Business intelligence reporting queries
