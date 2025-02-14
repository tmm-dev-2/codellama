from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import pandas as pd
import numpy as np
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional
import gc

from pattern_analyzer import PatternAnalyzer
from indicator_analyzer import IndicatorAnalyzer
from chart_maker import ChartMaker

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pattern_analyzer = PatternAnalyzer()
indicator_analyzer = IndicatorAnalyzer()
chart_maker = ChartMaker()

async def analyze_stream(symbol: str, timeframe: str):
    async def generate():
        try:
            yield json.dumps({"status": "fetching_data"}) + "\n"
            
            response = requests.get(
                f"http://localhost:5000/fetch_candles",
                params={"symbol": symbol, "timeframe": timeframe}
            )
            ohlcv_data = response.json()
            
            yield json.dumps({"status": "processing_data"}) + "\n"
            
            df = pd.DataFrame(ohlcv_data)
            df.index = range(len(df))
            df['time'] = pd.to_datetime(df['time'], unit='ms')
            
            required_columns = ['time', 'open', 'high', 'low', 'close', 'volume']
            for col in required_columns:
                if col not in df.columns:
                    df[col] = 0
                    
            yield json.dumps({"status": "analyzing_patterns"}) + "\n"
            patterns = pattern_analyzer.analyze_data(df)
            
            yield json.dumps({"status": "calculating_indicators"}) + "\n"
            indicators = indicator_analyzer.analyze_indicators(df)
            
            yield json.dumps({"status": "generating_charts"}) + "\n"
            pattern_charts = chart_maker.create_pattern_chart(df, patterns)
            
            final_response = {
                "status": "complete",
                "symbol": symbol,
                "timeframe": timeframe,
                "patterns": patterns,
                "indicators": indicators,
                "charts": pattern_charts,
                "data": ohlcv_data
            }
            
            yield json.dumps(final_response) + "\n"
            
        except Exception as e:
            yield json.dumps({"status": "error", "detail": str(e)}) + "\n"

    return StreamingResponse(generate(), media_type="application/x-ndjson")

@app.get("/analyze/{symbol}")
async def analyze_patterns(symbol: str, timeframe: str = "1D"):
    return await analyze_stream(symbol, timeframe)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
