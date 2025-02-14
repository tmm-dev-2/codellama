import numpy as np
import pandas as pd

# Generate 150 days test data
days = 150
base_price = 100

# Generate price changes with realistic volatility
price_changes = np.random.normal(0.001, 0.02, days).cumsum()
base_prices = base_price * (1 + price_changes)

# Create DataFrame with all OHLCV components
test_data = pd.DataFrame({
    'open': base_prices * (1 + np.random.normal(0, 0.005, days)),  # Opening prices
    'high': base_prices * (1 + np.random.normal(0.01, 0.008, days)),  # Day's high prices
    'low': base_prices * (1 + np.random.normal(-0.01, 0.008, days)),  # Day's low prices
    'close': base_prices * (1 + np.random.normal(0, 0.005, days)),  # Closing prices
    'volume': np.random.normal(1000000, 200000, days).astype(int)  # Daily volume
})

# Ensure high is always highest and low is always lowest
test_data['high'] = test_data[['open', 'high', 'close']].max(axis=1)
test_data['low'] = test_data[['open', 'low', 'close']].min(axis=1)
