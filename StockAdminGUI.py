import tkinter as tk
from tkinter import messagebox
import os
import stripe

stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
}
stripe.api_key = stripe_keys["secret_key"]

products = stripe.Product.list(limit=99)

window = tk.Tk()
window.title("Stock Admin")
window.minsize(width=300, height=200)

label = tk.Label(window, text="Leave blank = not run out of stock / infinite")
label.pack()

cmdlabel = tk.Label(window, text="")
cmdlabel.pack()

def submitStock(product, entry):
    newStockCount = str(entry.get())

    stripe.Product.modify(product.id,metadata={"stock":newStockCount})

    if newStockCount == '':
        cmdlabel.config(text="Set infinite stock quanity (will not go out of stock) of '"+product.name+"'")
    else:
        cmdlabel.config(text="Set stock quantity of '"+product.name+"' to "+str(newStockCount))

def sumbitDisabled(product, check_var):
    stripe.Product.modify(product.id,metadata={"disabled":("true" if check_var.get() == 1 else '')})
    if check_var.get() == 1:
        cmdlabel.config(text="Disabled "+product.name)
    else:
        cmdlabel.config(text="Enabled "+product.name)

for product in products.data:

    frame = tk.Frame(window)

    stockCount = ''
    if "stock" in product.metadata:
        stockCount = str(product.metadata["stock"])

    disabled = False
    if "disabled" in product.metadata:
        disabled = True

    label = tk.Label(frame, text=product.name+" ("+product.id+"):")
    label.grid(column=0, row=0)

    check_var = tk.IntVar(value=disabled)
    checkbox = tk.Checkbutton(frame, text="Disabled?", variable=check_var)
    checkbox.grid(column=0, row=1)
    button = tk.Button(frame, text="Submit Disabled", command=lambda a = product, b = check_var: sumbitDisabled(a, b))
    button.grid(column=1, row=1)

    entry = tk.Entry(frame)
    entry.insert(tk.END, stockCount)
    entry.grid(column=0, row=2)

    button = tk.Button(frame, text="Submit Stock", command=lambda a = product, b = entry: submitStock(a, b))
    button.grid(column=1, row=2)

    frame.pack()

window.mainloop()