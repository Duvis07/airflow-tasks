# Airflow ETL Project

Este proyecto implementa un pipeline ETL (Extract, Transform, Load) usando Apache Airflow para procesar datos de Olist E-commerce. El pipeline se ejecuta cada 5 minutos y sigue una arquitectura de medallón (Bronze, Silver, Gold).

## 🚀 Inicio Rápido

1. **Requisitos Previos**
   - Docker y Docker Compose
   - Git

2. **Instalación**
   ```bash
   git clone https://github.com/Duvis07/airflow-tasks.git
   cd airflow-tasks
   docker-compose up -d
   ```

3. **Acceso**
   - Airflow UI: http://localhost:8080
   - Usuario: admin
   - Contraseña: admin

## 🏗️ Estructura del Proyecto

```
airflow_etl_todo/
├── dags/
│   ├── data/              # Directorio para datos
│   │   ├── bronze/        # CSVs descargados
│   │   └── ecommerce.db   # Base de datos SQLite
│   └── etl_olist.py       # Definición del DAG
├── scripts/               # Scripts del ETL
│   ├── extract.py         # Descarga de datos
│   ├── load.py            # Carga en tablas bronze
│   ├── cleaning.py        # Creación de tablas silver
│   └── transform.py       # Creación de tablas gold
├── logs/                  # Logs de Airflow
├── plugins/               # Plugins personalizados
└── docker-compose.yaml    # Configuración de Docker
```

## 🔄 Pipeline ETL

### 1. Extract (extract.py)
- **Función**: `extract_data()`
- **Descripción**: Descarga archivos CSV desde Google Drive
- **Archivos**:
  - `olist_orders.csv`
  - `olist_order_payments.csv`
  - `olist_customers.csv`

### 2. Load (load.py)
- **Función**: `load_data()`
- **Descripción**: Carga CSVs en tablas bronze
- **Tablas**:
  - `bronze_olist_orders`
  - `bronze_olist_order_payments`
  - `bronze_olist_customers`

### 3. Clean (cleaning.py)
- **Función**: `clean_data()`
- **Descripción**: Crea tablas silver limpias
- **Tablas**:
  - `silver_orders`
  - `silver_order_payments`
  - `silver_customers`

### 4. Transform (transform.py)
- **Función**: `transform_data()`
- **Descripción**: Crea tablas gold con análisis
- **Análisis**:
  - Top 10 estados por ingresos
  - Métricas de tiempos de entrega

## 🐳 Configuración Docker

### Componentes
- **Airflow Webserver**: UI (puerto 8080)
- **Airflow Scheduler**: Programador
- **PostgreSQL**: Solo para metadatos internos de Airflow
- **LocalExecutor**: Ejecución de tareas

### Bases de Datos
- **SQLite** (`ecommerce.db`): Almacena todos los datos del ETL (bronze, silver, gold)
- **PostgreSQL**: Solo usado internamente por Airflow para su funcionamiento

### Volúmenes
- `/dags`: DAGs y datos
- `/scripts`: Código Python
- `/logs`: Logs de Airflow
- `/plugins`: Plugins personalizados

### Comandos Útiles
```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

## 📊 Arquitectura de Datos

### Bronze Layer
- Datos crudos en CSV
- Sin transformaciones
- Almacenamiento temporal

### Silver Layer
- Datos limpios
- Estructura optimizada
- Listos para análisis

### Gold Layer
- Datos agregados
- Métricas de negocio
- Tablas analíticas

## ⚙️ Configuración DAG
- **Schedule**: Cada 5 minutos
- **max_active_runs**: 1 (evita ejecuciones paralelas)
- **catchup**: False (no ejecuta DAGs históricos)

## 📝 Dependencias
- Apache Airflow 2.7.1
- Python 3.x
- pandas
- requests
- sqlite3

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
#   a i r f l o w - t a s k s 
 
 
