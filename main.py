import pandas as pd
import numpy as np
import os

# --- UTILIDADES ---

def clean_val(val, platform):
    if pd.isna(val) or str(val).strip() == '': return 0.0
    s = str(val).replace('"', '').replace("'", '').strip()
    if platform == 'DEGIRO':
        s = s.replace('.', '').replace(',', '.')
    elif platform == 'COINBASE':
        s = s.replace('€', '').replace(',', '').strip()
    try:
        return float(s)
    except:
        return 0.0

def calcular_impuestos(ganancia):
    if ganancia <= 0: return 0.0
    cuota = 0
    temp = ganancia
    # Tramos Ahorro España 2025
    tramos = [(6000, 0.19), (44000, 0.21), (150000, 0.23), (100000, 0.27), (float('inf'), 0.28)]
    for limite, tipo in tramos:
        porcion = min(temp, limite)
        cuota += porcion * tipo
        temp -= porcion
        if temp <= 0: break
    return cuota

def procesar_fifo(df, platform, anio_objetivo):
    map_cols = {
        'DEGIRO': {'id': 'ISIN', 'qty': 'Número', 'total': 'Total EUR', 'prod': 'Producto'},
        'COINBASE': {'id': 'Asset', 'qty': 'Quantity Transacted', 'total': 'Total (inclusive of fees and/or spread)', 'prod': 'Asset'}
    }
    m = map_cols[platform]
    portfolio = {}
    reporte = []

    for _, row in df.iterrows():
        asset = row[m['id']]
        qty = row[m['qty']]
        total_eur = row[m['total']]
        fecha = row['Fecha_dt']
        
        if asset not in portfolio: portfolio[asset] = []

        es_compra = (platform == 'DEGIRO' and qty > 0) or (platform == 'COINBASE' and row['Transaction Type'] == 'Buy')
        es_venta = (platform == 'DEGIRO' and qty < 0) or (platform == 'COINBASE' and row['Transaction Type'] == 'Sell')

        if es_compra:
            val_c = abs(total_eur)
            portfolio[asset].append({'fecha': fecha, 'qty': abs(qty), 'coste_u': val_c / abs(qty)})
        elif es_venta:
            qty_v, val_v, coste_a, q_pend = abs(qty), abs(total_eur), 0, abs(qty)
            fechas_c = []
            while q_pend > 0 and portfolio[asset]:
                lote = portfolio[asset][0]
                if lote['qty'] > q_pend:
                    coste_a += q_pend * lote['coste_u']
                    lote['qty'] -= q_pend
                    fechas_c.append(lote['fecha'].strftime('%Y-%m-%d'))
                    q_pend = 0
                else:
                    coste_a += lote['qty'] * lote['coste_u']
                    q_pend -= lote['qty']
                    fechas_c.append(lote['fecha'].strftime('%Y-%m-%d'))
                    portfolio[asset].pop(0)

            if fecha.year == anio_objetivo:
                reporte.append({
                    'Plataforma': platform,
                    'Fecha Venta': fecha.strftime('%Y-%m-%d'),
                    'Activo': asset,
                    'Cantidad': qty_v,
                    'Valor Venta': round(val_v, 2),
                    'Valor Compra': round(coste_a, 2),
                    'Ganancia/Pérdida': round(val_v - coste_a, 2),
                    'Origen Compra': ", ".join(set(fechas_c))
                })
    return pd.DataFrame(reporte)

# --- FLUJO DE CONSOLA ---

