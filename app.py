import streamlit as st
import sys
import os
import pandas as pd
import yaml

# Import core modules from src
from src.sql_engine import SQLEngine
from src.schema_manager import SchemaManager

def main():
    st.set_page_config(page_title="AI SQL Generator", layout="wide")
    
    st.title("AI SQL Generator")
    st.markdown("Query your own database using natural language and AI.")

    # Sidebar for configuration
    with st.sidebar:
        st.header("Settings")
        provider = st.selectbox("LLM Provider", ["groq", "local_llama", "gemini"])
        
        if provider == "local_llama":
            model_path = st.text_input("Model Path (.bin or .gguf)", value="llama-2-7b-chat.ggmlv3.q4_0.bin")
            st.info("Using `ctransformers` for local inference.")
        elif provider == "gemini":
            api_key = st.text_input("Gemini API Key", type="password", value="")
            if api_key:
                os.environ["GOOGLE_API_KEY"] = api_key
        elif provider == "groq":
            api_key = st.text_input("Groq API Key", type="password", value="")
            if api_key:
                os.environ["GROQ_API_KEY"] = api_key
            st.info("Using Groq Cloud (Llama 3.1 8B) for ultra-fast inference.")

        st.subheader("Database Connection")
        db_conn = st.text_input("Connection String", value="sqlite:///data/my_database.db")
        
        if st.button("Test Connection"):
            try:
                # Update config on the fly for the manager
                if os.path.exists("config.yaml"):
                    with open("config.yaml", "r") as f:
                        cfg = yaml.safe_load(f)
                else:
                    cfg = {'database': {}, 'llm': {}}
                    
                cfg['database']['connection_string'] = db_conn
                cfg['llm']['provider'] = provider
                if provider == "local_llama":
                    cfg['llm']['model_path'] = model_path
                    
                with open("config.yaml", "w") as f:
                    yaml.dump(cfg, f)

                sm = SchemaManager()
                schema = sm.get_schema_context()
                st.success("Connected! Schema loaded.")
                st.text_area("Live Schema Context", schema, height=150)
            except Exception as e:
                st.error(f"Connection failed: {e}")

    # Main area
    query = st.text_input("Ask a question about your database:", placeholder="e.g., How many records are in the users table?")

    if st.button("Generate SQL") and query:
        try:
            with st.spinner("Generating..."):
                sm = SchemaManager()
                schema_context = sm.get_schema_context()
                
                engine = SQLEngine()
                sql = engine.generate_sql(query, schema_context)
                st.session_state['generated_sql'] = sql
                st.session_state['show_execute'] = True
        except Exception as e:
            st.error(f"Error: {e}")

    # Display generated SQL and execution option
    if 'generated_sql' in st.session_state:
        st.subheader("Generated SQL")
        st.code(st.session_state['generated_sql'], language="sql")
        
        sql = st.session_state['generated_sql'].strip().upper()
        is_mutation = any(sql.startswith(cmd) for cmd in ["INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER"])

        if is_mutation:
            st.warning("⚠️ This query will modify your database content.")
            confirm = st.checkbox("I confirm I want to execute this change.")
            if confirm:
                if st.button("Execute Change"):
                    try:
                        sm = SchemaManager()
                        results, columns = sm.execute_query(st.session_state['generated_sql'])
                        st.success("Database updated successfully!")
                        # Clean up state
                        del st.session_state['generated_sql']
                        st.rerun()
                    except Exception as e:
                        st.error(f"Execution Error: {e}")
        else:
            if st.button("Run Query"):
                try:
                    sm = SchemaManager()
                    results, columns = sm.execute_query(st.session_state['generated_sql'])
                    st.subheader("Results")
                    df = pd.DataFrame(results, columns=columns)
                    st.dataframe(df)
                except Exception as e:
                    st.error(f"Execution Error: {e}")

if __name__ == "__main__":
    main()
