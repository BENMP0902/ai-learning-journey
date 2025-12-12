"""
Demostración de cómo TODO en una computadora es binario
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

print("=" * 70)
print("REPRESENTACIÓN BINARIA DE INFORMACIÓN")
print("=" * 70)

# ========================================
# 1. NÚMEROS ENTEROS
# ========================================
print("\n1️⃣  NÚMEROS ENTEROS")
print("-" * 70)

def decimal_a_binario(n, bits=8):
    """
    Convierte número decimal a binario
    
    Args:
        n: Número decimal (int)
        bits: Número de bits a usar (default 8)
    
    Returns:
        str: Representación binaria
    """
    if n < 0:
        # Complemento a 2 para negativos
        n = (1 << bits) + n  # 2^bits + n
    
    binario = bin(n)[2:]  # Quita el '0b'
    return binario.zfill(bits)  # Rellena con ceros a la izquierda


numeros = [0, 5, 13, 42, 127, 255]
print("Decimal → Binario (8 bits)")
print("Decimal |  Binario  | Explicación")
print("--------|-----------|-------------")
for num in numeros:
    binario = decimal_a_binario(num, 8)
    # Calcula valores posicionales
    valores = [int(bit) * (2 ** (7-i)) for i, bit in enumerate(binario)]
    explicacion = " + ".join([f"{v}" for v in valores if v > 0])
    print(f"  {num:3d}   | {binario} | {explicacion}")

# Números negativos (complemento a 2)
print("\nNúmeros negativos (complemento a 2, 8 bits):")
print("Decimal |  Binario  ")
print("--------|-----------|")
for num in [5, -5, -1, -128]:
    if num >= 0:
        binario = decimal_a_binario(num, 8)
    else:
        # Complemento a 2
        positivo = abs(num)
        binario_pos = decimal_a_binario(positivo, 8)
        # Invierte bits
        invertido = ''.join(['1' if b=='0' else '0' for b in binario_pos])
        # Suma 1
        valor_invertido = int(invertido, 2)
        binario = decimal_a_binario(valor_invertido + 1, 8)
    
    print(f" {num:4d}   | {binario}")


# ========================================
# 2. TEXTO (CARACTERES)
# ========================================
print("\n" + "=" * 70)
print("2️⃣  TEXTO (ASCII)")
print("-" * 70)

texto = "Hola IA"
print(f"Texto: '{texto}'")
print("\nCar | ASCII | Binario   | Hex")
print("----|-------|-----------|-----")
for char in texto:
    ascii_val = ord(char)  # Obtiene código ASCII
    binario = decimal_a_binario(ascii_val, 8)
    hexadecimal = hex(ascii_val)[2:].upper()
    print(f" {char}  |  {ascii_val:3d}  | {binario} | 0x{hexadecimal}")

# Codifica texto completo
print(f"\nTexto completo en binario:")
binario_completo = ' '.join([decimal_a_binario(ord(c), 8) for c in texto])
print(binario_completo)

# Tamaño en bits
print(f"\nTamaño: {len(texto)} caracteres × 8 bits = {len(texto) * 8} bits = {len(texto)} bytes")


# ========================================
# 3. NÚMEROS DECIMALES (PUNTO FLOTANTE)
# ========================================
print("\n" + "=" * 70)
print("3️⃣  NÚMEROS DECIMALES (Float 32 bits - IEEE 754)")
print("-" * 70)

import struct

def float_a_binario(f):
    """
    Convierte float a su representación binaria IEEE 754
    
    Float 32 bits:
    [1 bit signo][8 bits exponente][23 bits mantisa]
    """
    # Convierte float a bytes, luego a int
    bytes_repr = struct.pack('>f', f)
    int_repr = struct.unpack('>I', bytes_repr)[0]
    
    # Obtiene binario de 32 bits
    binario = bin(int_repr)[2:].zfill(32)
    
    # Separa componentes
    signo = binario[0]
    exponente = binario[1:9]
    mantisa = binario[9:]
    
    return signo, exponente, mantisa, binario


numeros_float = [0.0, 1.0, -1.0, 3.14159, 0.1]
print("Número | Binario completo (32 bits)")
print("-------|----------------------------------------------------------")
for f in numeros_float:
    signo, exp, mantisa, completo = float_a_binario(f)
    print(f"{f:7.5f} | {completo}")
    print(f"       | S:{signo} Exp:{exp} Mantisa:{mantisa}")

print("\n💡 Problema del 0.1 en binario:")
print(f"   0.1 en decimal = 0.00011001100110011... (infinito) en binario")
print(f"   Por eso: 0.1 + 0.2 = {0.1 + 0.2} (no exactamente 0.3)")


# ========================================
# 4. IMÁGENES
# ========================================
print("\n" + "=" * 70)
print("4️⃣  IMÁGENES (Pixeles RGB)")
print("-" * 70)

# Crea imagen pequeña 3×3 píxeles
imagen = np.array([
    [[255, 0, 0],   [0, 255, 0],   [0, 0, 255]],    # Fila 1: Rojo, Verde, Azul
    [[255, 255, 0], [255, 0, 255], [0, 255, 255]],  # Fila 2: Amarillo, Magenta, Cyan
    [[0, 0, 0],     [128, 128, 128], [255, 255, 255]]  # Fila 3: Negro, Gris, Blanco
], dtype=np.uint8)

print("Imagen 3×3 píxeles:")
print("\nPosición | RGB         | Binario")
print("---------|-------------|------------------------------------------")
for i in range(3):
    for j in range(3):
        r, g, b = imagen[i, j]
        bin_r = decimal_a_binario(r, 8)
        bin_g = decimal_a_binario(g, 8)
        bin_b = decimal_a_binario(b, 8)
        print(f"({i},{j})    | ({r:3d},{g:3d},{b:3d}) | R:{bin_r} G:{bin_g} B:{bin_b}")

print(f"\nTamaño total: 3×3 píxeles × 3 colores × 8 bits = {3*3*3*8} bits = {3*3*3} bytes")


# ========================================
# 5. AUDIO (simplificado)
# ========================================
print("\n" + "=" * 70)
print("5️⃣  AUDIO (Muestras digitales)")
print("-" * 70)

# Simula onda senoidal (440 Hz = nota La)
frecuencia_muestreo = 44100  # Hz (CD quality)
duracion = 0.01  # 10 milisegundos
frecuencia_nota = 440  # Hz (nota La)

t = np.linspace(0, duracion, int(frecuencia_muestreo * duracion), endpoint=False)
onda = np.sin(2 * np.pi * frecuencia_nota * t)

# Convierte a 16 bits (rango -32768 a 32767)
onda_16bit = (onda * 32767).astype(np.int16)

print(f"Onda senoidal 440 Hz (nota La)")
print(f"Frecuencia de muestreo: {frecuencia_muestreo} Hz")
print(f"Duración: {duracion} segundos")
print(f"Número de muestras: {len(onda_16bit)}")
print(f"\nPrimeras 5 muestras:")
print("Muestra | Valor decimal | Binario (16 bits)")
print("--------|---------------|-------------------")
for i in range(5):
    valor = onda_16bit[i]
    # Para negativos, usa complemento a 2
    if valor >= 0:
        binario = decimal_a_binario(valor, 16)
    else:
        binario = bin(valor & 0xFFFF)[2:].zfill(16)
    print(f"  {i}     | {valor:6d}        | {binario}")

print(f"\nTamaño: {len(onda_16bit)} muestras × 2 bytes = {len(onda_16bit) * 2} bytes")


# ========================================
# 6. OPERACIONES BINARIAS (Álgebra de Boole)
# ========================================
print("\n" + "=" * 70)
print("6️⃣  OPERACIONES BINARIAS (Álgebra de Boole)")
print("-" * 70)

a = 0b1100  # 12 en decimal
b = 0b1010  # 10 en decimal

print(f"a = {a:4d} = {bin(a)[2:].zfill(4)}")
print(f"b = {b:4d} = {bin(b)[2:].zfill(4)}")
print()

operaciones = [
    ("AND", a & b, "Solo 1 si ambos son 1"),
    ("OR",  a | b, "1 si al menos uno es 1"),
    ("XOR", a ^ b, "1 si son diferentes"),
    ("NOT a", ~a & 0b1111, "Invierte todos los bits"),
    ("Shift left (a << 1)", a << 1, "Multiplica por 2"),
    ("Shift right (a >> 1)", a >> 1, "Divide por 2"),
]

for nombre, resultado, descripcion in operaciones:
    binario = bin(resultado)[2:].zfill(4) if resultado >= 0 else bin(resultado & 0xFFFF)[2:][-4:]
    print(f"{nombre:20s} = {resultado:4d} = {binario}  ({descripcion})")


# ========================================
# RESUMEN FINAL
# ========================================
print("\n" + "=" * 70)
print("📊 RESUMEN: TODO ES BINARIO")
print("=" * 70)
print("""
Tipo de dato          | Representación
----------------------|------------------------------------------
Números enteros       | Binario directo o complemento a 2
Números decimales     | IEEE 754 (signo + exponente + mantisa)
Texto                 | ASCII/Unicode (cada carácter = número)
Imágenes              | Matriz de píxeles RGB (cada valor 0-255)
Audio                 | Secuencia de muestras de amplitud
Video                 | Secuencia de imágenes + audio
Instrucciones CPU     | Opcodes en binario (ej: ADD = 10000011)

