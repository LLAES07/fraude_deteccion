# 🛡️ Sistema de Detección de Fraude en Transacciones (Detector de Bots)

Este proyecto implementa un sistema de Machine Learning end-to-end diseñado para detectar transacciones fraudulentas y, específicamente, ataques de bots. El modelo analiza el comportamiento de los usuarios, los patrones temporales de compra y la información del dispositivo/IP para clasificar si una transacción es legítima o fraudulenta.

## 🏗️ Estructura del Proyecto

El proyecto sigue una arquitectura modular y escalable orientada a MLOps:

```text
fraude_deteccion/
├── artifacts/           # Modelos guardados, preprocesadores y datasets procesados
├── data/                # Datasets crudos (Fraud_Data.csv, IpAddress_to_Country.csv)
├── logs/                # Registros de ejecución del sistema
├── notebook/            # Notebooks de Jupyter para exploración de datos (EDA) y pruebas
├── src/                 # Código fuente principal
│   ├── Components/      # Componentes del pipeline (Ingesta, Transformación, Entrenamiento)
│   ├── pipeline/        # Pipelines orquestadores (Entrenamiento y Predicción)
│   ├── exception.py     # Manejo de excepciones personalizadas
│   ├── logger.py        # Configuración del sistema de logging
│   └── utils.py         # Funciones utilitarias (guardar/cargar objetos, etc.)
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Documentación del proyecto
```

## 🛠️ Tecnologías y Requisitos

- Python 3.8+
- Pandas, NumPy
- Scikit-Learn
- LightGBM
- Pickle

## ⚙️ Instalación

1. Clona el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd fraude_deteccion
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   # En Windows: 
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## 🧠 Feature Engineering y Transformación de Datos

El pipeline de transformación (`src/Components/data_transformation.py`) está diseñado para evitar el *data leakage* (fuga de datos) e incluye transformadores personalizados:

- **TimeFeaturesExtractor:** 
  - Calcula el tiempo entre la creación de la cuenta y la primera compra (`time_to_purchase_sec`).
  - Aplica transformación logarítmica para reducir sesgos (`log_time_to_purchase_sec`).
  - Crea una variable binaria `is_ultra_fast` para capturar compras que ocurren en menos de 3 segundos (comportamiento típico de bots).

- **HistoricalFeaturesExtractor:** 
  - *Se ajusta solo con los datos de entrenamiento* (para evitar leakage).
  - Cuenta el número de veces que se utiliza una dirección IP (`ip_count`).
  - Cuenta el número de veces que se utiliza un ID de dispositivo (`device_count`).
  - Cuenta el número de usuarios únicos por IP (`users_per_ip`).
  - Cuenta el número de usuarios únicos por dispositivo (`users_per_device`).

Luego, las variables numéricas se escalan con `StandardScaler` y las categóricas se codifican con `OneHotEncoder`.

## 🤖 Entrenamiento del Modelo

El modelo elegido es un clasificador **LightGBM**, debido a su eficiencia manejando grandes volúmenes de datos y variables numéricas escaladas. 

### Partición de Datos y Mitigación del Desbalanceo
Para capturar mejor el comportamiento real, los datos fueron divididos siguiendo una estrategia especial orientada a la detección de bots:

1. **Test Bots (Holdout de Enero):** Una porción de transacciones de Enero (20%) se aparta exclusivamente para testear la capacidad del modelo ante oleadas rápidas de bots (gran densidad).
2. **Train/Test Normal (Resto del año):** Los meses restantes se dividen en un 70% para entrenamiento y 30% de test normal (comportamiento habitual menos concentrado de bots).
3. **Scale_pos_weight:** Para solucionar el desbalanceo (donde las transacciones normales son inmensamente superiores a las fraudulentas), se calcula y aplica un peso dinámico sobre los positivos.

Ejecutar el pipeline de entrenamiento:
```bash
python -m src.pipeline.train_pipeline
```

## 🔮 Pipeline de Predicción

Para utilizar el modelo entrenado y clasificar nuevas transacciones en tiempo real o por lotes, se dispone del `PredictPipeline`. Este carga automáticamente el modelo LightGBM y el preprocesador guardados en formato `pickle`.

Para integrarlo o probarlo con nueva data:

```python
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# 1. Mapea la información de la nueva transacción
data = CustomData(
    user_id=12345,
    signup_time="2024-01-01 10:00:00",
    purchase_time="2024-01-01 10:00:02", # Ejemplo ultra-rápido (is_ultra_fast = 1)
    purchase_value=150.50,
    device_id="DEV001",
    source="Ads",
    browser="Chrome",
    sex="M",
    age=35,
    ip_address=3.456e9,
    country="US"
)

# 2. Convierte los datos a un DataFrame
df_input = data.get_data_as_data_frame()

# 3. Predice el fraude usando el pipeline
predict_pipeline = PredictPipeline()
prediccion, proba = predict_pipeline.predict(df_input)

print(f"Predicción (1=Fraude, 0=Legítima): {prediccion[0]}")
print(f"Probabilidad de Fraude: {proba[0]:.2%}")
```