#PLAN
#Write the stockmanagement
#Code stock alaerts for low stock and expiry
#Add a section for value calculations as well as transaction history

import tkinter as tk
from tkinter import filedialog
import json

root=tk.Tk()
root.title("SmartStock")
root.geometry("420x480")

default_font = ("Arial", 12)
label_font = ("Arial", 11)

#Status Label
status=tk.Label(root, text="", font=("Arial",10))
status.pack()
# base class
class Product:
    def __init__(self, id, name, price, quantity):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def low_stock_warning(self):
        if int(self.quantity) <= 5:
            target = stock_list.size() - 1
            stock_list.itemconfig(target, bg="red")

#subclass - inherits all attributes from base class, and adds extra attributes unique to this class
class Perishable(Product):
    def __init__(self, id, name, price, quantity, expiryDate, storageTemp):
        super().__init__(id, name, price, quantity)
        self.expiryDate = expiryDate
        self.storageTemp = storageTemp
        

#subclass
class Electronic(Product):
    def __init__(self, id, name, price, quantity, warrantyPeriod, powerUsage):
        super().__init__(id, name, price, quantity)
        self.warrantyPeriod = warrantyPeriod
        self.powerUsage = powerUsage

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

#Stock add function with an alert for empty input box- Angel
#Overhauled add function - Thomas:

