#PLAN
#Write the stockmanagement
#Code stock alerts for low stock and expiry
#Add a section for value calculations as well as transaction history

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
from datetime import datetime, date

root=tk.Tk()
root.title("SmartStock")
root.geometry("420x540")

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
    def __init__(self, value):
        self.value = value
   
    def increment(self):
        self.value += 1
        return self.value

counter = Counter(value=0)

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
    opt.set("Regular Product")

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
                text="Expiry Date (DD/MM/YYYY)",
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
            temp_unit = ttk.OptionMenu(self, temp_value, "Celsius (°C)", *temp_options)
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
            electronic_opts.grid_forget()
            perishable_opts.grid_forget()
        
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
    options = ["Regular Product", "Perishable Product", "Electronic Product"]
    stock_type = ttk.OptionMenu(add_window, opt, "Regular Product", *options, command=update_options)
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
        counter.value = stock_list.size()
        item_type = opt.get().strip()
        item_id = f"{counter.value:03}"
        global item_name
        item_name = stock_name.get().strip()
        item_price = stock_price.get().strip()
        item_quantity = stock_quantity.get().strip()
        
        if not item_name:
            add_status.config(text="Please enter a stock item name.", foreground= "red")
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

        try: #try/except loop to ensure item quantity entered cannot be negative or anything other than an integer - HTL
            item_quantity = int(item_quantity)
            if item_quantity < 0:
                add_status.config(text="Please enter a quantity of 0 or larger.", foreground="red")
                stock_price.focus_set()
                return
        except ValueError:
            add_status.config(text="Please enter a whole number for stock quantity.", foreground="red")
            stock_quantity.focus_set()
            return

        #Creates a new instance, depending on which (sub)class the user chose in the "add_stock_window" function
        if item_type == "Regular Product":
            stock = Product(item_id,item_name,item_price,item_quantity)
            stock_list.insert(tk.END, (f"Product: {stock.id}, {stock.name}, £{stock.price:.2f}, x{stock.quantity}"))

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
                
            exp_date = ""
            date_formats = ["%d/%m/%y","%d/%m/%Y","%d-%m-%y","%d-%m-%Y","%d.%m.%y","%d.%m.%Y"]
            for date_format in date_formats:
                try:
                    exp_date = datetime.strptime(item_expiry, date_format)
                    exp_date_only = str(exp_date)[:10].split("-")
                    exp_date_format = f"{exp_date_only[2]}-{exp_date_only[1]}-{exp_date_only[0]}"
                    break
                except ValueError:
                    pass

            if exp_date == "":
                add_status.config(text="Please enter a valid date (DD/MM/YYYY).", foreground="red")
                stock_expiry.focus_set()
                return
                
            stock = Perishable(item_id,item_name,item_price,item_quantity,item_expiry,item_temp)
            stock_list.insert(tk.END, (f"Perishable: {stock.id}, {stock.name}, £{stock.price:.2f}, x{stock.quantity}, {stock.expiryDate}, {stock.storageTemp}{temp_unit}"))

        elif item_type == "Electronic Product":
            #Electronic attributes
            item_warranty = stock_warranty.get().strip()
            power_usage = stock_power.get().strip()
            if not item_warranty:
                add_status.config(text="Please enter a stock item warranty period in months.", foreground= "red")
                stock_warranty.focus_set()
                return
            if not power_usage:
                add_status.config(text="Please enter a stock item power usage.", foreground= "red")
                stock_power.focus_set()
                return
            
            try: #try/except loop to ensure warranty entered cannot be negative, and must be an integer that is divisible by 3 - HTL
                item_warranty = int(item_warranty)
                if item_warranty >= 0:
                    assert item_warranty % 3 == 0
                else:
                    add_status.config(text="Please enter a warranty length of 0 or more months.", foreground="red")
                    stock_warranty.focus_set()
                    return
            except AssertionError:
                add_status.config(text="Please enter a warranty that is a multiple of 3 (3, 6, 9, etc.).", foreground="red")
                stock_warranty.focus_set()
                return
            except ValueError:
                add_status.config(text="Please enter a whole number for warranty length.", foreground="red")
                stock_warranty.focus_set()
                return
            
            try: #try/except loop to ensure power usage entered cannot be negative or anything other than an integer - HTL
                power_usage = int(power_usage)
                if power_usage < 0:
                    add_status.config(text="Please enter a power usage of 0 or more in Watts.", foreground="red")
                    stock_power.focus_set()
                    return
            except ValueError:
                add_status.config(text="Please enter a whole number for power usage.", foreground="red")
                stock_power.focus_set()
                return

            stock = Electronic(item_id,item_name,item_price,item_quantity,item_warranty,power_usage)
            stock_list.insert(tk.END, (f"Electronic: {stock.id}, {stock.name}, £{stock.price:.2f}, x{stock.quantity}, {stock.warrantyPeriod}mo, {stock.powerUsage}W"))
        
        counter.increment()

        stock.low_stock_warning()
        add_status.config(text="Stock Added!", foreground="green")
    except tk.TclError:
        status.config(text="An error occurred. Please close all 'Add Stock' windows and try again.",foreground="red")

