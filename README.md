# Airflow ETL Project

Este proyecto implementa un pipeline ETL (Extract, Transform, Load) usando Apache Airflow para procesar datos de Olist E-commerce. El pipeline se ejecuta cada 5 minutos y sigue una arquitectura de medallón (Bronze, Silver, Gold).

## Estructura del Proyecto

```
airflow_etl_todo/
├── dags/
│   ├── data/              # Directorio para archivos de datos
│   │   ├── bronze/        # Archivos CSV descargados
│   │   └── ecommerce.db   # Base de datos SQLite
│   └── etl_olist.py       # Definición del DAG
├── scripts/
│   ├── extract.py         # Descarga de datos
│   ├── load.py            # Carga en tablas bronze
│   ├── cleaning.py        # Creación de tablas silver
│   └── transform.py       # Creación de tablas gold
└── docker-compose.yaml     # Configuración de Docker
```

## Componentes del Pipeline

### 1. Extract (extract.py)
- **Función**: `extract_data()`
- **Descripción**: Descarga archivos CSV desde Google Drive
- **Archivos procesados**:
  - `olist_orders.csv`
  - `olist_order_payments.csv`
  - `olist_customers.csv`

### 2. Load (load.py)
- **Función**: `load_data()`
- **Descripción**: Carga los CSV en tablas bronze en SQLite
- **Tablas creadas**:
  - `bronze_olist_orders`
  - `bronze_olist_order_payments`
  - `bronze_olist_customers`

### 3. Clean (cleaning.py)
- **Función**: `clean_data()`
- **Descripción**: Crea tablas silver como copias limpias de las tablas bronze
- **Tablas creadas**:
  - `silver_orders`
  - `silver_order_payments`
  - `silver_customers`

### 4. Transform (transform.py)
- **Función**: `transform_data()`
- **Descripción**: Crea tablas gold con análisis de negocio
- **Análisis realizados**:
  - `gold_top_states`: Top 10 estados con mayor ingreso
  - `gold_delivery_comparison`: Comparación de tiempos de entrega estimados vs reales

## DAG (etl_olist.py)

- **Schedule**: Cada 5 minutos
- **Configuración**:
  - `max_active_runs=1`: Evita ejecuciones paralelas
  - `catchup=False`: No ejecuta DAGs históricos

### Flujo de Tareas
```
extract_data >> load_data >> cleaning_data >> transform_data
```

## Base de Datos

El proyecto utiliza SQLite (`ecommerce.db`) con una arquitectura de medallón:
- **Bronze**: Datos crudos desde CSV
- **Silver**: Datos limpios y estructurados
- **Gold**: Tablas analíticas para insights de negocio

## Requisitos

- Docker y Docker Compose
- Apache Airflow 2.7.1
- Python 3.x
- Dependencias:
  - pandas
  - sqlite3
#   a i r f l o w - t a s k s  
 