from indicator_analyzer import IndicatorAnalyzer
from lightweight_charts import Chart

class AutoIndicatorGenerator:
    def __init__(self):
        self.analyzer = IndicatorAnalyzer()
        
    def generate_indicator_charts(self, ohlcv_data):
        indicators = self.analyzer.analyze_indicators(ohlcv_data)
        
        charts = []
        for indicator in indicators:
            chart = Chart()
            chart.candlestick(ohlcv_data)
            chart.add_indicator(
                type=indicator['type'],
                values=indicator['values'],
                parameters=indicator['parameters']
            )
            charts.append(chart)
            
        return charts
