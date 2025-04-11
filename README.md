**Weekly Jobs Strategy**  
*A data-driven macroeconomic signal generator using Initial Jobless Claims*

---

**Overview:**

The Weekly Jobs Strategy project analyzes U.S. Initial Jobless Claims data to generate simple bullish or bearish signals that can inform trading strategies. This data is retrieved directly from the FRED (Federal Reserve Economic Data) API.

Initial jobless claims reflect how many people filed for unemployment for the first time in a given week. Sudden increases or decreases in these numbers can serve as indicators of broader economic shifts — making them valuable for traders and analysts.

---

**What This Script Does:**

1. Fetches weekly initial jobless claims from FRED.
2. Aligns the data to each Friday’s closing.
3. Calculates the week-over-week percentage change.
4. Generates a trading signal based on sharp changes:
   - **Signal = 1 (Bullish)** when claims drop by more than 2% (economic improvement).
   - **Signal = 0 (Bearish)** when claims rise by more than 2% (economic deterioration).
   - Otherwise, continues with the previous signal (neutral).

---

**Technologies Used:**

- Python 3.x  
- FRED API (for jobless claims data)  
- pandas (data manipulation)  
- numpy (numerical calculations)  
- yfinance (optional, for market data)  
- matplotlib (optional, for visualization)

---

**Setup Instructions:**

1. **Clone the repository:**

   ```
   git clone https://github.com/iampratyush4/Weekly-Jobs-Strategy.git
   cd Weekly-Jobs-Strategy
   ```

2. **Install required packages:**

   ```
   pip install -r requirements.txt
   ```

3. **Get a FRED API key:**

   - Visit: https://fred.stlouisfed.org/
   - Sign up and generate an API key.
   - Create a file named `Api_keys.py` in the project directory.
   - Add this line inside it:

     ```python
     FRED_API_KEY = "your_api_key_here"
     ```

4. **Run the script:**

   ```
   python Weekly_jobs_strategy.py
   ```

---

**Sample Output Table:**

| Date       | Initial Claims | Claims Change % | Signal |
|------------|----------------|------------------|--------|
| 2024-01-05 | 210000         | NaN              | NaN    |
| 2024-01-12 | 200000         | -4.76            | 1      |
| 2024-01-19 | 205000         | +2.50            | 0      |

---

**What’s Next (Planned Features):**

- Integration with stock market data to simulate the impact of signals  
- Backtesting functionality  
- Signal visualization and trend plotting  
- Alerts via Telegram or email when signal changes  
- Combining with other macroeconomic indicators  

---

**Author:**

Pratyush  
GitHub: https://github.com/iampratyush4  

---
