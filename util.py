from flask import session
import stripe

def getProducts():
    return stripe.Product.list(limit=99).data

def getStockCountFromProduct(product):
    if "stock" not in product.metadata:
        return -1
    else:
        return int(product.metadata["stock"])
    
def isProductDisabled(product):
    if "disabled" in product.metadata:
        return True
    return False

def expireLastCheckout():
    if 'checkout_id' in session:
        try:
            stripe.checkout.Session.expire(session['checkout_id'])
        except Exception as e:
            # will fail if the checkout session is not open
            pass
        session.pop('checkout_id')

def expireAllCheckoutsForProductID(product_id):
    paginationSize = 100
    lastObj = None
    while True:
        checkoutSessions = stripe.checkout.Session.list(status='open', limit=paginationSize, starting_after=lastObj)
        for cs in checkoutSessions:
            # product id is custom in our metadata so we must filter it manually first here
            if 'product_id' in cs.metadata:
                if cs.metadata['product_id'] == product_id:
                    try:
                        stripe.checkout.Session.expire(cs.id)
                    except Exception as e:
                        pass
        
        # if our list is full of the full requested limit, we must have another page to check. Set last object and run again with starting_after param to obtain the next page
        if len(checkoutSessions) == paginationSize:
            lastObj = checkoutSessions.data[-1]
        else:
            break

def isCheckoutRefunded(checkout_id):
    if checkout_id is not None:
        session = stripe.checkout.Session.retrieve(checkout_id)
        if session.payment_intent != None:
            payment_intent = stripe.PaymentIntent.retrieve(session.payment_intent, expand=['latest_charge'])
            return payment_intent.latest_charge.refunded
    return False