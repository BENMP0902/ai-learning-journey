"""
Simulación de transistor como interruptor digital
"""

class Transistor:
    """
    Transistor NPN básico simulado
    """
    def __init__(self, nombre="T1"):
        self.nombre = nombre
        self.estado = False  # OFF por defecto
    
    def aplicar_señal_base(self, voltaje_base):
        """
        Si voltaje_base > umbral (0.7V típicamente), transistor conduce
        
        Args:
            voltaje_base: Voltaje en voltios
        
        Returns:
            bool: True si conduce (ON), False si no (OFF)
        """
        UMBRAL = 0.7  # Voltios necesarios para activar
        
        if voltaje_base >= UMBRAL:
            self.estado = True  # Transistor ON
            return True
        else:
            self.estado = False  # Transistor OFF
            return False
    
    def conducir_corriente(self, corriente_entrada):
        """
        Si transistor está ON, permite pasar corriente
        
        Args:
            corriente_entrada: Corriente en amperios
        
        Returns:
            float: Corriente que sale (0 si está OFF)
        """
        if self.estado:
            # En transistor real, hay ganancia (β)
            ganancia = 100  # Típico para transistor NPN
            return corriente_entrada * ganancia
        else:
            return 0.0
    
    def __repr__(self):
        estado_str = "ON (1)" if self.estado else "OFF (0)"
        return f"Transistor {self.nombre}: {estado_str}"


# DEMOSTRACIÓN 1: Transistor como interruptor
print("=" * 60)
print("TRANSISTOR COMO INTERRUPTOR")
print("=" * 60)

transistor = Transistor("Q1")

# Caso 1: Sin señal en base
print("\n1. Sin voltaje en base (0V):")
transistor.aplicar_señal_base(0.0)
print(f"   {transistor}")
print(f"   Corriente de salida: {transistor.conducir_corriente(0.001):.6f} A")

# Caso 2: Con señal en base
print("\n2. Con voltaje en base (5V):")
transistor.aplicar_señal_base(5.0)
print(f"   {transistor}")
corriente_salida = transistor.conducir_corriente(0.001)  # 1 mA entrada
print(f"   Corriente de salida: {corriente_salida:.4f} A")
print(f"   ¡Ganancia de {corriente_salida / 0.001:.0f}×!")


# DEMOSTRACIÓN 2: Construir