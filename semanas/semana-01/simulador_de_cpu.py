"""
Simulador simplificado de CPU
Demuestra el ciclo Fetch-Decode-Execute
"""

class CPU:
    """
    Simulador de CPU de 8 bits con arquitectura simple
    """
    def __init__(self):
        # Registros de propósito general (8 bits)
        self.registros = {
            'R0': 0, 'R1': 0, 'R2': 0, 'R3': 0,
            'R4': 0, 'R5': 0, 'R6': 0, 'R7': 0
        }
        
        # Registros especiales
        self.PC = 0  # Program Counter (dirección de instrucción actual)
        self.IR = None  # Instruction Register (instrucción actual)
        self.ACC = 0  # Accumulator (resultado temporal)
        
        # Flags
        self.flags = {
            'ZERO': False,  # Resultado = 0
            'CARRY': False,  # Overflow en suma
            'NEGATIVE': False  # Resultado negativo
        }
        
        # Memoria (256 bytes)
        self.memoria = [0] * 256
        
        # Estadísticas
        self.ciclos = 0
        self.instrucciones_ejecutadas = 0
    
    def actualizar_flags(self, resultado):
        """Actualiza flags según resultado de operación"""
        self.flags['ZERO'] = (resultado == 0)
        self.flags['NEGATIVE'] = (resultado < 0)
        self.flags['CARRY'] = (resultado > 255 or resultado < 0)
    
    def fetch(self):
        """
        FASE 1: FETCH
        Busca instrucción de memoria apuntada por PC
        """
        print(f"\n[FETCH] PC={self.PC}")
        
        # Lee instrucción de memoria
        self.IR = self.memoria[self.PC]
        print(f"  Instrucción cargada en IR: 0x{self.IR:02X}")
        
        # Incrementa PC para siguiente instrucción
        self.PC += 1
        self.ciclos += 1
    
    def decode(self):
        """
        FASE 2: DECODE
        Decodifica instrucción y determina operación
        """
        print(f"[DECODE] Analizando instrucción...")
        
        # En CPU real, esto es hardware. Aquí lo simulamos
        # Formato simple: [4 bits opcode][4 bits operando]
        opcode = (self.IRContinuar10:16 p.m.& 0xF0) >> 4  # 4 bits superiores
        in poperando = self.IR & 0x0F  # 4 bits inferiores
        print(f"  Opcode: 0x{opcode:X}, Operando: 0x{operando:X}")
        
        self.ciclos += 1
        return opcode, operando

    def execute(self, opcode, operando):
        """
        FASE 3: EXECUTE
        Ejecuta la operación decodificada
        """
        print(f"[EXECUTE] Ejecutando operación...")
        
        # Set de instrucciones simplificado
        if opcode == 0x0:  # NOP (No Operation)
            print("  NOP - No hace nada")
        
        elif opcode == 0x1:  # LOAD Rn, [memoria]
            registro = f'R{operando}'
            direccion = self.memoria[self.PC]
            self.PC += 1
            self.registros[registro] = self.memoria[direccion]
            print(f"  LOAD {registro}, [{direccion}]")
            print(f"  {registro} = {self.registros[registro]}")
        
        elif opcode == 0x2:  # STORE [memoria], Rn
            registro = f'R{operando}'
            direccion = self.memoria[self.PC]
            self.PC += 1
            self.memoria[direccion] = self.registros[registro]
            print(f"  STORE [{direccion}], {registro}")
            print(f"  Memoria[{direccion}] = {self.memoria[direccion]}")
        
        elif opcode == 0x3:  # ADD R0, Rn
            registro = f'R{operando}'
            resultado = self.registros['R0'] + self.registros[registro]
            self.actualizar_flags(resultado)
            self.registros['R0'] = resultado & 0xFF  # Mantener 8 bits
            print(f"  ADD R0, {registro}")
            print(f"  R0 = {self.registros['R0']} (Flags: Z={self.flags['ZERO']}, C={self.flags['CARRY']})")
        
        elif opcode == 0x4:  # SUB R0, Rn
            registro = f'R{operando}'
            resultado = self.registros['R0'] - self.registros[registro]
            self.actualizar_flags(resultado)
            self.registros['R0'] = resultado & 0xFF
            print(f"  SUB R0, {registro}")
            print(f"  R0 = {self.registros['R0']}")
        
        elif opcode == 0x5:  # MOV Rd, Rs
            rd = operando >> 2  # 2 bits para destino
            rs = operando & 0x3  # 2 bits para source
            self.registros[f'R{rd}'] = self.registros[f'R{rs}']
            print(f"  MOV R{rd}, R{rs}")
            print(f"  R{rd} = {self.registros[f'R{rd}']}")
        
        elif opcode == 0xF:  # HALT
            print("  HALT - Deteniendo CPU")
            return False  # Señal de parada
        
        else:
            print(f"  ⚠️  Opcode desconocido: 0x{opcode:X}")
        
        self.ciclos += 1
        self.instrucciones_ejecutadas += 1
        return True  # Continuar ejecución

    def ejecutar_programa(self, programa):
        """
        Ejecuta programa completo
        
        Args:
            programa: Lista de instrucciones (bytes)
        """
        print("=" * 70)
        print("INICIANDO EJECUCIÓN DE PROGRAMA")
        print("=" * 70)
        
        # Carga programa en memoria
        for i, instruccion in enumerate(programa):
            self.memoria[i] = instruccion
        
        print(f"Programa cargado: {len(programa)} bytes")
        print(f"Dirección inicial: 0x{0:04X}")
        print()
        
        # Ciclo Fetch-Decode-Execute
        while self.PC < len(programa):
            print(f"\n{'─' * 70}")
            print(f"CICLO #{self.ciclos + 1}")
            print(f"{'─' * 70}")
            
            self.fetch()
            opcode, operando = self.decode()
            continuar = self.execute(opcode, operando)
            
            if not continuar:
                break
            
            # Muestra estado de registros
            self.mostrar_registros()
        
        print("\n" + "=" * 70)
        print("PROGRAMA FINALIZADO")
        print("=" * 70)
        self.mostrar_estadisticas()

    def mostrar_registros(self):
        """Muestra estado actual de registros"""
        print("\n📊 Estado de Registros:")
        for reg, valor in list(self.registros.items())[:4]:
            print(f"  {reg} = {valor:3d} (0x{valor:02X})", end="    ")
        print()
        for reg, valor in list(self.registros.items())[4:8]:
            print(f"  {reg} = {valor:3d} (0x{valor:02X})", end="    ")
        print()

    def mostrar_estadisticas(self):
        """Muestra estadísticas de ejecución"""
        print(f"\n📈 Estadísticas:")
        print(f"  Ciclos totales: {self.ciclos}")
        print(f"  Instrucciones ejecutadas: {self.instrucciones_ejecutadas}")
        print(f"  CPI (Cycles Per Instruction): {self.ciclos / max(self.instrucciones_ejecutadas, 1):.2f}")
        
        # Simula frecuencia
        frecuencia_ghz = 2.5  # Tu CPU
        tiempo_ciclo_ns = 1 / frecuencia_ghz  # nanosegundos
        tiempo_total = self.ciclos * tiempo_ciclo_ns
        print(f"  Tiempo estimado a 2.5 GHz: {tiempo_total:.2f} ns")