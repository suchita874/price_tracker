from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Email settings
SENDER_EMAIL = "appindia564@gmail.com"
RECEIVER_EMAIL = "mshira678@gmail.com"
EMAIL_PASSWORD = "byazkptaoxlxexau"  

def send_email(price, product_url):
    subject = "Price Drop Alert"
    body = f"The price has dropped to {price} for the product: {product_url}.\nTime to buy!"
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        connection.starttls()
        connection.login(user=SENDER_EMAIL, password=EMAIL_PASSWORD)
        connection.sendmail(from_addr=SENDER_EMAIL, to_addrs=RECEIVER_EMAIL, msg=msg.as_string())

# Function to scrape product price from Amazon
def get_product_price(url):
    header = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Accept-Language" : "v=b3;q=0.7"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    try:
        price = soup.find('span', {'id': 'priceblock_ourprice'}).text.strip()
    except AttributeError:
        price = None

    return price

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track_price', methods=['POST'])
def track_price():
    product_url = request.form['product_url']
    target_price = float(request.form['target_price'])
    
    price = get_product_price(product_url)
    if price:
        price = float(price.replace('$', '').replace(',', ''))
        if price < target_price:
            send_email(price, product_url)
            return render_template('index.html', price=price, alert="Price drop alert sent!")
        else:
            return render_template('index.html', price=price, alert="Price has not dropped yet.")
    else:
        return render_template('index.html', alert="Could not fetch price.")


def save_price_data():
    # Assuming you have the product price in a variable `price`
    product_data = [url, price.text.strip(), str(datetime.now())]

    # Write data to CSV
    with open('price_tracker.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(product_data)


if __name__ == '__main__':
    app.run(debug=True)
