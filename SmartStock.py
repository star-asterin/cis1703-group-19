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

tk.Label(
    root, 
    text="Add a new item",
    font=("Arial",11)).pack(pady=(15,5))

#User input
stock_name = tk.Entry(root, width=32, font=("Arial", 12))
stock_price = tk.Entry(root, width=32, font=("Arial", 12))
stock_quantity = tk.Entry(root, width=32, font=("Arial", 12))
tk.Label(
    root, 
    text="Name of item",
    font=("Arial",11)).pack(pady=(3))
stock_name.pack(pady=3)
tk.Label(
    root, 
    text="Price of item",
    font=("Arial",11)).pack(pady=(3))
stock_price.pack(pady=3)
tk.Label(
    root, 
    text="Quatity of item",
    font=("Arial",11)).pack(pady=(3))
stock_quantity.pack(pady=3)
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
            stock_list.itemconfig(tk.ACTIVE, bg="red")

#subclass - inherits all attributes from base class, plus attributes unique to this class
class Perishable(Product):
    def __init__(self, expiryDate, storageTemp, id, name, price, quantity):
        super().__init__(id, name, price, quantity)
        super().low_stock_warning()
        self.expiryDate = expiryDate
        self.storageTemp = storageTemp

#subclass
class Electronic(Product):
    def __init__(self, warrantyPeriod, powerUsage, id, name, price, quantity):
        super().__init__(id, name, price, quantity)
        super().low_stock_warning()
        self.warrantyPeriod = warrantyPeriod
        self.powerUsage = powerUsage

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

#Stock add function with an alert for empty input box- Angel
def add_stock():
    item_name = stock_name.get().strip()
    item_price = stock_price.get().strip()
    item_quantity = stock_quantity.get().strip()
    #converted to valid OOP code
    stock = Product("TEMPORARY_ID",item_name,item_price,item_quantity) #please finish this function - Thomas
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
    stock_list.insert(tk.END, (f"{stock.id},{stock.name},{stock.price},{stock.quantity}"))
    stock.low_stock_warning()
    #stock_list.insert(tk.END, stock)
    #stock_name.delete(0, tk.END)
    #stock_name.focus_set()
    status.config(text="Stock Added!", fg="green")
   
#Button for adding stock to the list.
    
add_button = tk.Button(btn_frame, text="Add Stock", command=add_stock).grid(row=0, column=0, padx=3)

#Listbox to display stock items
stock_list = tk.Listbox(root, width=40, height=10, font=("Arial", 12))
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

#
#
#
# file persistence and logging - Kostya
#
#
#

# Variable that tracks the current working inventory to prevent mis-overwrites
curSavePath = "inventorySave.json"

def saveToFile(event=None):
    """
    Default save function - on click it saves the current inventory to the program folder
    as "inventorySave.json", overwriting the previous save.
    """
# Event handler triggers "Save As" function instead of "Save" if Shift is held
    if event and (event.state & 0x1):
        saveAsFile()
        return

 # Converts the tkinter stock_list to an actual list type inventory
    invList = list(stock_list.get(0, tk.END))

# Empty inventory error
    if len(invList) == 0:
        status.config(text="Inventory is currently empty. Please add stock.", fg= "red")
        return

# Converts list type inventory to json, writes to inventory.json
    invData = json.dumps(invList, indent=4)
    with open(curSavePath, "w") as inv:
        inv.write(invData)
    status.config(text="Inventory saved to [curSavePath] in program folder...", fg="green")

def saveAsFile(event=None):
    """
    Function that opens a dialog window, allowing the user to browse their filesystem and save
    the current inventory to a separate .json file

    Only triggered if Save button is clicked while holding the SHIFT button.
    """
    global curSavePath

 # Converts the tkinter stock_list to an actual list type inventory
    invList = list(stock_list.get(0, tk.END))

# Empty inventory error
    if len(invList) == 0:
        status.config(text="Inventory is currently empty. Please add stock.", fg= "red")
        return

# Asks user to set a save location in new window, defaults to JSON file format
    saveLocation = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json"), ("All files", "*.*")],
        title="Save inventory as. . ."
    )
# This resets the button label back to Save Inventory, avoids a visual bug
    save_button.config(text="Save inventory")

# Cancels operation if saveLocation isn't set (user closed Save As window)
    if not saveLocation:
        return

# Updates current working inventory, Save function will now overwrite that instead of the default one
    curSavePath = saveLocation

# Converts list type inventory to json, writes to inventory.json
    invData = json.dumps(invList, indent=4)
    with open(curSavePath, "w") as inv:
        inv.write(invData)
    status.config(text=f"Inventory saved to [{saveLocation}]", fg="green")

def loadDefaultInventory(event=None):
    global curSavePath

    if event and (event.state & 0x1):
        loadFromFile()
        return
    
    try:
# Load default inventory file
        with open("inventorySave.json", "r") as inv:
            items = json.load(inv)
        stock_list.delete(0, tk.END)
        for item in items:
            stock_list.insert(tk.END, item)

# Reset working inventory to default one
        curSavePath = "inventorySave.json"
        status.config(text="Default inventory loaded from program folder", fg="green")
    except FileNotFoundError:
        status.config(text="Failed to load default inventory. Please Save one first.)", fg="red")

def loadFromFile():
    global curSavePath
# Load From prompt
    loadLocation = filedialog.askopenfilename(
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
        title="Load inventory from . . ."
    )

# Reset label, fixes a UI bug with holding SHIFT
    load_button.config(text="Load Inventory")

    if not loadLocation:
        return

    try:
# Load chosen inventory file
        with open(loadLocation, "r") as inv:
            items = json.load(inv)
        stock_list.delete(0, tk.END)
        for item in items:
            stock_list.insert(tk.END, item)

# Change working inventory to loaded one, so Save function overwrites this instead of Default inv
        curSavePath = loadLocation

        status.config(text=f"Inventory loaded from chosen folder. [{loadLocation}]", fg="green")
    except (FileNotFoundError, json.JSONDecodeError):
        status.config(text="Failed to load inventory. Inventory may be corrupted, or chosen file is not valid JSON.)", fg="red")

def checkLogs():
    pass

# Creates the Save button, separately assigns it to grid and binds function
save_button = tk.Button(btn_frame, text= "Save inventory")
save_button.grid(row=2, column=0, padx=3)
save_button.bind("<Button-1>", saveToFile)

# Creates Load button, separately assigns to grid
load_button = tk.Button(btn_frame, text= "Load inventory")
load_button.grid(row=2, column=1, padx=3)
load_button.bind("<Button-1>", loadDefaultInventory)

# Creates "Check Logs" button, separately assigns to grid
check_logs = tk.Button(btn_frame, text= "Transaction history", command=checkLogs)
check_logs.grid(row=3, column=0, padx=3)

# This binds the Shift key press event to the whole window with a lambda function, swaps Save and Load
# with their respective "as..." versions
root.bind("<KeyPress-Shift_L>",   lambda e: (save_button.config(text="Save inventory as. . ."),
                                             load_button.config(text="Load inventory from. . .")))
root.bind("<KeyPress-Shift_R>",   lambda e: (save_button.config(text="Save inventory as. . ."),
                                             load_button.config(text="Load inventory from. . .")))
root.bind("<KeyRelease-Shift_L>", lambda e: (save_button.config(text="Save inventory"),
                                             load_button.config(text="Load inventory")))
root.bind("<KeyRelease-Shift_R>", lambda e: (save_button.config(text="Save inventory"),
                                             load_button.config(text="Load inventory")))
# main loop to run the SmartStock application to view stock.
root.mainloop()