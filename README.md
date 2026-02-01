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

📖 Cómo usarlo

Exporta tus datos:

DEGIRO: Ve a Estado de cuenta > Exportar (formato CSV).

Coinbase: Genera el reporte de transacciones (formato CSV).

Organización:

Recomiendo guardar tus archivos .csv en la carpeta /data de este proyecto para tenerlos a mano.

Ejecución: Abre una terminal en la carpeta del proyecto y ejecuta:

Bash
python src/main.py
(Asegúrate de que el archivo python se llame main.py o ajusta el comando al nombre que le hayas puesto).

Interacción:
El script te pedirá el año a fiscalizar (ej. 2025).
Cuando te pida los archivos, simplemente arrastra el archivo .csv desde tu carpeta a la ventana de la terminal y pulsa Enter.

⚠️ Aviso Legal
Este software es una herramienta de ayuda técnica para facilitar el cálculo de datos masivos. No constituye asesoramiento fiscal profesional.
Los tramos del IRPF pueden variar según la Comunidad Autónoma o cambios legislativos.
Se recomienda encarecidamente verificar los resultados obtenidos antes de presentar la declaración de la Renta.
