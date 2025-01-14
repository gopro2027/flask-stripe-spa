#! /usr/bin/env python3.6

import os, threading
import stripe
from flask import Flask, redirect, request, jsonify, render_template, session
from util import *

SITE_DOMAIN = os.environ["SITE_DOMAIN"]

stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
    "endpoint_secret": os.environ["STRIPE_ENDPOINT_SECRET"],
}

stripe.api_key = stripe_keys["secret_key"]

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')
app.secret_key = os.environ["FLASK_SECRET"]

@app.route("/")
def index():
    return render_template("index.jinja2", intro=True, products=getProducts())

@app.route("/about")
def about():
    return render_template("about.jinja2")

@app.route("/contact")
def contact():
    return render_template("contact.jinja2")

@app.route('/product/<id>')
def get_user(id):
    id = int(id)
    product = getProducts()[id]
    if isProductDisabled(product):
        return redirect('/purchaseerror', code=303)
    price = None
    try:
        price = stripe.Price.retrieve(product.default_price)
    except Exception as e:
        pass
    return render_template("product.jinja2", product=product, price=price)

@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)

@app.route("/success")
def success():
    session_id = request.args.get("session_id")
    if isCheckoutRefunded(session_id):
        return redirect("/refunded")

    return render_template("success.jinja2")

@app.route("/cancelled")
def cancelled():
    expireLastCheckout()
    return render_template("cancelled.jinja2")

@app.route("/refunded")
def refunded():
    return render_template("refunded.jinja2")

@app.route("/purchaseerror")
def purchaseerror():
    return redirect("/")

@app.route("/create-checkout-session", methods=['POST'])
def create_checkout_session():
    productid = request.form.get('productid')
    products = getProducts()
    product = None
    for p in products:
        if p.id == productid:
            product = p
    if product == None:
        return redirect('/purchaseerror', code=303)
    
    stock = getStockCountFromProduct(product)

    if (stock != -1 and stock < 1):
        return redirect('/purchaseerror', code=303)
    
    if isProductDisabled(product):
        return redirect('/purchaseerror', code=303)
    try:
        expireLastCheckout()
        checkout_session = stripe.checkout.Session.create(
            #client_reference_id=current_user.id if current_user.is_authenticated else None,
            success_url=SITE_DOMAIN + "/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=SITE_DOMAIN + "/cancelled",
            #payment_method_types=["card"],
            shipping_address_collection={"allowed_countries": ["US", "CA"]},
            mode="payment",
            automatic_tax={'enabled': True},
            line_items=[
                {
                    'price': product.default_price,
                    'quantity': 1,
                }
            ],
            metadata={
                'product_id': product.id,
            },
        )

        session['checkout_id'] = checkout_session.id
        
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return redirect('/purchaseerror', code=303)
    
lock = threading.Lock()

@app.route("/stripe_webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, stripe_keys["endpoint_secret"]
        )

    except ValueError as e:
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        return "Invalid signature", 400

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        lock.acquire()
        try:
            print("[WEBHOOK] Payment was successful.")
            productId = event.data.object['metadata']['product_id']
            product = stripe.Product.retrieve(productId)
            stock = getStockCountFromProduct(product)

            if stock == 0:
                payment_intent = event.data.object['payment_intent']
                print("PAYMENT RECEIVED WITH NO STOCK LEFT!! Refunding "+str(payment_intent))
                stripe.Refund.create(payment_intent=payment_intent)
            else:
                newStock = stock - 1
                if (stock != -1):
                    stripe.Product.modify(product.id,metadata={"stock":str(newStock)})

                # out of stock, expire all open checkout sessions for this product and hopefully no out of stock purchases are made
                if (newStock == 0):
                    expireAllCheckoutsForProductID(productId)

        except Exception as e:
            print(e)
        lock.release()

    return "Success", 200
    

if __name__ == '__main__':
    app.run(debug=True, port=2027)

