from fastapi import FastAPI
from pattern_analyzer import PatternAnalyzer
from indicator_analyzer import IndicatorAnalyzer
from chart_maker import ChartMaker

app = FastAPI()

@app.get('/')
def root():
    return {'status': 'online', 'service': 'Pattern Analysis API'}
