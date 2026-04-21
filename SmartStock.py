#PLAN
#Write the stockmanagement,along with the subclasses
#Code stock alaerts for low stock and expiry
#Add a section for value calculations as well as transaction history

import tkinter as tk
from tkinter import messagebox

root=tk.Tk()
root.title("SmartStock")
root.geometry("420x480")

tk.Label(
    root, 
    text="Add a new item",
    font=("Arial",11)).pack(pady=(15,5))
