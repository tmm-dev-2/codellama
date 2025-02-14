from transformers import AutoModelForCausalLM, AutoTokenizer
import numpy as np
import pandas as pd
import json
from pattern_logic import PatternLogic

class PatternAnalyzer:
    def __init__(self):
        self.model = AutoModelForCausalLM.from_pretrained("tmm-dev/codellama-pattern-analysis")
        self.tokenizer = AutoTokenizer.from_pretrained("tmm-dev/codellama-pattern-analysis")
        self.basic_patterns = {
            'channel': {'min_points': 4, 'confidence_threshold': 0.7},
            'triangle': {'min_points': 3, 'confidence_threshold': 0.75},
            'support': {'min_touches': 2, 'confidence_threshold': 0.8},
            'resistance': {'min_touches': 2, 'confidence_threshold': 0.8},
            'double_top': {'max_deviation': 0.02, 'confidence_threshold': 0.85},
            'double_bottom': {'max_deviation': 0.02, 'confidence_threshold': 0.85}
        }
        self.pattern_logic = PatternLogic()

    def analyze_data(self, ohlcv_data):
        data_prompt = f"""TASK: Identify high-confidence technical patterns only. 
        Minimum confidence threshold: 0.8
        Required pattern criteria:
        1. Channel: Must have at least 3 touching points
        2. Triangle: Must have clear convergence point
        3. Support: Minimum 3 price bounces
        4. Resistance: Minimum 3 price rejections

        INPUT DATA:
        {ohlcv_data.to_json(orient='records')}

        Return ONLY high-confidence patterns (>0.8) in JSON format with exact price coordinates."""

        inputs = self.tokenizer(data_prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_length=1000)
        analysis = self.tokenizer.decode(outputs[0])

        return self.parse_analysis(analysis)
        
    def parse_analysis(self, analysis_text):
        try:
            json_start = analysis_text.find('{')
            json_end = analysis_text.rfind('}') + 1
            json_str = analysis_text[json_start:json_end]
            
            analysis_data = json.loads(json_str)
            patterns = []
            
            for pattern in analysis_data.get('patterns', []):
                pattern_type = pattern.get('type')
                
                if pattern_type in self.basic_patterns:
                    threshold = self.basic_patterns[pattern_type]['confidence_threshold']
                    if pattern.get('confidence', 0) >= threshold:
                        patterns.append({
                            'type': pattern_type,
                            'coordinates': pattern.get('coordinates', []),
                            'confidence': pattern.get('confidence'),
                            'metadata': {
                                'rules': self.basic_patterns[pattern_type],
                                'timestamp': pd.Timestamp.now().isoformat()
                            }
                        })
            
            return patterns
            
        except json.JSONDecodeError:
            return []
