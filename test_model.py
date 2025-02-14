from transformers import AutoModelForCausalLM, AutoTokenizer
import numpy as np
import pandas as pd

# Load model
model = AutoModelForCausalLM.from_pretrained("codellama/CodeLlama-7b-hf")
tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-7b-hf")

# Create test data
days = 150
base_price = 100
price_changes = np.random.normal(0.001, 0.02, days).cumsum()
prices = base_price * (1 + price_changes)

test_data = pd.DataFrame({
    'open': prices * (1 + np.random.normal(0, 0.005, days)),
    'high': prices * (1 + np.random.normal(0.01, 0.008, days)),
    'low': prices * (1 + np.random.normal(-0.01, 0.008, days)),
    'close': prices * (1 + np.random.normal(0, 0.005, days)),
    'volume': np.random.normal(1000000, 200000, days)
})

# Test pattern detection
prompt = f"""
Analyze this OHLCV data and detect patterns:
{test_data.head().to_string()}
Return: Pattern type and coordinates
"""

inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_length=500)
result = tokenizer.decode(outputs[0])

print("Model Output:", result)
