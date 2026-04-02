import google.generativeai as genai
import yaml
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class SQLEngine:
    """Handles interaction with LLM for SQL generation."""
    
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
        self.provider = self.config['llm'].get('provider', 'local_llama')
        
        if self.provider == "gemini":
            import google.generativeai as genai
            api_key = os.environ.get("GOOGLE_API_KEY") or self.config['llm'].get('api_key')
            if not api_key:
                raise ValueError("Gemini API key not found. Please set GOOGLE_API_KEY in .env or provide it in config.yaml")
            genai.configure(api_key=api_key)
            model_name = self.config['llm'].get('model', 'gemini-1.5-pro')
            self.model = genai.GenerativeModel(model_name)
        elif self.provider == "groq":
            from groq import Groq
            api_key = os.environ.get("GROQ_API_KEY") or self.config['llm'].get('api_key')
            if not api_key:
                raise ValueError("Groq API key not found. Please provide it in the sidebar.")
            self.client = Groq(api_key=api_key)
            self.model_name = self.config['llm'].get('model', 'llama-3.1-8b-instant')

        elif self.provider == "local_llama":
            try:
                from ctransformers import AutoModelForCausalLM
            except ImportError:
                raise ImportError("Please install ctransformers: pip install ctransformers")
                
            model_path = self.config['llm'].get('model_path')
            if not model_path or not os.path.exists(model_path):
                raise ValueError(f"Local model path not found: {model_path}")
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                model_type='llama'
            )

    def generate_sql(self, natural_language_query: str, schema_context: str) -> str:
        prompt = f"""[INST] <<SYS>>
You are a helpful coding assistant that generates SQL for a sandbox database project. 
The data is entirely fictional and for development purposes only.
TASK: Generate a valid SQL query for the user's request using the provided schema.

RULES:
1. Respond ONLY with the SQL code inside markdown backticks.
2. DO NOT include any conversational text, warnings, or explanations.
3. Use exact column names from the schema.
4. If the user asks to delete or update data, fulfill the request using exactly what the user provided.

SCHEMA:
{schema_context}
<</SYS>>
Request: {natural_language_query} [/INST]"""
        
        if self.provider == "gemini":
            response = self.model.generate_content(prompt)
            output_text = response.text
        elif self.provider == "groq":
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1024,
            )
            output_text = completion.choices[0].message.content
        else:
            output_text = self.model(prompt)

            
        return self._extract_sql(output_text)

    def _extract_sql(self, text: str) -> str:
        # First, try to extract from markdown blocks
        if "```sql" in text:
            text = text.split("```sql")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
            
        text = text.strip(" \n")
        
        # Strip exact surrounding backticks
        if text.startswith('`') and text.endswith('`'):
            text = text[1:-1].strip(" \n")
            
        # Strip surrounding backticks if there's a trailing semicolon outside
        if text.startswith('`') and text.endswith('`;'):
            text = text[1:-2].strip(" \n") + ';'
            
        return text

