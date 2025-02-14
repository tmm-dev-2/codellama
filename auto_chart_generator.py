from pattern_analyzer import PatternAnalyzer
from lightweight_charts import Chart

class AutoChartGenerator:
    def __init__(self):
        self.analyzer = PatternAnalyzer()
        
    def generate_pattern_charts(self, ohlcv_data):
        patterns = self.analyzer.analyze_data(ohlcv_data)
        
        charts = []
        for pattern in patterns:
            chart = Chart()
            chart.candlestick(ohlcv_data)
            chart.draw_pattern(
                pattern_type=pattern['type'],
                coordinates=pattern['coordinates']
            )
            charts.append(chart)
            
        return charts
