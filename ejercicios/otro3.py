import tkinter as tk
from tkinter import ttk
import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def guardar_clientes():
    """Saves the current list of clients to a text file."""
    try:
        with open("clientes.txt", "w") as f:
            for cliente in clientes:
                # Exclude 'Pagos' from the main clients.txt file as they are in separate files
                cliente_to_save = cliente.copy()
                if 'Pagos' in cliente_to_save: # Still include this check for robustness, though 'Pagos' shouldn't be in the list anymore
                    del cliente_to_save['Pagos']
                f.write(json.dumps(cliente_to_save) + "\n")
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
                    # 'Pagos' will be loaded from individual files when needed
                    clientes.append(cliente)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON from line: {line.strip()}")
        print("Clientes cargados correctamente.")
        # Print loaded data structure for debugging
        print("Loaded clients structure (excluding payments):", clientes)
    except FileNotFoundError:
        print("Archivo 'clientes.txt' no encontrado. No se cargaron clientes.")
    except IOError:
        print(f"Error al leer el archivo 'clientes.txt'.")
        if os.path.exists("clientes.txt"):
             try:
                 with open("clientes.txt", "w") as f:
                     f.write("")
                 print("Created empty 'clientes.txt' due to read error.")
             except IOError:
                 print("Could not create empty 'clientes.txt' after read error.")

def cargar_pagos_cliente(client):
    """Loads payment data for a specific client from their payment history file."""
    client_name = f"{client['Nombre']}_{client['Apellido']}".replace(" ", "_")
    payment_filename = f"{client_name}_pagos.txt"
    payments = []
    try:
        with open(payment_filename, "r") as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    try:
                        month, amount_str = parts
                        amount = float(amount_str)
                        payments.append({"Mes": month, "Monto": amount})
                    except ValueError:
                        print(f"Skipping line with invalid amount in {payment_filename}: {line.strip()}")
                else:
                    print(f"Skipping malformed line in {payment_filename}: {line.strip()}")
    except FileNotFoundError:
        print(f"Payment history file not found for {client['Nombre']} {client['Apellido']}: {payment_filename}")
        return [] # Return an empty list if the file doesn't exist
    except IOError:
        print(f"Error reading payment history file for {client['Nombre']} {client['Apellido']}: {payment_filename}")
        return [] # Return an empty list in case of other I/O errors

    return payments

def generate_receipt_pdf(client_name, month, amount):
    """Generates a PDF receipt for a payment."""
    try:
        filename = f"Recibo_{client_name.replace(' ', '_')}_{month}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        c.drawString(100, 750, "Recibo de Pago")
        c.drawString(100, 730, f"Cliente: {client_name}")
        c.drawString(100, 710, f"Mes Pagado: {month}")
        c.drawString(100, 690, f"Monto Pagado: ${amount:.2f}")
        c.save()
        print(f"Recibo generado: {filename}")
    except Exception as e:
        print(f"Error generating PDF: {e}")

# Removed record_monthly_payment as it's no longer needed

def calculate_monthly_total(month):
    """Calculates the total amount paid for a given month from the corresponding text file."""
    # This function might need to be adapted if monthly totals are calculated from individual client files
    # For now, keep the original logic which might be intended for a different overall totals file
    filename = f"pagos_{month}.txt"
    total_amount = 0.0
    try:
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    try:
                        amount = float(parts[2])
                        total_amount += amount
                    except ValueError:
                        print(f"Skipping line with invalid amount in {filename}: {line.strip()}")
                else:
                    print(f"Skipping malformed line in {filename}: {line.strip()}")
    except FileNotFoundError:
        return 0.0
    except IOError:
        print(f"Error reading file: {filename}. Returning current total.")

    return total_amount

