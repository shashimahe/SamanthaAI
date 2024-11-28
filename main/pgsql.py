import psycopg2

# Database connection details
DB_CONFIG = {
    "dbname": "samanthadb",
    "user": "shashimahe",
    "password": "Shashi@24",
    "host": "localhost",
    "port": 5432
}

# SQL to create a table
CREATE_TABLE_SQL = """
CREATE TABLE relationships (
    id SERIAL PRIMARY KEY,
    source_node_id INT REFERENCES nodes(id),
    target_node_id INT REFERENCES nodes(id),
    type VARCHAR(100) NOT NULL,
    properties JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
INSERT_NODES = """
INSERT INTO nodes (type, label, properties)
VALUES ("user", "Shashi", );
"""
try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Execute the SQL command
    cursor.execute(INSERT_NODES)
    conn.commit()  # Save changes

    print("Table created successfully!")
except psycopg2.Error as e:
    print(f"Error: {e}")
finally:
    # Close the connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()
