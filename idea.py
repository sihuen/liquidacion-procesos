import calculo_art


def main():

    lista_de_cosas_a_insertar_mas_adelante = []

    #preparar datos que seran usados
    novedades_anuales = traer_novedades_anuales()

    novedades = traer_novedades()
    # cuil | servicio | articulo | dias | obligaciones |  fecha_desde | fecha_hasta
    novedades = agregar_propiedades(novedades) # a cada novedad, agregar/calcular 3 propiedades (presentismo, goce, dias/oblig) 
    # cuil | servicio | articulo | dias | obligaciones |  fecha_desde | fecha_hasta | presentismo | goce | dias/oblig
    novedades_por_servicio = calcular_propiedades_por_servicio(novedades) # agrupar el resltado anterior por servicio
    generar_excel(novedades_por_servicio)

    guardar_en_la_base_nodeades = escribir(lista_de_cosas_a_insertar_mas_adelante)

def traer_novedades(origen, fecha_desde, fecha_hasta):
    if origen == 'gem':
        query = f"""SELECT p.cuil, servicio_id as servicio, situacion_revista, novedad_tipo.articulo, dias, obligaciones, fecha_desde, fecha_hasta
            FROM servicio_novedad WHERE etc etc"""
        return conn.execute(query).fetchall()
    if origen == 'rrhh':
        query = f"""SELECT p.cuil, legajorrhh as servicio, situacion_revista, novedad_tipo.articulo, dias, obligaciones, fecha_desde, fecha_hasta
            FROM servicio_novedad WHERE etc etc"""
        return conn.execute(query).fetchall()
    

def agregar_propiedades(novedades):
    for novedad in novedades:
        novedad.presentismo = calcular_presentismo(novedad)
        novedad.goce = calcular_goce(novedad)
        novedad.dias_obligaciones = calcular_dias_obligaciones(novedad)
    
    return novedades

def calcular_presentismo(novedad):
    if novedad.articulo == '50-5':
        if novedad.dias == 1:
            return 0
        if novedad.dias == 2:
            return 2
        if novedad.dias >= 5:
            novedad.articulo = 66
            # en el caso de que debamos tener constancia guardada de todos los 66 que creamos
            # crear_novedad(novedad)
    
        
def calcular_propiedades_por_servicio(novedades):
    return novedades.groupby(['servicio']).sum()

def generar_excel(datos):
    return datos.to_excel('test.xlsx')

def crear_novedad(novedad):
    lista_de_cosas_a_insertar_mas_adelante.append(novedad)


def escribir(novedades):
    for novedad in novedades:
        'insert novedad'