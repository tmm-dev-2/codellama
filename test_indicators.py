import numpy as np
import pandas as pd
from indicator_analyzer import IndicatorAnalyzer

# Generate 150 days of OHLCV data
np.random.seed(42)
days = 150
base_price = 100

price_changes = np.random.normal(0.001, 0.02, days).cumsum()
prices = base_price * (1 + price_changes)

test_data = {
    'open': prices * (1 + np.random.normal(0, 0.005, days)),
    'high': prices * (1 + np.random.normal(0.01, 0.008, days)),
    'low': prices * (1 + np.random.normal(-0.01, 0.008, days)),
    'close': prices * (1 + np.random.normal(0, 0.005, days)),
    'volume': np.random.normal(1000000, 200000, days)
}

df = pd.DataFrame(test_data)
df['high'] = df[['open', 'high', 'close']].max(axis=1)
df['low'] = df[['open', 'low', 'close']].min(axis=1)

# Test indicator analysis
analyzer = IndicatorAnalyzer()
indicators = analyzer.analyze_indicators(df)
print("Generated Indicators:", indicators)