def open_monthly_totals_window():
    """Opens a new window to display monthly totals."""
    monthly_totals_window = tk.Toplevel(root)
    monthly_totals_window.title("Totales Mensuales")
    monthly_totals_window.geometry("300x400")

    monthly_totals_text_popup = tk.Text(monthly_totals_window, height=15, width=30)
    monthly_totals_text_popup.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    scrollbar_totals = tk.Scrollbar(monthly_totals_text_popup)
    scrollbar_totals.pack(side=tk.RIGHT, fill=tk.Y)
    monthly_totals_text_popup.config(yscrollcommand=scrollbar_totals.set)
    scrollbar_totals.config(command=monthly_totals_text_popup.yview)


    months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    monthly_totals_text_popup.insert(tk.END, "Totales Mensuales:\n")
    for month in months:
        total = calculate_monthly_total(month)
        monthly_totals_text_popup.insert(tk.END, f"- {month}: ${total:.2f}\n")

    button_close = tk.Button(monthly_totals_window, text="Cerrar", command=monthly_totals_window.destroy)
    button_close.pack(pady=5)


root = tk.Tk()
root.title("Gestión de Clientes")
root.geometry("800x600")

clientes = []
selected_client_index = -1

def clear_fields():
    """Clears all entry fields."""
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_direccion.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    confirmation_label.config(text="")


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

    if not nombre or not apellido or not direccion or not telefono:
        confirmation_label.config(text="Por favor, complete todos los campos.")
        return

    if not telefono.isdigit():
        confirmation_label.config(text="El teléfono debe contener solo números.")
        return

    cliente = {
        "Nombre": nombre,
        "Apellido": apellido,
        "Dirección": direccion,
        "Teléfono": telefono
        # Payment history is stored in individual files, no need for a 'Pagos' key here
    }
    clientes.append(cliente)
    confirmation_label.config(text="Cliente dado de alta correctamente.")
    update_listbox()
    clear_fields()
    guardar_clientes()


def seleccionar_cliente(event):
    global selected_client_index
    try:
        selected_indices = listbox_clientes.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            selected_client_index = selected_index
            cliente = clientes[selected_index]
            clear_fields()
            entry_nombre.insert(0, cliente["Nombre"])
            entry_apellido.insert(0, cliente["Apellido"])
            entry_direccion.insert(0, cliente["Dirección"])
            entry_telefono.insert(0, cliente["Teléfono"])
            confirmation_label.config(text="")
        else:
            selected_client_index = -1
            clear_fields()

    except IndexError:
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

        if not nombre or not apellido or not direccion or not telefono:
            confirmation_label.config(text="Por favor, complete todos los campos para modificar.")
            return

        if not telefono.isdigit():
            confirmation_label.config(text="El teléfono debe contener solo números.")
            return

        clientes[selected_client_index]["Nombre"] = nombre
        clientes[selected_client_index]["Apellido"] = apellido
        clientes[selected_client_index]["Dirección"] = direccion
        clientes[selected_client_index]["Teléfono"] = telefono
        confirmation_label.config(text="Cliente modificado correctamente.")
        update_listbox()
        clear_fields()
        listbox_clientes.selection_clear(0, tk.END)
        selected_client_index = -1
        guardar_clientes()
    else:
        confirmation_label.config(text="Seleccione un cliente para modificar.")

def eliminar_cliente():
    """Removes the selected client from the list."""
    global selected_client_index
    if selected_client_index != -1:
        # Construct the filename for the client's payment history
        client_name = f"{clientes[selected_client_index]['Nombre']}_{clientes[selected_client_index]['Apellido']}".replace(" ", "_")
        payment_filename = f"{client_name}_pagos.txt"

        del clientes[selected_client_index]
        confirmation_label.config(text="Cliente eliminado correctamente.")
        update_listbox()
        clear_fields()
        listbox_clientes.selection_clear(0, tk.END)
        selected_client_index = -1
        guardar_clientes()

        # Optionally, remove the client's payment history file
        if os.path.exists(payment_filename):
            try:
                os.remove(payment_filename)
                print(f"Removed payment history file: {payment_filename}")
            except OSError as e:
                print(f"Error removing payment history file {payment_filename}: {e}")
    else:
        confirmation_label.config(text="Seleccione un cliente para eliminar.")


