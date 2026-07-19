# Gestión de Datos de Países en Python

Trabajo Práctico Integrador (TPI) — **Programación 1**
Tecnicatura Universitaria en Programación a Distancia (TUPaD) — Universidad Tecnológica Nacional (UTN)
Primer Cuatrimestre 2026

---

## Descripción del proyecto

Aplicación de consola desarrollada en **Python 3** que permite gestionar un
dataset de países cargado desde un archivo CSV. El sistema ofrece un menú
interactivo para agregar, actualizar, buscar, filtrar y ordenar países, además
de calcular estadísticas del conjunto. El dataset incluye **215 países** con datos
oficiales del Banco Mundial. El objetivo es afianzar el uso de listas,
diccionarios, funciones, estructuras condicionales y repetitivas, ordenamientos,
estadísticas básicas y manejo de archivos CSV.

Cada país se representa como un **diccionario** con cuatro campos (`nombre`,
`poblacion`, `superficie`, `continente`) y el conjunto completo es una **lista de
diccionarios** que se mantiene en memoria durante la ejecución.

## Datos académicos

> **Fuente de los datos:** las poblaciones corresponden a las cifras oficiales del
> Banco Mundial (Indicadores del Desarrollo Mundial, indicador SP.POP.TOTL, año
> 2025) tomadas del archivo de datos oficial actualizado el 13/07/2026. Las
> superficies corresponden al indicador del Banco Mundial AG.SRF.TOTL.K2 (km²,
> último dato disponible). El continente se asignó a partir del código ISO de cada
> país. El dataset cubre 215 países; la sección 4.5 de la documentación incluye una
> tabla de muestra y la referencia completa.

| | |
|---|---|
| **Universidad** | Universidad Tecnológica Nacional (UTN) |
| **Carrera** | Tecnicatura Universitaria en Programación a Distancia (TUPaD) |
| **Materia** | Programación 1 |
| **Cuatrimestre** | 1C 2026 |

## Integrantes

| Nombre | Rol / Participación |

| Mauro Villanueva | Diseño, desarrollo del código, documentación y pruebas |


## Estructura del repositorio

```
tpi-paises/
├── main.py            # Programa principal (menú y lógica completa)
├── data/
│   ├── paises.csv     # Dataset base de países
│   └── fuente_banco_mundial/   # Datos crudos del Banco Mundial (respaldo de la fuente)
│       ├── API_SP_POP_TOTL_DS2_es_csv_v2_1282.csv
│       └── Metadata_Country_API_SP_POP_TOTL_DS2_es_csv_v2_1282.csv
└── README.md          # Este archivo
```

## Requisitos

- Python 3.8 o superior.
- No requiere librerías de terceros: usa solo módulos de la biblioteca estándar
  (`os` y `csv`).

## Instrucciones de ejecución

1. Clonar o descargar el repositorio.
2. Situarse en la carpeta raíz del proyecto.
3. Ejecutar:

```bash
python main.py
```

(En algunos sistemas, `python3 main.py`.)

El programa carga automáticamente el archivo `data/paises.csv` al iniciar y
muestra el menú principal.

## Funcionalidades

- **Listar** todos los países cargados en una tabla formateada.
- **Agregar** un país nuevo (no se admiten campos vacíos ni nombres duplicados).
- **Actualizar** población y/o superficie de un país existente.
- **Buscar** por nombre con coincidencia parcial o exacta.
- **Filtrar** por continente, por rango de población o por rango de superficie.
- **Ordenar** por nombre, población o superficie (ascendente o descendente).
- **Estadísticas**: país con mayor y menor población, promedio de población,
  promedio de superficie y cantidad de países por continente.
- **Guardar** los cambios nuevamente en el CSV.

## Ejemplos de entrada y salida

### Estadísticas (opción 7)

```
 ESTADÍSTICAS
============================================================

Total de países: 215

Mayor población: India (1,463,865,525 hab.)
Menor población: Tuvalu (9,492 hab.)
Promedio de población: 38,094,571.21 hab.
Promedio de superficie: 653,674.48 km2

Cantidad de países por continente:
  América: 46
  Asia: 50
  Europa: 46
  Oceanía: 19
  África: 54
```

### Agregar país (opción 2)

```
Nombre del país: Ciudad del Vaticano
Población (entero positivo): 764
Superficie en km2 (entero positivo): 1
Continente: Europa

Éxito: país 'Ciudad del Vaticano' agregado correctamente.
```

### Manejo de errores

- Si se ingresa texto donde se espera un número, el programa lo rechaza y vuelve
  a solicitar el dato.
- Si el CSV tiene filas con formato inválido, se descartan e informan sin abortar
  la carga.
- Las búsquedas y filtros sin resultados muestran un mensaje claro en lugar de
  fallar.

## Enlaces

- **Repositorio GitHub:** https://github.com/9Mauro/TPI-PRG-I
- **Video demostrativo:** https://www.youtube.com/watch?v=b0pawWV3tdM
- **Documentación PDF:** incluida en la raíz del repositorio (`TPI_Programacion_I.pdf`).

## Fuentes

- Documentación oficial de Python en español: [Estructuras de datos](https://docs.python.org/es/3.14/tutorial/datastructures.html), [módulo csv](https://docs.python.org/es/3.14/library/csv.html), [control de flujo](https://docs.python.org/es/3.14/tutorial/controlflow.html) y [ordenamiento](https://docs.python.org/es/3.14/howto/sorting.html).
- Banco Mundial. (2025). [Población total (SP.POP.TOTL)](https://datos.bancomundial.org/indicador/SP.POP.TOTL), Indicadores del Desarrollo Mundial.
