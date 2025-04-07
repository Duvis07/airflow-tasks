import sqlite3

#Pistas
# En este paso la idea sería quitar duplicados, manejar nulos, pero como no es el objetivo, 
# Vamos a hacer una copia espejo de los datos, simulando que los datos ya están limpios.
# 1.Conectarse a la base de datos ecommerce.db ubicada en /opt/airflow/dags/data
# 2: Elimine la tabla Silver si ya existe, cree una tabla nueva Silver copiando 
#    todo el contenido de su tabla Bronze correspondiente
#    Cada bloque debe hacer una copia de la tabla Bronze a una nueva tabla Silver
# 3: Guardar los cambios y cerrar la conexión
# 4: Usa print() para mostrar el estado del proceso

def clean_data():
    db_path = '/opt/airflow/dags/data/ecommerce.db'
    
    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(" Iniciando proceso de limpieza...")
    
    # Crear tablas Silver como copias de las tablas Bronze
    tables = {
        'olist_orders': 'orders',
        'olist_order_payments': 'order_payments',
        'olist_customers': 'customers'
    }
    
    for bronze_name, silver_name in tables.items():
        # Eliminar tabla Silver si existe
        cursor.execute(f"DROP TABLE IF EXISTS silver_{silver_name}")
        
        # Crear tabla Silver como copia de Bronze
        cursor.execute(f"""
            CREATE TABLE silver_{silver_name} AS 
            SELECT * FROM bronze_{bronze_name}
        """)
        print(f" ✅ Tabla silver_{silver_name} creada exitosamente")
    
    # Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()
    print(" Proceso de limpieza completado. Todas las tablas Silver han sido creadas.")
