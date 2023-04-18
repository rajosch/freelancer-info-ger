import tkinter as tk
from tkinter import ttk, messagebox
from utils import save_invoice_to_csv, save_invoice_to_pdf
import configparser
import json
import os


class InvoiceApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Invoice Generator")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")
        self.next_item_id = 1 

        # Initialize StringVars for the freelancer's information
        self.freelancer_name_var = tk.StringVar()
        self.freelancer_address_var = tk.StringVar()
        self.umsatzsteuersatz_var = tk.StringVar()

        # Initialize StringVars for the client's information
        self.client_dropdown = ttk.Combobox(self)
        self.client_dropdown.grid(row=0, column=1, sticky="w")

        self.client_address_var = tk.StringVar()
        self.client_currency_var = tk.StringVar()
        self.client_english_var = tk.StringVar()
        self.client_umsatzsteuer_var = tk.StringVar()


        # Load the user profile and clients
        self.load_profile()
        self.create_clients_file_if_not_exists()

        self.create_widgets()
        self.clients = {}
        self.load_clients()


    def create_widgets(self):

        h1_font = ("Arial", 16, "bold")

        # Labels and input fields for invoice data
        tk.Label(self, text="Kunde", font=h1_font).grid(row=0, column=0, sticky="w")

        tk.Label(self, text="Name:").grid(row=1, column=0, sticky="w")
        self.client_dropdown.grid(row=1, column=1, sticky="w")
        self.client_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_client_labels())

        tk.Label(self, text="Addresse:").grid(row=2, column=0, sticky="w")
        self.client_address_label = tk.Label(self, text=self.client_address_var.get())
        self.client_address_label.grid(row=2, column=1, sticky="w")

        tk.Label(self, text="Währung:").grid(row=3, column=0, sticky="w")
        self.client_currency_label = tk.Label(self, text=self.client_currency_var.get())
        self.client_currency_label.grid(row=3, column=1, sticky="w")

        tk.Label(self, text="English:").grid(row=4, column=0, sticky="w")
        self.client_english_label = tk.Label(self, text=self.client_english_var.get())
        self.client_english_label.grid(row=4, column=1, sticky="w")

        tk.Label(self, text="Umsatzsteuer:").grid(row=5, column=0, sticky="w")
        self.client_umsatzsteuer_label = tk.Label(self, text=self.client_umsatzsteuer_var.get())
        self.client_umsatzsteuer_label.grid(row=5, column=1, sticky="w")

        
        tk.Label(self, text="Profil", font=h1_font).grid(row=0, column=10, sticky="w")

        tk.Label(self, text="Name:").grid(row=1, column=10, sticky="w")
        self.freelancer_name_label = tk.Label(self, text=self.freelancer_name_var.get())
        self.freelancer_name_label.grid(row=1, column=11, sticky="w")

        tk.Label(self, text="User Address:").grid(row=2, column=10, sticky="w")
        self.freelancer_address_label = tk.Label(self, text=self.freelancer_address_var.get())
        self.freelancer_address_label.grid(row=2, column=11, sticky="w")

        tk.Label(self, text="Umsatzsteuersatz (%):").grid(row=3, column=10, sticky="w")
        self.umsatzsteuersatz_label = tk.Label(self, text=self.umsatzsteuersatz_var.get())
        self.umsatzsteuersatz_label.grid(row=3, column=11, sticky="w")

        tk.Label(self, text="Invoice ID:").grid(row=19, column=4, sticky="w")
        self.invoice_id_var = tk.StringVar()
        tk.Entry(self, textvariable=self.invoice_id_var).grid(row=19, column=5, sticky="w")


        # Itemization table
        self.itemization_table = ttk.Treeview(self, columns=("Id", "Item", "Hours", "Hourly", "Price"))
        self.itemization_table.heading("Id", text="Item Id")
        self.itemization_table.heading("Item", text="Item Description")
        self.itemization_table.heading("Hours", text="Hours")
        self.itemization_table.heading("Hourly", text="Hourly")
        self.itemization_table.heading("Price", text="Price")
        self.itemization_table.column("#0", width=0, stretch=tk.NO)  # Hide the first (empty) column
        self.itemization_table.grid(row=20, column=4, columnspan=2)

        # Additional fields for itemized invoice (items, prices, taxes, etc.)
        # ...

        tk.Button(self, text="Add Item", command=self.add_item).grid(row=21, column=4)

        # Remove item button
        tk.Button(self, text="Remove Item", command=self.remove_item).grid(row=21, column=5)

        # Button to generate the invoice
        tk.Button(self, text="Generate Invoice", command=self.generate_invoice).grid(row=22, column=4, columnspan=2)

        # Button to setup the user profile
        tk.Button(self, text="Profil Setup", command=self.setup_profile).grid(row=5, column=11, columnspan=2)

        # Button to add client profile
        tk.Button(self, text="Add Client", command=self.add_client).grid(row=6, column=1, columnspan=2)

    def add_item(self):
        item_dialog = tk.Toplevel(self)
        item_dialog.title("Add Item")

        # Entry for item name
        tk.Label(item_dialog, text="Description:").grid(row=0, column=0, sticky="w")
        item_description_var = tk.StringVar()
        tk.Entry(item_dialog, textvariable=item_description_var).grid(row=0, column=1, sticky="w")

        # Entry for hours
        tk.Label(item_dialog, text="Hours:").grid(row=1, column=0, sticky="w")
        item_hours_var = tk.DoubleVar()
        tk.Entry(item_dialog, textvariable=item_hours_var).grid(row=1, column=1, sticky="w")

        # Entry for hourly
        tk.Label(item_dialog, text="Hourly:").grid(row=2, column=0, sticky="w")
        item_hourly_var = tk.DoubleVar()
        tk.Entry(item_dialog, textvariable=item_hourly_var).grid(row=2, column=1, sticky="w")

        # Button to add item to the table
        tk.Button(item_dialog, text="Add", command=lambda: self.insert_item(item_description_var.get(), item_hours_var.get(), item_hourly_var.get(), item_dialog)).grid(row=3, columnspan=2)


    def insert_item(self, item_description, item_hours, item_hourly, item_dialog):
        item_price = item_hourly * item_hours
        self.itemization_table.insert('', 'end', values=(self.next_item_id, item_description, item_hours, item_hourly, item_price))
        self.next_item_id += 1
        item_dialog.destroy()


    def remove_item(self):
        selected_item = self.itemization_table.selection()
        if selected_item:
            self.itemization_table.delete(selected_item)

    def generate_invoice(self):
        # Extract data from input fields
        client_name = self.client_dropdown.get()
        client_address = [client['Address'] for client in self.clients if client['Name'] == client_name][0]
        
        freelancer_name = self.freelancer_name_var.get()
        freelancer_address = self.freelancer_address_var.get()
        invoice_id = self.invoice_id_var.get()

         # Extract itemization data
        itemized_data = []
        for row in self.itemization_table.get_children():
            item = self.itemization_table.item(row)["values"]
            itemized_data.append(item)

        # Additional data extraction for itemized invoice (items, prices, taxes, etc.)
        # ...

        # Create and save the invoice as a CSV and PDF files
        save_invoice_to_csv(client_name, client_address, freelancer_name, freelancer_address, invoice_id, itemized_data)
        save_invoice_to_pdf(client_name, client_address, freelancer_name, freelancer_address, invoice_id, itemized_data)

        # Display a success message
        messagebox.showinfo("Invoice Created", "Invoice has been created and saved successfully.")


    def setup_profile(self):
        ProfileSetup(self)
    
    def load_profile(self):
        config = configparser.ConfigParser()
        config.read('profile.ini')
        if 'Profile' in config.sections():
            self.freelancer_name_var.set(config['Profile']['Name'])
            self.freelancer_address_var.set(config['Profile']['Address'])
            self.umsatzsteuersatz_var.set(config['Profile']['Umsatzsteuer'])

    def add_client(self):
        client_setup = ClientSetup(parent=self)
        client_setup.protocol("WM_DELETE_WINDOW", lambda: self.close_client_setup(client_setup))

    def close_client_setup(self, client_setup):
        self.load_clients()
        client_setup.destroy()

    def create_clients_file_if_not_exists(self):
        if not os.path.exists('clients.json'):
            with open('clients.json', 'w') as clients_file:
                json.dump({}, clients_file)


    
    def load_clients(self):
        if not os.path.exists('clients.json'):
            return

        with open('clients.json', 'r') as file:
            self.clients = json.load(file)

        client_names = list(self.clients.keys())
        self.client_dropdown['values'] = client_names


    def update_client_labels(self):
        selected_client = self.client_dropdown.get()
        client_data = self.clients[selected_client]

        client_address = client_data.get("address", "")
        self.client_address_var.set(client_address)
        self.client_address_label.config(text=self.client_address_var.get())

        client_currency = client_data.get("currency", "")
        self.client_currency_var.set(client_currency)
        self.client_currency_label.config(text=self.client_currency_var.get())

        client_english = client_data.get("english", "")
        self.client_english_var.set(client_english)
        self.client_english_label.config(text=self.client_english_var.get())

        client_umsatzsteuer = client_data.get("umsatzsteuer", "")
        self.client_umsatzsteuer_var.set(client_umsatzsteuer)
        self.client_umsatzsteuer_label.config(text=self.client_umsatzsteuer_var.get())