def record_payment(client_index, month, amount, payment_history_text_widget):
    """Records a payment for a given client and month and updates the history display."""
    if client_index != -1 and client_index < len(clientes):
        cliente = clientes[client_index]
        client_name = f"{cliente['Nombre']}_{cliente['Apellido']}".replace(" ", "_")
        payment_filename = f"{client_name}_pagos.txt"

        # Print values received by record_payment
        print(f"Inside record_payment - Received month: {month}, amount: {amount}")

        try:
            # Print values about to be written to the file
            print(f"Inside record_payment - About to write to {payment_filename}: Month={month}, Amount={amount:.2f}")
            with open(payment_filename, "a") as f:
                f.write(f"{month},{amount:.2f}\n")
            print(f"Pago registrado en {payment_filename}")

            # Read and display updated payment history from the file
            payment_history_text_widget.delete("1.0", tk.END)
            payment_history_text_widget.insert(tk.END, "Historial de Pagos:\n")
            try:
                with open(payment_filename, "r") as f:
                    for line in f:
                        parts = line.strip().split(',')
                        if len(parts) == 2:
                            p_month, p_amount = parts
                            payment_history_text_widget.insert(tk.END, f"- {p_month}: ${float(p_amount):.2f}\n")
                        else:
                             print(f"Skipping malformed line in {payment_filename}: {line.strip()}")
            except FileNotFoundError:
                payment_history_text_widget.insert(tk.END, "No hay historial de pagos para este cliente.")
            except IOError:
                 payment_history_text_widget.insert(tk.END, "Error al leer el historial de pagos.")


            # Generate PDF receipt after successful payment recording
            generate_receipt_pdf(f"{cliente['Nombre']} {cliente['Apellido']}", month, amount)

        except IOError:
            print(f"Error al registrar el pago en {payment_filename}")
            confirmation_label.config(text=f"Error al registrar el pago en {payment_filename}.")
        except ValueError:
             confirmation_label.config(text="Monto inválido. Ingrese un número.")
        except Exception as e: # Catch other potential errors during recording
             print(f"An unexpected error occurred during payment recording: {e}")
             confirmation_label.config(text=f"Error al registrar pago: {e}")


def open_payment_window():
    """Opens a new window to enter payment details and display history."""
    if selected_client_index == -1:
        confirmation_label.config(text="Seleccione un cliente para registrar un pago.")
        return

    payment_window = tk.Toplevel(root)
    payment_window.title("Registrar Pago")
    payment_window.geometry("400x300")

    payment_window.grab_set()

    label_month = tk.Label(payment_window, text="Mes:")
    label_month.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    month_variable = tk.StringVar(payment_window)
    month_variable.set(months[0]) # default value
    combobox_month = ttk.Combobox(payment_window, textvariable=month_variable, values=months, state="readonly")
    combobox_month.grid(row=0, column=1, padx=5, pady=5, sticky="we")


    label_amount = tk.Label(payment_window, text="Monto:")
    label_amount.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_amount = tk.Entry(payment_window)
    entry_amount.grid(row=1, column=1, padx=5, pady=5, sticky="we")

    label_payment_history_popup = tk.Label(payment_window, text="Historial de Pagos:")
    label_payment_history_popup.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")

    payment_history_text_popup = tk.Text(payment_window, height=8, width=40)
    payment_history_text_popup.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nswe")

    # Load and display payment history from the client-specific file when opening the window
    cliente = clientes[selected_client_index]
    client_name = f"{cliente['Nombre']}_{cliente['Apellido']}".replace(" ", "_")
    payment_filename = f"{client_name}_pagos.txt"

    payment_history_text_popup.delete("1.0", tk.END)
    payment_history_text_popup.insert(tk.END, "Historial de Pagos:\n")
    try:
        with open(payment_filename, "r") as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    p_month, p_amount = parts
                    payment_history_text_popup.insert(tk.END, f"- {p_month}: ${float(p_amount):.2f}\n")
                else:
                     print(f"Skipping malformed line in {payment_filename}: {line.strip()}")
    except FileNotFoundError:
        payment_history_text_popup.insert(tk.END, "No hay historial de pagos para este cliente.")
    except IOError:
        payment_history_text_popup.insert(tk.END, "Error al leer el historial de pagos.")


    def confirm_payment():
        """Confirms the payment and updates history display in the popup."""
        # Retrieve values from the widgets in the current payment window instance
        month = combobox_month.get()
        amount = entry_amount.get()

        # Add print statements to see the retrieved values
        print(f"Retrieved month in confirm_payment: {month}")
        print(f"Retrieved amount in confirm_payment: {amount}")


        if month and amount:
            try:
                amount = float(amount)
                # Pass the actual text widget to record_payment
                record_payment(selected_client_index, month, amount, payment_history_text_popup)
                confirmation_label.config(text=f"Pago de {amount} registrado para {clientes[selected_client_index]['Nombre']} en {month}.")
                # Keep window open to see updated history
            except ValueError:
                    confirmation_label.config(text="Monto inválido. Ingrese un número.")
            except Exception as e:
                 print(f"An unexpected error occurred during payment recording: {e}")
                 confirmation_label.config(text=f"Error al registrar pago: {e}")

        else:
            confirmation_label.config(text="Por favor, seleccione un mes e ingrese el monto.")


    button_confirm = tk.Button(payment_window, text="Confirmar Pago", command=confirm_payment)
    button_confirm.grid(row=4, column=0, columnspan=2, pady=10)

    payment_window.grid_columnconfigure(1, weight=1)
    payment_window.grid_rowconfigure(3, weight=1)

    payment_window.wait_window()


