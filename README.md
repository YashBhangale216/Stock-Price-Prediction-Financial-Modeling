# NVDA Next-Day Direction Prediction

A data science project that tries to predict whether NVIDIA (NVDA) stock will close **up or down tomorrow**, using technical indicators and machine learning.

**Main finding:** neither model beat the simple "always guess UP" baseline. Price-based indicators carried almost no usable signal for next-day direction. This project focuses on a careful, honest process, not on a high accuracy number.

---

## Goal

Predict the next trading day's direction for NVDA:
- `1` = tomorrow's close is higher than today's
- `0` = tomorrow's close is lower or equal

## Data

- **Source:** Yahoo Finance, downloaded with `yfinance`
- **Period:** 2016-01-04 to 2026-11-10 (2,730 trading days)
- **Fields:** Open, High, Low, Close, Volume (prices are split-adjusted with `auto_adjust=True`)

## Project steps

1. **Data pull** (`data_pull.py`): download NVDA history and save to `nvda_data.csv`.
2. **EDA:** closing price chart, daily returns histogram, and a stationarity test (ADF).
3. **Feature engineering:** Return, MA5, MA10, MA20, RSI (14), Volatility10, Volatility20.
4. **Target:** 1 if tomorrow's close is higher than today's, else 0. The last row is removed because it has no "tomorrow".
5. **Time-based split:** 80% train, 20% test, in date order.
6. **Models:** Logistic Regression (baseline) and Random Forest.
7. **Evaluation:** accuracy, confusion matrix, feature importance, and a backtest.

## Key decisions

- **Returns, not raw price.** The ADF test showed that Close price is non-stationary (p = 0.93), while daily returns are stationary (p = 0.00). So the features and target are built from returns and indicators.
- **Time-based split, not random.** A random split would let the model train on future days and test on past days (lookahead), which gives fake results.
- **Compared with a naive baseline.** Because NVDA rose on about 52% of test days, "always guess UP" already scores about 52%. A model must beat this to show real value.

## Results

Train: 2,167 days (2016-02-02 to 2024-09-11)
Test: 542 days (2024-09-12 to 2026-11-09)

| Model | Test accuracy |
|---|---|
| Naive baseline (always UP) | **0.5203** |
| Logistic Regression | 0.4760 |
| Random Forest | 0.5037 |

**What the confusion matrices show**
- Logistic Regression said UP on 370 of 542 days and DOWN on 172.
- Random Forest said DOWN on 475 of 542 days and UP on only 67.
- The two models lean in opposite directions, and both end near 50%. This suggests the features have no real signal.

**Feature importance (Random Forest):** all seven features are almost equal (0.127 to 0.152). No feature stands out.

### Backtest

Strategy: hold NVDA the next day when the model says UP, stay in cash when it says DOWN. Compared with buy and hold over the test period.

| | Final value of $1 |
|---|---|
| Buy and hold | 1.504 |
| Random Forest strategy | 1.489 |

The strategy did not beat buy and hold. The model stayed in cash for most of the second half of the test period, so it missed NVDA's rise.

An earlier version of the test showed the strategy slightly ahead (1.487 vs 1.422). That result depended on one extra final day (a 5.5% drop) that had no valid label. After removing it, the "win" disappeared. This shows how fragile the result was, so I treat the backtest as showing **no reliable edge**.

## Limitations

- Daily stock direction is very noisy, and news and events are not in the data.
- All features use only past prices.
- MA5, MA10 and MA20 are raw price levels. NVDA's price was very different in the train and test periods, so these features are on different scales. A better version uses the distance from each average (for example `Close / MA20 - 1`).
- One test period, one train/test split.
- The backtest ignores transaction costs and assumes cash earns 0%.
- Small accuracy changes (1 to 2%) are within noise. For example, removing one row shifted the split by one day and changed Logistic Regression accuracy by about 1%.

## Possible next steps

- Use distance-from-average features instead of raw moving averages.
- Walk-forward validation instead of a single split.
- Add market data (S&P 500, VIX), earnings dates, or news sentiment.
- Predict a longer horizon (one week) or predict volatility instead of direction.
- Add transaction costs to the backtest.

## How to run

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install pandas numpy yfinance matplotlib statsmodels scikit-learn
python data_pull.py          # creates nvda_data.csv
jupyter notebook             # open the notebook and use Restart + Run All
```

Run the notebook cells in order from top to bottom.

## Tech stack

Python, pandas, NumPy, yfinance, matplotlib, statsmodels, scikit-learn, Jupyter.

## Files

- `data_pull.py`: downloads the data
- `nvda_data.csv`: saved price data
- `pred_model.ipynb`: EDA, features, models, and backtest
- `README.md`: this file

## Author

Your name | LinkedIn | GitHub
