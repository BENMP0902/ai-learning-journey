"""
Simulador detallado del ciclo Fetch-Decode-Execute
Muestra cada paso interno del CPU
"""

class CPUDetallado:
    def __init__(self):
        # Registros de propósito general
        self.R = [0] * 8  # R0-R7
        
        # Registros especiales
        self.PC = 0  # Program Counter
        self.IR = None  # Instruction Register
        self.MAR = 0  # Memory Address Register
        self.MDR = 0  # Memory Data Register
        
        # ALU Flags
        self.Z = False  # Zero
        self.C = False  # Carry
        self.N = False  # Negative
        self.V = False  # Overflow
        
        # Memoria (256 bytes)
        self.memoria = [0] * 256
        
        # Estadísticas
        self.ciclo_actual = 0
        self.instrucciones_totales = 0
        
        # Bus (simulado)
        self.address_bus = 0
        self.data_bus = 0
        self.control_bus = ""
    
    def actualizar_flags(self, resultado, bits=8):
        """Actualiza flags según resultado"""
        max_val = (1 << bits) - 1
        
        self.Z = (resultado & max_val) == 0
        self.C = resultado > max_val or resultado < 0
        self.N = (resultado & (1 << (bits-1))) != 0
        self.V = self.C  # Simplificado
    
    def mostrar_estado(self, fase):
        """Muestra estado del CPU"""
        print(f"\n{'='*70}")
        print(f"CICLO {self.ciclo_actual} - FASE: {fase}")
        print(f"{'='*70}")
        
        print(f"\n📍 Registros Especiales:")
        print(f"   PC  = 0x{self.PC:04X}  (Próxima instrucción)")
        print(f"   IR  = {self.IR if self.IR else 'vacío'}  (Instrucción actual)")
        print(f"   MAR = 0x{self.MAR:04X}  (Dirección de memoria)")
        print(f"   MDR = 0x{self.MDR:02X}  (Dato de memoria)")
        
        print(f"\n📊 Registros de Propósito General:")
        for i in range(0, 8, 4):
            print(f"   ", end="")
            for j in range(4):
                if i+j < 8:
                    print(f"R{i+j}={self.R[i+j]:3d}  ", end="")
            print()
        
        print(f"\n🚩 Flags:")
        print(f"   Z={int(self.Z)} (Zero)  ", end="")
        print(f"C={int(self.C)} (Carry)  ", end="")
        print(f"N={int(self.N)} (Negative)  ", end="")
        print(f"V={int(self.V)} (Overflow)")
        
        print(f"\n🚌 Bus:")
        print(f"   Address Bus: 0x{self.address_bus:04X}")
        print(f"   Data Bus:    0x{self.data_bus:02X}")
        print(f"   Control Bus: {self.control_bus}")
    
    def fetch(self):
        """FASE 1: FETCH - Buscar instrucción"""
        print("\n" + "▶"*35)
        print("FASE 1: FETCH (BUSCAR INSTRUCCIÓN)")
        print("▶"*35)
        
        # Paso 1: PC indica dirección
        print(f"\n1️⃣  Program Counter apunta a: 0x{self.PC:04X}")
        self.MAR = self.PC
        print(f"   → MAR cargado con 0x{self.MAR:04X}")
        
        # Paso 2: Enviar dirección por Address Bus
        self.address_bus = self.MAR
        self.control_bus = "READ"
        print(f"\n2️⃣  Enviando señales por el bus:")
        print(f"   Address Bus → 0x{self.address_bus:04X}")
        print(f"   Control Bus → {self.control_bus}")
        
        # Paso 3: Leer de memoria
        self.MDR = self.memoria[self.MAR]
        self.data_bus = self.MDR
        print(f"\n3️⃣  Memoria responde:")
        print(f"   Data Bus ← 0x{self.data_bus:02X}")
        print(f"   → MDR cargado con 0x{self.MDR:02X}")
        
        # Paso 4: Cargar en IR
        self.IR = self.MDR
        print(f"\n4️⃣  Instrucción cargada en IR:")
        print(f"   IR = 0x{self.IR:02X}")
        
        # Paso 5: Incrementar PC
        self.PC += 1
        print(f"\n5️⃣  Program Counter incrementado:")
        print(f"   PC = 0x{self.PC:04X}")
        
        self.ciclo_actual += 1
        self.mostrar_estado("FETCH COMPLETADO")
        
        input("\n⏸️  Presiona ENTER para continuar a DECODE...")
    
    def decode(self):
        """FASE 2: DECODE - Decodificar instrucción"""
        print("\n" + "▶"*35)
        print("FASE 2: DECODE (DECODIFICAR)")
        print("▶"*35)
        
        # Extraer opcode y operandos
        opcode = (self.IR & 0xF0) >> 4
        operando = self.IR & 0x0F
        
        print(f"\n1️⃣  Analizando instrucción en IR: 0x{self.IR:02X}")
        print(f"   Binario: {bin(self.IR)[2:].zfill(8)}")
        print(f"   ")
        print(f"   ┌────────┬────────┐")
        print(f"   │ {bin(opcode)[2:].zfill(4)} │ {bin(operando)[2:].zfill(4)} │")
        print(f"   └────────┴────────┘")
        print(f"    Opcode   Operando")
        
        print(f"\n2️⃣  Opcode extraído: 0x{opcode:X}")
        
        # Decodificar instrucción
        instrucciones = {
            0x0: "NOP",
            0x1: "LOAD",
            0x2: "STORE",
            0x3: "ADD",
            0x4: "SUB",
            0x5: "MOV",
            0xF: "HALT"
        }
        
        nombre_inst = instrucciones.get(opcode, "UNKNOWN")
        print(f"   → Instrucción: {nombre_inst}")
        
        print(f"\n3️⃣  Operando: 0x{operando:X}")
        if opcode in [0x3, 0x4]:
            print(f"   → Registro fuente: R{operando}")
        elif opcode == 0x5:
            rd = operando >> 2
            rs = operando & 0x3
            print(f"   → Destino: R{rd}, Fuente: R{rs}")
        
        print(f"\n4️⃣  Control Unit genera señales:")
        if opcode == 0x3:  # ADD
            print(f"   • ALU_OP = ADD")
            print(f"   • REG_READ_1 = R0")
            print(f"   • REG_READ_2 = R{operando}")
            print(f"   • REG_WRITE = R0")
            print(f"   • UPDATE_FLAGS = TRUE")
        
        self.ciclo_actual += 1
        self.mostrar_estado("DECODE COMPLETADO")
        
        input("\n⏸️  Presiona ENTER para continuar a EXECUTE...")
        
        return opcode, operando
    
    def execute(self, opcode, operando):
        """FASE 3: EXECUTE - Ejecutar operación"""
        print("\n" + "▶"*35)
        print("FASE 3: EXECUTE (EJECUTAR)")
        print("▶"*35)
        
        if opcode == 0x3:  # ADD R0, Rn
            print(f"\n1️⃣  Leyendo operandos:")
            print(f"   R0 = {self.R[0]}")
            print(f"   R{operando} = {self.R[operando]}")
            
            print(f"\n2️⃣  Enviando a ALU:")
            print(f"   Input A: {self.R[0]}")
            print(f"   Input B: {self.R[operando]}")
            print(f"   Operation: ADD")
            
            print(f"\n3️⃣  ALU ejecutando suma:")
            a = self.R[0]
            b = self.R[operando]
            
            # Mostrar suma binaria
            print(f"   ")
            print(f"     {bin(a)[2:].zfill(8)}  ({a})")
            print(f"   + {bin(b)[2:].zfill(8)}  ({b})")
            print(f"   ─────────────")
            
            resultado = a + b
            print(f"     {bin(resultado & 0xFF)[2:].zfill(8)}  ({resultado & 0xFF})")
            
            # Actualizar flags
            self.actualizar_flags(resultado)
            
            print(f"\n4️⃣  Actualizando flags:")
            print(f"   Z (Zero) = {int(self.Z)}  ", end="")
            print(f"{'✓ Resultado es cero' if self.Z else '✗ Resultado no es cero'}")
            print(f"   C (Carry) = {int(self.C)}  ", end="")
            print(f"{'✓ Hubo overflow' if self.C else '✗ Sin overflow'}")
            print(f"   N (Negative) = {int(self.N)}")
            print(f"   V (Overflow) = {int(self.V)}")
            
            # Escribir resultado
            self.R[0] = resultado & 0xFF
            print(f"\n5️⃣  Escribiendo resultado:")
            print(f"   R0 = {self.R[0]}")
        
        elif opcode == 0xF:  # HALT
            print("\n   ⏹️  HALT - Deteniendo CPU")
            return False
        
        self.ciclo_actual += 1
        self.instrucciones_totales += 1
        self.mostrar_estado("EXECUTE COMPLETADO")
        
        return True
    
    def ejecutar_programa(self, programa):
        """Ejecuta programa completo"""
        print("\n" + "="*70)
        print("🚀 INICIANDO SIMULACIÓN DETALLADA DE CPU")
        print("="*70)
        
        # Cargar programa
        for i, instruccion in enumerate(programa):
            self.memoria[i] = instruccion
        
        print(f"\n📥 Programa cargado en memoria:")
        print(f"   Tamaño: {len(programa)} bytes")
        print(f"   Dirección inicial: 0x{0:04X}")
        
        print(f"\n📋 Contenido del programa:")
        for i, inst in enumerate(programa): 
            print(f"   0x{i:04X}: 0x{inst:02X}  ({bin(inst)[2:].zfill(8)})")    
        input("\n⏸️  Presiona ENTER para comenzar ejecución...")   
        
            # Ejecutar
        while self.PC < len(programa):
            self.fetch()
            opcode, operando = self.decode()
            continuar = self.execute(opcode, operando)       
            
            if not continuar:
                break    
            
            # Resumen
        print("\n" + "="*70)
        print("✅ PROGRAMA FINALIZADO")
        print("="*70)
        print(f"\n📊 Estadísticas:")
        print(f"   Ciclos totales: {self.ciclo_actual}")
        print(f"   Instrucciones: {self.instrucciones_totales}")
        print(f"   CPI: {self.ciclo_actual / max(self.instrucciones_totales, 1):.2f}")    
        print(f"\n🏁 Estado final de registros:")
        for i in range(8):
            print(f"   R{i} = {self.R[i]}")


if __name__ == "__main__":
    cpu = CPUDetallado()

    # Valores iniciales
    cpu.R[0] = 5
    cpu.R[1] = 3

    # Programa:
    # ADD R0, R1  → R0 = 5 + 3
    # HALT
    programa = [
        0x31,  # ADD R0, R1
        0xF0   # HALT
    ]

    cpu.ejecutar_programa(programa)