def add_stock_window():
    #Creates a new window
    add_window = tk.Toplevel(root)
    add_window.title("Add Stock")
    add_window.geometry("420x480")
    global opt
    opt = tk.StringVar(add_window)
    opt.set("Default Product")

    class DefaultOptions(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            global stock_name
            stock_name = tk.Entry(self, width=32, font=default_font)
            global stock_price
            stock_price = tk.Entry(self, width=32, font=default_font)
            global stock_quantity
            stock_quantity = tk.Entry(self, width=32, font=default_font)
            tk.Label(
                self, 
                text="Name of item",
                font=label_font).pack(pady=3)
            stock_name.pack(pady=3)
            tk.Label(
                self, 
                text="Price of item",
                font=label_font).pack(pady=3)
            stock_price.pack(pady=3)
            tk.Label(
                self, 
                text="Quantity of item",
                font=label_font).pack(pady=3)
            stock_quantity.pack(pady=3)

    class PerishableOptions(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            tk.Label(
                self,
                text="Expiry Date",
                font=label_font
            ).pack(pady=3)
            global stock_expiry
            stock_expiry = tk.Entry(self, width=32, font=default_font)
            stock_expiry.pack(pady=3)
            tk.Label(
                self,
                text="Storage Temperature",
                font=label_font
            ).pack(pady=3)
            global stock_temp
            stock_temp = tk.Entry(self, width=32, font=default_font)
            stock_temp.pack(pady=3)

    class ElectronicOptions(tk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            tk.Label(
                self,
                text="Warranty Period", 
                font=label_font
            ).pack(pady=3)
            global stock_warranty
            stock_warranty = tk.Entry(self, width=32, font=default_font)
            stock_warranty.pack(pady=3)
            tk.Label(
                self,
                text="Power Usage",
                font=label_font
            ).pack(pady=3)
            global stock_power
            stock_power = tk.Entry(self, width=32, font=default_font)
            stock_power.pack(pady=3)

    def update_options(selected):
        if selected == "Perishable Product":
            perishable_opts.pack()
            electronic_opts.pack_forget()
        elif selected == "Electronic Product":
            electronic_opts.pack()
            perishable_opts.pack_forget()
        else:
            electronic_opts.pack_forget()
            perishable_opts.pack_forget()
        

    def close_add_stock_window():
        add_window.destroy()

    perishable_opts = PerishableOptions(add_window)
    electronic_opts = ElectronicOptions(add_window)

    tk.Label(
        add_window, 
        text="Add a new item",
        font=label_font).pack(pady=(15,5))
    
    tk.Label(
        add_window,
        text="Select a Product Type",
        font=label_font
    ).pack(pady=3)

    #Allows user to choose which type of product they want to add
    options = ["Default Product", "Perishable Product", "Electronic Product"]
    stock_type = tk.OptionMenu(add_window, opt, *options, command=update_options)
    stock_type.pack()

    DefaultOptions(add_window).pack()

    add_button = tk.Button(add_window, text="Add Stock", command=add_stock).pack(side="bottom",pady=3)
    
    #Runs the rest of the add_stock function on button click, then closes the window

    add_window.mainloop()

def add_stock():
    #Now the only purpose of add_stock is to create a new object, using data from the "add_stock_window" function
    #Core attributes
    item_type = opt.get().strip()
    item_name = stock_name.get().strip()
    item_price = stock_price.get().strip()
    item_quantity = stock_quantity.get().strip()
    
     #please finish this function - Thomas
    if not item_name:
        status.config(text="Please enter a stock item name", fg= "red")
        stock_name.focus_set()
        return
    if not item_price:
        status.config(text="Please enter a stock item price.", fg= "red")
        stock_price.focus_set()
        return
    if not item_quantity:
        status.config(text="Please enter a stock item quantity.", fg= "red")
        stock_quantity.focus_set()
        return
    #Creates a new instance, depending on which (sub)class the user chose in the "add_stock_window" function
    if item_type == "Default Product":
        stock = Product("TEMPORARY_ID",item_name,item_price,item_quantity)
        stock_list.insert(tk.END, (f"Product, {stock.id}, {stock.name}, {stock.price}, {stock.quantity}"))

    elif item_type == "Perishable Product":
        #Perishable attributes
        item_expiry = stock_expiry.get().strip()
        item_temp = stock_temp.get().strip()
        if not item_expiry:
            status.config(text="Please enter a stock item expiry date.", fg= "red")
            stock_expiry.focus_set()
            return
        if not item_temp:
            status.config(text="Please enter a storage temperature.", fg= "red")
            stock_temp.focus_set()
            return
        stock = Perishable("TEMPORARY_ID",item_name,item_price,item_quantity,item_expiry,item_temp)
        stock_list.insert(tk.END, (f"Perishable, {stock.id}, {stock.name}, {stock.price}, {stock.quantity}, {stock.expiryDate}, {stock.storageTemp}"))

    elif item_type == "Electronic Product":
        #Electronic attributes
        item_warranty = stock_warranty.get().strip()
        power_usage = stock_power.get().strip()
        if not item_warranty:
            status.config(text="Please enter a stock item warranty period.", fg= "red")
            stock_warranty.focus_set()
            return
        if not power_usage:
            status.config(text="Please enter a stock item power usage.", fg= "red")
            stock_power.focus_set()
            return
        stock = Electronic("TEMPORARY_ID",item_name,item_price,item_quantity,item_warranty,power_usage)
        stock_list.insert(tk.END, (f"Electronic, {stock.id}, {stock.name}, {stock.price}, {stock.quantity}, {stock.warrantyPeriod}, {stock.powerUsage}"))

    stock.low_stock_warning()
    status.config(text="Stock Added!", fg="green")
   
#Button for adding stock to the list.
    
add_window_button = tk.Button(btn_frame, text="Add Stock", command=add_stock_window).grid(row=0, column=0, padx=3)

#Listbox to display stock items
stock_list = tk.Listbox(root, width=40, height=10, font=default_font)
stock_list.pack(pady=10)


#Function to remove selected stock from the list (Angel)
def remove_stock():
    selected = stock_list.curselection()
    if not selected:
        status.config(text="Please select a stock item to remove from the list.",
                      fg= "red")
        return
    stock_list.delete(selected)
    status.config(text="Stock has been removed from the list.",
                  fg="green")
    
#Button to remove selected stock from list
remove_button = tk.Button(btn_frame, text= "Remove stock", command=remove_stock) .grid(row=0, column=1, padx=3)  

#function for editing stock here



#function to display low stock warning here
# angel suggests utilising the status.config 


#function to display warning for expiring stock here
#angel suggests utilising the status.config 


#function for total cost of stock here



#function for transaction history logs here



#separate section for the 'health' of the stock summary here


# file persistence and logging - Kostya

def saveToFile():
    invList = list(stock_list.get(0, tk.END))
    
    saveLocation = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        title="Save Inventory to File"
    )

    if len(invList) == 0:
        status.config(text="Inventory is currently empty. Please add stock.", fg= "red")
        return

    invData = json.dumps(invList, indent=4)
    with open("inventory.json", "w") as inv:
        inv.write(invData)

def loadFromFile():
    pass

def checkLogs():
    pass

save_button = tk.Button(btn_frame, text= "Save to file", command=saveToFile) .grid(row=2, column=0, padx=3)
load_button = tk.Button(btn_frame, text= "Load from file", command=loadFromFile) .grid(row=2, column=1, padx=3)
check_logs = tk.Button(btn_frame, text= "Transaction history", command=checkLogs) .grid(row=3, column=0, padx=3)


#main loop to run the SmartSTock application to view stock.
root.mainloop()