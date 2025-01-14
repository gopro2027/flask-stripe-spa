# Lightweight Databaseless Flask Single Page Stripe Storefront

**main branch** = Decorated frontend ( implemented https://html5up.net/massively )<br>
**min branch** = No extra frontend added<br>

This repo is a very simple lightweight databaseless storefront based on Flask and Stripe to display your stripe products on a purchasable storefront which you can host on your own server. This also includes stock quantity tracking via a tkinter widget using Stripes built in metadata.

To use, simply add your products on your stripe dashboard, set up your api keys, deploy the server. Your products will automatically be read and listed.<br>
Set your stock quantities with StockAdminGUI.py<br>

![image](https://github.com/user-attachments/assets/755f3a95-3bdf-4b4f-87ec-10fe04133647)

![image](https://github.com/user-attachments/assets/684d72e8-a303-4937-ae00-3cacb3cff0be)

Open the project in visual studio code by double clicking `flask-stripe-spa.code-workspace`

Please follow this tutorial to set up a venv if you wish: https://code.visualstudio.com/docs/python/environments

first run:

```
pip install -r requirements.txt
```

set variables/keys with (windows use set, linux use export):

```
set FLASK_SECRET=<random uuid with https://www.uuidgenerator.net/>
set SITE_DOMAIN=<Url with no trailing slash eg: http://localhost:2027>
set STRIPE_SECRET_KEY=<Your secret key from stripe>
set STRIPE_PUBLISHABLE_KEY=<Your public key from stripe>
set STRIPE_ENDPOINT_SECRET=<Your webhook key from stripe>
```

For generating the endpoint webhook sercret: Generate at https://dashboard.stripe.com/test/webhooks . For testing locally, please follow the "Testing the webhook" section of this article to get your key https://testdriven.io/blog/flask-stripe-tutorial/ . Or, It also says how to do this on the stripe webhook page too. Click add endpoint then click Test in a local environment.

```
stripe login
stripe listen --forward-to 127.0.0.1:2027/stripe_webhook
```

To run the application:

```
python server.py
```

Once your secret key is set you can use the StockAdmin.py script to set the stock count of your items on stripe (default stock count is infinite)

To run stock admin or stock admin gui version:

```
python StockAdmin.py
python StockAdminGUI.py
```

Alternatively, you can set the stock and disabled values here in stripe by editing the metadata values manually:
![image](https://github.com/user-attachments/assets/8cf7a94a-751a-42c8-829e-06838bb8e9fb)

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

How to publish on a linux server:

Follow this tutorial https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04 or read below:

First, remember to modify server.py to turn off debug mode and set `host='0.0.0.0'` in the `app.run()` and then:

```
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
```

Then set up this project with a .venv in your home directory like ~/flask-stripe-spa/ (and also then `pip install wheel gunicorn flask`) then create this file `sudo nano /etc/systemd/system/flask-stripe-spa.service`

in that file put something like:

```
[Unit]
Description=Gunicorn instance to server home/<USERNAME>/flask-stripe-spa
After=network.target

[Service]
User=<USERNAME>
Group=www-data
WorkingDirectory=/home/<USERNAME>/flask-stripe-spa
Environment="PATH=/home/<USERNAME>/flask-stripe-spa/.venv/bin"
Environment="FLASK_SECRET=..."
Environment="SITE_DOMAIN=..."
Environment="STRIPE_SECRET_KEY=..."
Environment="STRIPE_PUBLISHABLE_KEY=..."
Environment="STRIPE_ENDPOINT_SECRET=..."
ExecStart=/home/<USERNAME>/flask-stripe-spa/.venv/bin/gunicorn --bind 0.0.0.0:2027 wsgi:app --workers=3

[Install]
WantedBy=multi-user.target
```

Then run/manage it with the commands

```
sudo ufw allow 2027
sudo systemctl daemon-reload
sudo systemctl restart flask-stripe-spa
sudo systemctl enable flask-stripe-spa
sudo systemctl status flask-stripe-spa
```
