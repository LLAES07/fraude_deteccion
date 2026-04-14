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
