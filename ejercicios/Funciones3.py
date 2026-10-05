def saludar():
  # Muestra un saludo en pantalla.
  print("¡Hola amiga!")
  input()

def saludar_nombre():
  # Muestra un saludo personalizado con el nombre proporcionado.
  nombre = input("Ingrese su nombre:")
  print(f"¡Hola {nombre}!")
  input('Enter para continuar!!!')

def factorial(n):
  # Calcula el factorial de un número entero positivo.
  #Args:
  # n: Un número entero positivo.
  #Returns:
  # El factorial de n.
  
  if n == 0:
    return 1
  elif n < 0:
    return "El factorial no está definido para números negativos."
  else:
    resultado = 1
    for i in range(1, n + 1):
      resultado *= i
    return resultado


def obtener_calificaciones(notas):
  # Recibe una lista de notas numéricas y devuelve una lista de calificaciones textuales.

  # Args:
  # notas: Una lista de números que representan las notas.

  # Returns:
  # Una lista de cadenas con las calificaciones correspondientes.
  
  calificaciones = []
  for nota in notas:
    if nota >= 0 and nota < 4:
      calificaciones.append("Desaprobado")
    elif nota >= 4 and nota < 6:
      calificaciones.append("Aprobado")
    elif nota >= 6 and nota < 8:
      calificaciones.append("Bueno")
    elif nota >= 8 and nota < 10:
      calificaciones.append("Muy Bueno")
    elif nota == 10:
      calificaciones.append("Excelente")
    else:
      calificaciones.append("Nota inválida")
  return calificaciones


def analizar_texto(texto):
  # Analiza una cadena de texto, calcula su longitud y la convierte a mayúsculas.

  # Args:
  # texto: La cadena de texto a analizar.

  # Returns:
  # Una tupla con la longitud de la cadena y la cadena en mayúsculas.
  
  longitud = len(texto)
  texto_mayusculas = texto.upper()
  return longitud, texto_mayusculas


def sumar_varios(*numeros):
  # Recibe una cantidad variable de números y devuelve su suma total.

  # Args:
  # *numeros: Argumentos numéricos variables.

  # Returns:
  # La suma total de los números.
  
  suma_total = 0
  for numero in numeros:
    suma_total += numero
  return suma_total


def mostrar_info(nombre, edad):
  # Recibe el nombre y la edad de una persona y los imprime en formato "nombre:edad".

  # Args:
  # nombre: El nombre de la persona (cadena de texto).
  # edad: La edad de la persona (número).
  print(f"{nombre}:{edad}")


def mostrar_info(nombre, edad, lista_personas):
  # Agrega el nombre y la edad a una lista y luego la imprime.
  lista_personas.append((nombre, edad))
  print("Lista actual de personas:")
  print(lista_personas)
  return lista_personas

def ordenar_lista(lista_personas):
  #Ordena la lista de personas por nombre y luego por edad
  # Ordenar primero por nombre y luego por edad (si hay nombres iguales)
  personas_ordenadas = sorted(lista_personas, key=lambda item: (item[0], item[1]))
  print("\nLista ordenada por nombre y luego por edad:")
  print(personas_ordenadas)
  input('Enter para continuar!!!')
  return personas_ordenadas

def cuadrados_lista(lista_personas):
  #alcula el cuadrado de la edad de cada persona en la lista usando map().
  # Extraer las edades de la lista de tuplas
  edades = [persona[1] for persona in lista_personas]

  # Crear una nueva lista con el cuadrado de cada edad usando map() y lambda
  edades_cuadrados = list(map(lambda edad: edad ** 2, edades))
  print("\nLista con edades al cuadrado (usando map()):")
  print(edades_cuadrados)
  input('Enter para continuar!!!')
  return edades_cuadrados

def filtrar_palabras_largas_for(lista_palabras, longitud_minima=5):
  # Filtra una lista de palabras usando un bucle for y devuelve solo aquellas con longitud mayor a longitud_minima.

  # Args:
  # lista_palabras: La lista de palabras a filtrar.
  # longitud_minima: La longitud mínima que debe tener una palabra para ser incluida (por defecto 5).

  # Returns:
  # Una nueva lista con las palabras filtradas.
  
  palabras_largas = []  # Inicializar una lista vacía para almacenar las palabras largas
  for palabra in lista_palabras: # Iterar sobre cada palabra en la lista original
    if len(palabra) > longitud_minima: # Verificar si la longitud de la palabra es mayor que la longitud mínima
      palabras_largas.append(palabra) # Si la condición es verdadera, agregar la palabra a la nueva lista
  return palabras_largas

