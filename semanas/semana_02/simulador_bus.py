"""
Simulador de Bus de Datos
Demuestra arbitración, contención y cuellos de botella
"""

import random
import time
from collections import deque
from dataclasses import dataclass
from typing import Literal

@dataclass
class Transaccion:
    """Representa una transacción en el bus"""
    origen: str
    destino: str
    direccion: int
    tipo: Literal['READ', 'WRITE']
    datos: bytes
    tamaño: int
    prioridad: int
    timestamp: float

class Bus:
    """Simula un bus de datos con arbitración"""
    
    def __init__(self, ancho_bits=64, frecuencia_mhz=5000):
        self.ancho_bits = ancho_bits
        self.frecuencia_mhz = frecuencia_mhz
        
        # Ancho de banda teórico
        self.bytes_por_ciclo = ancho_bits // 8
        self.ciclos_por_segundo = frecuencia_mhz * 1_000_000
        self.bandwidth_bps = self.bytes_por_ciclo * self.ciclos_por_segundo
        
        # Estado del bus
        self.ocupado = False
        self.transaccion_actual = None
        self.cola_espera = deque()
        
        # Líneas del bus (simuladas)
        self.address_bus = 0
        self.data_bus = 0
        self.control_signals = {
            'READ': False,
            'WRITE': False,
            'READY': False,
            'MREQ': False
        }
        
        # Estadísticas
        self.stats = {
            'transacciones_completadas': 0,
            'bytes_transferidos': 0,
            'ciclos_totales': 0,
            'ciclos_ocupado': 0,
            'ciclos_idle': 0,
            'conflictos': 0
        }
    
    def calcular_ciclos_necesarios(self, tamaño_bytes):
        """Calcula ciclos necesarios para transferir N bytes"""
        ciclos = tamaño_bytes / self.bytes_por_ciclo
        # Redondea hacia arriba
        return int(ciclos) + (1 if ciclos % 1 > 0 else 0)
    
    def agregar_transaccion(self, trans: Transaccion):
        """Agrega transacción a la cola"""
        if self.ocupado:
            self.stats['conflictos'] += 1
        
        self.cola_espera.append(trans)
        print(f"⏸️  {trans.origen}→{trans.destino}: {trans.tipo} "
              f"0x{trans.direccion:04X} ({trans.tamaño}B) "
              f"[Prioridad: {trans.prioridad}]")
    
    def arbitrar(self):
        """Selecciona próxima transacción (por prioridad)"""
        if not self.cola_espera:
            return None
        
        # Ordena por prioridad (mayor = más importante)
        self.cola_espera = deque(sorted(
            self.cola_espera,
            key=lambda t: t.prioridad,
            reverse=True
        ))
        
        return self.cola_espera.popleft()
    
    def ejecutar_transaccion(self, trans: Transaccion):
        """Simula ejecución de transacción en el bus"""
        print(f"\n{'='*70}")
        print(f"🚌 EJECUTANDO TRANSACCIÓN EN EL BUS")
        print(f"{'='*70}")
        
        self.ocupado = True
        self.transaccion_actual = trans
        
        # Fase 1: Dirección en Address Bus
        print(f"\n1️⃣  Address Bus ← 0x{trans.direccion:08X}")
        self.address_bus = trans.direccion
        self.control_signals['MREQ'] = True
        ciclos = 1
        
        # Fase 2: Señal de control
        if trans.tipo == 'READ':
            print(f"2️⃣  Control Bus ← READ")
            self.control_signals['READ'] = True
            ciclos += 1
        else:
            print(f"2️⃣  Control Bus ← WRITE")
            self.control_signals['WRITE'] = True
            print(f"    Data Bus ← {trans.datos[:16]}...")
            self.data_bus = int.from_bytes(trans.datos[:8], 'little')
            ciclos += 1
        
        # Fase 3: Transferencia de datos
        ciclos_datos = self.calcular_ciclos_necesarios(trans.tamaño)
        print(f"3️⃣  Transferencia de datos: {trans.tamaño} bytes")
        print(f"    Ancho del bus: {self.ancho_bits} bits ({self.bytes_por_ciclo} bytes/ciclo)")
        print(f"    Ciclos necesarios: {ciclos_datos}")
        ciclos += ciclos_datos
        
        # Fase 4: READY signal
        print(f"4️⃣  READY ← TRUE (transferencia completa)")
        self.control_signals['READY'] = True
        ciclos += 1
        
        # Actualizar estadísticas
        self.stats['transacciones_completadas'] += 1
        self.stats['bytes_transferidos'] += trans.tamaño
        self.stats['ciclos_totales'] += ciclos
        self.stats['ciclos_ocupado'] += ciclos
        
        # Calcular tiempo real
        tiempo_ns = (ciclos / self.ciclos_por_segundo) * 1_000_000_000
        bandwidth_real = (trans.tamaño / tiempo_ns) * 1_000_000_000  # B/s
        
        print(f"\n📊 Resumen:")
        print(f"   Ciclos totales: {ciclos}")
        print(f"   Tiempo: {tiempo_ns:.2f} ns")
        print(f"   Ancho banda usado: {bandwidth_real / 1e9:.2f} GB/s")
        print(f"   Eficiencia: {(bandwidth_real/self.bandwidth_bps)*100:.1f}%")
        
        # Liberar bus
        self.ocupado = False
        self.transaccion_actual = None
        self.control_signals = {k: False for k in self.control_signals}
        
        return ciclos
    
    def simular_ciclo(self):
        """Simula un ciclo del bus"""
        if not self.ocupado and self.cola_espera:
            trans = self.arbitrar()
            if trans:
                return self.ejecutar_transaccion(trans)
        else:
            self.stats['ciclos_idle'] += 1
            return 1
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas del bus"""
        print(f"\n{'='*70}")
        print(f"📊 ESTADÍSTICAS DEL BUS")
        print(f"{'='*70}")
        
        print(f"\n🚌 Especificaciones:")
        print(f"   Ancho: {self.ancho_bits} bits")
        print(f"   Frecuencia: {self.frecuencia_mhz} MHz")
        print(f"   Ancho banda teórico: {self.bandwidth_bps / 1e9:.2f} GB/s")
        
        print(f"\n📈 Uso:")
        print(f"   Transacciones completadas: {self.stats['transacciones_completadas']}")
        print(f"   Bytes transferidos: {self.stats['bytes_transferidos']:,} B")
        print(f"   = {self.stats['bytes_transferidos'] / 1024:.2f} KB")
        print(f"   = {self.stats['bytes_transferidos'] / 1024**2:.2f} MB")
        
        print(f"\n⏱️  Ciclos:")
        print(f"   Total: {self.stats['ciclos_totales']:,}")
        print(f"   Ocupado: {self.stats['ciclos_ocupado']:,}")
        print(f"   Idle: {self.stats['ciclos_idle']:,}")
        
        if self.stats['ciclos_totales'] > 0:
            utilizacion = (self.stats['ciclos_ocupado'] / 
                          self.stats['ciclos_totales']) * 100
            print(f"   Utilización: {utilizacion:.1f}%")
        
        if self.stats['conflictos'] > 0:
            print(f"\n⚠️  Conflictos (contención): {self.stats['conflictos']}")
        
        # Ancho de banda efectivo
        if self.stats['ciclos_ocupado'] > 0:
            tiempo_s = self.stats['ciclos_ocupado'] / self.ciclos_por_segundo
            bw_efectivo = self.stats['bytes_transferidos'] / tiempo_s
            eficiencia = (bw_efectivo / self.bandwidth_bps) * 100
            
            print(f"\n📉 Rendimiento:")
            print(f"   Ancho banda efectivo: {bw_efectivo / 1e9:.2f} GB/s")
            print(f"   Eficiencia: {eficiencia:.1f}%")


# ========================================
# EXPERIMENTO 1: Transferencias simples
# ========================================
print("="*70)
print("EXPERIMENTO 1: TRANSFERENCIAS BÁSICAS")
print("="*70)

bus1 = Bus(ancho_bits=64, frecuencia_mhz=5000)  # 64-bit, 5 GHz

# CPU lee de RAM
trans1 = Transaccion(
    origen="CPU",
    destino="RAM",
    direccion=0x1000,
    tipo='READ',
    datos=b'\x00' * 64,
    tamaño=64,  
    # 1 línea de cache
    prioridad=5,
    timestamp=time.time()
    )
bus1.agregar_transaccion(trans1)
bus1.simular_ciclo()
GPU escribe a RAM
trans2 = Transaccion(
    origen="GPU",
    destino="RAM",
    direccion=0x2000,
    tipo='WRITE',
    datos=b'\xFF' * 1024,
    tamaño=1024,  # 1 KB
    prioridad=3,
    timestamp=time.time()
    )
bus1.agregar_transaccion(trans2)
bus1.simular_ciclo()
bus1.mostrar_estadisticas()
========================================
EXPERIMENTO 2: Contención del bus
========================================
print("\n\n" + "="*70)
print("EXPERIMENTO 2: CONTENCIÓN DEL BUS")
print("="*70)
print("Múltiples dispositivos quieren usar el bus simultáneamente")
bus2 = Bus(ancho_bits=64, frecuencia_mhz=5000)
Simula múltiples dispositivos solicitando bus al mismo tiempo
dispositivos = ['CPU', 'GPU', 'NVMe', 'USB', 'Ethernet']
for i, disp in enumerate(dispositivos):
trans = Transaccion(
origen=disp,
destino="RAM",
direccion=0x1000 * (i+1),
tipo=random.choice(['READ', 'WRITE']),
datos=b'\x00' * 512,
tamaño=512,
prioridad=random.randint(1, 10),
timestamp=time.time()
)
bus2.agregar_transaccion(trans)
print(f"\n⚡ Arbitrando {len(bus2.cola_espera)} transacciones...")
print(f"   (Se ejecutarán por prioridad)\n")
while bus2.cola_espera:
bus2.simular_ciclo()
input("\n⏸️  Presiona ENTER para siguiente transacción...")
bus2.mostrar_estadisticas()
========================================
EXPERIMENTO 3: Comparación de anchos
========================================
print("\n\n" + "="*70)
print("EXPERIMENTO 3: COMPARACIÓN DE ANCHOS DE BUS")
print("="*70)
datos_test = b'\x00' * (1024 * 1024)  # 1 MB
configuraciones = [
(32, "Bus 32-bit (antiguo)"),
(64, "Bus 64-bit (actual)"),
(128, "Bus 128-bit (hipotético)"),
]
print(f"\nTransferencia de {len(datos_test) / 1024:.0f} KB:\n")
for ancho, nombre in configuraciones:
bus = Bus(ancho_bits=ancho, frecuencia_mhz=5000)
trans = Transaccion(
    origen="Test",
    destino="RAM",
    direccion=0x0,
    tipo='WRITE',
    datos=datos_test,
    tamaño=len(datos_test),
    prioridad=5,
    timestamp=time.time()
)

print(f"\n{nombre}:")
print(f"   Ancho banda teórico: {bus.bandwidth_bps / 1e9:.2f} GB/s")

ciclos = bus.calcular_ciclos_necesarios(len(datos_test))
tiempo_ns = (ciclos / bus.ciclos_por_segundo) * 1_000_000_000

print(f"   Ciclos necesarios: {ciclos:,}")
print(f"   Tiempo: {tiempo_ns:.0f} ns = {tiempo_ns/1000:.2f} μs")
========================================
LECCIONES PRÁCTICAS
========================================
print("\n\n" + "="*70)
print("💡 LECCIONES PARA PROGRAMACIÓN")
print("="*70)
print("""

MINIMIZA TRANSFERENCIAS CPU ↔ GPU 🔄

Cada transfer tiene overhead de ~5 μs
Agrupa operaciones en batches grandes
Mantén datos en GPU si los vas a reusar


ALINEA TUS DATOS AL ANCHO DEL BUS 📏

Transferir 64 bytes alineados = 1 ciclo
Transferir 63 bytes desalineados = 2 ciclos
En NumPy/PyTorch: usa arrays contiguos


USA DMA (Direct Memory Access) 🚀

Permite transferencias sin CPU
GPU puede leer/escribir RAM directamente
Libera CPU para otros cálculos


ENTIENDE TU TOPOLOGÍA PCIe 🗺️

GPU en slot x16 directo a CPU: Óptimo
GPU en slot x8 via chipset: Más lento
Verifica con: lspci -tv (Linux)



Ejemplo BAD:
for i in range(10000):
gpu_data = cpu_array[i:i+10]  # ❌ 10,000 transfers pequeños
result = gpu_compute(gpu_data)
Ejemplo GOOD:
gpu_data = cpu_array[:]  # ✅ 1 transfer grande
result = gpu_compute(gpu_data)
""")