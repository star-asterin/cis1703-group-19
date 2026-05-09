#PLAN
#Write the stockmanagement
#Code stock alerts for low stock and expiry
#Add a section for value calculations as well as transaction history

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
from datetime import datetime

root=tk.Tk()
root.title("SmartStock")
root.geometry("420x480")

default_font = ("Arial", 12)
label_font = ("Arial", 11)

#Status Label
status=ttk.Label(root, text="", font=("Arial",10))
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

#counter for incrementing product ID when a new item is created
class Counter:
    def __init__(self):
        self.value = 0
    
    def increment(self):
        self.value += 1
        return self.value

counter = Counter()

btn_frame = ttk.Frame(root)
btn_frame.pack(pady=5)

#Stock add function with an alert for empty input box- Angel
#Overhauled add function - Thomas:

def add_stock_window():
    #Creates a new window
    add_window = tk.Toplevel(root)
    add_window.title("Add Stock")
    add_window.geometry("420x480")

    add_window.columnconfigure(0, weight=1)
    add_window.columnconfigure(1, weight=1)
    add_window.columnconfigure(2, weight=1)
    add_window.columnconfigure(3, weight=1)

    global opt
    opt = tk.StringVar(add_window)
    opt.set("Default Product")

    class DefaultOptions(ttk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            global stock_name
            stock_name = ttk.Entry(self, width=32, font=default_font)
            global stock_price
            stock_price = ttk.Entry(self, width=32, font=default_font)
            global stock_quantity
            stock_quantity = ttk.Entry(self, width=32, font=default_font)
            ttk.Label(
                self, 
                text="Name of item",
                font=label_font).pack(pady=3)
            stock_name.pack(pady=3)
            ttk.Label(
                self, 
                text="Price of item",
                font=label_font).pack(pady=3)
            stock_price.pack(pady=3)
            ttk.Label(
                self, 
                text="Quantity of item",
                font=label_font).pack(pady=3)
            stock_quantity.pack(pady=3)

    class PerishableOptions(ttk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            ttk.Label(
                self,
                text="Expiry Date",
                font=label_font
            ).pack(pady=3)
            global stock_expiry
            stock_expiry = ttk.Entry(self, width=32, font=default_font)
            stock_expiry.pack(pady=3)
            ttk.Label(
                self,
                text="Storage Temperature",
                font=label_font
            ).pack(pady=3)
            global stock_temp
            stock_temp = ttk.Entry(self, width=16, font=default_font)
            stock_temp.pack(pady=3,side=tk.LEFT)
            global temp_value
            temp_value = tk.StringVar(value="Celsius (°C)")
            temp_options = ("Celsius (°C)","Fahrenheit (°F)")
            temp_unit = ttk.OptionMenu(self, temp_value, *temp_options)
            temp_unit.config(width=16)
            temp_unit.pack(pady=3,side=tk.RIGHT)

    class ElectronicOptions(ttk.Frame):
        def __init__(self, parent):
            super().__init__(parent)
            ttk.Label(
                self,
                text="Warranty Period", 
                font=label_font
            ).pack(pady=3)
            global stock_warranty
            stock_warranty = ttk.Entry(self, width=32, font=default_font)
            stock_warranty.pack(pady=3)
            ttk.Label(
                self,
                text="Power Usage",
                font=label_font
            ).pack(pady=3)
            global stock_power
            stock_power = ttk.Entry(self, width=32, font=default_font)
            stock_power.pack(pady=3)

    def update_options(selected):
        if selected == "Perishable Product":
            perishable_opts.grid(row=4,column=1,columnspan=2)
            electronic_opts.grid_forget()
        elif selected == "Electronic Product":
            electronic_opts.grid(row=4,column=1,columnspan=2)
            perishable_opts.grid_forget()
        else:
            electronic_opts.pack_forget()
            perishable_opts.pack_forget()
        
    def close_add_stock_window():
        add_window.destroy()

    perishable_opts = PerishableOptions(add_window)
    electronic_opts = ElectronicOptions(add_window)

    ttk.Label(
        add_window, 
        text="Add a new item",
        font=label_font).grid(row=0,column=1,columnspan=2)
    
    ttk.Label(
        add_window,
        text="Select a Product Type",
        font=label_font
    ).grid(row=1,column=1,columnspan=2)

    #Allows user to choose which type of product they want to add
    options = ["Default Product", "Perishable Product", "Electronic Product"]
    stock_type = ttk.OptionMenu(add_window, opt, *options, command=update_options)
    stock_type.grid(row=2,column=1,columnspan=2)

    DefaultOptions(add_window).grid(row=3,column=1,columnspan=2)

    global add_status
    add_status = ttk.Label(add_window, text="", font=("Arial",10))
    add_status.grid(row=5,column=1,columnspan=2)

    add_button = ttk.Button(add_window, text="Add Stock", command=add_stock).grid(row=6,column=1,columnspan=2)
    
    #Runs the rest of the add_stock function on button click, then closes the window

    add_window.mainloop()

def add_stock():

    def change_temp_unit(selected):
        if selected == "Fahrenheit (°F)":
            unit = "°F"
        else:
            unit = "°C"
        return unit
    
    #Now the only purpose of add_stock is to create a new object, using data from the "add_stock_window" function
    #Core attributes
    try:
        item_type = opt.get().strip()
        item_id = f"{counter.value:03}"
        global item_name
        item_name = stock_name.get().strip()
        item_price = stock_price.get().strip()
        item_quantity = stock_quantity.get().strip()
        
        if not item_name:
            add_status.config(text="Please enter a stock item name", foreground= "red")
            stock_name.focus_set()
            return
        if not item_price:
            add_status.config(text="Please enter a stock item price.", foreground= "red")
            stock_price.focus_set()
            return
        if not item_quantity:
            add_status.config(text="Please enter a stock item quantity.", foreground= "red")
            stock_quantity.focus_set()
            return
        try:
            item_quantity = int(item_quantity)
            if item_quantity < 0:
                add_status.config(text="Please enter a quantity of 0 or larger.", foreground="red")
                stock_price.focus_set()
                return
        except ValueError:
            add_status.config(text="Please enter a whole number for stock quantity.", foreground="red")
            stock_quantity.focus_set()
            return

        #Only allows item_price to be up to 2DP, raises an error if not input correctly
        try:
            item_price = float(item_price)
            if item_price >= 0:
                assert item_price == (round(item_price, 2))
            else: 
                add_status.config(text="Please enter a price value of 0 or larger.", foreground="red")
                stock_price.focus_set()
                return
        except AssertionError:
            add_status.config(text="Please only enter a price with up to 2 decimal points.", foreground="red")
            stock_price.focus_set()
            return
        except ValueError:
            add_status.config(text="Please only enter an integer/decimal number for the price.", foreground="red")
            stock_price.focus_set()
            return
        except:
            add_status.config(text="The price entered is not possible.", foreground="red")
            stock_price.focus_set()
            return

        #Creates a new instance, depending on which (sub)class the user chose in the "add_stock_window" function
        if item_type == "Default Product":
            stock = Product(item_id,item_name,item_price,item_quantity)
            stock_list.insert(tk.END, (f"Product: {stock.id}, {stock.name}, £{stock.price:.2f}, {stock.quantity}"))

        elif item_type == "Perishable Product":
            #Perishable attributes
            item_expiry = stock_expiry.get().strip()
            item_temp = stock_temp.get().strip()
            temp_unit = change_temp_unit(temp_value.get())
            if not item_expiry:
                add_status.config(text="Please enter a stock item expiry date.", foreground= "red")
                stock_expiry.focus_set()
                return
            if not item_temp:
                add_status.config(text="Please enter a storage temperature.", foreground= "red")
                stock_temp.focus_set()
                return
            stock = Perishable(item_id,item_name,item_price,item_quantity,item_expiry,item_temp)
            stock_list.insert(tk.END, (f"Perishable: {stock.id}, {stock.name}, £{stock.price:.2f}, {stock.quantity}, {stock.expiryDate}, {stock.storageTemp}{temp_unit}"))

        elif item_type == "Electronic Product":
            #Electronic attributes
            item_warranty = stock_warranty.get().strip()
            power_usage = stock_power.get().strip()
            if not item_warranty:
                add_status.config(text="Please enter a stock item warranty period.", foreground= "red")
                stock_warranty.focus_set()
                return
            if not power_usage:
                add_status.config(text="Please enter a stock item power usage.", foreground= "red")
                stock_power.focus_set()
                return
            stock = Electronic(item_id,item_name,item_price,item_quantity,item_warranty,power_usage)
            stock_list.insert(tk.END, (f"Electronic: {stock.id}, {stock.name}, £{stock.price:.2f}, {stock.quantity}, {stock.warrantyPeriod}, {stock.powerUsage}"))
        
        counter.increment()

        stock.low_stock_warning()
        add_status.config(text="Stock Added!", foreground="green")
    except tk.TclError:
        status.config(text="An error occurred. Please close all 'Add Stock' windows and try again.",foreground="red")

# Add event to logs
    writeLog(f"Added item: {item_name}")

#Button for adding stock to the list.
    
add_window_button = ttk.Button(btn_frame, text="Add Stock", command=add_stock_window, width=20).grid(row=0, column=0, padx=3)

frame = ttk.Frame(root, width=40, height=15)
frame.pack(pady=10)

scrollbar = ttk.Scrollbar(frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

sidescroll = ttk.Scrollbar(frame, orient="horizontal")
sidescroll.pack(side="bottom", fill="x")

#Listbox to display stock items
stock_list = tk.Listbox(frame, width=40, height=15, font=default_font, yscrollcommand=scrollbar.set, xscrollcommand=sidescroll.set)
stock_list.pack()

scrollbar.config(command=stock_list.yview)
sidescroll.config(command=stock_list.xview)


#Function to remove selected stock from the list (Angel)
def remove_stock():
    selected = stock_list.curselection()
    if not selected:
        status.config(text="Please select a stock item to remove from the list.",
                      foreground= "red")
        return
    stock_list.delete(selected)
    status.config(text="Stock has been removed from the list.",
                  foreground="green")

# Add event to logs
    writeLog(f"Removed item: {item_name}")

def edit_stock():
    pass

#Button to remove selected stock from list

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
        status.config(text="Inventory is currently empty. Please add stock.", foreground= "red")
        return

# Converts list type inventory to json, writes to inventory.json
    invData = json.dumps(invList, indent=4)
    with open(curSavePath, "w") as inv:
        inv.write(invData)
    status.config(text="Inventory saved to [curSavePath] in program folder...", foreground="green")
# Add event to logs
    writeLog(f"Saved inventory to [{curSavePath}]")


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
        status.config(text="Inventory is currently empty. Please add stock.", foreground= "red")
        return

# Asks user to set a save location in new window, defaults to JSON file format
    saveLocation = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json"), ("All files", "*.*")],
        title="Save inventory as. . ."
    )
# Adds log event
    writeLog(f"Saved inventory as [{curSavePath}]")

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
    status.config(text=f"Inventory saved to [{saveLocation}]", foreground="green")

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
        status.config(text="Default inventory loaded from program folder", foreground="green")
    except FileNotFoundError:
        status.config(text="Failed to load default inventory. Please Save one first.)", foreground="red")
# Add event to logs
    writeLog("Loaded default inventory [inventorySave.json]")



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

        status.config(text=f"Inventory loaded from chosen folder. [{loadLocation}]", foreground="green")
    except (FileNotFoundError, json.JSONDecodeError):
        status.config(text="Failed to load inventory. Inventory may be corrupted, or chosen file is not valid JSON.)", foreground="red")
# Add event to logs
    writeLog(f"Loaded inventory from [{loadLocation}]")

# Attempts to load logs from previous session
try:
    with open("inventoryLogs.json", "r") as logFile:
        logs = json.load(logFile)
except (FileNotFoundError, json.JSONDecodeError):
    logs = []

def writeLog(action):
    """
    Appends a timestamped action to the log and saves it to disk.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"timestamp": timestamp, "action": action}
    logs.append(entry)
    with open("inventoryLogs.json", "w") as logFile:
        json.dump(logs, logFile, indent=4)

def checkLogs():
    """
    Opens a new window displaying the full log w/ timestamps.
    """
    log_window = tk.Toplevel(root)
    log_window.title("Transaction History")
    log_window.geometry("520x400")

    ttk.Label(log_window, text="Transaction History", font=("Arial", 12, "bold")).pack(pady=(10, 5))

    # Scrollable text box
    frame = ttk.Frame(log_window)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    scrollbar = ttk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    log_box = tk.Text(frame, yscrollcommand=scrollbar.set, state=tk.DISABLED, wrap=tk.WORD)
    log_box.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=log_box.yview)

    # Populate log box
    log_box.config(state=tk.NORMAL)
    if not logs:
        log_box.insert(tk.END, "No transactions recorded yet.")
    else:
        for entry in logs:
            log_box.insert(tk.END, f"[{entry['timestamp']}]  {entry['action']}\n")
    log_box.config(state=tk.DISABLED)
    log_box.see(tk.END)  # scroll to most recent

    ttk.Button(log_window, text="Close", command=log_window.destroy).pack(pady=8)

edit_button = ttk.Button(btn_frame, text="Edit stock", command=edit_stock, width=20).grid(row=0, column=1, padx=3)
remove_button = ttk.Button(btn_frame, text= "Remove stock", command=remove_stock, width=20) .grid(row=1, column=0, padx=3)  

# Creates the Save button, separately assigns it to grid and binds function
save_button = ttk.Button(btn_frame, text= "Save inventory", width=20)
save_button.grid(row=2, column=0, padx=3)
save_button.bind("<Button-1>", saveToFile)

# Creates Load button, separately assigns to grid
load_button = ttk.Button(btn_frame, text= "Load inventory", width=20)
load_button.grid(row=2, column=1, padx=3)
load_button.bind("<Button-1>", loadDefaultInventory)

# Creates "Check Logs" button, separately assigns to grid
check_logs = ttk.Button(btn_frame, text= "Transaction history", command=checkLogs, width=20)
check_logs.grid(row=1, column=1, padx=3)

tipLabel=ttk.Label(root, text="Hold 'Shift' key to show alternative save and load options", font=("Arial",10))
tipLabel.pack()

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
