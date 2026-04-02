from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import IntegrityError
import yaml

class SchemaManager:
    """Handles database schema extraction and query execution."""
    
    def __init__(self, config_path: str = "config.yaml"):
        import os
        from src.init_db import init_db
        
        # Load config or use defaults
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = {
                'database': {'connection_string': "sqlite:///data/my_database.db"},
                'llm': {'provider': 'groq'}
            }
        
        self.connection_string = self.config['database'].get('connection_string', "sqlite:///data/my_database.db")
        
        # Auto-init if it's default SQLite and missing
        if self.connection_string.startswith("sqlite:///"):
            db_file = self.connection_string.replace("sqlite:///", "")
            if not os.path.exists(db_file):
                os.makedirs(os.path.dirname(db_file), exist_ok=True)
                init_db() # Call our init script
        
        self.engine = create_engine(self.connection_string)

    def get_schema_context(self) -> str:
        """Extracts table names and columns from the database."""
        inspector = inspect(self.engine)
        schema_parts = []
        
        for table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            col_list = [f"{col['name']} ({col['type']})" for col in columns]
            schema_parts.append(f"Table: {table_name}\nColumns: {', '.join(col_list)}")
            
        return "\n\n".join(schema_parts)

    def execute_query(self, sql_query: str):
        """Executes one or multiple generated SQL queries and returns results."""
        from sqlalchemy import text
        
        # Split by semicolon and filter out empty strings/comments
        statements = [s.strip() for s in sql_query.split(';') if s.strip()]
        
        results = []
        keys = []
        
        with self.engine.connect() as connection:
            trans = connection.begin()
            try:
                for statement in statements:
                    # Basic cleaning to remove comments which can confuse some drivers
                    clean_stmt = "\n".join([line for line in statement.splitlines() if not line.strip().startswith("--")])
                    if not clean_stmt.strip():
                        continue
                        
                    result = connection.execute(text(clean_stmt))
                    if result.returns_rows:
                        results = result.fetchall()
                        keys = result.keys()
                trans.commit()
                return results, keys
            except IntegrityError as e:
                trans.rollback()
                raise ValueError(f"Constraint failed (e.g. duplicate email/ID): {e.orig}")
            except Exception as e:
                trans.rollback()
                raise e