def mostrar_menu():
  """Muestra el menú de opciones al usuario."""
  print("\n--- Menú de Opciones ---")
  print("1. Saludo")
  print("2. Saludao con nombre")
  print("3. Factorial de un numero")
  print("4. Clasificaciones")
  print("5. Analizar texo")
  print("6. Sumar varios")
  print("7. Mostrar info")
  print('8. Ordenar lista')
  print('9. Cuadrados lista')
  print('10. Filtrar palabras')
  print("0. Salir")


  print("------------------------")


while True:
  mostrar_menu()
  eleccion = input("Ingresa el número de tu elección: ")

  if eleccion == '1':
    saludar()

  elif eleccion == '2':
    saludar_nombre()

  elif eleccion == '3':
    numero = int(input("Ingrese un numero: "))
    print(f"El factorial de {numero} es: {factorial(numero)}")
    input('Enter para continuar!!!')

  elif eleccion == '4':
    lista_notas = [3, 5, 7, 9, 10, 2, 11]
    lista_calificaciones = obtener_calificaciones(lista_notas)
    print(f"Notas: {lista_notas}")
    print(f"Calificaciones: {lista_calificaciones}")
    input('Enter para continuar!!!')

  elif eleccion == '5':
    cadena_ejemplo = "Hola mundo"
    longitud, texto_convertido = analizar_texto(cadena_ejemplo)
    print(f"Texto original: '{cadena_ejemplo}'")
    print(f"Longitud del texto: {longitud}")
    print(f"Texto en mayúsculas: '{texto_convertido}'")
    input('Enter para continuar!!!')

  elif eleccion == '6':
    print(f"Suma de 1, 2, 3: {sumar_varios(1, 2, 3)}")
    print(f"Suma de 10, 20: {sumar_varios(10, 20)}")
    print(f"Suma de ningún número: {sumar_varios()}")
    print(f"Suma de 5: {sumar_varios(5)}")
    input('Enter para continuar!!!')

 
  elif eleccion == '7':
    # Lógica para verificar y/o crear la lista 'personas' fuera de la función
    if 'personas' in globals() and isinstance(globals()['personas'], list):
      respuesta = input("La lista 'personas' ya existe. ¿Desea crear una nueva lista (n) o continuar agregando personas (c)? (n/c): ")
      if respuesta.lower() == 'n':
        personas = []
        print("Se ha creado una nueva lista 'personas'.")
      else:
        personas = globals()['personas']
        print("Continuando con la lista 'personas' existente.")
    else:
      personas = []
      print("La lista 'personas' no existe. Creando una nueva lista.")    

    # Carga interactiva de personas
    nombre = input("Ingrese el nombre de la persona: ")
    edad = int(input("Ingrese la edad de la persona: "))
    personas = mostrar_info(nombre, edad, personas)
  
    while True:
      respuesta = input("¿Desea seguir cargando más personas? (s/n): ")
      if respuesta.lower() == 's':
        nombre = input("Ingrese el nombre de la persona: ")
        edad = int(input("Ingrese la edad de la persona: "))
        personas = mostrar_info(nombre, edad, personas)
        input()

      else:
        print(personas)
        input('Enter para continuar!!!')
        break
        

  elif eleccion == '8':
    personas_ordenadas = ordenar_lista(personas)

  elif eleccion == '9':
    edades_cuadrados = cuadrados_lista(personas_ordenadas)


  elif eleccion == '10':
    lista_palabras = ["manzana", "banana", "kiwi", "naranja", "uva", "pera", "sandía"]
    palabras_filtradas_for = filtrar_palabras_largas_for(lista_palabras)

    print("Lista original de palabras:", lista_palabras)
    print("Lista de palabras con más de 5 letras (usando for):", palabras_filtradas_for)
    input('Enter para continuar!!!')
  
  elif eleccion == '0':
    print("Saliendo del programa. ¡Adiós!")
    break  # Sale del bucle while
  
  else:
    print("Opción no válida. Por favor, intenta de nuevo.")



