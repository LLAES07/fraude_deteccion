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
