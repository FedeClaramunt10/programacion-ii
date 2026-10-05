import tkinter as tk
from tkinter import ttk
import json

def guardar_clientes():
    """Saves the current list of clients to a text file."""
    try:
        with open("clientes.txt", "w") as f:
            for cliente in clientes:
                f.write(json.dumps(cliente) + "\n")
        print("Clientes guardados correctamente.")
    except IOError:
        print("Error al guardar los clientes.")

def cargar_clientes():
    """Loads client data from the 'clientes.txt' file."""
    global clientes
    clientes = [] # Clear the current list before loading
    try:
        with open("clientes.txt", "r") as f:
            for line in f:
                try:
                    cliente = json.loads(line.strip())
                    clientes.append(cliente)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from line: {line.strip()}")
        print("Clientes cargados correctamente.")
    except FileNotFoundError:
        print("Archivo 'clientes.txt' no encontrado. No se cargaron clientes.")
    except IOError:
        print("Error al leer el archivo 'clientes.txt'.")

root = tk.Tk()
root.title("Gestión de Clientes")
root.geometry("800x600") # Increased height to accommodate payment history

# List to store client data
clientes = []

# Variable to hold the index of the selected client
selected_client_index = -1

def clear_fields():
    """Clears all entry fields."""
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    confirmation_label.config(text="")
    # The payment history text widget is now in the payment window, so we don't clear it here

def update_listbox():
    """Clears and repopulates the listbox with current client data."""
    listbox_clientes.delete(0, tk.END)
    for cliente in clientes:
        listbox_clientes.insert(tk.END, f"{cliente['Nombre']} {cliente['Apellido']}")


def dar_alta_cliente():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    direccion = entry_direccion.get()
    telefono = entry_telefono.get()

    if nombre and apellido and direccion and telefono:
        cliente = {
            "Nombre": nombre,
            "Apellido": apellido,
            "Dirección": direccion,
            "Teléfono": telefono,
            "Pagos": {} # Initialize payments as an empty dictionary
        }
        clientes.append(cliente)
        confirmation_label.config(text="Cliente dado de alta correctamente.")
        update_listbox() # Add client to the listbox
        clear_fields() # Clear the entry fields after successful registration
        guardar_clientes() # Save clients after adding
    else:
        confirmation_label.config(text="Por favor, complete todos los campos.")

def seleccionar_cliente(event):
    global selected_client_index
    try:
        # Get the index of the selected item
        selected_indices = listbox_clientes.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_client_index = selected_index
            cliente = clientes[selected_index]
            # Populate the entry fields with the selected client's data
            clear_fields() # Clear fields before populating
            entry_nombre.insert(0, cliente["Nombre"])
            entry_apellido.insert(0, cliente["Apellido"])
            entry_direccion.insert(0, cliente["Dirección"])
            entry_telefono.insert(0, cliente["Teléfono"])
            confirmation_label.config(text="")

            # Payment history is now displayed in the payment window, not the main window

        else:
             # If nothing is selected, clear the selection index and fields
            selected_client_index = -1
            clear_fields()

    except IndexError:
        # Handle the case where no item is selected (should be covered by else above now)
        selected_client_index = -1
        clear_fields()
        confirmation_label.config(text="No hay cliente seleccionado.")


def modificar_cliente():
    global selected_client_index
    if selected_client_index != -1:
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()

        if nombre and apellido and direccion and telefono:
            clientes[selected_client_index]["Nombre"] = nombre
            clientes[selected_client_index]["Apellido"] = apellido
            clientes[selected_client_index]["Dirección"] = direccion
            clientes[selected_client_index]["Teléfono"] = telefono
            confirmation_label.config(text="Cliente modificado correctamente.")
            update_listbox() # Update the listbox
            clear_fields() # Clear the selection and entry fields after modification
            listbox_clientes.selection_clear(0, tk.END) # Clear listbox selection
            selected_client_index = -1 # Reset selected index
            guardar_clientes() # Save clients after modifying
        else:
            confirmation_label.config(text="Por favor, complete todos los campos para modificar.")
    else:
        confirmation_label.config(text="Seleccione un cliente para modificar.")

def eliminar_cliente():
    """Removes the selected client from the list."""
    global selected_client_index
    if selected_client_index != -1:
        del clientes[selected_client_index]
        confirmation_label.config(text="Cliente eliminado correctamente.")
        update_listbox() # Update the listbox
        clear_fields() # Clear the entry fields and selection
        listbox_clientes.selection_clear(0, tk.END) # Clear listbox selection
        selected_client_index = -1 # Reset selected index
        guardar_clientes() # Save clients after deleting
    else:
        confirmation_label.config(text="Seleccione un cliente para eliminar.")


def record_payment(client_index, month, amount, payment_history_text_widget):
    """Records a payment for a given client and month and updates the history display."""
    if client_index != -1 and client_index < len(clientes):
        clientes[client_index]["Pagos"][month] = amount
        # Update the payment history display in the payment window
        payment_history_text_widget.delete("1.0", tk.END)
        cliente = clientes[client_index]
        if cliente["Pagos"]:
            payment_history_text_widget.insert(tk.END, "Historial de Pagos:\n")
            for month, amount in cliente["Pagos"].items():
                payment_history_text_widget.insert(tk.END, f"- {month}: ${amount:.2f}\n")
        else:
            payment_history_text_widget.insert(tk.END, "No hay historial de pagos para este cliente.")
        guardar_clientes() # Save clients after recording payment