# Add event to logs
    writeLog(f"Added item: {item_name}")

#Button for adding stock to the list.
    
add_window_button = ttk.Button(btn_frame, text="Add stock", command=add_stock_window, width=20).grid(row=0, column=0, padx=3)

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

# Function for editing stock here
def edit_stock():
    selected_index = stock_list.curselection()
    if not selected_index:
        status.config(text="Please select a stock item to edit from the list.", foreground="red")
        return
    item_str= stock_list.get(selected_index)
    
    try:
        parts= item_str.split(", ")
        header = parts [0].split(": ")
        item_type = header[0]
        item_id = header[1]
        item_name= parts[1]
        item_price = parts[2].replace("£", "")
        item_quantity = parts[3].replace("x", "")
    except Exception:
        status.config(text=" Error parsing the item for editing.", foreground="red")
        return
    
    edit_window = tk.Toplevel(root)
    edit_window.title(f"Edit Stock Item {item_id}")
    edit_window.geometry("300x400")

    ttk.Label(edit_window, text=f"Editing {item_type} (ID: {item_id})", font=("arial", 10, "bold")).pack(pady=10)
    ttk.Label(edit_window, text="Name: ").pack()
    name_entry = ttk.Entry(edit_window)
    name_entry.insert(0, item_name)
    name_entry.pack(pady=2)
    
    ttk.Label(edit_window, text="Price (): ").pack()
    price_entry = ttk.Entry(edit_window)
    price_entry.insert(0, item_price)
    price_entry.pack(pady=2)
    
    ttk.Label(edit_window, text="Quantity: ").pack()
    quantity_entry = ttk.Entry(edit_window)
    quantity_entry.insert(0, item_quantity)
    quantity_entry.pack(pady=2)
    
    extra_entries = {}
    if item_type == "Perishable":
        ttk.Label(edit_window, text="Expiry Date: ").pack()
        expiry_entry = ttk.Entry(edit_window)
        expiry_entry.insert(0, parts[4])
        expiry_entry.pack(pady=2)
        extra_entries['expiry'] = expiry_entry
        
        ttk.Label(edit_window, text="Temperature: ").pack()
        temp_entry = ttk.Entry(edit_window)
        temp_entry.insert(0, parts [5])
        temp_entry.pack(pady=2)
        extra_entries['temperature'] = temp_entry
    
    elif item_type == "Electronic":
        ttk.Label(edit_window, text="Warranty (mo) : ").pack()
        warranty_entry = ttk.Entry(edit_window)
        warranty_entry.insert(0, parts[4].replace("mo", ""))
        warranty_entry.pack(pady=2)
        extra_entries['warranty'] = warranty_entry
        
        ttk.Label(edit_window, text= "Power (W): ").pack()
        power_entry = ttk.Entry(edit_window)
        power_entry.insert(0, parts[5].replace("W", ""))
        power_entry.pack(pady=2)
        extra_entries['power'] = power_entry
        
    def save_edits():
        try:
            new_name = name_entry.get().strip()
            new_price = float(price_entry.get().strip())
            new_quantity = int(quantity_entry.get().strip())
            
            #reconstruct string
            if item_type == "Regular Product" or item_type == "Product":
                new_str = f"Product: {item_id}, {new_name}, £{new_price:.2f}, x{new_quantity}"
            elif item_type == "Perishable":
                new_str = f"Perishable: {item_id}, {new_name}, £{new_price:.2f}, x{new_quantity}, {extra_entries['expiry'].get()}, {extra_entries['temperature'].get()}"
            elif item_type == "Electronic":
                new_str = f"Electronic: {item_id}, {new_name}, £{new_price:.2f}, x{new_quantity}, {extra_entries['warranty'].get()}mo, {extra_entries['power'].get()}W"
                  
            stock_list.delete(selected_index)
            stock_list.insert(selected_index, new_str)

            #update background if low stock
            if new_quantity <= 5:
                stock_list.itemconfig(selected_index, bg="red")
            else:
                stock_list.itemconfig(selected_index, bg="white")
            
            status.config(text="Stock item updated successfully.", foreground="green")
            writeLog(f"Edited item: {item_name} to {new_name}")
            edit_window.destroy()
        except ValueError:
            status.config(text="Please ensure price is a number and quantity is a whole number.", foreground="red")
    ttk.Button(edit_window, text="Save Changes", command=save_edits).pack(pady=10)






