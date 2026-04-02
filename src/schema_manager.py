from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import IntegrityError
import yaml

class SchemaManager:
    """Handles database schema extraction and query execution."""
    
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.connection_string = self.config['database'].get('connection_string')
        if not self.connection_string:
            raise ValueError("Database connection string not found in config.")
        
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

