#PLAN
#Write the stockmanagement,along with the subclasses
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
stock_entry = tk.Entry(root, width=32, font=("Arial", 12))
stock_entry.pack(pady=5)
#Status Label
status=tk.Label(root, text="", font=("Arial",10))
status.pack()

def add_stock():
    stock = stock_entry.get().strip()
    if not stock:
        status.config(text="Please enter a stock item name", fg= "red")
        stock_entry.focus_set()
        return
    stock_list.insert(tk.END, stock)
    stock_entry.delete(0, tk.END)
    stock_entry.focus_set()
    status.config(text="Stock Added!", fg="green")
    
add_button = tk.Button(root, text="Add Stock", command=add_stock)
add_button.pack(pady=5)
#Listbox to display stock items
stock-list = tk.Listbox(root, width=40, height=10, font=("Arial", 12))
stock_list.pack(pady=10)




















root.mainloop()