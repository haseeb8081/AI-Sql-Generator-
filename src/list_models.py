import google.generativeai as genai
import yaml
import os

def list_gemini_models():
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        api_key = config['llm'].get('api_key')
        if not api_key:
            print("No API key found in config.yaml")
            return

        genai.configure(api_key=api_key)
        
        print("Available models supporting generateContent:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_gemini_models()
