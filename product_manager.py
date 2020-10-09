import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import LabelFrame, Label, Button, Entry, Frame, Scrollbar, Style
from ttkthemes import themed_tk
from db import Database
from ConvertToExcel import convert, calc_profit
import os

if __name__ == '__main__':
    
    db = Database("store.db")


    def populate_list():
        product_list_listbox.delete(0, tk.END)
        for num, row in enumerate(db.fetch_all_rows()):
            string = ""
            for i in row:
                string = string + "  |  " + str(i)
            string = str(num + 1) + string
            product_list_listbox.insert(tk.END, string)


    # Function to bind listbox


    def select_item(event):
        try:
            global selected_item

            # To query the selection, use curselection method. It returns a list of item indexes
            index = product_list_listbox.curselection()[0]

            selected_item = product_list_listbox.get(index)

            selected_item = selected_item.split("  |  ")

            selected_item = db.fetch_by_product_id(selected_item[1])

            clear_input()

            product_id_entry.insert(0, selected_item[0][1])
            product_name_entry.insert(0, selected_item[0][2])
            customer_entry.insert(0, selected_item[0][3])
            seller_entry.insert(0, selected_item[0][4])
            cost_price_entry.insert(0, selected_item[0][5])
            selling_price_entry.insert(0, selected_item[0][6])
        except IndexError:
            pass


    # Create main window
    root = themed_tk.ThemedTk()
    root.set_theme("scidpurple")

    root.title("Product Manager")
    # root.geometry("640x480+10+10")
    # root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)


    entry_frame = LabelFrame(root, text="Enter Product Details")
    # Product Name
    product_name_var = tk.StringVar()
    product_name_label = Label(entry_frame, text="Product Name: ")
    product_name_label.grid(row=0, column=0, sticky="w", padx=10)
    product_name_entry = Entry(entry_frame, textvariable=product_name_var)
    product_name_entry.grid(row=0, column=1)

    # Product ID
    product_id_var = tk.StringVar()
    product_id_label = Label(entry_frame, text="Product ID: ")
    product_id_label.grid(row=1, column=0, sticky="w", padx=10)
    product_id_entry = Entry(entry_frame, textvariable=product_id_var)
    product_id_entry.grid(row=1, column=1)

    # Customer
    customer_var = tk.StringVar()
    customer_label = Label(entry_frame, text="Customer: ")
    customer_label.grid(row=0, column=2, sticky="w", padx=10)
    customer_entry = Entry(entry_frame, textvariable=customer_var)
    customer_entry.grid(row=0, column=3)

    # Seller
    seller_var = tk.StringVar()
    seller_label = Label(entry_frame, text="Seller: ")
    seller_label.grid(row=1, column=2, sticky="w", padx=10)
    seller_entry = Entry(entry_frame, textvariable=seller_var)
    seller_entry.grid(row=1, column=3)

    # Cost Price
    cost_price_var = tk.StringVar()
    cost_price_label = Label(entry_frame, text="Cost Price: ")
    cost_price_label.grid(row=0, column=4, sticky="w", padx=10)
    cost_price_entry = Entry(entry_frame, textvariable=cost_price_var)
    cost_price_entry.grid(row=0, column=5)

    # Selling Price
    selling_price_var = tk.StringVar()
    selling_price_label = Label(entry_frame, text="Selling Price: ")
    selling_price_label.grid(row=1, column=4, sticky="w", padx=10)
    selling_price_entry = Entry(entry_frame, textvariable=selling_price_var)
    selling_price_entry.grid(row=1, column=5)

    # ========================#

    # Product List
    # frame containing product listing and scrollbar
    listing_frame = Frame(root, borderwidth=2, relief="groove")
    product_list_listbox = tk.Listbox(listing_frame)
    product_list_listbox.grid(row=0, column=0, padx=10, pady=5, sticky="we")
    # binding list box to show selected items in the entry fields.
    product_list_listbox.bind("<<ListboxSelect>>", select_item)

    # Create ScrollBar
    scroll_bar = Scrollbar(listing_frame)
    scroll_bar.config(command=product_list_listbox.yview)
    scroll_bar.grid(row=0, column=1, sticky="ns")

    # Attach Scrollbar to Listbox
    product_list_listbox.config(yscrollcommand=scroll_bar.set)

    # =========================#

    # Create Statusbar using Label widget onto root
    statusbar_label = tk.Label(
        root, text="Status: ", bg="#ffb5c5", anchor="w", font=("Helvetica", 9)
    )
    statusbar_label.grid(row=3, column=0, sticky="we", padx=10)


    # ========================#

    # Button Functions


    def add_item():
        if (
            product_id_var.get() == ""
            or product_name_var.get() == ""
            or customer_var.get() == ""
            or seller_var.get() == ""
            or cost_price_var.get() == ""
            or selling_price_var.get() == ""
        ):
            messagebox.showerror(title="Required Fields", message="Please enter all fields")
            return

        db.insert(
            product_id_var.get(),
            product_name_var.get(),
            customer_var.get(),
            seller_var.get(),
            cost_price_var.get(),
            selling_price_var.get(),
        )
        clear_input()
        populate_list()
        statusbar_label["text"] = "Status: Product added successfully"


    def update_item():
        if (
            product_id_var.get() == ""
            or product_name_var.get() == ""
            or customer_var.get() == ""
            or seller_var.get() == ""
            or cost_price_var.get() == ""
            or selling_price_var.get() == ""
        ):
            messagebox.showerror(title="Required Fields", message="Please enter all fields")
            return
        db.update(
            selected_item[0][0],
            product_id_var.get(),
            product_name_var.get(),
            customer_var.get(),
            seller_var.get(),
            cost_price_var.get(),
            selling_price_var.get(),
        )
        populate_list()
        statusbar_label["text"] = "Status: Product updated successfully"


    def remove_item():
        db.remove(selected_item[0][1])
        clear_input()
        populate_list()
        statusbar_label["text"] = "Status: Product removed from the list successfully"


    def clear_input():
        product_id_entry.delete(0, tk.END)
        product_name_entry.delete(0, tk.END)
        customer_entry.delete(0, tk.END)
        seller_entry.delete(0, tk.END)
        cost_price_entry.delete(0, tk.END)
        selling_price_entry.delete(0, tk.END)


    def export_to_excel():
        convert()
        calc_profit()
        statusbar_label["text"] = f"Status: Excel file created in {os.getcwd()}"


    # Buttons
    button_frame = Frame(root, borderwidth=2, relief="groove")

    add_item_btn = Button(button_frame, text="Add item", command=add_item)
    add_item_btn.grid(row=0, column=0, sticky="we", padx=10, pady=5)

    remove_item_btn = Button(button_frame, text="Remove item", command=remove_item)
    remove_item_btn.grid(row=0, column=1, sticky="we", padx=10, pady=5)

    update_item_btn = Button(button_frame, text="Update item", command=update_item)
    update_item_btn.grid(row=0, column=2, sticky="we", padx=10, pady=5)

    clear_item_btn = Button(button_frame, text="Clear Input", command=clear_input)
    clear_item_btn.grid(row=0, column=3, sticky="we", padx=10, pady=5)

    export_to_excel_btn = Button(
        button_frame, text="Export To Excel", command=export_to_excel
    )
    export_to_excel_btn.grid(row=0, column=4, sticky="we", padx=10, pady=5)


    entry_frame.grid(row=0, column=0, sticky="we", padx=10, pady=5)
    button_frame.grid(row=1, column=0, sticky="we", padx=10, pady=5)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    button_frame.grid_columnconfigure(2, weight=1)
    button_frame.grid_columnconfigure(3, weight=1)
    button_frame.grid_columnconfigure(4, weight=1)
    listing_frame.grid(row=2, column=0, sticky="we", padx=10)
    listing_frame.grid_columnconfigure(0, weight=2)

    populate_list()

    root.mainloop()