def open_payment_window():
    """Opens a new window to enter payment details and display history."""
    if selected_client_index == -1:
        confirmation_label.config(text="Seleccione un cliente para registrar un pago.")
        return

    payment_window = tk.Toplevel(root)
    payment_window.title("Registrar Pago")
    payment_window.geometry("400x300") # Increased size for history display

    # Make the payment window modal
    payment_window.grab_set()

    # Label and Combobox for Month selection
    label_month = tk.Label(payment_window, text="Mes:")
    label_month.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    month_variable = tk.StringVar(payment_window)
    month_variable.set(months[0]) # default value
    combobox_month = ttk.Combobox(payment_window, textvariable=month_variable, values=months, state="readonly")
    combobox_month.grid(row=0, column=1, padx=5, pady=5, sticky="we")


    # Label and Entry for Amount
    label_amount = tk.Label(payment_window, text="Monto:")
    label_amount.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_amount = tk.Entry(payment_window)
    entry_amount.grid(row=1, column=1, padx=5, pady=5, sticky="we")

    # Label and Text widget for Payment History in the payment window
    label_payment_history_popup = tk.Label(payment_window, text="Historial de Pagos:")
    label_payment_history_popup.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")

    payment_history_text_popup = tk.Text(payment_window, height=8, width=40)
    payment_history_text_popup.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nswe")

    # Populate payment history in the payment window
    cliente = clientes[selected_client_index]
    if cliente["Pagos"]:
        payment_history_text_popup.insert(tk.END, "Historial de Pagos:\n")
        for month, amount in cliente["Pagos"].items():
            payment_history_text_popup.insert(tk.END, f"- {month}: ${amount:.2f}\n")
    else:
        payment_history_text_popup.insert(tk.END, "No hay historial de pagos para este cliente.")


    def confirm_payment():
        """Confirms the payment and updates history display in the popup."""
        month = month_variable.get()
        amount = entry_amount.get()

        if month and amount:
            try:
                amount = float(amount)
                record_payment(selected_client_index, month, amount, payment_history_text_popup) # Pass text widget
                confirmation_label.config(text=f"Pago de {amount} registrado para {clientes[selected_client_index]['Nombre']} en {month}.")
                # Keep window open to see updated history
            except ValueError:
                confirmation_label.config(text="Monto inválido. Ingrese un número.")
        else:
            confirmation_label.config(text="Por favor, seleccione un mes e ingrese el monto.")


    # Confirm Payment Button
    button_confirm = tk.Button(payment_window, text="Confirmar Pago", command=confirm_payment)
    button_confirm.grid(row=4, column=0, columnspan=2, pady=10)

    # Configure grid weights for the payment window
    payment_window.grid_columnconfigure(1, weight=1)
    payment_window.grid_rowconfigure(3, weight=1) # Make history text area expandable


    # Wait until the payment window is closed
    payment_window.wait_window()


# Labels
label_nombre = tk.Label(root, text="Nombre:")
label_apellido = tk.Label(root, text="Apellido:")
label_direccion = tk.Label(root, text="Dirección:")
label_telefono = tk.Label(root, text="Teléfono:")
confirmation_label = tk.Label(root, text="")
# Removed payment history label and text widget from the main window

# Entry widgets
entry_nombre = tk.Entry(root)
entry_apellido = tk.Entry(root)
entry_direccion = tk.Entry(root)
entry_telefono = tk.Entry(root)

# Buttons
button_alta = tk.Button(root, text="Alta", command=dar_alta_cliente)
button_modificar = tk.Button(root, text="Modificar", command=modificar_cliente)
button_eliminar = tk.Button(root, text="Eliminar", command=eliminar_cliente) # Bind delete button
button_cobrar = tk.Button(root, text="Cobrar", command=open_payment_window) # Call the new function

# Listbox to display clients
listbox_clientes = tk.Listbox(root)

# Removed payment history text widget from the main window

# Arrange using grid
label_nombre.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_nombre.grid(row=0, column=1, padx=5, pady=5, sticky="we")
label_apellido.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_apellido.grid(row=1, column=1, padx=5, pady=5, sticky="we")
label_direccion.grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_direccion.grid(row=2, column=1, padx=5, pady=5, sticky="we")
label_telefono.grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_telefono.grid(row=3, column=1, padx=5, pady=5, sticky="we")

button_alta.grid(row=4, column=0, padx=5, pady=10, sticky="we")
button_modificar.grid(row=4, column=1, padx=5, pady=10, sticky="we")
button_eliminar.grid(row=4, column=2, padx=5, pady=10, sticky="we") # Position delete button as well
button_cobrar.grid(row=4, column=3, padx=5, pady=10, sticky="we") # Position the new button

confirmation_label.grid(row=5, column=0, columnspan=4, pady=10) # Adjust columnspan for the new button

listbox_clientes.grid(row=0, column=4, rowspan=6, padx=10, pady=5, sticky="nswe") # Position and stretch listbox, adjust column

# Removed grid positioning for payment history label and text widget from the main window


# Configure grid weights so the listbox column expands
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(4, weight=1) # Adjust for the new column
# Removed grid_rowconfigure for the payment history text area in the main window


# Bind the select event to the seleccionar_cliente function
listbox_clientes.bind("<<ListboxSelect>>", seleccionar_cliente)

# Call cargar_clientes when the application starts
cargar_clientes()
update_listbox() # Update the listbox after loading clients

# Call guardar_clientes when the window is closed
root.protocol("WM_DELETE_WINDOW", lambda: (guardar_clientes(), root.destroy()))

root.mainloop()