#function to display low stock warning here
# angel suggests utilising the status.config 


#function to display warning for expiring stock here
#angel suggests utilising the status.config 


#function for total cost of stock here
def calculate_total_cost():
    total_price = 0
    item_list = list(stock_list.get(0, tk.END))
    for item in item_list:
        if ": " in item:
            newstring = item[1:]
            newlist = str(newstring).split(", ")
            item_price = newlist[2]
            item_quantity = newlist[3][1:]
            item_price1 = item_price[1:]
            total_price += float(item_price1) * int(item_quantity)
    total_cost_label.config(text=f"Total Cost: £{total_price:.2f}")


total_cost_label = ttk.Label(root, text=f"")
total_cost_label.pack()

total_cost_button = ttk.Button(root, text="Calculate Total Cost", command=calculate_total_cost)
total_cost_button.pack()
#function for transaction history logs here



#separate section for the 'health' of the stock summary here

#
#
#
# file persistence and logging - Kostya


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

    ttk.Button(log_window, text="Close", command=log_window.destroy).pack(pady=3)

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
                                             load_button.config(text="Load inventory from. . .",width=22)))
root.bind("<KeyPress-Shift_R>",   lambda e: (save_button.config(text="Save inventory as. . ."),
                                             load_button.config(text="Load inventory from. . .",width=22)))
root.bind("<KeyRelease-Shift_L>", lambda e: (save_button.config(text="Save inventory"),
                                             load_button.config(text="Load inventory",width=20)))
root.bind("<KeyRelease-Shift_R>", lambda e: (save_button.config(text="Save inventory"),
                                             load_button.config(text="Load inventory",width=20)))

# Health report / dashboard funcsion

