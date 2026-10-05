class Triangulo:
    def __init__(self, lado1, lado2, lado3):
        #Inicializa los atributos de la clase Triangulo.
        self.lado1 = lado1
        self.lado2 = lado2
        self.lado3 = lado3

    def imprimir_lado_mayor(self):
        #Imprime el valor del lado con un tamaño mayor.
        lado_mayor = max(self.lado1, self.lado2, self.lado3)
        print(f"El lado mayor del triángulo es: {lado_mayor}")

    def tipo_triangulo(self):
        #Determina y retorna el tipo de triángulo.
        if self.lado1 == self.lado2 == self.lado3:
            return "equilátero"
        elif self.lado1 == self.lado2 or self.lado1 == self.lado3 or self.lado2 == self.lado3:
            return "isósceles"
        else:
            return "escaleno"
        

# Ejemplo de uso:
# Creamos una instancia de la clase Triangulo
triangulo1 = Triangulo(5, 5, 5)

# Imprimimos el lado mayor
triangulo1.imprimir_lado_mayor()

# Determinamos y imprimimos el tipo de triángulo
print(f"El triángulo es de tipo: {triangulo1.tipo_triangulo()}")

print("-" * 20) # Separador

triangulo2 = Triangulo(7, 4, 7)
triangulo2.imprimir_lado_mayor()
print(f"El triángulo es de tipo: {triangulo2.tipo_triangulo()}")

print("-" * 20) # Separador

triangulo3 = Triangulo(3, 6, 8)
triangulo3.imprimir_lado_mayor()
print(f"El triángulo es de tipo: {triangulo3.tipo_triangulo()}")


