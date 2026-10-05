class Agenda:
    def __init__(self):
        """Initializes an empty list to store contacts."""
        self.contactos = []

    def añadir_contacto(self, nombre, telefono, email):
        """Adds a new contact to the agenda."""
        contacto = {
            'nombre': nombre,
            'telefono': telefono,
            'email': email
        }
        self.contactos.append(contacto)

    def lista_contactos(self):
        """Lists all contacts in the agenda."""
        if not self.contactos:
            print("No hay contactos en la agenda.")
        else:
            print("--- Contactos ---")
            for contacto in self.contactos:
                print(f"Nombre: {contacto['nombre']}")
                print(f"Teléfono: {contacto['telefono']}")
                print(f"Email: {contacto['email']}")
                print("-" * 10)

    def buscar_contacto(self, nombre):
        """Searches for a contact by name and displays their information."""
        nombre_lower = nombre.lower()
        for contacto in self.contactos:
            if contacto['nombre'].lower() == nombre_lower:
                print("--- Contacto Encontrado ---")
                print(f"Nombre: {contacto['nombre']}")
                print(f"Teléfono: {contacto['telefono']}")
                print(f"Email: {contacto['email']}")
                return
        print(f"El contacto '{nombre}' no fue encontrado.")

    def editar_contacto(self, nombre, nuevo_telefono, nuevo_email):
        """Edits an existing contact's phone and email."""
        nombre_lower = nombre.lower()
        for contacto in self.contactos:
            if contacto['nombre'].lower() == nombre_lower:
                contacto['telefono'] = nuevo_telefono
                contacto['email'] = nuevo_email
                print(f"Información del contacto '{nombre}' actualizada.")
                return
        print(f"El contacto '{nombre}' no fue encontrado para editar.")

    def cerrar_agenda(self):
        """Prints a message indicating that the agenda is being closed."""
        print("Cerrando la agenda. ¡Hasta luego!")



def mostrar_menu():
    """Displays the available options to the user."""
    print("\n--- Menú de la Agenda ---")
    print("1. Añadir contacto")
    print("2. Listar contactos")
    print("3. Buscar contacto")
    print("4. Editar contacto")
    print("5. Cerrar agenda")
    print("-------------------------")

def ejecutar_opcion(opcion, agenda):
    """Executes the selected option based on user input."""
    if opcion == '1':
        nombre = input("Ingrese el nombre: ")
        telefono = input("Ingrese el teléfono: ")
        email = input("Ingrese el email: ")
        agenda.añadir_contacto(nombre, telefono, email)
    elif opcion == '2':
        agenda.lista_contactos()
    elif opcion == '3':
        nombre = input("Ingrese el nombre del contacto a buscar: ")
        agenda.buscar_contacto(nombre)
    elif opcion == '4':
        nombre = input("Ingrese el nombre del contacto a editar: ")
        nuevo_telefono = input("Ingrese el nuevo teléfono: ")
        nuevo_email = input("Ingrese el nuevo email: ")
        agenda.editar_contacto(nombre, nuevo_telefono, nuevo_email)
    elif opcion == '5':
        agenda.cerrar_agenda()
        return True  # Indicate to stop the loop
    else:
        print("Opción no válida. Por favor, ingrese un número del 1 al 5.")
    return False # Indicate to continue the loop

agenda = Agenda()

while True:
    mostrar_menu()
    opcion = input("Seleccione una opción: ")
    if ejecutar_opcion(opcion, agenda):
        break

