import numpy as np
import pandas as pd
from pattern_analyzer import PatternAnalyzer

# Generate 150 days of realistic OHLCV data
np.random.seed(42)  # For reproducibility
days = 150
base_price = 100

# Create price movements with trends and volatility
price_changes = np.random.normal(0.001, 0.02, days).cumsum()
prices = base_price * (1 + price_changes)

test_data = {
    'open': prices * (1 + np.random.normal(0, 0.005, days)),
    'high': prices * (1 + np.random.normal(0.01, 0.008, days)),
    'low': prices * (1 + np.random.normal(-0.01, 0.008, days)),
    'close': prices * (1 + np.random.normal(0, 0.005, days)),
    'volume': np.random.normal(1000000, 200000, days)
}

# Convert to pandas DataFrame for better handling
df = pd.DataFrame(test_data)

# Ensure high is highest and low is lowest for each day
df['high'] = df[['open', 'high', 'close']].max(axis=1)
df['low'] = df[['open', 'low', 'close']].min(axis=1)

# Test pattern detection
analyzer = PatternAnalyzer()
patterns = analyzer.analyze_data(df)
print("Detected Patterns:", patterns)
