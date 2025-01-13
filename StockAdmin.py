import os
import stripe

stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
}
stripe.api_key = stripe_keys["secret_key"]

products = stripe.Product.list(limit=99)
index = 0
for product in products.data:
    print("Stripe Product Index "+str(index)+": "+product.id+" | "+product.name+" | "+product.description)
    keyName = "stock"
    if keyName not in product.metadata:
        print("Current stock is set to infinite (not set)")
    else:
        print("Current stock is set to: "+product.metadata[keyName])
    print("Please enter a new stock count (click enter with no input for infinite):")
    newStock = str(input())
    stripe.Product.modify(product.id,metadata={keyName:newStock})
    index = index + 1