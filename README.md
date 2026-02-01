# 📊 Calculadora Fiscal FIFO (España) - DEGIRO & COINBASE

Este proyecto automatiza el cálculo de ganancias y pérdidas patrimoniales para la declaración de la Renta en España, procesando reportes de **DEGIRO** y **Coinbase**.

## 🛠️ Funcionalidades

- **Procesamiento Inteligente:** Limpieza y normalización de formatos numéricos (coma/punto decimal, símbolos de moneda) de los CSV exportados.
- **Algoritmo FIFO:** Implementación estricta del criterio *First-In-First-Out* (Primero en entrar, primero en salir) para casar ventas con sus compras correspondientes.
- **Estimación IRPF:** Cálculo automático de la cuota a pagar basándose en los **tramos del ahorro de 2025**.
- **Informe Consolidado:** Generación de un archivo `.csv` final con el desglose operación por operación y el resumen total.

## 🚀 Requisitos e Instalación

Necesitas tener **Python 3.x** instalado.

1. Clona el repositorio o descarga el código.
2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt

## 📖 Cómo usarlo

### 1. Exporta tus datos
* **DEGIRO:** Ve a *Estado de cuenta > Exportar* (selecciona formato `.csv`).
* **Coinbase:** Genera el reporte de transacciones (selecciona formato `.csv`).

### 2. Organización
Recomiendo guardar tus archivos descargados en la carpeta `/data` de este proyecto para tenerlos localizados, aunque puedes tenerlos en cualquier lugar de tu PC.

### 3. Ejecución
Abre una terminal en la carpeta principal del proyecto y ejecuta el siguiente comando:

```bash
python src/main.py
```

### 4. Interacción
El script te pedirá el año a fiscalizar (ej. 2025).

Cuando te pida la ruta de los archivos, simplemente arrastra el archivo .csv desde tu carpeta a la ventana de la terminal y pulsa Enter. El script limpiará automáticamente las comillas o rutas extrañas.

⚠️ Aviso Legal
Descargo de responsabilidad:

Este software es una herramienta de ingeniería diseñada para facilitar el cálculo masivo de datos. No constituye asesoramiento fiscal profesional.

Los tramos del IRPF pueden variar según la Comunidad Autónoma o cambios legislativos anuales.

Se recomienda encarecidamente verificar los resultados obtenidos antes de presentar la declaración de la Renta oficial.
