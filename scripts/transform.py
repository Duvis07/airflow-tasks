import sqlite3
import os

# Pistas 
# 1. Conectarse a la base de datos donde están las tablas Silver
# 2. Guarda los queries realizados en el trabajo pasado como un string

def transform_data():
    db_path = '/opt/airflow/dags/data/ecommerce.db'
    # Conexión a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query 1: Top 10 estados con mayor ingreso (str)
    query1 = """
    DROP TABLE IF EXISTS gold_top_states;
    CREATE TABLE gold_top_states AS
    WITH order_values AS (
        SELECT 
            c.customer_state,
            SUM(op.payment_value) as total_revenue
        FROM silver_orders o
        JOIN silver_order_payments op ON o.order_id = op.order_id
        JOIN silver_customers c ON o.customer_id = c.customer_id
        GROUP BY c.customer_state
    )
    SELECT 
        customer_state,
        total_revenue,
        RANK() OVER (ORDER BY total_revenue DESC) as revenue_rank
    FROM order_values
    ORDER BY total_revenue DESC
    LIMIT 10;
    """

    # Query 2: Comparación de tiempos reales vs estimados por mes y año (str)
    query2 = """
    DROP TABLE IF EXISTS gold_delivery_comparison;
    CREATE TABLE gold_delivery_comparison AS
    SELECT 
        strftime('%Y', order_delivered_customer_date) as year,
        strftime('%m', order_delivered_customer_date) as month,
        COUNT(*) as total_orders,
        AVG(JULIANDAY(order_delivered_customer_date) - JULIANDAY(order_estimated_delivery_date)) as avg_delivery_difference,
        SUM(CASE WHEN JULIANDAY(order_delivered_customer_date) <= JULIANDAY(order_estimated_delivery_date) THEN 1 ELSE 0 END) as on_time_deliveries,
        SUM(CASE WHEN JULIANDAY(order_delivered_customer_date) > JULIANDAY(order_estimated_delivery_date) THEN 1 ELSE 0 END) as delayed_deliveries
    FROM silver_orders
    WHERE order_delivered_customer_date IS NOT NULL
    GROUP BY year, month
    ORDER BY year, month;
    """

    print("🚀 Ejecutando queries para crear tablas Gold...")
    cursor.executescript(query1)
    cursor.executescript(query2)

    conn.commit()
    conn.close()
    print("✅ Tablas Gold creadas en ecommerce.db: 'gold_top_states' y 'gold_delivery_comparison'")