class ProfileSetup(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Profile Setup")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_var = tk.StringVar()
        tk.Entry(self, textvariable=self.name_var).grid(row=0, column=1, sticky="w")

        tk.Label(self, text="Address:").grid(row=1, column=0, sticky="w")
        self.address_var = tk.StringVar()
        tk.Entry(self, textvariable=self.address_var).grid(row=1, column=1, sticky="w")

        tk.Label(self, text="Umsatzsteuer (%):").grid(row=2, column=0, sticky="w")
        self.tax_var = tk.DoubleVar()
        tk.Entry(self, textvariable=self.tax_var).grid(row=2, column=1, sticky="w")

        tk.Button(self, text="Save Profile", command=self.save_profile).grid(row=3, columnspan=2)

    def save_profile(self):
        config = configparser.ConfigParser()
        config['Profile'] = {
            'Name': self.name_var.get(),
            'Address': self.address_var.get(),
            'Umsatzsteuer': self.tax_var.get()
        }
        with open('profile.ini', 'w') as configfile:
            config.write(configfile)
        self.destroy()

        # Update the user information in the main app
        self.master.load_profile()
        self.master.freelancer_name_label.config(text=self.master.freelancer_name_var.get())
        self.master.freelancer_address_label.config(text=self.master.freelancer_address_var.get())
        self.master.umsatzsteuersatz_label.config(text=self.master.umsatzsteuersatz_var.get())



class ClientSetup(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.title("Client Setup")
        
        # Define the client name and address entry widgets
        tk.Label(self, text="Name:").grid(row=0, column=0, sticky="w")
        self.name_var = tk.StringVar()
        self.client_name_entry = tk.Entry(self, textvariable=self.name_var)
        self.client_name_entry.grid(row=0, column=1, sticky="w")

        tk.Label(self, text="Addresse:").grid(row=1, column=0, sticky="w")
        self.address_var = tk.StringVar()
        self.client_address_entry = tk.Entry(self, textvariable=self.address_var)
        self.client_address_entry.grid(row=1, column=1, sticky="w")

        tk.Label(self, text="Währung:").grid(row=2, column=0, sticky="w")
        self.currency_var = tk.StringVar()
        self.currency_combobox = ttk.Combobox(self, textvariable=self.currency_var, values=["€", "$"])
        self.currency_combobox.current(0) # set the default value to €
        self.currency_combobox.grid(row=2, column=1, sticky="w")

        self.english_var = tk.BooleanVar()
        self.client_checkbox = tk.Checkbutton(self, text="Englisch:", variable=self.english_var)
        self.client_checkbox.grid(row=3, column=0, sticky="w")

        self.umsatzsteuer_var = tk.BooleanVar()
        self.client_checkbox = tk.Checkbutton(self, text="Umsatzsteuer hinzufügen (bei deutschen Kunden):", variable=self.umsatzsteuer_var)
        self.client_checkbox.grid(row=4, column=0, sticky="w")
        
        
        tk.Button(self, text="Save", command=self.save_client).grid(row=5, columnspan=2)

    def save_client(self):
        client_name = self.name_var.get()
        client_address = self.address_var.get()
        client_currency = self.currency_var.get()
        client_english = self.english_var.get()
        client_umsatzsteuer = self.umsatzsteuer_var.get()
        if not client_name or not client_address:
            messagebox.showerror("Error", "Please enter client name and address.")
            return

        client = {
            "name": client_name,
            "address": client_address,
            "currency": client_currency,
            "english": client_english,
            "umsatzsteuer": client_umsatzsteuer

        }

        if os.path.exists('clients.json'):
            with open('clients.json', 'r') as file:
                clients = json.load(file)
        else:
            clients = {}

        clients[client_name] = client

        with open('clients.json', 'w') as file:
            json.dump(clients, file)

        self.parent.load_clients()
        self.destroy()

