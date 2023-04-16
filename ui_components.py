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

        # Load the user profile and clients
        self.load_profile()
        self.load_clients()

        self.create_widgets()


    def create_widgets(self):
        # Labels and input fields for invoice data
        tk.Label(self, text="Client Name:").grid(row=0, column=0, sticky="w")
        self.client_name_label = tk.Label(self, text="")
        self.client_name_label.grid(row=0, column=1, sticky="w")

        tk.Label(self, text="Client Address:").grid(row=1, column=0, sticky="w")
        self.client_address_label = tk.Label(self, text="")
        self.client_address_label.grid(row=1, column=1, sticky="w")

        tk.Label(self, text="User Name:").grid(row=0, column=8, sticky="w")
        self.freelancer_name_label = tk.Label(self, text=self.freelancer_name_var.get())
        self.freelancer_name_label.grid(row=0, column=9, sticky="w")

        tk.Label(self, text="User Address:").grid(row=1, column=8, sticky="w")
        self.freelancer_address_label = tk.Label(self, text=self.freelancer_address_var.get())
        self.freelancer_address_label.grid(row=1, column=9, sticky="w")

        tk.Label(self, text="Umsatzsteuersatz:").grid(row=2, column=8, sticky="w")
        self.freelancer_address_label = tk.Label(self, text=self.umsatzsteuersatz_var.get())
        self.freelancer_address_label.grid(row=2, column=9, sticky="w")

        tk.Label(self, text="Invoice ID:").grid(row=4, column=0, sticky="w")
        self.invoice_id_var = tk.StringVar()
        tk.Entry(self, textvariable=self.invoice_id_var).grid(row=4, column=1, sticky="w")


        # Itemization table
        self.itemization_table = ttk.Treeview(self, columns=("Id", "Item", "Price", "Tax"))
        self.itemization_table.heading("Id", text="Item Id")
        self.itemization_table.heading("Item", text="Item Description")
        self.itemization_table.heading("Price", text="Price")
        self.itemization_table.heading("Tax", text="Tax")
        self.itemization_table.column("#0", width=0, stretch=tk.NO)  # Hide the first (empty) column
        self.itemization_table.grid(row=5, column=0, columnspan=2)

        # Additional fields for itemized invoice (items, prices, taxes, etc.)
        # ...

        tk.Button(self, text="Add Item", command=self.add_item).grid(row=6, column=0)

        # Remove item button
        tk.Button(self, text="Remove Item", command=self.remove_item).grid(row=6, column=1)

        # Button to generate the invoice
        tk.Button(self, text="Generate Invoice", command=self.generate_invoice).grid(row=7, columnspan=2)

        # Button to setup the user profile
        tk.Button(self, text="Setup Profile", command=self.setup_profile).grid(row=8, columnspan=2)

        # Button to add client profile
        tk.Button(self, text="Setup Client", command=self.setup_client).grid(row=8, column=4, columnspan=2)


    def add_item(self):
        item_dialog = tk.Toplevel(self)
        item_dialog.title("Add Item")

        # Entry for item name
        tk.Label(item_dialog, text="Item:").grid(row=0, column=0, sticky="w")
        item_name_var = tk.StringVar()
        tk.Entry(item_dialog, textvariable=item_name_var).grid(row=0, column=1, sticky="w")

        # Entry for item price
        tk.Label(item_dialog, text="Price:").grid(row=1, column=0, sticky="w")
        item_price_var = tk.DoubleVar()
        tk.Entry(item_dialog, textvariable=item_price_var).grid(row=1, column=1, sticky="w")

        # Entry for item tax
        tk.Label(item_dialog, text="Tax:").grid(row=2, column=0, sticky="w")
        item_tax_var = tk.DoubleVar()
        tk.Entry(item_dialog, textvariable=item_tax_var).grid(row=2, column=1, sticky="w")

        # Button to add item to the table
        tk.Button(item_dialog, text="Add", command=lambda: self.insert_item(item_name_var.get(), item_price_var.get(), item_tax_var.get(), item_dialog)).grid(row=3, columnspan=2)


    def insert_item(self, item_name, item_price, item_tax, item_dialog):

        self.itemization_table.insert('', 'end', values=(self.next_item_id, item_name, item_price, item_tax))
        self.next_item_id += 1  # Increment the next_item_id value
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

    def setup_client(self):
        ClientSetup(self)

    
    def load_clients(self):
        if os.path.exists('clients.json'):
            with open('clients.json', 'r') as clients_file:
                self.clients = json.load(clients_file)
                client_names = [client['Name'] for client in self.clients]
                self.client_dropdown['values'] = client_names
                if client_names:
                    self.client_dropdown.set(client_names[0])
                    self.update_client_labels()

    def update_client_labels(self):
        selected_client = [client for client in self.clients if client['Name'] == self.client_dropdown.get()][0]
        self.client_name_label.config(text=selected_client['Name'])
        self.client_address_label.config(text=selected_client['Address'])




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


class ClientSetup(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Client Setup")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Client Name:").grid(row=0, column=0, sticky="w")
        self.name_var = tk.StringVar()
        tk.Entry(self, textvariable=self.name_var).grid(row=0, column=1, sticky="w")

        tk.Label(self, text="Client Address:").grid(row=1, column=0, sticky="w")
        self.address_var = tk.StringVar()
        tk.Entry(self, textvariable=self.address_var).grid(row=1, column=1, sticky="w")

        tk.Button(self, text="Save Client", command=self.save_client).grid(row=2, columnspan=2)

    def save_client(self):
        client = {
            'Name': self.name_var.get(),
            'Address': self.address_var.get()
        }

        clients = []
        if os.path.exists('clients.json'):
            with open('clients.json', 'r') as clients_file:
                clients = json.load(clients_file)

        clients.append(client)

        with open('clients.json', 'w') as clients_file:
            json.dump(clients, clients_file)

        self.destroy()
