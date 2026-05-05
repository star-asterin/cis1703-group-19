#PLAN
#Write the stockmanagement
#Code stock alaerts for low stock and expiry
#Add a section for value calculations as well as transaction history

import tkinter as tk


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

#subclass - inherits all attributes from base class, plus attributes unique to this class
class Perishable(Product):
    def __init__(self, expiryDate, storageTemp, id, name, price, quantity):
        super().__init__(id, name, price, quantity)
        self.expiryDate = expiryDate
        self.storageTemp = storageTemp

#subclass
class Electronic(Product):
    def __init__(self, warrantyPeriod, powerUsage, id, name, price, quantity):
        super().__init__(id, name, price, quantity)
        self.warrantyPeriod = warrantyPeriod
        self.powerUsage = powerUsage

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

#Stock add function with an alert for empty input box- Angel
def add_stock():
    item_name = stock_name.get().strip()
    #converted to valid OOP code
    stock = Product("TEMPORARY_ID",item_name,0,0) #please finish this function - Thomas
    if not item_name:
        status.config(text="Please enter a stock item name", fg= "red")
        stock_name.focus_set()
        return
    stock_list.insert(tk.END, (f"{stock.id},{stock.name},{stock.price},{stock.quantity}"))
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










#main loop to run the SmartSTock application to view stock.
root.mainloop()