# Labels
label_nombre = tk.Label(root, text="Nombre:")
label_apellido = tk.Label(root, text="Apellido:")
label_direccion = tk.Label(root, text="Dirección:")
label_telefono = tk.Label(root, text="Teléfono:")
confirmation_label = tk.Label(root, text="")

# Entry widgets
entry_nombre = tk.Entry(root)
entry_apellido = tk.Entry(root)
entry_direccion = tk.Entry(root)
entry_telefono = tk.Entry(root)

# Buttons
button_alta = tk.Button(root, text="Alta", command=dar_alta_cliente)
button_modificar = tk.Button(root, text="Modificar", command=modificar_cliente)
button_eliminar = tk.Button(root, text="Eliminar", command=eliminar_cliente)
button_cobrar = tk.Button(root, text="Cobrar", command=open_payment_window)
button_ver_totales = tk.Button(root, text="Ver Totales Mensuales", command=open_monthly_totals_window)

# Listbox to display clients
listbox_clientes = tk.Listbox(root)

# Add scrollbar to the listbox
scrollbar_clientes = tk.Scrollbar(root, orient=tk.VERTICAL)
listbox_clientes.config(yscrollcommand=scrollbar_clientes.set) # Corrected line
scrollbar_clientes.config(command=listbox_clientes.yview) # Corrected line

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
button_eliminar.grid(row=4, column=2, padx=5, pady=10, sticky="we")
button_cobrar.grid(row=4, column=3, padx=5, pady=10, sticky="we")
button_ver_totales.grid(row=5, column=0, columnspan=4, padx=5, pady=10, sticky="we")

confirmation_label.grid(row=6, column=0, columnspan=4, pady=10)

listbox_clientes.grid(row=0, column=4, rowspan=7, padx=(10, 0), pady=5, sticky="nswe")
scrollbar_clientes.grid(row=0, column=5, rowspan=7, padx=(0, 10), pady=5, sticky="nswe")


root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(4, weight=1)
root.grid_columnconfigure(5, weight=0)
root.grid_rowconfigure(6, weight=1)


listbox_clientes.bind("<<ListboxSelect>>", seleccionar_cliente)

cargar_clientes()
update_listbox()

root.protocol("WM_DELETE_WINDOW", lambda: (guardar_clientes(), root.destroy()))

root.mainloop()