💡 En tu computadora, ABSOLUTAMENTE TODO son 0s y 1s
   La "magia" es cómo se interpretan esos bits.
""")
```

---

## 3️⃣ ¿Qué hace el CPU?

### **Información Técnica**

El **CPU (Central Processing Unit)** o "procesador" es el **cerebro de la computadora**. Ejecuta las instrucciones de los programas realizando operaciones aritméticas, lógicas y de control.

### **Componentes principales del CPU:**

#### **A) ALU (Arithmetic Logic Unit)**
- Realiza operaciones aritméticas: suma, resta, multiplicación, división
- Operaciones lógicas: AND, OR, NOT, XOR
- Comparaciones: mayor que, menor que, igual

#### **B) CU (Control Unit)**
- **Dirige el tráfico:** Controla flujo de datos entre CPU, memoria y dispositivos
- **Decodifica instrucciones:** Interpreta qué hacer
- **Genera señales de control:** Activa componentes en el momento correcto

#### **C) Registros**
- **Memoria ultra-rápida dentro del CPU**
- Almacenan datos temporales durante ejecución
- Tipos:
  - **Program Counter (PC):** Dirección de siguiente instrucción
  - **Instruction Register (IR):** Instrucción actual
  - **Accumulator:** Resultados temporales
  - **Registros de propósito general:** r0, r1, ..., r15

#### **D) Cache**
- Memoria intermedia entre CPU y RAM
- **L1 Cache:** La más rápida (32-64 KB), dentro de cada núcleo
- **L2 Cache:** Intermedia (256-512 KB por núcleo)
- **L3 Cache:** Compartida (8-32 MB), entre todos los núcleos

### **Ciclo de instrucción (Fetch-Decode-Execute):**
```
1. FETCH (Buscar):
   - PC indica dirección de memoria
   - CPU lee instrucción de RAM/cache
   - Carga instrucción en IR
   - Incrementa PC

2. DECODE (Decodificar):
   - CU analiza instrucción en IR
   - Identifica operación (ADD, LOAD, JUMP, etc.)
   - Determina operandos necesarios

3. EXECUTE (Ejecutar):
   - ALU realiza la operación
   - Resultado se guarda en registro o memoria
   - Actualiza flags (carry, zero, overflow, etc.)

4. REPITE (miles de millones de veces por segundo)