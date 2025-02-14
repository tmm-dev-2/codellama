from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import pandas as pd
import numpy as np
from pattern_analyzer import PatternAnalyzer
from indicator_analyzer import IndicatorAnalyzer
from chart_maker import ChartMaker
from test_data import test_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/analyze/{symbol}")
async def analyze_patterns(symbol: str, timeframe: str = "1D"):
    try:
        # Fetch OHLCV data
        candle_response = requests.get(f"http://localhost:5000/fetch_candles?symbol={symbol}&timeframe={timeframe}")
        ohlcv_data = candle_response.json()
        
        # Create DataFrame with correct column structure
        df = pd.DataFrame(ohlcv_data)
        df = df.rename(columns={'time': 'timestamp'})
        
        # Initialize analyzers
        pattern_analyzer = PatternAnalyzer()
        indicator_analyzer = IndicatorAnalyzer()
        chart_maker = ChartMaker()
        
        # Get analysis results
        patterns = pattern_analyzer.analyze_data(df)
        indicators = indicator_analyzer.analyze_indicators(df)
        pattern_charts = chart_maker.create_pattern_chart(df, patterns)
        
        return {
            "patterns": patterns,
            "indicators": indicators,
            "charts": pattern_charts,
            "ohlcv_data": ohlcv_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "Pattern Analysis API",
        "endpoints": {
            "analyze": "/analyze/{symbol}",
            "docs": "/docs",
            "health": "/health"
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
