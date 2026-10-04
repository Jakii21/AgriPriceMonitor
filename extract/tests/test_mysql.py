import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="aiki",
        database="agriproject_db"
    )

    if conn.is_connected():
        print("MySQL connection successful!")

except mysql.connector.Error as e:
    print("MySQL connection error:", e)

finally:
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("Connection closed.")

