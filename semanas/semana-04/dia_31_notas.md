# Resumen de Ejercicios -- Python (Sesión de Práctica)

## 1. Conceptos trabajados

Durante esta sesión se reforzaron los siguientes conceptos fundamentales
de Python:

-   List comprehension
-   Slicing avanzado en strings
-   Métodos básicos de listas
-   Listas anidadas (matrices)
-   Procesamiento de texto tipo logs
-   Pensamiento algorítmico mediante pseudocódigo

------------------------------------------------------------------------

## 2. Estructura mental para resolver problemas

Antes de escribir código, sigue siempre este orden:

1.  **Entender el problema**
    -   ¿Qué entra?
    -   ¿Qué sale?
    -   ¿Hay condiciones o transformaciones?
2.  **Pensar en pseudocódigo**
    -   Recorrer colección
    -   Evaluar condición (si existe)
    -   Transformar datos (si aplica)
    -   Guardar resultado
3.  **Elegir la herramienta correcta**
    -   list comprehension → filtrado / transformación
    -   slicing → strings y listas
    -   bucles → lógica más compleja
    -   diccionarios → conteo y agrupación
4.  **Escribir código claro**
    -   Priorizar legibilidad sobre brevedad

------------------------------------------------------------------------

## 3. Notas clave por ejercicio

### List Comprehension

-   Filtrar y transformar en una sola expresión.
-   Sintaxis mental: nueva_lista = \[transformación for elemento in
    colección if condición\]

Errores comunes: - Confundir pares/impares. - Usar nombres de variables
poco claros. - Sobrescribir tipos built-in (`list`, `dict`).

------------------------------------------------------------------------

### Slicing en strings

-   Forma general: secuencia\[inicio:fin:paso\]

Ejemplos importantes: - Invertir: `[::-1]` - Saltos: `[::2]` -
Subcadenas por índice o dinámicas con `find()`.

------------------------------------------------------------------------

### Métodos de listas

-   `sorted()` vs `.sort()`
-   `max()` y `min()` para valores extremos.
-   Promedios se entienden mejor calculándolos manualmente.

Patrón esencial: - acumulador + recorrido + división final.

------------------------------------------------------------------------

### Listas anidadas (matrices)

-   Acceso: `matriz[fila][columna]`
-   Diagonal: índices iguales.
-   Transpuesta: filas ↔ columnas.

Patrones mentales: - Comprensiones anidadas. - Pensar en filas primero,
luego columnas.

------------------------------------------------------------------------

### Problema real (logs)

-   Filtrado con `startswith()`.
-   Conteo manual con contadores o diccionarios.
-   Separar pasos: filtrar → procesar → analizar.

Este patrón se usa en: - Ciberseguridad - Monitoreo - Data engineering

------------------------------------------------------------------------

## 4. Buenas prácticas generales

-   Usar nombres de variables semánticos.
-   No modificar datos originales si no es necesario.
-   Evitar sobrescribir funciones built-in.
-   Preferir soluciones claras y mantenibles.
-   Separar lógica en pasos comprensibles.
-   Primero claridad, luego optimización.

------------------------------------------------------------------------

## 5. Regla de oro

> "Si puedes explicar tu solución en pseudocódigo, puedes escribir el
> código."

Este enfoque forma pensamiento de programador, no solo memorizar
sintaxis.
