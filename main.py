"""
Trabajo Práctico Integrador - Programación 1 (TUPaD / UTN)
Gestión de Datos de Países en Python: filtros, ordenamientos y estadísticas.

Autor: Mauro Villanueva
Descripción:
    Aplicación de consola que gestiona un dataset de países cargado desde un
    archivo CSV. Permite agregar, actualizar, buscar, filtrar y ordenar países,
    y calcular estadísticas. El estado se mantiene en memoria como una lista de
    diccionarios y puede persistirse nuevamente en el CSV.

Estructura de datos:
    Cada país es un diccionario:
        {
            "nombre": str,
            "poblacion": int,
            "superficie": int,   # km2
            "continente": str
        }
    El conjunto de países es una lista de esos diccionarios.
"""

import os
import csv

# ---------------------------------------------------------------------------
# Configuración global
# ---------------------------------------------------------------------------

RUTA_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "paises.csv")
CAMPOS = ["nombre", "poblacion", "superficie", "continente"]


# ---------------------------------------------------------------------------
# Utilidades de interfaz
# ---------------------------------------------------------------------------

def limpiar_pantalla():
    """Limpia la consola de forma multiplataforma (Windows / Unix)."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """Detiene la ejecución hasta que el usuario presione Enter."""
    leer_entrada("\nPresione Enter para continuar...")


def imprimir_encabezado(titulo):
    """Imprime un encabezado uniforme para cada sección."""
    print("\n" + "=" * 60)
    print(f" {titulo}")
    print("=" * 60 + "\n")


# ---------------------------------------------------------------------------
# Validaciones de entrada (una responsabilidad cada una)
# ---------------------------------------------------------------------------

def leer_entrada(mensaje=""):
    """
    Lectura central de teclado con control de errores.
    Todas las lecturas del programa pasan por aquí, de modo que la interrupción
    con Ctrl+C (KeyboardInterrupt) o el cierre de la entrada estándar (EOFError)
    se manejan de forma uniforme y ordenada en lugar de abortar el programa con
    un error. En esos casos se informa y se cierra el programa de forma limpia.
    """
    try:
        return input(mensaje)
    except (KeyboardInterrupt, EOFError):
        print("\n\nEntrada interrumpida por el usuario. Cerrando el programa...")
        raise SystemExit(0)


def leer_texto(mensaje):
    """Solicita un texto no vacío. Repite hasta obtener una entrada válida."""
    while True:
        valor = leer_entrada(mensaje).strip()
        if valor:
            return valor
        print("Error: el campo no puede quedar vacío.\n")


def leer_entero_positivo(mensaje):
    """Solicita un entero > 0. Valida el tipo y repite ante entradas inválidas."""
    while True:
        entrada = leer_entrada(mensaje).strip()
        if not entrada.isdigit():
            print("Error: ingrese un número entero positivo (solo dígitos).\n")
            continue
        valor = int(entrada)
        if valor <= 0:
            print("Error: el valor debe ser mayor que cero.\n")
            continue
        return valor


def leer_entero_positivo_opcional(mensaje):
    """
    Igual que leer_entero_positivo pero permite dejar vacío (devuelve None).
    Se usa en la actualización, donde un campo vacío significa 'no modificar'.
    """
    while True:
        entrada = leer_entrada(mensaje).strip()
        if entrada == "":
            return None
        if not entrada.isdigit():
            print("Error: ingrese un entero positivo o deje vacío para omitir.\n")
            continue
        valor = int(entrada)
        if valor <= 0:
            print("Error: el valor debe ser mayor que cero.\n")
            continue
        return valor


def leer_opcion(mensaje, opciones_validas):
    """
    Solicita una opción y la valida contra un conjunto de valores permitidos.
    La comparación no distingue mayúsculas de minúsculas. Repite hasta que el
    usuario ingrese una de las opciones válidas, evitando fallos por entradas
    fuera de rango o vacías.
    """
    validas = ", ".join(sorted(opciones_validas))
    while True:
        opcion = leer_entrada(mensaje).strip().lower()
        if opcion in opciones_validas:
            return opcion
        print(f"Error: opción inválida. Opciones válidas: {validas}.\n")


# ---------------------------------------------------------------------------
# Manejo de archivos CSV
# ---------------------------------------------------------------------------

def cargar_paises(ruta=RUTA_CSV):
    """
    Lee el CSV y devuelve una lista de diccionarios.
    Controla errores de formato: descarta filas con datos numéricos inválidos
    o campos faltantes, informando al usuario sin abortar la carga.
    """
    paises = []
    if not os.path.exists(ruta):
        print(f"Aviso: no se encontró el archivo '{ruta}'. Se inicia con lista vacía.\n")
        return paises

    try:
        with open(ruta, mode="r", encoding="utf-8", newline="") as archivo:
            lector = csv.DictReader(archivo)
            for numero, fila in enumerate(lector, start=2):  # línea 1 = encabezado
                try:
                    nombre = fila["nombre"].strip()
                    continente = fila["continente"].strip()
                    poblacion = int(fila["poblacion"].strip())
                    superficie = int(fila["superficie"].strip())

                    if not nombre or not continente:
                        raise ValueError("campo de texto vacío")
                    if poblacion <= 0 or superficie <= 0:
                        raise ValueError("valor numérico no positivo")

                    paises.append({
                        "nombre": nombre,
                        "poblacion": poblacion,
                        "superficie": superficie,
                        "continente": continente,
                    })
                except (KeyError, ValueError, AttributeError):
                    print(f"Aviso: fila {numero} descartada por formato inválido.")
    except OSError as error:
        print(f"Error al leer el archivo: {error}\n")

    return paises


def guardar_paises(paises, ruta=RUTA_CSV):
    """Persiste la lista de países en el CSV. Devuelve True si tuvo éxito."""
    try:
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, mode="w", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
            escritor.writeheader()
            escritor.writerows(paises)
        return True
    except OSError as error:
        print(f"Error al guardar el archivo: {error}\n")
        return False


# ---------------------------------------------------------------------------
# Operaciones sobre el dataset
# ---------------------------------------------------------------------------

def buscar_por_nombre_exacto(paises, nombre):
    """Devuelve el país cuyo nombre coincide exactamente (sin distinguir mayúsculas), o None."""
    for pais in paises:
        if pais["nombre"].lower() == nombre.lower():
            return pais
    return None


def agregar_pais(paises):
    """Agrega un país validando que no existan campos vacíos ni duplicados."""
    imprimir_encabezado("AGREGAR PAÍS")

    nombre = leer_texto("Nombre del país: ")
    if buscar_por_nombre_exacto(paises, nombre) is not None:
        print(f"\nError: '{nombre}' ya existe en el dataset.")
        return

    poblacion = leer_entero_positivo("Población (entero positivo): ")
    superficie = leer_entero_positivo("Superficie en km2 (entero positivo): ")
    continente = leer_texto("Continente: ")

    paises.append({
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente,
    })
    print(f"\nÉxito: país '{nombre}' agregado correctamente.")


def actualizar_pais(paises):
    """Actualiza población y/o superficie de un país existente."""
    imprimir_encabezado("ACTUALIZAR PAÍS")

    if not paises:
        print("No hay países cargados.")
        return

    nombre = leer_texto("Nombre del país a actualizar: ")
    pais = buscar_por_nombre_exacto(paises, nombre)
    if pais is None:
        print(f"\nError: no se encontró el país '{nombre}'.")
        return

    print(f"\nDatos actuales -> Población: {pais['poblacion']:,} | "
        f"Superficie: {pais['superficie']:,} km2")
    print("Deje el campo vacío para conservar el valor actual.\n")

    nueva_poblacion = leer_entero_positivo_opcional("Nueva población: ")
    nueva_superficie = leer_entero_positivo_opcional("Nueva superficie (km2): ")

    if nueva_poblacion is None and nueva_superficie is None:
        print("\nNo se realizaron cambios.")
        return

    if nueva_poblacion is not None:
        pais["poblacion"] = nueva_poblacion
    if nueva_superficie is not None:
        pais["superficie"] = nueva_superficie

    print(f"\nÉxito: país '{pais['nombre']}' actualizado correctamente.")


def buscar_pais(paises):
    """Busca países por coincidencia parcial o exacta en el nombre."""
    imprimir_encabezado("BUSCAR PAÍS")

    if not paises:
        print("No hay países cargados.")
        return

    termino = leer_texto("Ingrese el nombre o parte del nombre: ").lower()
    resultados = [p for p in paises if termino in p["nombre"].lower()]

    if not resultados:
        print(f"\nSin resultados para '{termino}'.")
        return

    print(f"\nSe encontraron {len(resultados)} coincidencia(s):")
    mostrar_tabla(resultados)


# ---------------------------------------------------------------------------
# Filtros
# ---------------------------------------------------------------------------

def filtrar_por_continente(paises):
    """Filtra países por continente (coincidencia exacta sin distinguir mayúsculas)."""
    continente = leer_texto("Ingrese el continente: ")
    resultados = [p for p in paises if p["continente"].lower() == continente.lower()]
    if not resultados:
        print(f"\nSin países en el continente '{continente}'.")
    else:
        print(f"\nPaíses en {continente}:")
        mostrar_tabla(resultados)


def filtrar_por_rango(paises, clave, etiqueta):
    """
    Filtra por un rango numérico sobre 'clave' (poblacion o superficie).
    Valida que el mínimo no supere al máximo.
    """
    print(f"\nDefina el rango de {etiqueta}:")
    minimo = leer_entero_positivo("  Valor mínimo: ")
    maximo = leer_entero_positivo("  Valor máximo: ")

    if minimo > maximo:
        print("\nError: el mínimo no puede ser mayor que el máximo.")
        return

    resultados = [p for p in paises if minimo <= p[clave] <= maximo]
    if not resultados:
        print(f"\nSin países con {etiqueta} entre {minimo:,} y {maximo:,}.")
    else:
        print(f"\nPaíses con {etiqueta} entre {minimo:,} y {maximo:,}:")
        mostrar_tabla(resultados)


def menu_filtros(paises):
    """Submenú de filtros: continente, rango de población o de superficie."""
    imprimir_encabezado("FILTRAR PAÍSES")

    if not paises:
        print("No hay países cargados.")
        return

    print("1. Por continente")
    print("2. Por rango de población")
    print("3. Por rango de superficie")
    opcion = leer_opcion("\nSeleccione una opción: ", {"1", "2", "3"})

    if opcion == "1":
        filtrar_por_continente(paises)
    elif opcion == "2":
        filtrar_por_rango(paises, "poblacion", "población")
    elif opcion == "3":
        filtrar_por_rango(paises, "superficie", "superficie")


# ---------------------------------------------------------------------------
# Ordenamientos
# ---------------------------------------------------------------------------

def ordenar_paises(paises):
    """Ordena por nombre, población o superficie, en sentido ascendente o descendente."""
    imprimir_encabezado("ORDENAR PAÍSES")

    if not paises:
        print("No hay países cargados.")
        return

    print("Criterio de orden:")
    print("1. Nombre")
    print("2. Población")
    print("3. Superficie")
    criterio = leer_opcion("\nSeleccione un criterio: ", {"1", "2", "3"})
    claves = {"1": "nombre", "2": "poblacion", "3": "superficie"}
    clave = claves[criterio]

    print("\nSentido:")
    print("1. Ascendente")
    print("2. Descendente")
    sentido = leer_opcion("\nSeleccione el sentido: ", {"1", "2"})
    descendente = (sentido == "2")

    if clave == "nombre":
        ordenados = sorted(paises, key=lambda p: p["nombre"].lower(), reverse=descendente)
    else:
        ordenados = sorted(paises, key=lambda p: p[clave], reverse=descendente)

    texto_sentido = "descendente" if descendente else "ascendente"
    print(f"\nPaíses ordenados por {clave} ({texto_sentido}):")
    mostrar_tabla(ordenados)


# ---------------------------------------------------------------------------
# Estadísticas
# ---------------------------------------------------------------------------

def mostrar_estadisticas(paises):
    """Muestra país con mayor y menor población, promedios y conteo por continente."""
    imprimir_encabezado("ESTADÍSTICAS")

    if not paises:
        print("No hay países cargados.")
        return

    mayor = max(paises, key=lambda p: p["poblacion"])
    menor = min(paises, key=lambda p: p["poblacion"])
    promedio_poblacion = sum(p["poblacion"] for p in paises) / len(paises)
    promedio_superficie = sum(p["superficie"] for p in paises) / len(paises)

    print(f"Total de países: {len(paises)}\n")
    print(f"Mayor población: {mayor['nombre']} ({mayor['poblacion']:,} hab.)")
    print(f"Menor población: {menor['nombre']} ({menor['poblacion']:,} hab.)")
    print(f"Promedio de población: {promedio_poblacion:,.2f} hab.")
    print(f"Promedio de superficie: {promedio_superficie:,.2f} km2\n")

    conteo = contar_por_continente(paises)
    print("Cantidad de países por continente:")
    for continente in sorted(conteo):
        print(f"  {continente}: {conteo[continente]}")


def contar_por_continente(paises):
    """Devuelve un diccionario {continente: cantidad}."""
    conteo = {}
    for pais in paises:
        continente = pais["continente"]
        conteo[continente] = conteo.get(continente, 0) + 1
    return conteo


# ---------------------------------------------------------------------------
# Presentación de datos
# ---------------------------------------------------------------------------

def mostrar_tabla(paises):
    """
    Imprime una tabla formateada con los países recibidos.
    El ancho de la columna Nombre se adapta al país más largo de la lista,
    con un tope máximo: los nombres que lo superan se truncan con puntos
    suspensivos para que las columnas nunca se desalineen.
    """
    if not paises:
        print("(sin datos)")
        return

    ANCHO_MAXIMO_NOMBRE = 38  # tope para no desbordar en nombres muy largos

    # Ancho de la columna Nombre: el del país más largo, acotado al tope.
    ancho_nombre = max(len("Nombre"), max(len(p["nombre"]) for p in paises))
    ancho_nombre = min(ancho_nombre, ANCHO_MAXIMO_NOMBRE)

    def recortar(texto, ancho):
        """Trunca el texto con '...' si supera el ancho de la columna."""
        if len(texto) > ancho:
            return texto[:ancho - 3] + "..."
        return texto

    ancho_total = ancho_nombre + 16 + 20 + 14

    encabezado = (f"\n{'Nombre':<{ancho_nombre}}"
                f"{'Población':>16}"
                f"{'Superficie (km2)':>20}"
                f"{'Continente':>14}")
    print(encabezado)
    print("-" * ancho_total)
    for pais in paises:
        nombre = recortar(pais["nombre"], ancho_nombre)
        print(f"{nombre:<{ancho_nombre}}"
            f"{pais['poblacion']:>16,}"
            f"{pais['superficie']:>20,}"
            f"{pais['continente']:>14}")
    print("-" * ancho_total)


def listar_todos(paises):
    """Muestra el listado completo de países cargados."""
    imprimir_encabezado("LISTADO COMPLETO")
    if not paises:
        print("No hay países cargados.")
    else:
        print(f"Total: {len(paises)} países")
        mostrar_tabla(paises)


# ---------------------------------------------------------------------------
# Persistencia manual
# ---------------------------------------------------------------------------

def guardar_en_archivo(paises):
    """Opción de menú para persistir los cambios en el CSV."""
    imprimir_encabezado("GUARDAR CAMBIOS")
    if guardar_paises(paises):
        print(f"Éxito: {len(paises)} países guardados en '{RUTA_CSV}'.")


# ---------------------------------------------------------------------------
# Menú principal
# ---------------------------------------------------------------------------

def mostrar_menu():
    """Imprime el menú principal de opciones."""
    print("\n" + "=" * 60)
    print(" GESTIÓN DE DATOS DE PAÍSES")
    print("=" * 60)
    print(" 1. Listar todos los países")
    print(" 2. Agregar país")
    print(" 3. Actualizar país (población / superficie)")
    print(" 4. Buscar país por nombre")
    print(" 5. Filtrar países")
    print(" 6. Ordenar países")
    print(" 7. Mostrar estadísticas")
    print(" 8. Guardar cambios en el CSV")
    print(" 0. Salir")
    print("=" * 60)


def main():
    """Punto de entrada. Carga datos y ejecuta el bucle principal del menú."""
    limpiar_pantalla()
    print("Cargando dataset de países...\n")
    paises = cargar_paises()
    print(f"Se cargaron {len(paises)} países.")
    pausar()

    while True:
        limpiar_pantalla()
        mostrar_menu()
        opcion = leer_entrada("\nSeleccione una opción: ").strip()

        if opcion == "1":
            listar_todos(paises)
        elif opcion == "2":
            agregar_pais(paises)
        elif opcion == "3":
            actualizar_pais(paises)
        elif opcion == "4":
            buscar_pais(paises)
        elif opcion == "5":
            menu_filtros(paises)
        elif opcion == "6":
            ordenar_paises(paises)
        elif opcion == "7":
            mostrar_estadisticas(paises)
        elif opcion == "8":
            guardar_en_archivo(paises)
        elif opcion == "0":
            imprimir_encabezado("SALIR")
            respuesta = leer_opcion(
                "¿Desea guardar los cambios antes de salir? (s/n): ", {"s", "n"})
            if respuesta == "s":
                guardar_paises(paises)
                print("Cambios guardados.")
            print("\nPrograma finalizado. ¡Hasta luego!")
            break
        else:
            print("\nOpción inválida. Intente nuevamente.")

        pausar()


if __name__ == "__main__":
    main()