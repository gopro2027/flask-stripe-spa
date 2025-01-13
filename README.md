# Single page app stripe products

Please follow this tutorial to set up a venv if you wish: https://code.visualstudio.com/docs/python/environments

first run:

```
pip install -r requirements.txt
```

if you modify it and add new pip packages, run:

```
pip freeze > requirements.txt
```

to run the application:

```
python server.py
```

set variables/keys with (windows use set, linux use export):

```
set FLASK_SECRET=<random uuid with https://www.uuidgenerator.net/>
set SITE_DOMAIN=<Url with no trailing slash eg: http://localhost:2027>
set STRIPE_SECRET_KEY=<Your secret key from stripe>
set STRIPE_PUBLISHABLE_KEY=<Your public key from stripe>
set STRIPE_ENDPOINT_SECRET=<Your webhook key from stripe>
```

For generating the endpoint webhook sercret: Generate at https://dashboard.stripe.com/test/webhooks . For testing locally, please follow the "Testing the webhook" secion of this article to get your key https://testdriven.io/blog/flask-stripe-tutorial/ . Or, It also says how to do this on the stripe webhook page too. Click add endpoint then click Test in a local environment.

Once your secret key is set you can use the StockAdmin.py script to set the stock count of your items on stripe (default stock count is infinite)

To run stock admin or stock admin gui version:

```
python StockAdmin.py
python StockAdminGUI.py
```

Python 3.6 or newer required.

Test credit card number for test mode:

```
4242 4242 4242 4242
```

For proper coding formatting in the html/jinja files, please install the following extensions:

```
Better Jinja
djLint
```

Then remember to change the file type in the bottom right corner on html/jinja files from html to Jinja HTML
