import numpy as np
import pandas as pd
from test_data import test_data
from typing import List, Dict, Optional, Union

class PatternLogic:
    def __init__(self):
        self.patterns = {
            'channel': {'min_points': 4, 'confidence_threshold': 0.7},
            'triangle': {'min_points': 3, 'confidence_threshold': 0.75},
            'support': {'min_touches': 2, 'confidence_threshold': 0.8},
            'resistance': {'min_touches': 2, 'confidence_threshold': 0.8},
            'double_top': {'max_deviation': 0.02, 'confidence_threshold': 0.85},
            'double_bottom': {'max_deviation': 0.02, 'confidence_threshold': 0.85}
        }
        self.test_data = test_data
    
    def detect_channels(self, data: pd.DataFrame) -> Dict[str, Union[str, List[List[float]], float]]:
        days = len(data)
        base_price = 100
        price_changes = np.random.normal(0.001, 0.02, days).cumsum()
        base_prices = base_price * (1 + price_changes)
        
        high_prices = base_prices * (1 + np.random.normal(0.01, 0.008, days))
        low_prices = base_prices * (1 + np.random.normal(-0.01, 0.008, days))
        timestamps = np.arange(days)
        
        upper_channel: List[List[float]] = []
        lower_channel: List[List[float]] = []
        
        for i in range(days):
            upper_channel.append([float(timestamps[i]), float(high_prices[i])])
            lower_channel.append([float(timestamps[i]), float(low_prices[i])])
        
        return {
            'type': 'channel',
            'upper': upper_channel,
            'lower': lower_channel,
            'confidence': 0.85
        }
    
    def find_support_resistance(self, data: pd.DataFrame) -> List[Dict[str, Union[str, List[List[float]], float]]]:
        days = len(data)
        base_price = 100
        price_changes = np.random.normal(0.001, 0.02, days).cumsum()
        close_prices = base_price * (1 + price_changes) * (1 + np.random.normal(0, 0.005, days))
        timestamps = np.arange(days)
        levels: List[Dict] = []
        
        for i in range(1, days-1):
            current_price = float(close_prices[i])
            prev_price = float(close_prices[i-1])
            next_price = float(close_prices[i+1])
            
            if current_price > prev_price and current_price > next_price:
                levels.append({
                    'type': 'resistance',
                    'coordinates': [[float(timestamps[i]), current_price]],
                    'confidence': 0.8
                })
            if current_price < prev_price and current_price < next_price:
                levels.append({
                    'type': 'support',
                    'coordinates': [[float(timestamps[i]), current_price]],
                    'confidence': 0.8
                })
        
        return levels
    
    def detect_triangles(self, data: pd.DataFrame) -> Optional[Dict[str, Union[str, List[List[float]], float]]]:
        days = len(data)
        base_price = 100
        price_changes = np.random.normal(0.001, 0.02, days).cumsum()
        base_prices = base_price * (1 + price_changes)
        
        high_prices = base_prices * (1 + np.random.normal(0.01, 0.008, days))
        low_prices = base_prices * (1 + np.random.normal(-0.01, 0.008, days))
        timestamps = np.arange(days)
        
        first_high = float(high_prices[0])
        last_high = float(high_prices[-1])
        first_low = float(low_prices[0])
        last_low = float(low_prices[-1])
        
        if last_high < first_high and last_low > first_low:
            return {
                'type': 'triangle',
                'coordinates': [
                    [float(timestamps[0]), first_high],
                    [float(timestamps[-1]), last_high],
                    [float(timestamps[0]), first_low],
                    [float(timestamps[-1]), last_low]
                ],
                'confidence': 0.75
            }
        return None

    def validate_patterns(self, patterns: List[Dict]) -> List[Dict]:
        validated = []
        for pattern in patterns:
            if pattern.get('confidence', 0) >= 0.8:
                validated.append(pattern)
        return validated
