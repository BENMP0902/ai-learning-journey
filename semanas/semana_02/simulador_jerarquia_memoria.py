"""
Simulador de Jerarquía de Memoria
Demuestra cache hits/misses y su impacto en rendimiento
"""

import random
import time
from collections import OrderedDict

class MemoryHierarchy:
    """Simula la jerarquía completa de memoria"""
    
    def __init__(self):
        # Latencias en nanosegundos
        self.LATENCIAS = {
            'L1': 1,
            'L2': 3,
            'L3': 15,
            'RAM': 100,
            'SSD': 10000,  # 10 μs
            'HDD': 5000000  # 5 ms
        }
        
        # Tamaños en bytes
        self.TAMAÑOS = {
            'L1': 64 * 1024,        # 64 KB
            'L2': 512 * 1024,       # 512 KB
            'L3': 16 * 1024 * 1024, # 16 MB
            'RAM': 32 * 1024 * 1024 * 1024,  # 32 GB
        }
        
        # Caches (usando LRU)
        self.L1 = OrderedDict()
        self.L2 = OrderedDict()
        self.L3 = OrderedDict()
        self.RAM = {}
        
        # Estadísticas
        self.stats = {
            'L1_hits': 0,
            'L1_misses': 0,
            'L2_hits': 0,
            'L2_misses': 0,
            'L3_hits': 0,
            'L3_misses': 0,
            'RAM_accesses': 0,
            'total_latency': 0
        }
        
        # Línea de cache (64 bytes)
        self.CACHE_LINE_SIZE = 64
    
    def _cache_line_address(self, address):
        """Calcula dirección de línea de cache"""
        return (address // self.CACHE_LINE_SIZE) * self.CACHE_LINE_SIZE
    
    def _evict_if_full(self, cache, max_size):
        """Política LRU: saca el más antiguo si está lleno"""
        current_size = len(cache) * self.CACHE_LINE_SIZE
        if current_size >= max_size:
            cache.popitem(last=False)  # Saca el primero (más antiguo)
    
    def leer_memoria(self, address):
        """
        Lee dato de memoria, simulando jerarquía completa
        
        Returns:
            tuple: (dato, latencia_total_ns, nivel_encontrado)
        """
        line_addr = self._cache_line_address(address)
        latencia_acumulada = 0
        
        # Intenta L1
        if line_addr in self.L1:
            self.stats['L1_hits'] += 1
            latencia_acumulada += self.LATENCIAS['L1']
            # Mueve al final (más recientemente usado)
            self.L1.move_to_end(line_addr)
            return self.L1[line_addr], latencia_acumulada, 'L1'
        
        self.stats['L1_misses'] += 1
        latencia_acumulada += self.LATENCIAS['L1']

            # Intenta L2
        if line_addr in self.L2:
            self.stats['L2_hits'] += 1
            latencia_acumulada += self.LATENCIAS['L2']
            # Copia a L1
            self._evict_if_full(self.L1, self.TAMAÑOS['L1'])
            self.L1[line_addr] = self.L2[line_addr]
            self.L2.move_to_end(line_addr)
            return self.L2[line_addr], latencia_acumulada, 'L2'
        
        self.stats['L2_misses'] += 1
        latencia_acumulada += self.LATENCIAS['L2']
        
        # Intenta L3
        if line_addr in self.L3:
            self.stats['L3_hits'] += 1
            latencia_acumulada += self.LATENCIAS['L3']
            # Copia a L2 y L1
            self._evict_if_full(self.L2, self.TAMAÑOS['L2'])
            self.L2[line_addr] = self.L3[line_addr]
            self._evict_if_full(self.L1, self.TAMAÑOS['L1'])
            self.L1[line_addr] = self.L3[line_addr]
            self.L3.move_to_end(line_addr)
            return self.L3[line_addr], latencia_acumulada, 'L3'
        
        self.stats['L3_misses'] += 1
        latencia_acumulada += self.LATENCIAS['L3']
        
        # Intenta RAM
        if line_addr in self.RAM:
            self.stats['RAM_accesses'] += 1
            latencia_acumulada += self.LATENCIAS['RAM']
            dato = self.RAM[line_addr]
        else:
            # Simula carga desde disco (primera vez)
            latencia_acumulada += self.LATENCIAS['SSD']
            dato = f"Dato_{line_addr}"
            self.RAM[line_addr] = dato
        
        # Propaga hacia arriba (inclusive policy)
        self._evict_if_full(self.L3, self.TAMAÑOS['L3'])
        self.L3[line_addr] = dato
        self._evict_if_full(self.L2, self.TAMAÑOS['L2'])
        self.L2[line_addr] = dato
        self._evict_if_full(self.L1, self.TAMAÑOS['L1'])
        self.L1[line_addr] = dato
        
        self.stats['total_latency'] += latencia_acumulada
        return dato, latencia_acumulada, 'RAM'

    def mostrar_estadisticas(self):
        """Muestra estadísticas de accesos"""
        total_accesos = self.stats['L1_hits'] + self.stats['L1_misses']
        
        print("\n" + "="*70)
        print("📊 ESTADÍSTICAS DE JERARQUÍA DE MEMORIA")
        print("="*70)
        
        print(f"\n🎯 Cache L1:")
        print(f"   Hits:   {self.stats['L1_hits']:,}")
        print(f"   Misses: {self.stats['L1_misses']:,}")
        if total_accesos > 0:
            hit_rate_l1 = (self.stats['L1_hits'] / total_accesos) * 100
            print(f"   Hit Rate: {hit_rate_l1:.2f}%")
        
        print(f"\n🎯 Cache L2:")
        print(f"   Hits:   {self.stats['L2_hits']:,}")
        print(f"   Misses: {self.stats['L2_misses']:,}")
        
        print(f"\n🎯 Cache L3:")
        print(f"   Hits:   {self.stats['L3_hits']:,}")
        print(f"   Misses: {self.stats['L3_misses']:,}")
        
        print(f"\n💾 RAM:")
        print(f"   Accesos: {self.stats['RAM_accesses']:,}")
        
        print(f"\n⏱️  Latencia Total: {self.stats['total_latency']:,} ns")
        print(f"   = {self.stats['total_latency'] / 1_000:.2f} μs")
        print(f"   = {self.stats['total_latency'] / 1_000_000:.2f} ms")
        
        if total_accesos > 0:
            latencia_promedio = self.stats['total_latency'] / total_accesos
            print(f"\n⏱️  Latencia Promedio por Acceso: {latencia_promedio:.2f} ns")

if __name__== "__main__":
    mem = MemoryHierarchy()

    direcciones = [
        0x1000, 0x1004, 0x1008,  # misma línea → hits
        0x2000,
        0x3000,
        0x1000,                # debería ser hit
        0x4000,
        0x1004                 # otro hit
    ]

    for addr in direcciones:
        dato, latencia, nivel = mem.leer_memoria(addr)
        print(f"Dirección {hex(addr)} → {nivel} | {latencia} ns")

    mem.mostrar_estadisticas()



'''
========================================
EXPERIMENTO 1: Acceso Secuencial
========================================
print("="*70)
print("EXPERIMENTO 1: ACCESO SECUENCIAL (Localidad Espacial)")
print("="*70)
print("Leyendo 1000 direcciones consecutivas (simula recorrer array)")
mem1 = MemoryHierarchy()
inicio_addr = 0x1000
for i in range(1000):
address = inicio_addr + i * 4  # int de 4 bytes
dato, latencia, nivel = mem1.leer_memoria(address)
if i < 5 or i % 100 == 0:
    print(f"Dirección 0x{address:04X}: {dato[:20]}... ({latencia} ns, {nivel})")
mem1.mostrar_estadisticas()
========================================
EXPERIMENTO 2: Acceso Aleatorio
========================================
print("\n\n" + "="*70)
print("EXPERIMENTO 2: ACCESO ALEATORIO (Sin Localidad)")
print("="*70)
print("Leyendo 1000 direcciones aleatorias")
mem2 = MemoryHierarchy()
for i in range(1000):
address = random.randint(0, 10000000) * 64  # Alineado a línea de cache
dato, latencia, nivel = mem2.leer_memoria(address)
if i < 5:
    print(f"Dirección 0x{address:08X}: {dato[:20]}... ({latencia} ns, {nivel})")
mem2.mostrar_estadisticas()
========================================
EXPERIMENTO 3: Working Set que cabe en L1
========================================
print("\n\n" + "="*70)
print("EXPERIMENTO 3: WORKING SET PEQUEÑO (Cabe en L1)")
print("="*70)
print("Accediendo repetidamente a 100 direcciones (6.4 KB)")
mem3 = MemoryHierarchy()
direcciones = [i * 64 for i in range(100)]  # 100 líneas de cache = 6.4 KB
for iteracion in range(10):
for addr in direcciones:
dato, latencia, nivel = mem3.leer_memoria(addr)
mem3.mostrar_estadisticas()
========================================
COMPARACIÓN VISUAL
========================================
print("\n\n" + "="*70)
print("📈 COMPARACIÓN DE ESCENARIOS")
print("="*70)
escenarios = {
"Secuencial": mem1.stats,
"Aleatorio": mem2.stats,
"Working Set": mem3.stats
}
print(f"\n{'Escenario':<15} {'L1 Hit%':<12} {'Latencia Prom':<15}")
print("-" * 70)
for nombre, stats in escenarios.items():
total = stats['L1_hits'] + stats['L1_misses']
if total > 0:
hit_rate = (stats['L1_hits'] / total) * 100
lat_prom = stats['total_latency'] / total
print(f"{nombre:<15} {hit_rate:>6.2f}%      {lat_prom:>8.2f} ns")
========================================
LECCIÓN PRÁCTICA
========================================
print("\n\n" + "="*70)
print("💡 LECCIONES PARA PROGRAMACIÓN")
print("="*70)
print("""

ACCESO SECUENCIAL ES REY 👑

Secuencial: ~98% L1 hit rate
Aleatorio: ~10% L1 hit rate
Diferencia: 10× en latencia


MANTÉN TU WORKING SET PEQUEÑO 📦

Si cabe en L1 (64 KB): Rendimiento óptimo
Si cabe en L3 (16 MB): Aceptable
Si necesita RAM: Lento


CACHE LINE AWARENESS 📏

Datos contiguos se cargan juntos (64 bytes)
Estructura tus datos para aprovechar esto


PARA MACHINE LEARNING 🤖

Arrays grandes (matrices): Prefiere operaciones por bloques
Mini-batches que caben en cache
Evita saltos aleatorios en memoria



    Ejemplo MALO (Python/NumPy):
    for i in range(1000000):
    for j in range(1000):
    result[j] += matrix[i][j]  # ❌ Salta por toda la matriz
    Ejemplo BUENO:
    for i in range(1000000):
    result += matrix[i]  # ✅ Acceso secuencial, vectorizado
    """)

'''