from chart_maker import ChartMaker
from fastapi import FastAPI


class TriggerHandler:
    def __init__(self):
        self.chart_maker = ChartMaker()
    
    async def handle_chart_trigger(self, trigger_data):
        # Extract chart image and OHLCV data
        chart_image = trigger_data['image']
        ohlcv_data = trigger_data['ohlcv']
        
        # Generate pattern charts
        pattern_charts = self.chart_maker.generate_all_variations(ohlcv_data)
        
        # Return generated charts through API
        return {
            'pattern_charts': pattern_charts,
            'timestamp': trigger_data['timestamp']
        }
