import sqlite3
import os

def init_db():
    db_path = "data/my_database.db"
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        join_date DATE,
        city TEXT
    )
    ''')
    
    # Create Products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        category TEXT,
        price REAL
    )
    ''')
    
    # Create Sales table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        sale_date DATE,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    ''')
    
    # Insert Sample data
    users = [
        (1, 'Alice Johnson', 'alice@example.com', '2023-01-15', 'New York'),
        (2, 'Bob Smith', 'bob@example.com', '2023-02-20', 'Los Angeles'),
        (3, 'Charlie Brown', 'charlie@example.com', '2023-03-10', 'Chicago'),
        (4, 'Diana Prince', 'diana@example.com', '2023-04-05', 'New York'),
        (5, 'Evan Wright', 'evan@example.com', '2023-05-11', 'Seattle'),
        (6, 'Fiona Glenanne', 'fiona@example.com', '2023-06-21', 'Miami'),
        (7, 'George Miller', 'george@example.com', '2023-07-08', 'Chicago'),
        (8, 'Hannah Abbott', 'hannah@example.com', '2023-08-30', 'Houston'),
        (9, 'Ian Malcolm', 'ian@example.com', '2023-09-14', 'Austin'),
        (10, 'Julia Roberts', 'julia@example.com', '2023-10-01', 'Los Angeles'),
    ]
    
    products = [
        (1, 'Laptop', 'Electronics', 1200.00),
        (2, 'Phone', 'Electronics', 800.00),
        (3, 'Monitor', 'Electronics', 300.00),
        (4, 'Coffee Maker', 'Appliances', 100.00),
        (5, 'Office Chair', 'Furniture', 150.00),
        (6, 'Desk Lamp', 'Furniture', 45.00),
        (7, 'Wireless Mouse', 'Electronics', 25.00),
        (8, 'Mechanical Keyboard', 'Electronics', 110.00),
        (9, 'Blender', 'Appliances', 60.00),
        (10, 'Toaster', 'Appliances', 40.00),
    ]
    
    sales = [
        (1, 1, 1, 1, '2023-05-01'),
        (2, 2, 2, 1, '2023-05-02'),
        (3, 1, 4, 2, '2023-05-03'),
        (4, 3, 3, 1, '2023-05-04'),
        (5, 4, 1, 1, '2023-05-05'),
        (6, 5, 5, 2, '2023-06-10'),
        (7, 6, 7, 1, '2023-06-12'),
        (8, 7, 8, 1, '2023-07-20'),
        (9, 8, 2, 1, '2023-08-01'),
        (10, 9, 10, 3, '2023-09-15'),
        (11, 10, 1, 1, '2023-10-02'),
        (12, 1, 7, 2, '2023-10-05'),
        (13, 2, 8, 1, '2023-10-10'),
        (14, 3, 9, 1, '2023-11-11'),
        (15, 6, 4, 1, '2023-11-20'),
        (16, 8, 5, 4, '2023-12-01'),
        (17, 10, 3, 2, '2023-12-15'),
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO users VALUES (?,?,?,?,?)', users)
    cursor.executemany('INSERT OR IGNORE INTO products VALUES (?,?,?,?)', products)
    cursor.executemany('INSERT OR IGNORE INTO sales VALUES (?,?,?,?,?)', sales)
    
    conn.commit()
    conn.close()
    print(f"Database created successfully at {db_path}")

if __name__ == "__main__":
    init_db()
