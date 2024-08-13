import pandas as pd
import yaml
import mysql.connector
import articulos


with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

gem = mysql.connector.connect(
    host = config['gem']["host"],
    user = config['gem']["user"],
    password = config['gem']["password"],
    database = config['gem']["database"]
)

engine = gem.cursor(buffered=True)

def barrido_presentismo(origen, fecha_desde, fecha_hasta):
    
    novedades = servicio_novedades(origen, fecha_desde,fecha_hasta)
    novedades_generadas = procesar_novedades(novedades)
    # df.to_excel("excel_magico.xlsx")
    # print(df)
    # que retorne un json 

def servicio_novedades(origen, fecha_desde, fecha_hasta):
    if origen == 'gem':
        query = f"""SELECT 
                p.cuil,
                sn.servicio_id,
                sn.fecha_desde,
                sn.fecha_hasta,
                sn.dias,
                sn.obligaciones,
                concat(nt.articulo, '-', nt.inciso) as articulo,
                nt.descripcion_corta,
                nt.tipo
            FROM servicio_novedad sn 
                JOIN novedad_tipo nt ON nt.id = sn.novedad_tipo_id
                join servicio s on s.id = sn.servicio_id
                join persona p on p.id = s.persona_id
            WHERE sn.fecha_desde = '{fecha_desde}' and sn.fecha_hasta = '{fecha_hasta}' and ((nt.tipo = 'A' OR nt.tipo = 'S') OR (nt.articulo = '50' AND nt.inciso = '8'));"""
    
    engine.execute(query)
    rows = engine.fetchall()
    columns = [desc[0] for desc in engine.description]
    df = pd.DataFrame(rows, columns=columns)
    # for columna, valor in df.iterrows():
    #     print(columna, valor)
    # else:
    #     query = f"""SELECT 
    #         n.Percuil,
    #         n.SrvPofCod,
    #         sn.servicio_id,
    #         sn.fecha_desde,
    #         sn.fecha_hasta,
    #         nt.articulo,
    #         nt.inciso,
    #         nt.descripcion_corta,
    #         nt.tipo
    #     FROM novedad n 
    #         JOIN novedad_tipo nt ON nt.id = sn.novedad_tipo_id
    #         join servicio s on s.id = sn.servicio_id
    #         WHERE sn.fecha_desde = '{fecha_desde}' and sn.fecha_hasta = '{fecha_hasta}' and ((nt.tipo = 'A' OR nt.tipo = 'S') OR (nt.articulo = '50' AND nt.inciso = '8'));"""

  
    # engine.close()
    # gem.close()
    return df

def procesar_novedades(novedades):
    for novedad in novedades:
        novedad.presentismo = articulos.articulos(novedad)
        

# def calcular_presentismo(novedad):
    

barrido_presentismo('gem', '2024-07-01', '2024-07-31')
# def procesar_novedades(novedades):
#     for novedad in novedades:
        



