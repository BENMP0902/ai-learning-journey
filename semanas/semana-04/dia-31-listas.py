# Ejercicio 1: List comprehension
numeros = range(1,101)

# Creamos uns lista con los numeros del 1 al 100 que sean divisibles por 3 y 5
div_3_y_5 = [n for n in numeros if n % 3 == 0 and n % 5 == 0]

#Alternativ[{a
divi_3_5 = []

for n in numeros:
    if n % 3 == 0 and n % 5 == 0:
        divi_3_5.append(n)


# Mostrar resultadoa
print(div_3_y_5)
print(divi_3_5)

#Ejercicio 1: números pares
#Dado un rango del 1 al 50, crea una lista que contenga únicamente los números pares.
numbers_1 = range(1,51)
pares = [n for n in numbers_1 if n % 2 == 0]
print(pares)

#Ejercicio 2: números mayores a un umbral
#Dada la lista [3, 7, 12, 25, 30, 41, 56], crea una nueva lista con los números mayores a 20.
list = [3, 7, 12, 25, 30, 41, 56]
umbral = [n for n in list if n > 20]
print(umbral)

# Ejercicio 3: transformación de valores
# Dado un rango del 1 al 10, crea una lista con el cuadrado de cada número.
cuadrados = [n**2 for n in range(1,11)]
print(cuadrados)

# Ejercicio 4: filtrado y transformación combinados
# Dado un rango del 1 al 20, crea una lista con el cuadrado únicamente de los números impares.
cuadrado_impares = [n**2 for n in range(1,21) if n % 2 != 0]
print(cuadrado_impares)

# Ejercicio 5: trabajo con cadenas
# Dada la lista ["python", "java", "c++", "go", "rust"], crea una lista con las palabras que tengan más de 3 caracteres y conviértelas a mayúsculas.
palabras = ["python", "java", "c++", "go", "rust"]
palabras_mayus = [p.upper() for p in palabras if len(p) > 3] 


# Ejercicio 6: condiciones múltiples
# Dado un rango del 1 al 100, crea una lista con los números que sean divisibles por 4 pero no por 8.
div_4_not_8 = [n for n in range(1,101) if n % 4 == 0 and n % 8 != 0]
print(div_4_not_8)

# Ejercicio 7: estructura mental (pseudocódigo)
# Antes de escribir cualquier código, redacta el pseudocódigo para uno de los ejercicios anteriores. Por ejemplo:
# – Recorrer la colección
# – Evaluar la condición
# – Aplicar la transformación
# – Guardar el resultado

# 1. Identificar la coleccion de entrada
# 2. Recorrer cada elemento de la coleccion
# 3. Evaluar una condicion(opcional)
# 4. Tramsformar el elemto (opcional)
# 5. Guardar el resultado en una nueva coleccion
#  ¡De una collecion original, gernero una nueva coleccion aplicando reglas claras!
#---------------------------------------------------------------------------------------------------

# Ejercicio 2: Slicing avanzado
texto = "Python para Inteligencia Artificial"
# Extrae: "para", texto invertido, cada 2da letra

# Pseudocodigo:
# 1. Definir la cadena de texto original.
# 2. Para extraer "para": Identificar el índice inicial y final de la palabra dentro del texto.
#                         Aplicar slicing con esos índices.
# 3. Para invertir texto: Aplicar slicing con un paso negativo.
# 4. Para obtener cada segunda letra: Aplicar slicing con un paso de 2.
# 5. Mostrar o almacenar cada resultado

# Extraer la palabra "para"
palabra_para = texto[7:11]

# Invertir todo el texto 
texto_invertido = texto[::-1]

# Obtener cada segunda letra
cada_segunda_letra = texto[::2]

print(palabra_para)
print(texto_invertido)
print(cada_segunda_letra)
# -------------------------------------------------------------------------------------------------------

# Ejercicio 3: Métodos de listas
ventas = [120, 450, 230, 890, 340]
# Ordena, encuentra max/min, calcula promedio sin sum()

# Pseudocodigo
# 1. Definir lista de ventas
# 2. Crear una version ordenada de la lista (sin modificar la original)
# 3. Obtener el valor maximo de la lista.
# 4. Obtener el valor minimo de la lista.
# 5. Calcular el promedio:  - Inicializar un acumulador en cero.
#                           - Recorrer cada valor de la lista
#                           - Sumar cada valor al acumulador
#                           - Dividir el total entre la cantidad de elementos
# 6. Mostrar los resultados
#-------------------------------------------------

# Ordenar la lista(sin modificar la original)
ventas_ordenadas = sorted(ventas)

# Obtener valor maximo y minimo
venta_maxima = max(ventas)
venta_minima = min(ventas)

# Calcular el promedio sin usar sum()
total = 0
for venta in ventas:
    total += venta

promedio = total / len(ventas)

print("Ventas ordenadas: ", ventas_ordenadas)
print("Venta maxima: ", venta_maxima)
print("Venta minima: ", venta_minima)
print("Promedio: ", promedio)
#-------------------------------------------------------

# Ejercicio 4: Nested lists
matriz = [
    [1,2,3], 
    [4,5,6], 
    [7,8,9]
]
# Extrae diagonal, transpón la matriz
""" 
Psuedocodigo:
    Parte A: Extraer la diagonal principal
        1. Identificar la matriz(lista de listas)
        2. Recorrer los indices de la matriz (de  0 hasta tamaño -1)
        3. En cada iteracion: Tomar el elemento cuya fila y columna tengan el mismo indice.
        4. Guardar esos elementos en una nueva lista.
    Parte B: 
        1. Determinar el numero de filas y columnas.
        2. Recorrer los índices de las columnas.
        3. Para cada columna: 
            - Recorrer todas las filas.
            - Tomar el elemento correspondiente a esa columna.
        4. Agrupar los elementos para formar las nuevas filas de la matriz transpuesta.
 """
# Extraer la diagonal principal 
diagonal = [matriz[i][i] for i in range(len(matriz))]

# Transponer la matriz
transpuesta = [[fila[i] for fila in matriz] for i in range(len(matriz[0]))]

print("Diagonal: ", diagonal)
print("Transpuesta: ", transpuesta)
# -------------------------------------------------------

# Ejercicio 5: Problema real
logs = ["ERROR: fallo", "INFO: ok", "ERROR: crash", "INFO: ok"]
# Filtra solo ERRORs, cuenta frecuencias
""" Pseudocodigo:
    Parte A: filtrar solo errores
        1. Definir la lista de logs.
        2. Recorrer cada entrada del log.
        3. Verificar si la entrada comienza con "ERROR".
        4. Si cumple la condicion, agregarla a una nueva lista.

    Parte B: contar frecuencias
        1. Inicializar un contador en cero o una estructura de conteo.
        2. Recorrer la lista de errores filtrados.
        3, Incrementar el contador por cada error encontrado.
        4. Guardar y/o mostrar la frecuencia total. """

# Filtar solo los logs de error
errores = [log for log in logs if log.startswith("ERROR")]

# Contar la frecuencia de errores sin usar collections.Counter
frecuencia_errores = 0 
for error in errores:
    frecuencia_errores += 1

# Alternativa
frecuencia_error = sum(1 for log in logs if log.startswith("ERROR"))

print("Errores encontrados: ", errores)
print("Total de errores: ", frecuencia_errores)
print(frecuencia_error)