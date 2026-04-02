# AI-Powered SQL Generator
Query your database using natural language! 🚀

## Features
- **NL to SQL**: Instantly convert questions into functional SQL.
- **Multi-Model Support**: Use local Llama 2 (via GGUF) or high-speed cloud providers (Groq, Gemini).
- **Interactive UI**: Preview results, verify schemas, and execute changes directly from Streamlit.
- **Safety Mode**: Automatic detection and confirmation required for data-modifying queries (INSERT/UPDATE/DELETE).

## 🚀 How to Run Locally

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database**:
   ```bash
   python src/init_db.py
   ```

3. **Launch the App**:
   ```bash
   streamlit run app.py
   ```

## ☁️ Deploying on Streamlit Cloud

1. **GitHub**: Push your fork of this repository to GitHub.
2. **Connect**: Go to [share.streamlit.io](https://share.streamlit.io), connect your GitHub account, and select this repository.
3. **Settings**:
   - **Main file path**: `app.py`
   - **Secrets** (Optional): You can store your `GROQ_API_KEY` or `GOOGLE_API_KEY` in the [Streamlit Secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/secrets-management) dashboard for automatic login.
4. **Deploy**: Hit 'Deploy' and your app will be live!

## 🛠️ Project Structure
- `app/`: Streamlit frontend logic.
- `src/`: Backend logic for SQL generation and database management.
- `data/`: Local SQLite database storage.
- `config.yaml`: Central configuration for LLM and Database.
