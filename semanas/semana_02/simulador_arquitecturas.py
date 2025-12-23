"""
Simulador que compara Von Neumann vs Harvard
Demuestra el cuello de botella y las ventajas de cada arquitectura
"""

from dataclasses import dataclass
from typing import List, Literal
import random

@dataclass
class Instruccion:
    """Representa una instrucción de máquina"""
    opcode: str
    operandos: List[int]
    accede_memoria: bool  # ¿Necesita leer/escribir datos?
    
    def __repr__(self):
        ops = ', '.join(map(str, self.operandos))
        mem = " [MEM]" if self.accede_memoria else ""
        return f"{self.opcode} {ops}{mem}"


class ArquitecturaVonNeumann:
    """Simula arquitectura Von Neumann clásica"""
    
    def __init__(self):
        self.memoria = [0] * 65536  # 64 KB unificada
        self.pc = 0  # Program Counter
        self.registros = [0] * 8
        
        # Estadísticas
        self.ciclos = 0
        self.ciclos_fetch = 0
        self.ciclos_mem_data = 0
        self.instrucciones_ejecutadas = 0
        self.conflictos_bus = 0
    
    def ejecutar_programa(self, programa: List[Instruccion]):
        """Ejecuta un programa instrucción por instrucción"""
        print("="*70)
        print("🏛️  ARQUITECTURA VON NEUMANN")
        print("="*70)
        
        for i, instruccion in enumerate(programa):
            if i < 5 or i % 100 == 0:
                print(f"\nInstrucción {i}: {instruccion}")
            
            # FASE 1: FETCH (usar bus)
            if i < 5:
                print(f"  Ciclo {self.ciclos}: FETCH instrucción (bus ocupado)")
            self.ciclos += 1
            self.ciclos_fetch += 1
            
            # FASE 2: DECODE (no usa bus)
            self.ciclos += 1
            
            # FASE 3: EXECUTE
            if instruccion.accede_memoria:
                # Necesita acceder memoria de datos (conflicto!)
                if i < 5:
                    print(f"  Ciclo {self.ciclos}: Acceso a memoria de DATOS (bus ocupado otra vez)")
                self.ciclos += 1
                self.ciclos_mem_data += 1
                self.conflictos_bus += 1
            else:
                self.ciclos += 1
            
            self.instrucciones_ejecutadas += 1
        
        self.mostrar_estadisticas()
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas de ejecución"""
        print(f"\n{'─'*70}")
        print("📊 ESTADÍSTICAS VON NEUMANN")
        print(f"{'─'*70}")
        print(f"Instrucciones ejecutadas: {self.instrucciones_ejecutadas}")
        print(f"Ciclos totales: {self.ciclos}")
        print(f"  ├─ Ciclos FETCH instrucción: {self.ciclos_fetch}")
        print(f"  ├─ Ciclos acceso datos: {self.ciclos_mem_data}")
        print(f"  └─ Otros (decode, execute): {self.ciclos - self.ciclos_fetch - self.ciclos_mem_data}")
        print(f"\n⚠️  Conflictos de bus: {self.conflictos_bus}")
        print(f"CPI (Cycles Per Instruction): {self.ciclos / self.instrucciones_ejecutadas:.2f}")


class ArquitecturaHarvard:
    """Simula arquitectura Harvard pura"""
    
    def __init__(self):
        self.memoria_programa = [0] * 32768  # 32 KB para código
        self.memoria_datos = [0] * 8192      # 8 KB para datos
        self.pc = 0
        self.registros = [0] * 8
        
        # Estadísticas
        self.ciclos = 0
        self.instrucciones_ejecutadas = 0
        self.accesos_paralelos = 0
    
    def ejecutar_programa(self, programa: List[Instruccion]):
        """Ejecuta programa aprovechando buses paralelos"""
        print("\n\n" + "="*70)
        print("🎓 ARQUITECTURA HARVARD")
        print("="*70)
        
        for i, instruccion in enumerate(programa):
            if i < 5 or i % 100 == 0:
                print(f"\nInstrucción {i}: {instruccion}")
            
            # FASE 1: FETCH + Posible acceso datos (PARALELO)
            if instruccion.accede_memoria:
                if i < 5:
                    print(f"  Ciclo {self.ciclos}: FETCH instrucción (bus programa)")
                    print(f"                      + Acceso datos (bus datos)")
                    print(f"                      → PARALELO ✨")
                self.accesos_paralelos += 1
            else:
                if i < 5:
                    print(f"  Ciclo {self.ciclos}: FETCH instrucción (bus programa)")
            self.ciclos += 1
            
            # FASE 2: DECODE
            self.ciclos += 1
            
            # FASE 3: EXECUTE (si no accedió memoria antes, ejecuta directo)
            if not instruccion.accede_memoria:
                self.ciclos += 1
            # Si ya accedió memoria en paralelo, no añade ciclo extra
            
            self.instrucciones_ejecutadas += 1
        
        self.mostrar_estadisticas()
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas"""
        print(f"\n{'─'*70}")
        print("📊 ESTADÍSTICAS HARVARD")
        print(f"{'─'*70}")
        print(f"Instrucciones ejecutadas: {self.instrucciones_ejecutadas}")
        print(f"Ciclos totales: {self.ciclos}")
        print(f"\n✨ Accesos paralelos (I+D): {self.accesos_paralelos}")
        print(f"CPI (Cycles Per Instruction): {self.ciclos / self.instrucciones_ejecutadas:.2f}")


