try:
    import gradio as gr
    print("✅ Gradio imported successfully")
except:
    print("❌ Gradio import failed")

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    print("✅ Transformers imported successfully")
except:
    print("❌ Transformers import failed")

try:
    from lightweight_charts import Chart
    print("✅ Lightweight Charts imported successfully")
except:
    print("❌ Lightweight Charts import failed")

try:
    from fastapi import FastAPI
    print("✅ FastAPI imported successfully")
except:
    print("❌ FastAPI import failed")

try:
    from datasets import Dataset, load_dataset
    print("✅ Datasets imported successfully")
except:
    print("❌ Datasets import failed")
