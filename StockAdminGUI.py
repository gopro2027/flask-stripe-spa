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

def submitStock(product, entry):
    newStockCount = str(entry.get())

    stripe.Product.modify(product.id,metadata={keyName:newStockCount})

    if newStockCount == '':
        messagebox.showinfo("Information", "Set infinite stock quanity (will not go out of stock)")
    else:
        messagebox.showinfo("Information", "Set stock quantity of '"+product.name+"' to "+str(newStockCount))

for product in products.data:

    keyName = "stock"
    stockCount = ''
    if keyName in product.metadata:
        stockCount = str(product.metadata[keyName])

    label = tk.Label(window, text=product.name+" ("+product.id+"):")
    label.pack()

    entry = tk.Entry(window)
    entry.insert(tk.END, stockCount)
    entry.pack()

    button = tk.Button(window, text="Submit", command=lambda a = product, b = entry: submitStock(a, b))
    button.pack()

window.mainloop()