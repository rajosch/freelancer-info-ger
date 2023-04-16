import tkinter as tk
from tkinter import ttk, messagebox
from utils import save_invoice_to_csv, save_invoice_to_pdf

class InvoiceApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Invoice Generator")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")
        self.create_widgets()

    def create_widgets(self):
        # Labels and input fields for invoice data
        tk.Label(self, text="Client Name:").grid(row=0, column=0, sticky="w")
        self.client_name_var = tk.StringVar()
        tk.Entry(self, textvariable=self.client_name_var).grid(row=0, column=1, sticky="w")

        tk.Label(self, text="Client Address:").grid(row=1, column=0, sticky="w")
        self.client_address_var = tk.StringVar()
        tk.Entry(self, textvariable=self.client_address_var).grid(row=1, column=1, sticky="w")

        tk.Label(self, text="Freelancer Name:").grid(row=2, column=0, sticky="w")
        self.freelancer_name_var = tk.StringVar()
        tk.Entry(self, textvariable=self.freelancer_name_var).grid(row=2, column=1, sticky="w")

        tk.Label(self, text="Freelancer Address:").grid(row=3, column=0, sticky="w")
        self.freelancer_address_var = tk.StringVar()
        tk.Entry(self, textvariable=self.freelancer_address_var).grid(row=3, column=1, sticky="w")

        tk.Label(self, text="Invoice ID:").grid(row=4, column=0, sticky="w")
        self.invoice_id_var = tk.StringVar()
        tk.Entry(self, textvariable=self.invoice_id_var).grid(row=4, column=1, sticky="w")


        # Itemization table
        self.itemization_table = ttk.Treeview(self, columns=("Item", "Price", "Tax"))
        self.itemization_table.heading("Item", text="Item")
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
        self.itemization_table.insert('', 'end', values=(item_name, item_price, item_tax))
        item_dialog.destroy()


    def remove_item(self):
        selected_item = self.itemization_table.selection()
        if selected_item:
            self.itemization_table.delete(selected_item)

    def generate_invoice(self):
        # Extract data from input fields
        client_name = self.client_name_var.get()
        client_address = self.client_address_var.get()
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
