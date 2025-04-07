import pandas as pd
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def extract_data():
    urls = {
        'olist_orders': '17F6q-lhV7HOFDsxyWIy_UTZlw5g-Wauw',
        'olist_order_payments': '1iW5c438VGlzsh4yyqoikBX0hHsZZGXL2',
        'olist_customers': '1YOuXnoJrUDo20b6NBmn1ZwDy-GZ9PdYG'
    }

    # Configurar sesión de requests con reintentos
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    bronze_dir = '/opt/airflow/dags/data/bronze'
    os.makedirs(bronze_dir, exist_ok=True)

    for name, url in urls.items():
        try:
            print(f"⬇️ Descargando {name} desde {url}")
            path = 'https://drive.google.com/uc?export=download&id='+url
            
            # Descargar con timeout de 5 minutos
            response = session.get(path, timeout=300)
            response.raise_for_status()
            
            # Guardar contenido en un archivo temporal
            temp_file = os.path.join(bronze_dir, f"{name}_temp.csv")
            with open(temp_file, 'wb') as f:
                f.write(response.content)
            
            # Leer con pandas y guardar en formato CSV
            df = pd.read_csv(temp_file)
            bronze_path = os.path.join(bronze_dir, f"{name}.csv")
            df.to_csv(bronze_path, index=False)
            
            # Eliminar archivo temporal
            os.remove(temp_file)
            print(f"✅ {name} descargado y guardado en bronze.")
            
        except Exception as e:
            print(f"❌ Error al procesar {name}: {str(e)}")
            raise  # Re-lanzar el error para que Airflow lo detecte