def summonHealthReport():
    """
    On call, generates a new window with quick health indicators
    """
    # Get all items currently in the listbox as a list
    itemsList = list(stock_list.get(0, tk.END))
    itemsListCount = len(itemsList)

    # Variables and counters for the report
    lowStockCount = 0
    totalValue = 0.0
    lowStockCountList = []
    perishablesCount = 0
    defaultsCount = 0
    electronicsCount = 0
    category2valueMap = {} # Maps each item name to the total stock value for that item
    expiringStockList = []
    expiredStockList = []

    for item in itemsList:
        #try:
        parts = item.split(", ")
        itemType = parts[0].split(":")[0]
        itemName = parts[1].strip()
        price = float(parts[2].replace("£", ""))
        quantity = int(parts[3].replace("x", ""))

        # Calculate total value for this item (price * quantity)
        itemValue = price * quantity
        totalValue += itemValue


        # Add to the appropriate type counter
        if itemType == "Perishable":
            parts = parts[4].split("/")
            year = parts[2]; month = parts[1]; day = parts[0]
            day = int(day); month = int(month); year = int(year)
            expiry_date = date(day=day,month=month,year=year)
            if len(str(year)) == 4:
                expiry_date = date(day=day,month=month,year=year)
            else:
                newYear = f"20{year}"
                newYear = int(newYear)
                print(newYear)
                expiry_date = date(day=day,month=month,year=newYear)
            current_date = date.today()
            days_until_expiry = (expiry_date - current_date).days

            if days_until_expiry < 0:
                days_until_expiry = str(days_until_expiry)
                expiredStockList.append(f"{itemName}, {days_until_expiry[1:]}")
            elif days_until_expiry <= 7:
                expiringStockList.append(f"{itemName}, {days_until_expiry}")
            

            perishablesCount += 1
        elif itemType == "Electronic":
            electronicsCount += 1
        else:
            defaultsCount += 1

        # Accumulate value per item name for the breakdown section
        category2valueMap[itemName] = category2valueMap.get(itemName, 0) + itemValue

        # If quantity is 5 or below, flag as low stock
        if quantity <= 5:
            lowStockCount += 1
            lowStockCountList.append(itemName)

        # except (IndexError, ValueError):
        #     # Skip any entries that can't be parsed cleanly
        #     pass

    # Sjummon the report popup window
    healthReportWindow = tk.Toplevel(root)
    healthReportWindow.title("Inventory At A Glance")
    healthReportWindow.geometry("350x550")

    # Report title 4 window
    ttk.Label(healthReportWindow, text="Inventory Summary", font=("Arial", 12, "bold")).pack(pady=10)

    # DISPLAY total item count
    ttk.Label(healthReportWindow, text=f"Total Items: {itemsListCount}", font=("Arial", 11)).pack(pady=(5, 0))

    # Show percentage breakdown by product type if there are anyit
    if itemsListCount > 0:
        percentagePerishables = (perishablesCount / itemsListCount) * 100
        percentageElectronics = (electronicsCount / itemsListCount) * 100
        percentageDefaults = (defaultsCount / itemsListCount) * 100
        ttk.Label(healthReportWindow,
                 text=f"{percentageDefaults:.1f}% Regular  |  {percentagePerishables:.1f}% Perishable  |  {percentageElectronics:.1f}% Electronic",
                 font=("Arial", 10), foreground="gray").pack(pady=(0, 5))

    # Show low stock count in red if any items are low, black otherwise
    lowStockLabelColor = "red" if lowStockCount > 0 else "black"
    ttk.Label(healthReportWindow, text=f"Low Stock Alerts: {lowStockCount}", font=("Arial", 11), foreground=lowStockLabelColor).pack(pady=(5, 0))

    # If there are low stock items, list each one by name
    if lowStockCountList:
        ttk.Label(healthReportWindow, text="Currently low on:", font=("Arial", 10, "italic")).pack(pady=(2, 0))
        for name in lowStockCountList:
            ttk.Label(healthReportWindow, text=f"  • {name}", font=("Arial", 10), foreground="red").pack()

    if expiringStockList:
        ttk.Label(healthReportWindow,text="Expiring Stock:",font=label_font).pack(pady=(2,0))
        for name in expiringStockList:
            ttk.Label(healthReportWindow, text=f"Item: {name} days until expiry date").pack()
    if expiredStockList:
        ttk.Label(healthReportWindow,text="Expired Stock:",font=label_font).pack(pady=(2,0))
        for name in expiredStockList:
            ttk.Label(healthReportWindow, text=f"Item: {name} days past expiry date").pack()

    # Show the total combined stock value
    ttk.Label(healthReportWindow, text=f"\nTotal Value: £{totalValue:.2f}", font=("Arial", 11)).pack(pady=(10, 0))

    # Show a per-item value breakdown sorted from highest to lowest value
    if totalValue > 0 and category2valueMap:
        ttk.Label(healthReportWindow, text="Value breakdown:", font=("Arial", 10, "italic")).pack(pady=(2, 0))
        for name, val in sorted(category2valueMap.items(), key=lambda x: x[1], reverse=True):
            # Calculate what percentage of total value this item represents
            percentage = (val / totalValue) * 100
            ttk.Label(healthReportWindow, text=f"  • {name}: {percentage:.1f}%  (£{val:.2f})",
                     font=("Arial", 10)).pack()
                     
    ttk.Button(healthReportWindow, text="Close Report Window", command=healthReportWindow.destroy).pack(pady=3)


# Button that opens the health report window
health_button = ttk.Button(btn_frame, text="Health Report", command=summonHealthReport, width=20)
health_button.grid(row=3, column=1, padx=3)

# main loop to run the SmartStock application to view stock.
root.mainloop()
