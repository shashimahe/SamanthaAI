import psycopg2

# Run this command in WSL to port forward 
# ssh -L 5432:localhost:5432 -p 8022 u0_a294@192.168.168.188

# Database connection details
DB_CONFIG = {
    "dbname": "SamanthaDB",
    "user": "shashimahe",
    "password": "Shashi@24",
    "host": "localhost",
    "port": 5432
}

def UpdateDB(query):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Execute the SQL command
        cursor.execute(query)
        
        conn.commit()  # Save changes

        return "Successfully!"
    except psycopg2.Error as e:
        return f"Error: {e}"

def SearchDB(query):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        # Execute the SQL command
        cursor.execute(query)

        rows = cursor.fetchall()
        output = ""
        for row in rows:
            output += f"{row}\n"
        return output
    except psycopg2.Error as e:
        print(f"Error: {e}")