def main():
    print("\n" + "="*60)
    print("🚀 AUDITORÍA FISCAL CONSOLIDADA: DEGIRO & COINBASE")
    print("="*60)
    
    anio = int(input("📅 ¿De qué año quieres el informe? (ej. 2025): "))
    all_results = []

    # 1. PROCESAR DEGIRO
    print("\n" + "-"*30)
    print("🏦 PASO 1: DEGIRO")
    path_degiro = input("📁 Arrastra el CSV de DEGIRO (o Enter para saltar): ").strip().replace("'", "").replace('"', "")
    
    if path_degiro:
        try:
            df_d = pd.read_csv(path_degiro)
            df_d['Fecha_dt'] = pd.to_datetime(df_d['Fecha'], format='%d-%m-%Y')
            df_d['Número'] = df_d['Número'].apply(lambda x: clean_val(x, 'DEGIRO'))
            df_d['Total EUR'] = df_d['Total EUR'].apply(lambda x: clean_val(x, 'DEGIRO'))
            df_d = df_d.sort_values('Fecha_dt')
            res_d = procesar_fifo(df_d, 'DEGIRO', anio)
            if not res_d.empty:
                print(f"✅ DEGIRO: {res_d['Ganancia/Pérdida'].sum():.2f} € de rendimiento.")
                all_results.append(res_d)
            else: print("⚠️ No hubo ventas en DEGIRO este año.")
        except Exception as e: print(f"❌ Error en DEGIRO: {e}")

    # 2. PROCESAR COINBASE
    print("\n" + "-"*30)
    print("🪙 PASO 2: COINBASE")
    path_cb = input("📁 Arrastra el CSV de COINBASE (o Enter para saltar): ").strip().replace("'", "").replace('"', "")
    
    if path_cb:
        try:
            df_c = pd.read_csv(path_cb, skiprows=3) # Empieza en la fila 4 (index 3)
            df_c['Fecha_dt'] = pd.to_datetime(df_c['Timestamp']).dt.tz_localize(None)
            for col in ['Quantity Transacted', 'Total (inclusive of fees and/or spread)']:
                df_c[col] = df_c[col].apply(lambda x: clean_val(x, 'COINBASE'))
            df_c = df_c[df_c['Transaction Type'].isin(['Buy', 'Sell', 'Convert'])]
            df_c = df_c.sort_values('Fecha_dt')
            res_c = procesar_fifo(df_c, 'COINBASE', anio)
            if not res_c.empty:
                print(f"✅ COINBASE: {res_c['Ganancia/Pérdida'].sum():.2f} € de rendimiento.")
                all_results.append(res_c)
            else: print("⚠️ No hubo ventas en Coinbase este año.")
        except Exception as e: print(f"❌ Error en Coinbase: {e}")

    # 3. RESULTADO FINAL CONSOLIDADO
    if not all_results:
        print("\n❌ No hay datos suficientes para generar informe.")
        return

    df_final = pd.concat(all_results, ignore_index=True)
    total_neto = df_final['Ganancia/Pérdida'].sum()
    impuesto = calcular_impuestos(total_neto)

    print("\n" + "="*60)
    print(f"📊 RESULTADO FINAL CONSOLIDADO {anio}")
    print("="*60)
    print(f"💰 Rendimiento Neto Total:  {total_neto:>10.2f} €")
    print(f"💸 Impuesto Total a Pagar:  {impuesto:>10.2f} €")
    print(f"📈 Tipo Medio Estimado:     {(impuesto/total_neto*100 if total_neto>0 else 0):>10.2f} %")
    print("="*60)

    # Añadir resumen al CSV
    resumen = pd.DataFrame([
        {'Plataforma': '', 'Activo': ''},
        {'Plataforma': 'TOTAL CONSOLIDADO', 'Ganancia/Pérdida': round(total_neto, 2)},
        {'Plataforma': 'CUOTA IRPF ESTIMADA', 'Ganancia/Pérdida': round(impuesto, 2)}
    ])
    df_output = pd.concat([df_final, resumen], ignore_index=True)
    
    output_name = f"Informe_Fiscal_Consolidado_{anio}.csv"
    df_output.to_csv(output_name, index=False, sep=';', encoding='utf-8-sig')
    print(f"\n📄 Archivo consolidado generado: {output_name}")

if __name__ == "__main__":
    main()