class ArquitecturaHarvardModificada:
    """Simula arquitectura Harvard Modificada (CPUs modernos)"""
    
    def __init__(self):
        # Memoria unificada (Von Neumann)
        self.memoria = [0] * 65536
        
        # Caches separados (Harvard)
        self.i_cache = {}  # Cache de instrucciones
        self.d_cache = {}  # Cache de datos
        self.i_cache_size = 32 * 1024  # 32 KB
        self.d_cache_size = 32 * 1024  # 32 KB
        
        self.pc = 0
        self.registros = [0] * 8
        
        # Estadísticas
        self.ciclos = 0
        self.instrucciones_ejecutadas = 0
        self.i_cache_hits = 0
        self.i_cache_misses = 0
        self.d_cache_hits = 0
        self.d_cache_misses = 0
        self.accesos_paralelos = 0
    
    def acceder_i_cache(self, direccion):
        """Accede cache de instrucciones"""
        if direccion in self.i_cache:
            self.i_cache_hits += 1
            return True, 1  # Hit, 1 ciclo
        else:
            self.i_cache_misses += 1
            # Miss: debe ir a memoria (penalidad)
            self.i_cache[direccion] = self.memoria[direccion]
            return False, 10  # Miss, 10 ciclos (aprox L2 o RAM)
    
    def acceder_d_cache(self, direccion):
        """Accede cache de datos"""
        if direccion in self.d_cache:
            self.d_cache_hits += 1
            return True, 1
        else:
            self.d_cache_misses += 1
            self.d_cache[direccion] = self.memoria[direccion]
            return False, 10
    
    def ejecutar_programa(self, programa: List[Instruccion]):
        """Ejecuta programa con caches Harvard"""
        print("\n\n" + "="*70)
        print("🔄 ARQUITECTURA HARVARD MODIFICADA (CPU Moderno)")
        print("="*70)
        
        for i, instruccion in enumerate(programa):
            if i < 5 or i % 100 == 0:
                print(f"\nInstrucción {i}: {instruccion}")
            
            # FASE 1: FETCH de I-Cache
            i_hit, i_ciclos = self.acceder_i_cache(self.pc)
            
            if instruccion.accede_memoria:
                # FASE 1b: Acceso D-Cache (puede ser paralelo si ambos hit)
                d_hit, d_ciclos = self.acceder_d_cache(0x3000)  # Dirección ejemplo
                
                if i_hit and d_hit:
                    # Ambos en cache: PARALELO
                    if i < 5:
                        print(f"  Ciclo {self.ciclos}: I-Cache HIT + D-Cache HIT")
                        print(f"                      → PARALELO ✨")
                    self.ciclos += 1
                    self.accesos_paralelos += 1
                else:
                    # Al menos uno miss: penalidad
                    if i < 5:
                        status_i = "HIT" if i_hit else "MISS"
                        status_d = "HIT" if d_hit else "MISS"
                        print(f"  Ciclo {self.ciclos}: I-Cache {status_i} ({i_ciclos} ciclos)")
                        print(f"                      D-Cache {status_d} ({d_ciclos} ciclos)")
                    self.ciclos += max(i_ciclos, d_ciclos)
            else:
                # Solo FETCH
                if i < 5:
                    status = "HIT" if i_hit else "MISS"
                    print(f"  Ciclo {self.ciclos}: I-Cache {status} ({i_ciclos} ciclos)")
                self.ciclos += i_ciclos
            
            # FASE 2: DECODE
            self.ciclos += 1
            
            # FASE 3: EXECUTE
            self.ciclos += 1
            
            self.instrucciones_ejecutadas += 1
            self.pc += 4  # Instrucción de 4 bytes
        
        self.mostrar_estadisticas()
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas detalladas"""
        print(f"\n{'─'*70}")
        print("📊 ESTADÍSTICAS HARVARD MODIFICADA")
        print(f"{'─'*70}")
        print(f"Instrucciones ejecutadas: {self.instrucciones_ejecutadas}")
        print(f"Ciclos totales: {self.ciclos}")
        
        print(f"\n📦 I-Cache (Instrucciones):")
        total_i = self.i_cache_hits + self.i_cache_misses
        if total_i > 0:
            print(f"   Hits: {self.i_cache_hits} ({self.i_cache_hits/total_i*100:.1f}%)")
            print(f"   Misses: {self.i_cache_misses} ({self.i_cache_misses/total_i*100:.1f}%)")
        
        print(f"\n📦 D-Cache (Datos):")
        total_d = self.d_cache_hits + self.d_cache_misses
        if total_d > 0:
            print(f"   Hits: {self.d_cache_hits} ({self.d_cache_hits/total_d*100:.1f}%)")
            print(f"   Misses: {self.d_cache_misses} ({self.d_cache_misses/total_d*100:.1f}%)")
        
        print(f"\n✨ Accesos paralelos (I+D ambos hit): {self.accesos_paralelos}")
        print(f"CPI (Cycles Per Instruction): {self.ciclos / self.instrucciones_ejecutadas:.2f}")


# ========================================
# GENERA PROGRAMA DE PRUEBA
# ========================================

def generar_programa(n=1000, prob_mem=0.5):
    """Genera programa sintético para benchmark"""
    opcodes = ['ADD', 'SUB', 'MUL', 'MOV', 'CMP', 'JMP', 'LOAD', 'STORE']
    programa = []
    
    for _ in range(n):
        opcode = random.choice(opcodes)
        operandos = [random.randint(0, 7) for _ in range(2)]
        # Algunas instrucciones acceden memoria
        accede_mem = (opcode in ['LOAD', 'STORE']) or (random.random() < prob_mem)
        
        programa.append(Instruccion(opcode, operandos, accede_mem))
    
    return programa


# ========================================
# BENCHMARK COMPARATIVO
# ========================================

print("="*70)
print("🏁 BENCHMARK: COMPARACIÓN DE ARQUITECTURAS")
print("="*70)
print(f"\nPrograma de prueba: 1000 instrucciones")
print(f"50% acceden memoria de datos\n")

# Genera mismo programa para todas las arquitecturas
random.seed(42)  # Reproducibilidad
programa = generar_programa(n=1000, prob_mem=0.5)

input("Presiona ENTER para ejecutar Von Neumann...")
von = ArquitecturaVonNeumann()
von.ejecutar_programa(programa)

input("\nPresiona ENTER para ejecutar Harvard...")
harvard = ArquitecturaHarvard()
harvard.ejecutar_programa(programa)

input("\nPresiona ENTER para ejecutar Harvard Modificada...")
harvard_mod = ArquitecturaHarvardModificada()
harvard_mod.ejecutar_programa(programa)


# ========================================
# COMPARACIÓN FINAL
# ========================================

print("\n\n" + "="*70)
print("📊 COMPARACIÓN FINAL")
print("="*70)

print(f"\n{'Arquitectura':<25} {'Ciclos':<12} {'CPI':<8} {'Speedup'}")
print("─"*70)

von_cpi = von.ciclos / von.instrucciones_ejecutadas
harv_cpi = harvard.ciclos / harvard.instrucciones_ejecutadas
mod_cpi = harvard_mod.ciclos / harvard_mod.instrucciones_ejecutadas

print(f"{'Von Neumann':<25} {von.ciclos:<12} {von_cpi:<8.2f} 1.00×")
print(f"{'Harvard':<25} {harvard.ciclos:<12} {harv_cpi:<8.2f} {von.ciclos/harvard.ciclos:.2f}×")
print(f"{'Harvard Modificada':<25} {harvard_mod.ciclos:Continuar11:37 p.m.<12} {mod_cpi:<8.2f} {von.ciclos/harvard_mod.ciclos:.2f}×")
print(f"\n💡 INTERPRETACIÓN:")
speedup_harv = von.ciclos / harvard.ciclos
speedup_mod = von.ciclos / harvard_mod.ciclos
print(f"   • Harvard es {speedup_harv:.1f}× más rápida que Von Neumann")
print(f"   • Harvard Modificada es {speedup_mod:.1f}× más rápida")
print(f"   • Cache hits permiten paralelismo sin complejidad de Harvard pura")

---

## 🎯 **APLICACIONES MODERNAS**

### **¿Dónde se usa cada arquitectura HOY?**

| Tipo | Dispositivo | Arquitectura | Razón |
|------|-------------|--------------|-------|
| **CPU Desktop/Laptop** | Intel, AMD, Apple M | Harvard Modificada | Balance rendimiento/flexibilidad |
| **Smartphone** | ARM (Snapdragon, Bionic) | Harvard Modificada | Eficiencia energética + velocidad |
| **Microcontrolador** | Arduino, PIC | Harvard Pura | Bajo costo, determinismo |
| **DSP** | Audio, señales | Harvard Pura | Procesamiento tiempo real |
| **GPU** | NVIDIA, AMD | SIMT (Similar Harvard) | Paralelismo masivo |
| **TPU** | Google Tensor | Arquitectura custom | Optimizado para IA |

### **Tu Intel Ultra 9 en Detalle:**
Arquitectura: Harvard Modificada Multi-nivel
Nivel 1 (por núcleo):
├─ I-Cache: 32 KB (8-way)
├─ D-Cache: 32 KB (8-way)
└─ TLB separados (I-TLB, D-TLB)
→ Harvard PURO aquí
Nivel 2 (por núcleo):
└─ Cache unificado: 512 KB - 1 MB
→ Von Neumann (flexible)
Nivel 3 (compartido):
└─ Cache unificado: 16-24 MB
→ Von Neumann
Memoria Principal:
└─ RAM: 32 GB DDR5
→ Von Neumann (código y datos juntos)