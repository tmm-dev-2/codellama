import numpy as np
import pandas as pd
from auto_chart_generator import AutoChartGenerator
from indicator_chart_generator import AutoIndicatorGenerator

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

# Test pattern charts
pattern_gen = AutoChartGenerator()
pattern_charts = pattern_gen.generate_pattern_charts(df)
print("Generated Pattern Charts:", len(pattern_charts))

# Test indicator charts
indicator_gen = AutoIndicatorGenerator()
indicator_charts = indicator_gen.generate_indicator_charts(df)
print("Generated Indicator Charts:", len(indicator_charts))
