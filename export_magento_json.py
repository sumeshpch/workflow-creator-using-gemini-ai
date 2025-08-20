import mysql.connector
import json

# 🔧 Configure your Magento DB connection here
db_config = {
    "host": "localhost",
    "user": "your_magento_db_user",
    "password": "your_magento_db_password",
    "database": "your_magento_database"
}

# 📦 List of tables to export
tables = [
    "sales_order",
    "sales_order_item",
    "customer_entity",
    "catalog_product_entity"
]

# 📁 Connect and fetch data
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    
    export_data = {}

    for table in tables:
        print(f"Exporting table: {table}")
        cursor.execute(f"SELECT * FROM {table} LIMIT 500")  # Limit optional
        rows = cursor.fetchall()
        export_data[table] = rows

    # 💾 Save to magento_dump.json
    with open("magento_dump.json", "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print("✅ Export complete: magento_dump.json")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
