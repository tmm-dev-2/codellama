from lightweight_charts import Chart
import pandas as pd
import numpy as np

class ChartMaker:
    def __init__(self):
        self.patterns = [
            'channel', 'triangle', 'head_shoulders',
            'double_top', 'double_bottom', 'wedge',
            'flag', 'pennant'
        ]
        
        self.indicators = [
            'ema', 'sma', 'rsi', 'macd', 
            'bollinger', 'ichimoku', 'pivot_points'
        ]
    
    def create_pattern_chart(self, ohlcv_data, patterns):
        chart = Chart()
        
        # Format OHLCV data for charting
        chart_data = []
        for index, row in ohlcv_data.iterrows():
            data_point = {
                'time': row['time'] if isinstance(row['time'], int) else int(row['time'].timestamp() * 1000),
                'open': float(row['open']),
                'high': float(row['high']),
                'low': float(row['low']),
                'close': float(row['close']),
                'volume': float(row['volume'])
            }
            chart_data.append(data_point)
        
        # Create main price series
        chart.create_series('price', 'Candlestick', chart_data)
        
        # Add volume series
        volume_data = [{
            'time': d['time'],
            'value': d['volume']
        } for d in chart_data]
        chart.create_series('volume', 'Histogram', volume_data)
        
        # Add patterns as overlays
        for pattern in patterns:
            if pattern['type'] in self.patterns and 'coordinates' in pattern:
                chart.create_series(
                    f"pattern_{pattern['type']}", 
                    'Line', 
                    pattern['coordinates'],
                    {
                        'color': 'rgba(76, 175, 80, 0.5)',
                        'lineWidth': 2,
                        'title': f"{pattern['type']} ({pattern.get('confidence', 0):.2f})"
                    }
                )
        
        return chart
    
    
    def generate_all_variations(self, ohlcv_data):
        charts = []
        for pattern in self.patterns:
            pattern_chart = self.create_pattern_chart(ohlcv_data, [{'type': pattern}])
            charts.append({
                'type': pattern,
                'chart': pattern_chart
            })
        return charts
